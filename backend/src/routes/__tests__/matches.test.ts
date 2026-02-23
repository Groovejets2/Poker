/**
 * Matches Route Tests - TypeScript with TypeORM
 */

import request from 'supertest';
import express, { Express } from 'express';
import matchesRouter from '../matches';
import { AppDataSource } from '../../database/data-source';
import { Match } from '../../database/entities/Match';
import { MatchPlayer } from '../../database/entities/MatchPlayer';
import { User } from '../../database/entities/User';
import { createMockRepository } from '../../__tests__/helpers/mockRepository';
import jwt from 'jsonwebtoken';

// Mock TypeORM
jest.mock('../../database/data-source');

// Mock auth middleware
jest.mock('../../middleware/auth', () => {
  return jest.fn((req: any, res: any, next: any) => {
    const authHeader = req.headers.authorization;
    if (!authHeader) {
      return res.status(401).json({
        error: { code: 'UNAUTHORIZED', message: 'Missing authentication token' }
      });
    }
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

describe('Matches Routes', () => {
  let app: Express;
  let mockMatchRepository: ReturnType<typeof createMockRepository>;
  let mockMatchPlayerRepository: ReturnType<typeof createMockRepository>;
  let testToken: string;

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();

    // Create Express app
    app = express();
    app.use(express.json());
    app.use('/matches', matchesRouter);

    // Create mock repositories
    mockMatchRepository = createMockRepository();
    mockMatchPlayerRepository = createMockRepository();

    // Mock getRepository to return appropriate repository
    (AppDataSource.getRepository as jest.Mock).mockImplementation((entity: any) => {
      if (entity === Match) return mockMatchRepository;
      if (entity === MatchPlayer) return mockMatchPlayerRepository;
      return createMockRepository();
    });

    // Create test JWT token
    testToken = jwt.sign(
      { user_id: 1, username: 'testuser' },
      process.env.JWT_SECRET || 'test-secret',
      { expiresIn: '1h' }
    );
  });

  describe('GET /matches/tournament/:tournament_id', () => {
    it('should list all matches for a tournament', async () => {
      const mockMatches = [
        {
          id: 1,
          tournament: { id: 1 },
          table_number: 1,
          game_number: 1,
          status: 'completed',
          winner: { id: 2, username: 'player1' } as User,
        },
        {
          id: 2,
          tournament: { id: 1 },
          table_number: 1,
          game_number: 2,
          status: 'active',
          winner: null,
        }
      ];

      const queryBuilder = {
        leftJoinAndSelect: jest.fn().mockReturnThis(),
        where: jest.fn().mockReturnThis(),
        orderBy: jest.fn().mockReturnThis(),
        addOrderBy: jest.fn().mockReturnThis(),
        getMany: jest.fn().mockResolvedValue(mockMatches)
      };

      mockMatchRepository.createQueryBuilder.mockReturnValue(queryBuilder);

      const response = await request(app)
        .get('/matches/tournament/1');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('tournament_id', 1);
      expect(response.body).toHaveProperty('matches');
      expect(response.body.matches).toHaveLength(2);
      expect(response.body.matches[0]).toHaveProperty('winner', 'player1');
      expect(response.body.matches[1]).toHaveProperty('winner', null);
    });
  });

  describe('GET /matches/:id', () => {
    it('should get match details with players', async () => {
      const mockMatch = {
        id: 1,
        tournament: { id: 1 },
        table_number: 1,
        game_number: 1,
        status: 'completed',
        winner: { id: 2, username: 'player1' } as User,
        completed_at: new Date('2026-02-23T20:00:00Z')
      };

      const mockPlayers = [
        {
          id: 1,
          user: { id: 2, username: 'player1' } as User,
          match: mockMatch,
          starting_stack: 1000,
          ending_stack: 2500,
          status: 'active'
        },
        {
          id: 2,
          user: { id: 3, username: 'player2' } as User,
          match: mockMatch,
          starting_stack: 1000,
          ending_stack: 0,
          status: 'busted'
        }
      ];

      mockMatchRepository.findOne.mockResolvedValue(mockMatch);
      mockMatchPlayerRepository.find.mockResolvedValue(mockPlayers);

      const response = await request(app)
        .get('/matches/1');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('id', 1);
      expect(response.body).toHaveProperty('winner', 'player1');
      expect(response.body).toHaveProperty('players');
      expect(response.body.players).toHaveLength(2);
      expect(response.body.players[0]).toHaveProperty('username', 'player1');
      expect(response.body.players[0]).toHaveProperty('ending_stack', 2500);
    });

    it('should return 404 if match not found', async () => {
      mockMatchRepository.findOne.mockResolvedValue(null);

      const response = await request(app)
        .get('/matches/999');

      expect(response.status).toBe(404);
      expect(response.body.error.code).toBe('NOT_FOUND');
    });
  });

  describe('POST /matches/:id/submit-score', () => {
    it('should submit match score successfully', async () => {
      const mockMatch = {
        id: 1,
        tournament: { id: 1 },
        table_number: 1,
        game_number: 1,
        status: 'active',
        winner: null,
        completed_at: null
      } as Match;

      const mockMatchPlayer1 = {
        id: 1,
        match: mockMatch,
        user: { id: 2 } as User,
        starting_stack: 1000,
        ending_stack: 0,
        status: 'active'
      } as MatchPlayer;

      const mockMatchPlayer2 = {
        id: 2,
        match: mockMatch,
        user: { id: 3 } as User,
        starting_stack: 1000,
        ending_stack: 0,
        status: 'active'
      } as MatchPlayer;

      mockMatchRepository.findOne.mockResolvedValue(mockMatch);
      mockMatchRepository.save.mockResolvedValue(mockMatch);
      mockMatchPlayerRepository.findOne
        .mockResolvedValueOnce(mockMatchPlayer1)
        .mockResolvedValueOnce(mockMatchPlayer2);
      mockMatchPlayerRepository.save.mockResolvedValue({});

      const response = await request(app)
        .post('/matches/1/submit-score')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          winner_id: 2,
          results: [
            { user_id: 2, ending_stack: 2000, status: 'active' },
            { user_id: 3, ending_stack: 0, status: 'busted' }
          ]
        });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('message', 'Match score submitted');
      expect(response.body).toHaveProperty('match_id', 1);
      expect(mockMatchRepository.save).toHaveBeenCalled();
      expect(mockMatchPlayerRepository.save).toHaveBeenCalledTimes(2);
    });

    it('should return 401 if not authenticated', async () => {
      const response = await request(app)
        .post('/matches/1/submit-score')
        .send({
          winner_id: 2,
          results: []
        });

      expect(response.status).toBe(401);
      expect(response.body.error.code).toBe('UNAUTHORIZED');
    });

    it('should return 400 if winner_id is missing', async () => {
      const response = await request(app)
        .post('/matches/1/submit-score')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          results: []
        });

      expect(response.status).toBe(400);
      expect(response.body.error.code).toBe('INVALID_REQUEST');
      expect(response.body.error.message).toContain('Missing winner_id or results');
    });

    it('should return 400 if results are missing', async () => {
      const response = await request(app)
        .post('/matches/1/submit-score')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          winner_id: 2
        });

      expect(response.status).toBe(400);
      expect(response.body.error.code).toBe('INVALID_REQUEST');
      expect(response.body.error.message).toContain('Missing winner_id or results');
    });

    it('should return 404 if match not found', async () => {
      mockMatchRepository.findOne.mockResolvedValue(null);

      const response = await request(app)
        .post('/matches/1/submit-score')
        .set('Authorization', `Bearer ${testToken}`)
        .send({
          winner_id: 2,
          results: [
            { user_id: 2, ending_stack: 2000, status: 'active' }
          ]
        });

      expect(response.status).toBe(404);
      expect(response.body.error.code).toBe('NOT_FOUND');
    });
  });
});
