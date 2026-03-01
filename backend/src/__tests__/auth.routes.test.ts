/**
 * Phase 3.8: Auth Routes Unit Tests
 * Tests cookie-based authentication: login, refresh, logout, register
 */

import request from 'supertest';
import express from 'express';
import cookieParser from 'cookie-parser';

// Mock TypeORM AppDataSource
const mockSave = jest.fn();
const mockFindOne = jest.fn();
const mockCreate = jest.fn();
const mockGetRepository = jest.fn(() => ({
  findOne: mockFindOne,
  save: mockSave,
  create: mockCreate,
}));

jest.mock('../database/data-source', () => ({
  AppDataSource: { getRepository: mockGetRepository },
}));

// Mock bcryptjs
jest.mock('bcryptjs', () => ({
  compare: jest.fn(),
  hash: jest.fn().mockResolvedValue('hashed-password'),
}));

import bcrypt from 'bcryptjs';
import authRouter from '../routes/auth';

const buildApp = () => {
  const app = express();
  app.use(express.json());
  app.use(cookieParser());
  app.use('/api/auth', authRouter);
  return app;
};

describe('Auth Routes - Phase 3.8', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockCreate.mockImplementation((data: any) => data);
  });

  // -------------------------------------------------------------------------
  describe('POST /api/auth/register', () => {
    it('should register a new user successfully', async () => {
      mockSave.mockResolvedValue({ id: 1, username: 'player1', email: null });

      const res = await request(buildApp())
        .post('/api/auth/register')
        .send({ username: 'player1', password: 'secure123' });

      expect(res.status).toBe(201);
      expect(res.body.user_id).toBe(1);
      expect(res.body.username).toBe('player1');
    });

    it('should reject username shorter than 3 chars', async () => {
      const res = await request(buildApp())
        .post('/api/auth/register')
        .send({ username: 'ab', password: 'secure123' });
      expect(res.status).toBe(400);
      expect(res.body.error.code).toBe('INVALID_REQUEST');
    });

    it('should reject password shorter than 6 chars', async () => {
      const res = await request(buildApp())
        .post('/api/auth/register')
        .send({ username: 'player1', password: '123' });
      expect(res.status).toBe(400);
    });

    it('should reject duplicate username', async () => {
      const err: any = new Error('UNIQUE constraint failed: users.username');
      mockSave.mockRejectedValue(err);

      const res = await request(buildApp())
        .post('/api/auth/register')
        .send({ username: 'existing', password: 'secure123' });

      expect(res.status).toBe(409);
      expect(res.body.error.code).toBe('CONFLICT');
    });
  });

  // -------------------------------------------------------------------------
  describe('POST /api/auth/login', () => {
    const mockUser = {
      id: 1, username: 'player1', role: 'player',
      password_hash: 'hashed', refresh_token_hash: null, refresh_token_expires_at: null,
    };

    it('should login and return user data + set httpOnly cookies', async () => {
      mockFindOne.mockResolvedValue(mockUser);
      (bcrypt.compare as jest.Mock).mockResolvedValue(true);
      mockSave.mockResolvedValue(mockUser);

      const res = await request(buildApp())
        .post('/api/auth/login')
        .send({ username: 'player1', password: 'secure123' });

      expect(res.status).toBe(200);
      expect(res.body.user_id).toBe(1);
      expect(res.body.username).toBe('player1');
      expect(res.body.role).toBe('player');
      // Token must NOT be in response body (security)
      expect(res.body.token).toBeUndefined();
      // Cookies should be set
      const cookies = res.headers['set-cookie'] as string[];
      expect(cookies).toBeDefined();
      expect(cookies.some((c: string) => c.startsWith('access_token='))).toBe(true);
      expect(cookies.some((c: string) => c.startsWith('refresh_token='))).toBe(true);
      // Cookies must be httpOnly
      expect(cookies.some((c: string) => c.includes('HttpOnly'))).toBe(true);
    });

    it('should reject missing credentials', async () => {
      const res = await request(buildApp())
        .post('/api/auth/login')
        .send({ username: 'player1' });
      expect(res.status).toBe(400);
    });

    it('should reject wrong password', async () => {
      mockFindOne.mockResolvedValue(mockUser);
      (bcrypt.compare as jest.Mock).mockResolvedValue(false);

      const res = await request(buildApp())
        .post('/api/auth/login')
        .send({ username: 'player1', password: 'wrongpass' });

      expect(res.status).toBe(401);
      expect(res.body.error.code).toBe('UNAUTHORIZED');
    });

    it('should reject unknown user', async () => {
      mockFindOne.mockResolvedValue(null);

      const res = await request(buildApp())
        .post('/api/auth/login')
        .send({ username: 'ghost', password: 'secure123' });

      expect(res.status).toBe(401);
    });
  });

  // -------------------------------------------------------------------------
  describe('POST /api/auth/logout', () => {
    it('should clear cookies and return success message', async () => {
      // No DB lookup needed if no cookie is present
      const res = await request(buildApp())
        .post('/api/auth/logout');

      expect(res.status).toBe(200);
      expect(res.body.message).toBe('Logged out successfully');
    });

    it('should nullify DB token on logout with valid cookie', async () => {
      const mockUserForLogout = {
        id: 42, username: 'player1', role: 'player',
        refresh_token_hash: 'oldhash', refresh_token_expires_at: new Date(),
      };
      mockFindOne.mockResolvedValue(mockUserForLogout);
      mockSave.mockResolvedValue(mockUserForLogout);

      // Build a minimal signed access token for the cookie
      const jwt = require('jsonwebtoken');
      const token = jwt.sign(
        { user_id: 42, username: 'player1', role: 'player' },
        process.env.JWT_SECRET!,
        { expiresIn: 900 }
      );

      const res = await request(buildApp())
        .post('/api/auth/logout')
        .set('Cookie', `access_token=${token}`);

      expect(res.status).toBe(200);
      expect(mockSave).toHaveBeenCalledWith(
        expect.objectContaining({ refresh_token_hash: null, refresh_token_expires_at: null })
      );
    });
  });

  // -------------------------------------------------------------------------
  describe('POST /api/auth/refresh', () => {
    it('should return 401 when no refresh cookie present', async () => {
      const res = await request(buildApp())
        .post('/api/auth/refresh');

      expect(res.status).toBe(401);
      expect(res.body.error.code).toBe('UNAUTHORIZED');
    });

    it('should return 401 for invalid refresh token', async () => {
      const res = await request(buildApp())
        .post('/api/auth/refresh')
        .set('Cookie', 'refresh_token=invalid.token.here');

      expect(res.status).toBe(401);
    });

    it('should rotate tokens on valid refresh cookie', async () => {
      const jwt = require('jsonwebtoken');
      const crypto = require('crypto');

      const REFRESH_SECRET = process.env.REFRESH_SECRET!;
      const JWT_SECRET = process.env.JWT_SECRET!;

      // Build a valid refresh JWT
      const refreshToken = jwt.sign(
        { user_id: 7, username: 'player7', role: 'player' },
        REFRESH_SECRET,
        { expiresIn: '7d' }
      );
      // Compute its sha256 hash (matches what the route stores)
      const storedHash = crypto.createHash('sha256').update(refreshToken).digest('hex');

      const mockUserForRefresh = {
        id: 7, username: 'player7', role: 'player',
        refresh_token_hash: storedHash,
        refresh_token_expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
      };
      mockFindOne.mockResolvedValue(mockUserForRefresh);
      mockSave.mockResolvedValue(mockUserForRefresh);

      const res = await request(buildApp())
        .post('/api/auth/refresh')
        .set('Cookie', `refresh_token=${refreshToken}`);

      expect(res.status).toBe(200);
      expect(res.body.user_id).toBe(7);
      expect(res.body.username).toBe('player7');
      // New tokens issued as cookies
      const cookies = res.headers['set-cookie'] as string[];
      expect(cookies.some((c: string) => c.startsWith('access_token='))).toBe(true);
      expect(cookies.some((c: string) => c.startsWith('refresh_token='))).toBe(true);
      // DB must have been updated with new hash
      expect(mockSave).toHaveBeenCalledWith(
        expect.objectContaining({ refresh_token_hash: expect.any(String) })
      );
    });
  });
});
