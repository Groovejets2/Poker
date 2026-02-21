/**
 * Authentication Route Tests
 */

const request = require('supertest');
const express = require('express');
const bcrypt = require('bcryptjs');
const authRoutes = require('../auth');
const database = require('../../database/db');

// Mock database
jest.mock('../../database/db', () => ({
  run: jest.fn(),
  get: jest.fn()
}));

describe('Auth Routes', () => {
  let app;

  beforeEach(() => {
    app = express();
    app.use(express.json());
    app.use('/auth', authRoutes);
    jest.clearAllMocks();
  });

  describe('POST /auth/login', () => {
    test('should return 400 if username or password missing', async () => {
      const res = await request(app)
        .post('/auth/login')
        .send({ username: 'player1' });

      expect(res.status).toBe(400);
      expect(res.body.error.code).toBe('INVALID_REQUEST');
    });

    test('should return 401 if user not found', async () => {
      database.get.mockResolvedValue(null);

      const res = await request(app)
        .post('/auth/login')
        .send({ username: 'nonexistent', password: 'password123' });

      expect(res.status).toBe(401);
      expect(res.body.error.code).toBe('UNAUTHORIZED');
    });

    test('should return 401 if password incorrect', async () => {
      database.get.mockResolvedValue({
        id: 1,
        username: 'player1',
        password_hash: await bcrypt.hash('password123', 12)
      });

      const res = await request(app)
        .post('/auth/login')
        .send({ username: 'player1', password: 'wrongpassword' });

      expect(res.status).toBe(401);
      expect(res.body.error.code).toBe('UNAUTHORIZED');
    });

    test('should return token if credentials valid', async () => {
      const hash = await bcrypt.hash('password123', 12);
      database.get.mockResolvedValue({
        id: 1,
        username: 'player1',
        password_hash: hash
      });

      const res = await request(app)
        .post('/auth/login')
        .send({ username: 'player1', password: 'password123' });

      expect(res.status).toBe(200);
      expect(res.body.token).toBeDefined();
      expect(res.body.user_id).toBe(1);
      expect(res.body.username).toBe('player1');
      expect(res.body.expires_in).toBe(3600);
    });
  });

  describe('POST /auth/register', () => {
    test('should reject invalid username', async () => {
      const res = await request(app)
        .post('/auth/register')
        .send({ username: 'ab', password: 'password123' });

      expect(res.status).toBe(400);
      expect(res.body.error.code).toBe('INVALID_REQUEST');
    });

    test('should reject weak password', async () => {
      const res = await request(app)
        .post('/auth/register')
        .send({ username: 'player1', password: 'weak' });

      expect(res.status).toBe(400);
      expect(res.body.error.code).toBe('INVALID_REQUEST');
    });

    test('should reject invalid email', async () => {
      const res = await request(app)
        .post('/auth/register')
        .send({
          username: 'player1',
          password: 'password123',
          email: 'invalid-email'
        });

      expect(res.status).toBe(400);
      expect(res.body.error.code).toBe('INVALID_REQUEST');
    });

    test('should create user successfully', async () => {
      database.run.mockResolvedValue({ id: 1 });

      const res = await request(app)
        .post('/auth/register')
        .send({
          username: 'newplayer',
          password: 'password123',
          email: 'new@test.local'
        });

      expect(res.status).toBe(201);
      expect(res.body.user_id).toBe(1);
      expect(res.body.username).toBe('newplayer');
    });

    test('should return 409 if username exists', async () => {
      database.run.mockRejectedValue(
        new Error('UNIQUE constraint failed: users.username')
      );

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
});
