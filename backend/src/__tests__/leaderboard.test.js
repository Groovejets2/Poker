/**
 * Leaderboard Routes Tests
 */

const request = require('supertest');
const express = require('express');
const leaderboardRoutes = require('../routes/leaderboard');
const database = require('../database/db');

jest.mock('../database/db');

const app = express();
app.use(express.json());
app.use('/leaderboard', leaderboardRoutes);

describe('Leaderboard Routes', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('GET /leaderboard', () => {
    it('should return global leaderboard', async () => {
      database.all.mockResolvedValue([
        {
          user_id: 1,
          username: 'player1',
          tournaments_played: 5,
          tournament_wins: 2,
          avg_finish: 2.5,
          total_winnings: 150.00
        }
      ]);

      const res = await request(app).get('/leaderboard');

      expect(res.status).toBe(200);
      expect(res.body.leaderboard).toHaveLength(1);
      expect(res.body.leaderboard[0].rank).toBe(1);
      expect(res.body.updated_at).toBeDefined();
    });

    it('should respect limit parameter', async () => {
      database.all.mockResolvedValue([]);

      await request(app).get('/leaderboard?limit=10');

      expect(database.all).toHaveBeenCalledWith(expect.any(String), expect.arrayContaining([10, 0]));
    });

    it('should cap limit at 100', async () => {
      database.all.mockResolvedValue([]);

      await request(app).get('/leaderboard?limit=500');

      expect(database.all).toHaveBeenCalledWith(expect.any(String), expect.arrayContaining([100, 0]));
    });
  });

  describe('GET /leaderboard/:user_id', () => {
    it('should return player stats', async () => {
      database.get.mockResolvedValue({
        user_id: 1,
        username: 'player1',
        tournaments_played: 5,
        tournament_wins: 2,
        avg_finish: 2.5,
        total_winnings: 150.00
      });

      const res = await request(app).get('/leaderboard/1');

      expect(res.status).toBe(200);
      expect(res.body.username).toBe('player1');
      expect(res.body.total_winnings).toBe(150.00);
    });

    it('should return 404 for nonexistent user', async () => {
      database.get.mockResolvedValue(null);

      const res = await request(app).get('/leaderboard/999');

      expect(res.status).toBe(404);
      expect(res.body.error.code).toBe('NOT_FOUND');
    });
  });
});
