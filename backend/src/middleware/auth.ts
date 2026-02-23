import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

/**
 * JWT payload interface
 */
export interface JwtPayload {
  user_id: number;
  username: string;
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
    const decoded = jwt.verify(
      token,
      process.env.JWT_SECRET || 'dev-secret-key'
    ) as JwtPayload;

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
