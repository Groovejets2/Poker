/**
 * Leaderboard Route Tests
 */

const request = require('supertest');
const express = require('express');
const leaderboardRoutes = require('../leaderboard');
const database = require('../../database/db');

jest.mock('../../database/db');

describe('Leaderboard Routes', () => {
  let app;

  beforeEach(() => {
    app = express();
    app.use(express.json());
    app.use('/', leaderboardRoutes);
    jest.clearAllMocks();
  });

  describe('GET /', () => {
    test('should return global leaderboard', async () => {
      database.all.mockResolvedValue([
        {
          user_id: 1,
          username: 'player1',
          tournaments_played: 5,
          tournament_wins: 2,
          avg_finish: 2.0,
          total_winnings: 250.00
        },
        {
          user_id: 2,
          username: 'player2',
          tournaments_played: 3,
          tournament_wins: 1,
          avg_finish: 3.5,
          total_winnings: 100.00
        }
      ]);

      const res = await request(app).get('/');

      expect(res.status).toBe(200);
      expect(res.body.leaderboard).toHaveLength(2);
      expect(res.body.leaderboard[0].rank).toBe(1);
      expect(res.body.leaderboard[1].rank).toBe(2);
    });

    test('should support pagination', async () => {
      database.all.mockResolvedValue([]);

      const res = await request(app)
        .get('/')
        .query({ limit: 25, offset: 50 });

      expect(res.status).toBe(200);
      expect(database.all).toHaveBeenCalledWith(
        expect.any(String),
        expect.arrayContaining([25, 50])
      );
    });

    test('should limit max results to 100', async () => {
      database.all.mockResolvedValue([]);

      await request(app)
        .get('/')
        .query({ limit: 500 });

      const callArgs = database.all.mock.calls[0][1];
      expect(callArgs[0]).toBeLessThanOrEqual(100);
    });
  });

  describe('GET /:user_id', () => {
    test('should return 404 if user not found', async () => {
      database.get.mockResolvedValue(null);

      const res = await request(app).get('/999');

      expect(res.status).toBe(404);
      expect(res.body.error.code).toBe('NOT_FOUND');
    });

    test('should return player stats', async () => {
      database.get.mockResolvedValue({
        user_id: 1,
        username: 'player1',
        tournaments_played: 5,
        tournament_wins: 2,
        avg_finish: 2.0,
        total_winnings: 250.00
      });

      const res = await request(app).get('/1');

      expect(res.status).toBe(200);
      expect(res.body.username).toBe('player1');
      expect(res.body.tournaments_played).toBe(5);
      expect(res.body.tournament_wins).toBe(2);
    });

    test('should handle users with no tournament history', async () => {
      database.get.mockResolvedValue({
        user_id: 2,
        username: 'newplayer',
        tournaments_played: 0,
        tournament_wins: 0,
        avg_finish: null,
        total_winnings: 0
      });

      const res = await request(app).get('/2');

      expect(res.status).toBe(200);
      expect(res.body.tournaments_played).toBe(0);
    });

    test('should calculate correct averages', async () => {
      database.get.mockResolvedValue({
        user_id: 1,
        username: 'player1',
        tournaments_played: 4,
        tournament_wins: 1,
        avg_finish: 2.75,
        total_winnings: 150.50
      });

      const res = await request(app).get('/1');

      expect(res.status).toBe(200);
      expect(res.body.avg_finish).toBe(2.75);
    });
  });
});
