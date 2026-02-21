/**
 * Tournament Route Tests
 */

const request = require('supertest');
const express = require('express');
const jwt = require('jsonwebtoken');
const tournamentRoutes = require('../tournaments');
const database = require('../../database/db');

jest.mock('../../database/db');

describe('Tournament Routes', () => {
  let app;
  let token;

  beforeEach(() => {
    app = express();
    app.use(express.json());
    app.use('/', tournamentRoutes);

    token = jwt.sign(
      { user_id: 1, username: 'player1' },
      'dev-secret-key',
      { expiresIn: 3600 }
    );

    jest.clearAllMocks();
  });

  describe('GET /', () => {
    test('should return tournaments with pagination', async () => {
      database.all.mockResolvedValue([
        { id: 1, name: 'Tournament 1', status: 'scheduled', player_count: 3, max_players: 8 }
      ]);
      database.get.mockResolvedValue({ count: 1 });

      const res = await request(app)
        .get('/')
        .query({ page: 1, limit: 20 });

      expect(res.status).toBe(200);
      expect(res.body.tournaments).toHaveLength(1);
      expect(res.body.pagination.total).toBe(1);
    });

    test('should filter by status', async () => {
      database.all.mockResolvedValue([]);
      database.get.mockResolvedValue({ count: 0 });

      const res = await request(app)
        .get('/')
        .query({ status: 'scheduled' });

      expect(res.status).toBe(200);
      expect(database.all).toHaveBeenCalledWith(
        expect.stringContaining('status = ?'),
        expect.arrayContaining(['scheduled'])
      );
    });
  });

  describe('GET /:id', () => {
    test('should return 404 if tournament not found', async () => {
      database.get.mockResolvedValue(null);

      const res = await request(app).get('/1');

      expect(res.status).toBe(404);
      expect(res.body.error.code).toBe('NOT_FOUND');
    });

    test('should return tournament with players', async () => {
      database.get.mockResolvedValue({
        id: 1,
        name: 'Tournament 1',
        status: 'scheduled'
      });
      database.all.mockResolvedValue([
        { user_id: 1, username: 'player1', status: 'registered' }
      ]);

      const res = await request(app).get('/1');

      expect(res.status).toBe(200);
      expect(res.body.id).toBe(1);
      expect(res.body.players).toHaveLength(1);
    });
  });

  describe('POST /:id/register', () => {
    test('should return 401 if not authenticated', async () => {
      const res = await request(app)
        .post('/1/register')
        .send({});

      expect(res.status).toBe(401);
    });

    test('should return 404 if tournament not found', async () => {
      database.get.mockResolvedValue(null);

      const res = await request(app)
        .post('/999/register')
        .set('Authorization', `Bearer ${token}`)
        .send({});

      expect(res.status).toBe(404);
    });

    test('should return 409 if already registered', async () => {
      database.get.mockResolvedValue({ id: 1, max_players: 8, buy_in_chips: 10000 });
      database.get
        .mockResolvedValueOnce({ id: 1, max_players: 8, buy_in_chips: 10000 })
        .mockResolvedValueOnce({ id: 1, user_id: 1 }); // existing registration

      const res = await request(app)
        .post('/1/register')
        .set('Authorization', `Bearer ${token}`)
        .send({});

      expect(res.status).toBe(409);
    });

    test('should return 400 if tournament full', async () => {
      database.get
        .mockResolvedValueOnce({ id: 1, max_players: 2, buy_in_chips: 10000 })
        .mockResolvedValueOnce(null) // not already registered
        .mockResolvedValueOnce({ count: 2 }); // tournament full

      const res = await request(app)
        .post('/1/register')
        .set('Authorization', `Bearer ${token}`)
        .send({});

      expect(res.status).toBe(400);
    });

    test('should register player successfully', async () => {
      database.get
        .mockResolvedValueOnce({ id: 1, max_players: 8, buy_in_chips: 10000 })
        .mockResolvedValueOnce(null) // not already registered
        .mockResolvedValueOnce({ count: 2 }); // 2 seats available
      database.run.mockResolvedValue({ id: 1 });

      const res = await request(app)
        .post('/1/register')
        .set('Authorization', `Bearer ${token}`)
        .send({});

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.player_count).toBe(3);
    });
  });

  describe('DELETE /:id/unregister', () => {
    test('should return 401 if not authenticated', async () => {
      const res = await request(app).delete('/1/unregister');

      expect(res.status).toBe(401);
    });

    test('should return 404 if not registered', async () => {
      database.run.mockResolvedValue({ changes: 0 });

      const res = await request(app)
        .delete('/1/unregister')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(404);
    });

    test('should unregister successfully', async () => {
      database.run.mockResolvedValue({ changes: 1 });

      const res = await request(app)
        .delete('/1/unregister')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
    });
  });
});
