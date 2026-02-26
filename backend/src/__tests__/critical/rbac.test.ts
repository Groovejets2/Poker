/**
 * CRIT-6: Role-Based Access Control Tests
 *
 * Tests to ensure RBAC system prevents unauthorized access
 * and allows authorized access based on user roles.
 */

import request from 'supertest';
import express from 'express';
import { AppDataSource } from '../../database/data-source';
import { User } from '../../database/entities/User';
import authRoutes from '../../routes/auth';
import tournamentRoutes from '../../routes/tournaments';
import authMiddleware from '../../middleware/auth';
import errorHandler from '../../middleware/errorHandler';
import bcrypt from 'bcryptjs';

const app = express();
app.use(express.json());
app.use('/api/auth', authRoutes);
app.use('/api/tournaments', tournamentRoutes);
app.use(errorHandler);

describe('CRIT-6: Role-Based Access Control', () => {
  beforeAll(async () => {
    // Initialize test database
    if (!AppDataSource.isInitialized) {
      await AppDataSource.initialize();
    }
  });

  afterAll(async () => {
    // Clean up
    if (AppDataSource.isInitialized) {
      await AppDataSource.destroy();
    }
  });

  beforeEach(async () => {
    // Clear users table before each test
    const userRepository = AppDataSource.getRepository(User);
    await userRepository.clear();
  });

  describe('User Entity - Role Column', () => {
    it('should create user with default role "player"', async () => {
      const userRepository = AppDataSource.getRepository(User);
      const passwordHash = await bcrypt.hash('password123', 12);

      const user = userRepository.create({
        username: 'testplayer',
        email: 'player@test.com',
        password_hash: passwordHash,
      });

      const savedUser = await userRepository.save(user);

      expect(savedUser.role).toBe('player');
    });

    it('should allow creating user with role "admin"', async () => {
      const userRepository = AppDataSource.getRepository(User);
      const passwordHash = await bcrypt.hash('password123', 12);

      const user = userRepository.create({
        username: 'testadmin',
        email: 'admin@test.com',
        password_hash: passwordHash,
        role: 'admin',
      });

      const savedUser = await userRepository.save(user);

      expect(savedUser.role).toBe('admin');
    });

    it('should allow creating user with role "moderator"', async () => {
      const userRepository = AppDataSource.getRepository(User);
      const passwordHash = await bcrypt.hash('password123', 12);

      const user = userRepository.create({
        username: 'testmod',
        email: 'mod@test.com',
        password_hash: passwordHash,
        role: 'moderator',
      });

      const savedUser = await userRepository.save(user);

      expect(savedUser.role).toBe('moderator');
    });
  });

  describe('JWT Payload - Role Inclusion', () => {
    it('should include role in JWT token on login', async () => {
      // Register a user (will have default role 'player')
      await request(app)
        .post('/api/auth/register')
        .send({
          username: 'jwttest',
          email: 'jwt@test.com',
          password: 'password123',
        });

      // Login
      const response = await request(app)
        .post('/api/auth/login')
        .send({
          username: 'jwttest',
          password: 'password123',
        });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('token');
      expect(response.body).toHaveProperty('role');
      expect(response.body.role).toBe('player');
    });

    it('should include admin role in JWT for admin user', async () => {
      // Create admin user directly
      const userRepository = AppDataSource.getRepository(User);
      const passwordHash = await bcrypt.hash('adminpass', 12);
      await userRepository.save({
        username: 'admin',
        email: 'admin@test.com',
        password_hash: passwordHash,
        role: 'admin',
      });

      // Login as admin
      const response = await request(app)
        .post('/api/auth/login')
        .send({
          username: 'admin',
          password: 'adminpass',
        });

      expect(response.status).toBe(200);
      expect(response.body.role).toBe('admin');
    });
  });

  describe('Tournament Creation Authorization', () => {
    let playerToken: string;
    let adminToken: string;

    beforeEach(async () => {
      // Create player user
      const userRepository = AppDataSource.getRepository(User);
      const playerHash = await bcrypt.hash('playerpass', 12);
      await userRepository.save({
        username: 'player',
        email: 'player@test.com',
        password_hash: playerHash,
        role: 'player',
      });

      // Create admin user
      const adminHash = await bcrypt.hash('adminpass', 12);
      await userRepository.save({
        username: 'admin',
        email: 'admin@test.com',
        password_hash: adminHash,
        role: 'admin',
      });

      // Get tokens
      const playerResponse = await request(app)
        .post('/api/auth/login')
        .send({ username: 'player', password: 'playerpass' });
      playerToken = playerResponse.body.token;

      const adminResponse = await request(app)
        .post('/api/auth/login')
        .send({ username: 'admin', password: 'adminpass' });
      adminToken = adminResponse.body.token;
    });

    it('should reject tournament creation by regular player (403)', async () => {
      const response = await request(app)
        .post('/api/tournaments')
        .set('Authorization', `Bearer ${playerToken}`)
        .send({
          name: 'Test Tournament',
          buy_in_chips: 1000,
          entry_fee_usd: 10,
          max_players: 8,
          scheduled_at: new Date().toISOString(),
        });

      expect(response.status).toBe(403);
      expect(response.body.error.code).toBe('FORBIDDEN');
      expect(response.body.error.message).toContain('Insufficient permissions');
    });

    it('should allow tournament creation by admin (201)', async () => {
      const response = await request(app)
        .post('/api/tournaments')
        .set('Authorization', `Bearer ${adminToken}`)
        .send({
          name: 'Admin Tournament',
          buy_in_chips: 1000,
          entry_fee_usd: 10,
          max_players: 8,
          scheduled_at: new Date().toISOString(),
        });

      expect(response.status).toBe(201);
      expect(response.body.name).toBe('Admin Tournament');
    });

    it('should return appropriate error message for unauthorized users', async () => {
      const response = await request(app)
        .post('/api/tournaments')
        .set('Authorization', `Bearer ${playerToken}`)
        .send({
          name: 'Test',
          buy_in_chips: 1000,
          entry_fee_usd: 10,
          max_players: 8,
          scheduled_at: new Date().toISOString(),
        });

      expect(response.status).toBe(403);
      expect(response.body.error).toMatchObject({
        code: 'FORBIDDEN',
        message: expect.stringContaining('Insufficient permissions'),
        required_role: 'admin',
      });
    });
  });

  describe('Registration - Role Assignment', () => {
    it('should assign "player" role to new registrations', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          username: 'newuser',
          email: 'new@test.com',
          password: 'password123',
        });

      expect(response.status).toBe(201);

      // Verify in database
      const userRepository = AppDataSource.getRepository(User);
      const user = await userRepository.findOne({ where: { username: 'newuser' } });
      expect(user?.role).toBe('player');
    });

    it('should NOT allow setting role during registration via API', async () => {
      // Try to register with admin role
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          username: 'hacker',
          email: 'hacker@test.com',
          password: 'password123',
          role: 'admin', // Attempt to set admin role
        });

      // Registration might succeed, but role should be 'player'
      const userRepository = AppDataSource.getRepository(User);
      const user = await userRepository.findOne({ where: { username: 'hacker' } });
      expect(user?.role).toBe('player');
    });
  });
});
