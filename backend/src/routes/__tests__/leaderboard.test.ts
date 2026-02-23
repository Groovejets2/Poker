/**
 * Leaderboard Route Tests - TypeScript with TypeORM
 */

import request from 'supertest';
import express, { Express } from 'express';
import leaderboardRouter from '../leaderboard';
import { AppDataSource } from '../../database/data-source';
import { User } from '../../database/entities/User';
import { createMockRepository } from '../../__tests__/helpers/mockRepository';

// Mock TypeORM
jest.mock('../../database/data-source');

describe('Leaderboard Routes', () => {
  let app: Express;
  let mockUserRepository: ReturnType<typeof createMockRepository>;

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();

    // Create Express app
    app = express();
    app.use(express.json());
    app.use('/leaderboard', leaderboardRouter);

    // Create mock repository
    mockUserRepository = createMockRepository();

    (AppDataSource.getRepository as jest.Mock).mockImplementation((entity: any) => {
      if (entity === User) return mockUserRepository;
      return createMockRepository();
    });
  });

  describe('GET /leaderboard', () => {
    it('should get global leaderboard with rankings', async () => {
      const mockLeaderboard = [
        {
          user_id: '1',
          username: 'player1',
          tournaments_played: '10',
          tournament_wins: '3',
          avg_finish: '2.50',
          total_winnings: '1500.00'
        },
        {
          user_id: '2',
          username: 'player2',
          tournaments_played: '8',
          tournament_wins: '2',
          avg_finish: '3.25',
          total_winnings: '800.00'
        },
        {
          user_id: '3',
          username: 'player3',
          tournaments_played: '5',
          tournament_wins: '0',
          avg_finish: '4.00',
          total_winnings: '200.00'
        }
      ];

      const queryBuilder = {
        leftJoin: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        addSelect: jest.fn().mockReturnThis(),
        groupBy: jest.fn().mockReturnThis(),
        addGroupBy: jest.fn().mockReturnThis(),
        orderBy: jest.fn().mockReturnThis(),
        offset: jest.fn().mockReturnThis(),
        limit: jest.fn().mockReturnThis(),
        getRawMany: jest.fn().mockResolvedValue(mockLeaderboard)
      };

      mockUserRepository.createQueryBuilder.mockReturnValue(queryBuilder);

      const response = await request(app)
        .get('/leaderboard');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('leaderboard');
      expect(response.body).toHaveProperty('updated_at');
      expect(response.body.leaderboard).toHaveLength(3);

      // Check first place
      expect(response.body.leaderboard[0]).toEqual({
        rank: 1,
        user_id: 1,
        username: 'player1',
        tournaments_played: 10,
        tournament_wins: 3,
        avg_finish: 2.50,
        total_winnings: 1500.00
      });

      // Check second place
      expect(response.body.leaderboard[1]).toEqual({
        rank: 2,
        user_id: 2,
        username: 'player2',
        tournaments_played: 8,
        tournament_wins: 2,
        avg_finish: 3.25,
        total_winnings: 800.00
      });
    });

    it('should respect limit parameter', async () => {
      const queryBuilder = {
        leftJoin: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        addSelect: jest.fn().mockReturnThis(),
        groupBy: jest.fn().mockReturnThis(),
        addGroupBy: jest.fn().mockReturnThis(),
        orderBy: jest.fn().mockReturnThis(),
        offset: jest.fn().mockReturnThis(),
        limit: jest.fn().mockReturnThis(),
        getRawMany: jest.fn().mockResolvedValue([])
      };

      mockUserRepository.createQueryBuilder.mockReturnValue(queryBuilder);

      await request(app)
        .get('/leaderboard')
        .query({ limit: '10' });

      expect(queryBuilder.limit).toHaveBeenCalledWith(10);
    });

    it('should cap limit at 100', async () => {
      const queryBuilder = {
        leftJoin: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        addSelect: jest.fn().mockReturnThis(),
        groupBy: jest.fn().mockReturnThis(),
        addGroupBy: jest.fn().mockReturnThis(),
        orderBy: jest.fn().mockReturnThis(),
        offset: jest.fn().mockReturnThis(),
        limit: jest.fn().mockReturnThis(),
        getRawMany: jest.fn().mockResolvedValue([])
      };

      mockUserRepository.createQueryBuilder.mockReturnValue(queryBuilder);

      await request(app)
        .get('/leaderboard')
        .query({ limit: '500' }); // Requesting 500

      expect(queryBuilder.limit).toHaveBeenCalledWith(100); // Should be capped at 100
    });

    it('should respect offset parameter for pagination', async () => {
      const mockLeaderboard = [
        {
          user_id: '4',
          username: 'player4',
          tournaments_played: '3',
          tournament_wins: '0',
          avg_finish: '5.00',
          total_winnings: '50.00'
        }
      ];

      const queryBuilder = {
        leftJoin: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        addSelect: jest.fn().mockReturnThis(),
        groupBy: jest.fn().mockReturnThis(),
        addGroupBy: jest.fn().mockReturnThis(),
        orderBy: jest.fn().mockReturnThis(),
        offset: jest.fn().mockReturnThis(),
        limit: jest.fn().mockReturnThis(),
        getRawMany: jest.fn().mockResolvedValue(mockLeaderboard)
      };

      mockUserRepository.createQueryBuilder.mockReturnValue(queryBuilder);

      const response = await request(app)
        .get('/leaderboard')
        .query({ offset: '10' });

      expect(queryBuilder.offset).toHaveBeenCalledWith(10);
      // Rank should be offset + index + 1 = 10 + 0 + 1 = 11
      expect(response.body.leaderboard[0].rank).toBe(11);
    });

    it('should handle users with no tournament data', async () => {
      const mockLeaderboard = [
        {
          user_id: '5',
          username: 'newplayer',
          tournaments_played: '0',
          tournament_wins: '0',
          avg_finish: null,
          total_winnings: '0'
        }
      ];

      const queryBuilder = {
        leftJoin: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        addSelect: jest.fn().mockReturnThis(),
        groupBy: jest.fn().mockReturnThis(),
        addGroupBy: jest.fn().mockReturnThis(),
        orderBy: jest.fn().mockReturnThis(),
        offset: jest.fn().mockReturnThis(),
        limit: jest.fn().mockReturnThis(),
        getRawMany: jest.fn().mockResolvedValue(mockLeaderboard)
      };

      mockUserRepository.createQueryBuilder.mockReturnValue(queryBuilder);

      const response = await request(app)
        .get('/leaderboard');

      expect(response.status).toBe(200);
      expect(response.body.leaderboard[0]).toEqual({
        rank: 1,
        user_id: 5,
        username: 'newplayer',
        tournaments_played: 0,
        tournament_wins: 0,
        avg_finish: null,
        total_winnings: 0
      });
    });
  });

  describe('GET /leaderboard/:user_id', () => {
    it('should get player stats', async () => {
      const mockStats = {
        user_id: '1',
        username: 'player1',
        tournaments_played: '10',
        tournament_wins: '3',
        avg_finish: '2.50',
        total_winnings: '1500.00'
      };

      const queryBuilder = {
        leftJoin: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        addSelect: jest.fn().mockReturnThis(),
        where: jest.fn().mockReturnThis(),
        groupBy: jest.fn().mockReturnThis(),
        addGroupBy: jest.fn().mockReturnThis(),
        getRawOne: jest.fn().mockResolvedValue(mockStats)
      };

      mockUserRepository.createQueryBuilder.mockReturnValue(queryBuilder);

      const response = await request(app)
        .get('/leaderboard/1');

      expect(response.status).toBe(200);
      expect(response.body).toEqual({
        user_id: 1,
        username: 'player1',
        tournaments_played: 10,
        tournament_wins: 3,
        avg_finish: 2.50,
        total_winnings: 1500.00
      });
    });

    it('should return 404 if user not found', async () => {
      const queryBuilder = {
        leftJoin: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        addSelect: jest.fn().mockReturnThis(),
        where: jest.fn().mockReturnThis(),
        groupBy: jest.fn().mockReturnThis(),
        addGroupBy: jest.fn().mockReturnThis(),
        getRawOne: jest.fn().mockResolvedValue(null)
      };

      mockUserRepository.createQueryBuilder.mockReturnValue(queryBuilder);

      const response = await request(app)
        .get('/leaderboard/999');

      expect(response.status).toBe(404);
      expect(response.body.error.code).toBe('NOT_FOUND');
      expect(response.body.error.message).toContain('User not found');
    });

    it('should handle player with no tournament history', async () => {
      const mockStats = {
        user_id: '5',
        username: 'newplayer',
        tournaments_played: '0',
        tournament_wins: '0',
        avg_finish: null,
        total_winnings: '0'
      };

      const queryBuilder = {
        leftJoin: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        addSelect: jest.fn().mockReturnThis(),
        where: jest.fn().mockReturnThis(),
        groupBy: jest.fn().mockReturnThis(),
        addGroupBy: jest.fn().mockReturnThis(),
        getRawOne: jest.fn().mockResolvedValue(mockStats)
      };

      mockUserRepository.createQueryBuilder.mockReturnValue(queryBuilder);

      const response = await request(app)
        .get('/leaderboard/5');

      expect(response.status).toBe(200);
      expect(response.body).toEqual({
        user_id: 5,
        username: 'newplayer',
        tournaments_played: 0,
        tournament_wins: 0,
        avg_finish: null,
        total_winnings: 0
      });
    });
  });
});
