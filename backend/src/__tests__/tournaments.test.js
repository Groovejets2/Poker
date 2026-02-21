/**
 * Tournament Routes Tests
 */

const request = require('supertest');
const express = require('express');
const tournamentRoutes = require('../routes/tournaments');
const authMiddleware = require('../middleware/auth');
const database = require('../database/db');

jest.mock('../database/db');
jest.mock('../middleware/auth', () => (req, res, next) => {
  req.user = { user_id: 1, username: 'player1' };
  next();
});

const app = express();
app.use(express.json());
app.use('/tournaments', tournamentRoutes);

describe('Tournament Routes', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('GET /tournaments', () => {
    it('should list tournaments', async () => {
      database.all.mockResolvedValue([
        { id: 1, name: 'Tournament 1', status: 'scheduled', player_count: 3, max_players: 8 }
      ]);
      database.get.mockResolvedValue({ count: 1 });

      const res = await request(app).get('/tournaments');

      expect(res.status).toBe(200);
      expect(res.body.tournaments.length).toBe(1);
      expect(res.body.pagination.total).toBe(1);
    });

    it('should filter by status', async () => {
      database.all.mockResolvedValue([]);
      database.get.mockResolvedValue({ count: 0 });

      const res = await request(app).get('/tournaments?status=completed');

      expect(res.status).toBe(200);
      expect(database.all).toHaveBeenCalledWith(expect.stringContaining('status = ?'), ['completed', 20, 0]);
    });

    it('should paginate results', async () => {
      database.all.mockResolvedValue([]);
      database.get.mockResolvedValue({ count: 50 });

      const res = await request(app).get('/tournaments?page=2&limit=10');

      expect(res.status).toBe(200);
      expect(database.all).toHaveBeenCalledWith(expect.any(String), expect.arrayContaining([10, 10]));
    });
  });

  describe('GET /tournaments/:id', () => {
    it('should get tournament details', async () => {
      database.get.mockResolvedValue({
        id: 1,
        name: 'Tournament 1',
        status: 'scheduled'
      });
      database.all.mockResolvedValue([
        { user_id: 1, username: 'player1', status: 'registered' }
      ]);

      const res = await request(app).get('/tournaments/1');

      expect(res.status).toBe(200);
      expect(res.body.name).toBe('Tournament 1');
      expect(res.body.players.length).toBe(1);
    });

    it('should return 404 for nonexistent tournament', async () => {
      database.get.mockResolvedValue(null);

      const res = await request(app).get('/tournaments/999');

      expect(res.status).toBe(404);
      expect(res.body.error.code).toBe('NOT_FOUND');
    });
  });

  describe('POST /tournaments/:id/register', () => {
    it('should register for tournament', async () => {
      database.get.mockResolvedValueOnce({ id: 1, max_players: 8, buy_in_chips: 10000 });
      database.get.mockResolvedValueOnce({ count: 2 });
      database.run.mockResolvedValue({ id: 1 });

      const res = await request(app).post('/tournaments/1/register').send({});

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.player_count).toBe(3);
    });

    it('should reject if already registered', async () => {
      database.get.mockResolvedValueOnce({ id: 1, max_players: 8 });
      database.get.mockResolvedValueOnce({ id: 1 });

      const res = await request(app).post('/tournaments/1/register').send({});

      expect(res.status).toBe(409);
      expect(res.body.error.code).toBe('CONFLICT');
    });

    it('should reject if tournament full', async () => {
      database.get.mockResolvedValueOnce({ id: 1, max_players: 4 });
      database.get.mockResolvedValueOnce({ count: 4 });

      const res = await request(app).post('/tournaments/1/register').send({});

      expect(res.status).toBe(400);
      expect(res.body.error.code).toBe('INVALID_REQUEST');
    });

    it('should reject nonexistent tournament', async () => {
      database.get.mockResolvedValue(null);

      const res = await request(app).post('/tournaments/999/register').send({});

      expect(res.status).toBe(404);
    });
  });

  describe('DELETE /tournaments/:id/unregister', () => {
    it('should unregister from tournament', async () => {
      database.run.mockResolvedValue({ changes: 1 });

      const res = await request(app).delete('/tournaments/1/unregister');

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
    });

    it('should return 404 if not registered', async () => {
      database.run.mockResolvedValue({ changes: 0 });

      const res = await request(app).delete('/tournaments/1/unregister');

      expect(res.status).toBe(404);
      expect(res.body.error.code).toBe('NOT_FOUND');
    });
  });
});
