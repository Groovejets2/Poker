import { Router, Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { AppDataSource } from '../database/data-source';
import { User } from '../database/entities/User';
import * as validators from '../utils/validation';

const router = Router();
const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-key';
const JWT_EXPIRY = 3600; // 1 hour

/**
 * POST /auth/login
 * Login user and return JWT token
 */
router.post('/login', async (req: Request, res: Response, next: NextFunction) => {
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

    const userRepository = AppDataSource.getRepository(User);
    const user = await userRepository.findOne({
      where: { username }
    });

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
router.post('/register', async (req: Request, res: Response, next: NextFunction) => {
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
    const userRepository = AppDataSource.getRepository(User);

    const newUser = userRepository.create({
      username,
      email: email || null,
      password_hash: passwordHash
    });

    const savedUser = await userRepository.save(newUser);

    res.status(201).json({
      user_id: savedUser.id,
      username: savedUser.username,
      message: 'User created successfully'
    });
  } catch (err: any) {
    if (err.message?.includes('UNIQUE constraint failed') || err.code === 'ER_DUP_ENTRY') {
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

export default router;
