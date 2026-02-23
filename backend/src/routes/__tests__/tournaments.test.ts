/**
 * Tournaments Route Tests - TypeScript with TypeORM
 */

import request from 'supertest';
import express, { Express } from 'express';
import tournamentsRouter from '../tournaments';
import { AppDataSource } from '../../database/data-source';
import { Tournament } from '../../database/entities/Tournament';
import { TournamentPlayer } from '../../database/entities/TournamentPlayer';
import { User } from '../../database/entities/User';
import { createMockRepository } from '../../__tests__/helpers/mockRepository';
import jwt from 'jsonwebtoken';

// Mock TypeORM
jest.mock('../../database/data-source');

// Mock auth middleware by directly setting req.user
jest.mock('../../middleware/auth', () => {
  return jest.fn((req: any, res: any, next: any) => {
    const authHeader = req.headers.authorization;
    if (!authHeader) {
      return res.status(401).json({
        error: { code: 'UNAUTHORIZED', message: 'Missing authentication token' }
      });
    }
    // Decode token and attach user
    const token = authHeader.replace('Bearer ', '');
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET || 'test-secret') as any;
      req.user = { user_id: decoded.user_id, username: decoded.username };
      next();
    } catch (err) {
      return res.status(401).json({
        error: { code: 'UNAUTHORIZED', message: 'Invalid token' }
      });
    }
  });
});

describe('Tournaments Routes', () => {
  let app: Express;
  let mockTournamentRepository: ReturnType<typeof createMockRepository>;
  let mockTournamentPlayerRepository: ReturnType<typeof createMockRepository>;
  let mockUserRepository: ReturnType<typeof createMockRepository>;
  let testToken: string;

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();

    // Create Express app
    app = express();
    app.use(express.json());
    app.use('/tournaments', tournamentsRouter);

    // Create mock repositories
    mockTournamentRepository = createMockRepository();
    mockTournamentPlayerRepository = createMockRepository();
    mockUserRepository = createMockRepository();

    // Mock getRepository to return appropriate repository
    (AppDataSource.getRepository as jest.Mock).mockImplementation((entity: any) => {
      if (entity === Tournament) return mockTournamentRepository;
      if (entity === TournamentPlayer) return mockTournamentPlayerRepository;
      if (entity === User) return mockUserRepository;
      return createMockRepository();
    });

    // Create test JWT token
    testToken = jwt.sign(
      { user_id: 1, username: 'testuser' },
      process.env.JWT_SECRET || 'test-secret',
      { expiresIn: '1h' }
    );
  });

  describe('GET /tournaments', () => {
    it('should list tournaments with pagination', async () => {
      const mockTournaments = [
        {
          id: 1,
          name: 'Tournament 1',
          status: 'scheduled',
          buy_in_chips: 1000,
          entry_fee_usd: 10,
          max_players: 8,
          scheduled_at: new Date('2026-02-28T19:00:00Z'),
        },
        {
          id: 2,
          name: 'Tournament 2',
          status: 'active',
          buy_in_chips: 2000,
          entry_fee_usd: 20,
          max_players: 6,
          scheduled_at: new Date('2026-03-01T20:00:00Z'),
        }
      ];

      const queryBuilder = {
        where: jest.fn().mockReturnThis(),
        orderBy: jest.fn().mockReturnThis(),
        skip: jest.fn().mockReturnThis(),
        take: jest.fn().mockReturnThis(),
        getManyAndCount: jest.fn().mockResolvedValue([mockTournaments, 2])
      };

      mockTournamentRepository.createQueryBuilder.mockReturnValue(queryBuilder);
      mockTournamentPlayerRepository.count.mockResolvedValue(3);

      const response = await request(app)
        .get('/tournaments')
        .query({ page: '1', limit: '20' });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('tournaments');
      expect(response.body).toHaveProperty('pagination');
      expect(response.body.tournaments).toHaveLength(2);
      expect(response.body.pagination).toEqual({
        total: 2,
        page: 1,
        limit: 20,
        pages: 1
      });
    });

    it('should filter tournaments by status', async () => {
      const queryBuilder = {
        where: jest.fn().mockReturnThis(),
        orderBy: jest.fn().mockReturnThis(),
        skip: jest.fn().mockReturnThis(),
        take: jest.fn().mockReturnThis(),
        getManyAndCount: jest.fn().mockResolvedValue([[], 0])
      };

      mockTournamentRepository.createQueryBuilder.mockReturnValue(queryBuilder);

      await request(app)
        .get('/tournaments')
        .query({ status: 'active' });

      expect(queryBuilder.where).toHaveBeenCalledWith('t.status = :status', { status: 'active' });
    });
  });

  describe('POST /tournaments', () => {
    it('should create a new tournament successfully', async () => {
      const newTournament = {
        id: 1,
        name: 'Friday Night Poker',
        description: 'Weekly tournament',
        status: 'scheduled',
        buy_in_chips: 1000,
        entry_fee_usd: 10.00,
        max_players: 8,
        scheduled_at: new Date('2026-02-28T19:00:00Z'),
        created_by: { id: 1 } as User,
        created_at: new Date(),
        updated_at: new Date(),
      };

      const mockUser = {
        id: 1,
        username: 'testuser',
        email: 'test@example.com'
      } as User;

      mockUserRepository.findOne.mockResolvedValue(mockUser);
      mockTournamentRepository.create.mockReturnValue(newTournament);
      mockTournamentRepository.save.mockResolvedValue(newTournament);

      const response = await request(app)
        .post('/tournaments')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          name: 'Friday Night Poker',
          description: 'Weekly tournament',
          buy_in_chips: 1000,
          entry_fee_usd: 10.00,
          max_players: 8,
          scheduled_at: '2026-02-28T19:00:00Z'
        });

      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('id', 1);
      expect(response.body).toHaveProperty('name', 'Friday Night Poker');
      expect(response.body).toHaveProperty('player_count', 0);
      expect(response.body).toHaveProperty('seats_available', 8);
    });

    it('should return 401 if not authenticated', async () => {
      const response = await request(app)
        .post('/tournaments')
        .send({
          name: 'Test Tournament',
          buy_in_chips: 1000,
          entry_fee_usd: 10,
          max_players: 8,
          scheduled_at: '2026-02-28T19:00:00Z'
        });

      expect(response.status).toBe(401);
      expect(response.body.error.code).toBe('UNAUTHORIZED');
    });

    it('should return 400 if required fields are missing', async () => {
      const response = await request(app)
        .post('/tournaments')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          name: 'Test Tournament'
          // Missing other required fields
        });

      expect(response.status).toBe(400);
      expect(response.body.error.code).toBe('INVALID_REQUEST');
      expect(response.body.error.message).toContain('Missing required fields');
    });

    it('should return 400 if name is too short', async () => {
      const response = await request(app)
        .post('/tournaments')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          name: 'AB', // Too short
          buy_in_chips: 1000,
          entry_fee_usd: 10,
          max_players: 8,
          scheduled_at: '2026-02-28T19:00:00Z'
        });

      expect(response.status).toBe(400);
      expect(response.body.error.message).toContain('Name must be 3-128 characters');
    });

    it('should return 400 if buy_in_chips is less than 1', async () => {
      const mockUser = {
        id: 1,
        username: 'testuser',
        email: 'test@example.com'
      } as User;

      mockUserRepository.findOne.mockResolvedValue(mockUser);

      const response = await request(app)
        .post('/tournaments')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          name: 'Test Tournament',
          buy_in_chips: -5, // Invalid - negative number (truthy but < 1)
          entry_fee_usd: 10,
          max_players: 8,
          scheduled_at: '2026-02-28T19:00:00Z'
        });

      expect(response.status).toBe(400);
      expect(response.body.error.message).toContain('Buy-in chips must be at least 1');
    });

    it('should return 400 if entry_fee_usd is negative', async () => {
      const response = await request(app)
        .post('/tournaments')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          name: 'Test Tournament',
          buy_in_chips: 1000,
          entry_fee_usd: -5, // Invalid
          max_players: 8,
          scheduled_at: '2026-02-28T19:00:00Z'
        });

      expect(response.status).toBe(400);
      expect(response.body.error.message).toContain('Entry fee cannot be negative');
    });

    it('should return 400 if max_players is out of range', async () => {
      const response = await request(app)
        .post('/tournaments')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          name: 'Test Tournament',
          buy_in_chips: 1000,
          entry_fee_usd: 10,
          max_players: 10, // Out of range (2-8)
          scheduled_at: '2026-02-28T19:00:00Z'
        });

      expect(response.status).toBe(400);
      expect(response.body.error.message).toContain('Max players must be between 2 and 8');
    });

    it('should return 400 if scheduled_at is invalid date', async () => {
      const response = await request(app)
        .post('/tournaments')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          name: 'Test Tournament',
          buy_in_chips: 1000,
          entry_fee_usd: 10,
          max_players: 8,
          scheduled_at: 'not-a-date' // Invalid
        });

      expect(response.status).toBe(400);
      expect(response.body.error.message).toContain('Invalid scheduled_at date format');
    });

    it('should return 401 if user not found', async () => {
      mockUserRepository.findOne.mockResolvedValue(null);

      const response = await request(app)
        .post('/tournaments')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          name: 'Test Tournament',
          buy_in_chips: 1000,
          entry_fee_usd: 10,
          max_players: 8,
          scheduled_at: '2026-02-28T19:00:00Z'
        });

      expect(response.status).toBe(401);
      expect(response.body.error.code).toBe('UNAUTHORIZED');
      expect(response.body.error.message).toContain('User not found');
    });
  });

  describe('GET /tournaments/:id', () => {
    it('should get tournament details with players', async () => {
      const mockTournament = {
        id: 1,
        name: 'Test Tournament',
        status: 'scheduled',
        buy_in_chips: 1000,
        entry_fee_usd: 10,
        max_players: 8,
        scheduled_at: new Date('2026-02-28T19:00:00Z'),
        created_by: { id: 1, username: 'admin' } as User
      };

      const mockPlayers = [
        {
          id: 1,
          user: { id: 2, username: 'player1' } as User,
          tournament: mockTournament,
          starting_stack: 1000
        },
        {
          id: 2,
          user: { id: 3, username: 'player2' } as User,
          tournament: mockTournament,
          starting_stack: 1000
        }
      ];

      mockTournamentRepository.findOne.mockResolvedValue(mockTournament);
      mockTournamentPlayerRepository.find.mockResolvedValue(mockPlayers);

      const response = await request(app)
        .get('/tournaments/1');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('id', 1);
      expect(response.body).toHaveProperty('name', 'Test Tournament');
      expect(response.body.players).toHaveLength(2);
      expect(response.body.players[0]).toHaveProperty('username', 'player1');
    });

    it('should return 404 if tournament not found', async () => {
      mockTournamentRepository.findOne.mockResolvedValue(null);

      const response = await request(app)
        .get('/tournaments/999');

      expect(response.status).toBe(404);
      expect(response.body.error.code).toBe('NOT_FOUND');
    });
  });

  describe('POST /tournaments/:id/register', () => {
    it('should register user for tournament', async () => {
      const mockTournament = {
        id: 1,
        name: 'Test Tournament',
        max_players: 8,
        buy_in_chips: 1000
      } as Tournament;

      mockTournamentRepository.findOne.mockResolvedValue(mockTournament);
      mockTournamentPlayerRepository.findOne.mockResolvedValue(null); // Not already registered
      mockTournamentPlayerRepository.count.mockResolvedValue(5); // 5 players already
      mockTournamentPlayerRepository.save.mockResolvedValue({});

      const response = await request(app)
        .post('/tournaments/1/register')
        .set('Authorization', `Bearer ${testToken}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('player_count', 6);
      expect(response.body).toHaveProperty('seats_available', 2);
    });

    it('should return 404 if tournament not found', async () => {
      mockTournamentRepository.findOne.mockResolvedValue(null);

      const response = await request(app)
        .post('/tournaments/999/register')
        .set('Authorization', `Bearer ${testToken}`);

      expect(response.status).toBe(404);
      expect(response.body.error.code).toBe('NOT_FOUND');
    });

    it('should return 409 if already registered', async () => {
      const mockTournament = {
        id: 1,
        name: 'Test Tournament',
        max_players: 8,
        buy_in_chips: 1000
      } as Tournament;

      const existingRegistration = {
        id: 1,
        tournament: mockTournament,
        user: { id: 1 } as User
      };

      mockTournamentRepository.findOne.mockResolvedValue(mockTournament);
      mockTournamentPlayerRepository.findOne.mockResolvedValue(existingRegistration);

      const response = await request(app)
        .post('/tournaments/1/register')
        .set('Authorization', `Bearer ${testToken}`);

      expect(response.status).toBe(409);
      expect(response.body.error.code).toBe('CONFLICT');
      expect(response.body.error.message).toContain('Already registered');
    });

    it('should return 400 if tournament is full', async () => {
      const mockTournament = {
        id: 1,
        name: 'Test Tournament',
        max_players: 8,
        buy_in_chips: 1000
      } as Tournament;

      mockTournamentRepository.findOne.mockResolvedValue(mockTournament);
      mockTournamentPlayerRepository.findOne.mockResolvedValue(null);
      mockTournamentPlayerRepository.count.mockResolvedValue(8); // Full

      const response = await request(app)
        .post('/tournaments/1/register')
        .set('Authorization', `Bearer ${testToken}`);

      expect(response.status).toBe(400);
      expect(response.body.error.code).toBe('INVALID_REQUEST');
      expect(response.body.error.message).toContain('Tournament full');
    });
  });

  describe('DELETE /tournaments/:id/unregister', () => {
    it('should unregister user from tournament', async () => {
      mockTournamentPlayerRepository.delete.mockResolvedValue({ affected: 1 });

      const response = await request(app)
        .delete('/tournaments/1/unregister')
        .set('Authorization', `Bearer ${testToken}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('message', 'Unregistered from tournament');
    });

    it('should return 404 if registration not found', async () => {
      mockTournamentPlayerRepository.delete.mockResolvedValue({ affected: 0 });

      const response = await request(app)
        .delete('/tournaments/999/unregister')
        .set('Authorization', `Bearer ${testToken}`);

      expect(response.status).toBe(404);
      expect(response.body.error.code).toBe('NOT_FOUND');
    });
  });
});
