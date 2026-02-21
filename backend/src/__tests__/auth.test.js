/**
 * Authentication Routes Tests
 */

const request = require('supertest');
const express = require('express');
const authRoutes = require('../routes/auth');
const database = require('../database/db');

// Mock database
jest.mock('../database/db');

const app = express();
app.use(express.json());
app.use('/auth', authRoutes);

describe('Auth Routes', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('POST /auth/register', () => {
    it('should register new user', async () => {
      database.run.mockResolvedValue({ id: 1 });

      const res = await request(app)
        .post('/auth/register')
        .send({
          username: 'newuser',
          email: 'new@test.com',
          password: 'password123'
        });

      expect(res.status).toBe(201);
      expect(res.body.user_id).toBe(1);
      expect(res.body.username).toBe('newuser');
    });

    it('should reject invalid username', async () => {
      const res = await request(app)
        .post('/auth/register')
        .send({
          username: 'ab',
          password: 'password123'
        });

      expect(res.status).toBe(400);
      expect(res.body.error.code).toBe('INVALID_REQUEST');
    });

    it('should reject short password', async () => {
      const res = await request(app)
        .post('/auth/register')
        .send({
          username: 'testuser',
          password: '123'
        });

      expect(res.status).toBe(400);
    });

    it('should reject invalid email', async () => {
      const res = await request(app)
        .post('/auth/register')
        .send({
          username: 'testuser',
          email: 'not-an-email',
          password: 'password123'
        });

      expect(res.status).toBe(400);
    });

    it('should reject duplicate username', async () => {
      const err = new Error('UNIQUE constraint failed');
      err.message = 'UNIQUE constraint failed: users.username';
      database.run.mockRejectedValue(err);

      const res = await request(app)
        .post('/auth/register')
        .send({
          username: 'existing',
          password: 'password123'
        });

      expect(res.status).toBe(409);
      expect(res.body.error.code).toBe('CONFLICT');
    });
  });

  describe('POST /auth/login', () => {
    it('should login successfully', async () => {
      database.get.mockResolvedValue({
        id: 1,
        username: 'player1',
        password_hash: '$2a$12$mockhashedpassword'
      });

      const res = await request(app)
        .post('/auth/login')
        .send({
          username: 'player1',
          password: 'password123'
        });

      expect(res.status).toBe(200);
      expect(res.body.token).toBeDefined();
      expect(res.body.user_id).toBe(1);
      expect(res.body.expires_in).toBe(3600);
    });

    it('should reject missing credentials', async () => {
      const res = await request(app)
        .post('/auth/login')
        .send({ username: 'player1' });

      expect(res.status).toBe(400);
    });

    it('should reject nonexistent user', async () => {
      database.get.mockResolvedValue(null);

      const res = await request(app)
        .post('/auth/login')
        .send({
          username: 'nonexistent',
          password: 'password123'
        });

      expect(res.status).toBe(401);
      expect(res.body.error.code).toBe('UNAUTHORIZED');
    });
  });
});
