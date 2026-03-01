/**
 * Auth Route Tests - TypeScript with TypeORM
 */

import request from 'supertest';
import express, { Express } from 'express';
import cookieParser from 'cookie-parser';
import authRouter from '../auth';
import { AppDataSource } from '../../database/data-source';
import { User } from '../../database/entities/User';
import bcrypt from 'bcryptjs';
import { createMockRepository } from '../../__tests__/helpers/mockRepository';

// Mock TypeORM
jest.mock('../../database/data-source');

describe('Auth Routes', () => {
  let app: Express;
  let mockUserRepository: ReturnType<typeof createMockRepository>;

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();

    // Create Express app
    app = express();
    app.use(express.json());
    app.use(cookieParser());
    app.use('/auth', authRouter);

    // Create mock repository
    mockUserRepository = createMockRepository();
    (AppDataSource.getRepository as jest.Mock).mockReturnValue(mockUserRepository);
  });

  describe('POST /auth/register', () => {
    it('should register a new user successfully', async () => {
      const newUser = {
        id: 1,
        username: 'newuser',
        email: 'new@example.com',
        password_hash: 'hashedpassword',
        role: 'player', // CRIT-6: Default role
        created_at: new Date(),
        updated_at: new Date(),
      };

      mockUserRepository.findOne.mockResolvedValue(null); // Username not taken
      mockUserRepository.create.mockReturnValue(newUser);
      mockUserRepository.save.mockResolvedValue(newUser);

      const response = await request(app)
        .post('/auth/register')
        .send({
          username: 'newuser',
          email: 'new@example.com',
          password: 'password123'
        });

      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('user_id', 1);
      expect(response.body).toHaveProperty('username', 'newuser');
      expect(response.body).toHaveProperty('message', 'User created successfully');
    });

    it('should return 400 if username is missing', async () => {
      const response = await request(app)
        .post('/auth/register')
        .send({
          email: 'test@example.com',
          password: 'password123'
        });

      expect(response.status).toBe(400);
      expect(response.body.error.code).toBe('INVALID_REQUEST');
    });

    it('should return 400 if password is too short', async () => {
      const response = await request(app)
        .post('/auth/register')
        .send({
          username: 'testuser',
          email: 'test@example.com',
          password: '123'
        });

      expect(response.status).toBe(400);
      expect(response.body.error.message).toContain('at least 6 characters');
    });

    it('should return 409 if username already exists', async () => {
      // Mock bcrypt to return a hash
      const bcrypt = require('bcryptjs');
      bcrypt.hash = jest.fn().mockResolvedValue('hashedpassword');

      // Mock save to throw a unique constraint error
      const duplicateError = new Error('UNIQUE constraint failed: users.username');
      mockUserRepository.create.mockReturnValue({ username: 'existinguser' });
      mockUserRepository.save.mockRejectedValue(duplicateError);

      const response = await request(app)
        .post('/auth/register')
        .send({
          username: 'existinguser',
          email: 'new@example.com',
          password: 'password123'
        });

      expect(response.status).toBe(409);
      expect(response.body.error.code).toBe('CONFLICT');
    });
  });

  describe('POST /auth/login', () => {
    it('should login successfully with valid credentials', async () => {
      const user = {
        id: 1,
        username: 'testuser',
        password_hash: 'hashedpassword',
        email: 'test@example.com',
        role: 'player', // CRIT-6: Include role
        refresh_token_hash: null,
        refresh_token_expires_at: null,
      } as User;

      mockUserRepository.findOne.mockResolvedValue(user);
      mockUserRepository.save.mockResolvedValue(user);

      // Mock bcrypt.compare to return true for valid password
      bcrypt.compare = jest.fn().mockResolvedValue(true);

      const response = await request(app)
        .post('/auth/login')
        .send({
          username: 'testuser',
          password: 'password123'
        });

      expect(response.status).toBe(200);
      // Phase 3.8: token is in httpOnly cookie, NOT in response body
      expect(response.body).not.toHaveProperty('token');
      expect(response.body).toHaveProperty('user_id', 1);
      expect(response.body).toHaveProperty('username', 'testuser');
      expect(response.body).toHaveProperty('role', 'player'); // CRIT-6: Check role in response
      const cookies: string[] = Array.isArray(response.headers['set-cookie'])
        ? response.headers['set-cookie'] as string[]
        : [response.headers['set-cookie'] as string];
      expect(cookies.some((c: string) => c.startsWith('access_token='))).toBe(true);
    });

    it('should return 400 if username is missing', async () => {
      const response = await request(app)
        .post('/auth/login')
        .send({
          password: 'password123'
        });

      expect(response.status).toBe(400);
      expect(response.body.error.code).toBe('INVALID_REQUEST');
    });

    it('should return 401 if user does not exist', async () => {
      mockUserRepository.findOne.mockResolvedValue(null);

      const response = await request(app)
        .post('/auth/login')
        .send({
          username: 'nonexistent',
          password: 'password123'
        });

      expect(response.status).toBe(401);
      expect(response.body.error.code).toBe('UNAUTHORIZED');
    });

    it('should return 401 if password is incorrect', async () => {
      const user = {
        id: 1,
        username: 'testuser',
        password_hash: 'hashedpassword',
      } as User;

      mockUserRepository.findOne.mockResolvedValue(user);

      // Mock bcrypt.compare to return false for incorrect password
      bcrypt.compare = jest.fn().mockResolvedValue(false);

      const response = await request(app)
        .post('/auth/login')
        .send({
          username: 'testuser',
          password: 'wrongpassword'
        });

      expect(response.status).toBe(401);
      expect(response.body.error.code).toBe('UNAUTHORIZED');
    });
  });
});
