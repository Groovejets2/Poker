import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

/**
 * JWT payload interface
 * CRIT-6 FIX: Added role field for RBAC
 */
export interface JwtPayload {
  user_id: number;
  username: string;
  role: string; // 'player' | 'admin' | 'moderator'
}

/**
 * Extend Express Request to include user property
 */
declare global {
  namespace Express {
    interface Request {
      user?: JwtPayload;
    }
  }
}

// CRIT-1 FIX: Require JWT_SECRET - no fallback allowed
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) {
  console.error('FATAL: JWT_SECRET environment variable is not set');
  console.error('Generate a secret with: openssl rand -base64 32');
  console.error('Then add to .env file: JWT_SECRET=your_generated_secret');
  process.exit(1);
}

/**
 * JWT Authentication Middleware
 * Verifies JWT token and attaches decoded payload to req.user
 */
const authMiddleware = (req: Request, res: Response, next: NextFunction): void => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    res.status(401).json({
      error: {
        code: 'UNAUTHORIZED',
        message: 'Missing authentication token'
      }
    });
    return;
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET) as JwtPayload;

    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({
      error: {
        code: 'UNAUTHORIZED',
        message: 'Invalid or expired token'
      }
    });
    return;
  }
};

export default authMiddleware;
