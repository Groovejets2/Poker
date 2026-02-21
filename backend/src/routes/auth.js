/**
 * Authentication Routes
 */

const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const database = require('../database/db');
const validators = require('../utils/validation');

const router = express.Router();
const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-key';
const JWT_EXPIRY = 3600; // 1 hour

/**
 * POST /auth/login
 * Login user and return JWT token
 */
router.post('/login', async (req, res, next) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({
        error: {
          code: 'INVALID_REQUEST',
          message: 'Username and password are required'
        }
      });
    }

    const user = await database.get(
      'SELECT id, username, password_hash FROM users WHERE username = ?',
      [username]
    );

    if (!user) {
      return res.status(401).json({
        error: {
          code: 'UNAUTHORIZED',
          message: 'Invalid credentials'
        }
      });
    }

    const passwordMatch = await bcrypt.compare(password, user.password_hash);
    if (!passwordMatch) {
      return res.status(401).json({
        error: {
          code: 'UNAUTHORIZED',
          message: 'Invalid credentials'
        }
      });
    }

    const token = jwt.sign(
      { user_id: user.id, username: user.username },
      JWT_SECRET,
      { expiresIn: JWT_EXPIRY }
    );

    res.json({
      token,
      user_id: user.id,
      username: user.username,
      expires_in: JWT_EXPIRY
    });
  } catch (err) {
    next(err);
  }
});

/**
 * POST /auth/register
 * Create new user account
 */
router.post('/register', async (req, res, next) => {
  try {
    const { username, email, password } = req.body;

    if (!validators.username(username)) {
      return res.status(400).json({
        error: {
          code: 'INVALID_REQUEST',
          message: 'Username: 3-32 chars, alphanumeric + underscore'
        }
      });
    }

    if (!validators.password(password)) {
      return res.status(400).json({
        error: {
          code: 'INVALID_REQUEST',
          message: 'Password must be at least 6 characters'
        }
      });
    }

    if (email && !validators.email(email)) {
      return res.status(400).json({
        error: {
          code: 'INVALID_REQUEST',
          message: 'Invalid email format'
        }
      });
    }

    const passwordHash = await bcrypt.hash(password, 12);

    const result = await database.run(
      'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
      [username, email || null, passwordHash]
    );

    res.status(201).json({
      user_id: result.id,
      username: username,
      message: 'User created successfully'
    });
  } catch (err) {
    if (err.message?.includes('UNIQUE constraint failed')) {
      return res.status(409).json({
        error: {
          code: 'CONFLICT',
          message: 'Username or email already exists'
        }
      });
    }
    next(err);
  }
});

module.exports = router;
