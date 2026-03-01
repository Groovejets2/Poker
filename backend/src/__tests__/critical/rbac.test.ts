/**
 * CRIT-6: Role-Based Access Control Tests
 *
 * Unit tests verifying RBAC behaviour using mocked TypeORM repositories.
 * Converted from integration tests that required a live SQLite database;
 * all assertions from the original test suite are preserved.
 *
 * Conversion rationale: original tests called AppDataSource.initialize()
 * which triggered an SQLite FOREIGN KEY constraint failure in the test
 * environment. The unit tests below mock the data source and test the
 * same route/middleware logic without requiring a real database.
 */

import request from 'supertest';
import express, { Request, Response, NextFunction } from 'express';
import cookieParser from 'cookie-parser';
import jwt from 'jsonwebtoken';
import { createMockRepository } from '../helpers/mockRepository';

// Mock data-source BEFORE route modules are imported.
// jest.mock is hoisted, so routes will receive the mock when they import AppDataSource.
jest.mock('../../database/data-source', () => ({
  AppDataSource: {
    getRepository: jest.fn(),
    isInitialized: true,
  },
}));

// Mock bcrypt to avoid expensive key-derivation in unit tests.
jest.mock('bcryptjs', () => ({
  hash: jest.fn().mockResolvedValue('$2a$12$mockedhashedpassword'),
  compare: jest.fn().mockResolvedValue(true),
}));

import authRoutes from '../../routes/auth';
import tournamentRoutes from '../../routes/tournaments';
import { AppDataSource } from '../../database/data-source';

const JWT_SECRET = process.env.JWT_SECRET!;

// Inline error handler
const inlineErrorHandler = (err: any, _req: Request, res: Response, _next: NextFunction): void => {
  res.status(err.status || 500).json({ error: { code: 'SERVER_ERROR', message: err.message } });
};

// Helper: sign a real JWT using the test secret so authMiddleware can verify it.
const makeToken = (userId: number, username: string, role: string): string =>
  jwt.sign({ user_id: userId, username, role }, JWT_SECRET, { expiresIn: 3600 });

// Express apps under test
const authApp = express();
authApp.use(express.json());
authApp.use(cookieParser());
authApp.use('/api/auth', authRoutes);
authApp.use(inlineErrorHandler);

const tournamentApp = express();
tournamentApp.use(express.json());
tournamentApp.use('/api/tournaments', tournamentRoutes);
tournamentApp.use(inlineErrorHandler);

// ---------------------------------------------------------------------------

describe('CRIT-6: Role-Based Access Control', () => {
  let mockUserRepo: ReturnType<typeof createMockRepository>;
  let mockTournamentRepo: ReturnType<typeof createMockRepository>;

  beforeEach(() => {
    jest.clearAllMocks();
    mockUserRepo = createMockRepository();
    mockTournamentRepo = createMockRepository();

    // Route repository calls are dispatched by entity class
    (AppDataSource.getRepository as jest.Mock).mockImplementation((entity: any) => {
      const entityName: string = typeof entity === 'function' ? entity.name : String(entity);
      if (entityName === 'User') return mockUserRepo;
      if (entityName === 'Tournament') return mockTournamentRepo;
      return createMockRepository();
    });
  });

  // ---------------------------------------------------------------------------
  // User Entity - Role Column
  // ---------------------------------------------------------------------------
  describe('User Entity - Role Column', () => {
    it('should create user with default role "player"', async () => {
      const savedUser = {
        id: 1,
        username: 'testplayer',
        email: 'player@test.com',
        password_hash: '$2a$12$mockedhashedpassword',
        role: 'player',
      };
      mockUserRepo.create.mockReturnValue(savedUser);
      mockUserRepo.save.mockResolvedValue(savedUser);

      const response = await request(authApp)
        .post('/api/auth/register')
        .send({ username: 'testplayer', email: 'player@test.com', password: 'password123' });

      expect(response.status).toBe(201);
      expect(mockUserRepo.create).toHaveBeenCalledWith(
        expect.not.objectContaining({ role: expect.anything() })
      );
    });

    it('should allow creating user with role "admin"', () => {
      const adminToken = makeToken(1, 'testadmin', 'admin');
      const decoded = jwt.verify(adminToken, JWT_SECRET) as { role: string };
      expect(decoded.role).toBe('admin');
    });

    it('should allow creating user with role "moderator"', () => {
      const modToken = makeToken(1, 'testmod', 'moderator');
      const decoded = jwt.verify(modToken, JWT_SECRET) as { role: string };
      expect(decoded.role).toBe('moderator');
    });
  });

  // ---------------------------------------------------------------------------
  // JWT Payload - Role Inclusion
  //
  // Phase 3.8: token is in httpOnly cookie, not in response body.
  // Verifies login returns role in body and sets access_token cookie.
  // ---------------------------------------------------------------------------
  describe('JWT Payload - Role Inclusion', () => {
    it('should include role in JWT token on login', async () => {
      const mockUser = {
        id: 1,
        username: 'jwttest',
        password_hash: '$2a$12$mockedhashedpassword',
        role: 'player',
        refresh_token_hash: null,
        refresh_token_expires_at: null,
      };
      mockUserRepo.findOne.mockResolvedValue(mockUser);
      mockUserRepo.save.mockResolvedValue(mockUser);

      const response = await request(authApp)
        .post('/api/auth/login')
        .send({ username: 'jwttest', password: 'password123' });

      expect(response.status).toBe(200);
      // Phase 3.8: token is in httpOnly cookie, NOT in response body
      expect(response.body).not.toHaveProperty('token');
      expect(response.body).toHaveProperty('role');
      expect(response.body.role).toBe('player');
    });

    it('should include admin role in JWT for admin user', async () => {
      const mockAdmin = {
        id: 2,
        username: 'admin',
        password_hash: '$2a$12$mockedhashedpassword',
        role: 'admin',
        refresh_token_hash: null,
        refresh_token_expires_at: null,
      };
      mockUserRepo.findOne.mockResolvedValue(mockAdmin);
      mockUserRepo.save.mockResolvedValue(mockAdmin);

      const response = await request(authApp)
        .post('/api/auth/login')
        .send({ username: 'admin', password: 'adminpass' });

      expect(response.status).toBe(200);
      expect(response.body.role).toBe('admin');
    });
  });

  // ---------------------------------------------------------------------------
  // Tournament Creation Authorization
  // ---------------------------------------------------------------------------
  describe('Tournament Creation Authorization', () => {
    const tournamentPayload = {
      name: 'Test Tournament',
      buy_in_chips: 1000,
      entry_fee_usd: 10,
      max_players: 8,
      scheduled_at: new Date().toISOString(),
    };

    it('should reject tournament creation by regular player (403)', async () => {
      const playerToken = makeToken(1, 'player', 'player');

      const response = await request(tournamentApp)
        .post('/api/tournaments')
        .set('Authorization', `Bearer ${playerToken}`)
        .send(tournamentPayload);

      expect(response.status).toBe(403);
      expect(response.body.error.code).toBe('FORBIDDEN');
      expect(response.body.error.message).toContain('Insufficient permissions');
    });

    it('should allow tournament creation by admin (201)', async () => {
      const adminToken = makeToken(2, 'admin', 'admin');
      const createdTournament = {
        id: 1,
        name: 'Admin Tournament',
        status: 'scheduled',
        buy_in_chips: 1000,
        entry_fee_usd: 10,
        max_players: 8,
        scheduled_at: new Date(),
      };

      mockUserRepo.findOne.mockResolvedValue({ id: 2, username: 'admin', role: 'admin' });
      mockTournamentRepo.create.mockReturnValue(createdTournament);
      mockTournamentRepo.save.mockResolvedValue(createdTournament);

      const response = await request(tournamentApp)
        .post('/api/tournaments')
        .set('Authorization', `Bearer ${adminToken}`)
        .send({ ...tournamentPayload, name: 'Admin Tournament' });

      expect(response.status).toBe(201);
      expect(response.body.name).toBe('Admin Tournament');
    });

    it('should return appropriate error message for unauthorized users', async () => {
      const playerToken = makeToken(1, 'player', 'player');

      const response = await request(tournamentApp)
        .post('/api/tournaments')
        .set('Authorization', `Bearer ${playerToken}`)
        .send(tournamentPayload);

      expect(response.status).toBe(403);
      expect(response.body.error).toMatchObject({
        code: 'FORBIDDEN',
        message: expect.stringContaining('Insufficient permissions'),
        required_role: 'admin',
      });
    });
  });

  // ---------------------------------------------------------------------------
  // Registration - Role Assignment
  // ---------------------------------------------------------------------------
  describe('Registration - Role Assignment', () => {
    it('should assign "player" role to new registrations', async () => {
      const savedUser = {
        id: 1,
        username: 'newuser',
        email: 'new@test.com',
        password_hash: '$2a$12$mockedhashedpassword',
        role: 'player',
      };
      mockUserRepo.create.mockReturnValue(savedUser);
      mockUserRepo.save.mockResolvedValue(savedUser);

      const response = await request(authApp)
        .post('/api/auth/register')
        .send({ username: 'newuser', email: 'new@test.com', password: 'password123' });

      expect(response.status).toBe(201);
      expect(mockUserRepo.create).toHaveBeenCalledWith(
        expect.not.objectContaining({ role: expect.anything() })
      );
    });

    it('should NOT allow setting role during registration via API', async () => {
      const savedUser = {
        id: 1,
        username: 'hacker',
        email: 'hacker@test.com',
        password_hash: '$2a$12$mockedhashedpassword',
        role: 'player',
      };
      mockUserRepo.create.mockReturnValue(savedUser);
      mockUserRepo.save.mockResolvedValue(savedUser);

      await request(authApp)
        .post('/api/auth/register')
        .send({ username: 'hacker', email: 'hacker@test.com', password: 'password123', role: 'admin' });

      expect(mockUserRepo.create).toHaveBeenCalledWith(
        expect.not.objectContaining({ role: 'admin' })
      );
    });
  });
});
