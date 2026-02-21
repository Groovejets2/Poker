/**
 * Match Route Tests
 */

const request = require('supertest');
const express = require('express');
const jwt = require('jsonwebtoken');
const matchRoutes = require('../matches');
const database = require('../../database/db');

jest.mock('../../database/db');

describe('Match Routes', () => {
  let app;
  let token;

  beforeEach(() => {
    app = express();
    app.use(express.json());
    app.use('/', matchRoutes);

    token = jwt.sign(
      { user_id: 1, username: 'player1' },
      'dev-secret-key'
    );

    jest.clearAllMocks();
  });

  describe('GET /tournament/:tournament_id', () => {
    test('should return matches for tournament', async () => {
      database.all.mockResolvedValue([
        { id: 1, table_number: 1, game_number: 1, status: 'completed', winner: 'player1' }
      ]);

      const res = await request(app).get('/tournament/1');

      expect(res.status).toBe(200);
      expect(res.body.matches).toHaveLength(1);
    });

    test('should return empty matches list', async () => {
      database.all.mockResolvedValue([]);

      const res = await request(app).get('/tournament/1');

      expect(res.status).toBe(200);
      expect(res.body.matches).toHaveLength(0);
    });
  });

  describe('GET /:id', () => {
    test('should return 404 if match not found', async () => {
      database.get.mockResolvedValue(null);

      const res = await request(app).get('/999');

      expect(res.status).toBe(404);
      expect(res.body.error.code).toBe('NOT_FOUND');
    });

    test('should return match with players', async () => {
      database.get.mockResolvedValue({
        id: 1,
        tournament_id: 1,
        table_number: 1,
        status: 'completed',
        winner_id: 1
      });
      database.all.mockResolvedValue([
        { user_id: 1, username: 'player1', status: 'won', ending_stack: 25000 },
        { user_id: 2, username: 'player2', status: 'eliminated', ending_stack: 0 }
      ]);

      const res = await request(app).get('/1');

      expect(res.status).toBe(200);
      expect(res.body.players).toHaveLength(2);
    });
  });

  describe('POST /:id/submit-score', () => {
    test('should return 401 if not authenticated', async () => {
      const res = await request(app)
        .post('/1/submit-score')
        .send({});

      expect(res.status).toBe(401);
    });

    test('should return 400 if missing required fields', async () => {
      const res = await request(app)
        .post('/1/submit-score')
        .set('Authorization', `Bearer ${token}`)
        .send({ winner_id: 1 });

      expect(res.status).toBe(400);
      expect(res.body.error.code).toBe('INVALID_REQUEST');
    });

    test('should submit score successfully', async () => {
      database.run.mockResolvedValue({ changes: 1 });

      const res = await request(app)
        .post('/1/submit-score')
        .set('Authorization', `Bearer ${token}`)
        .send({
          winner_id: 1,
          results: [
            { user_id: 1, ending_stack: 25000, status: 'won' },
            { user_id: 2, ending_stack: 0, status: 'eliminated' }
          ]
        });

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
    });

    test('should update all player records', async () => {
      database.run.mockResolvedValue({ changes: 1 });

      const results = [
        { user_id: 1, ending_stack: 25000, status: 'won' },
        { user_id: 2, ending_stack: 0, status: 'eliminated' }
      ];

      await request(app)
        .post('/1/submit-score')
        .set('Authorization', `Bearer ${token}`)
        .send({ winner_id: 1, results });

      expect(database.run).toHaveBeenCalledTimes(3); // 1 match update + 2 player updates
    });
  });
});
