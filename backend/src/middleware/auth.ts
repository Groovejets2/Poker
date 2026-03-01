import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export interface JwtPayload { user_id: number; username: string; role: string; }

declare global { namespace Express { interface Request { user?: JwtPayload; } } }

const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) {
  console.error('FATAL: JWT_SECRET environment variable is not set');
  console.error('Generate a secret with: openssl rand -base64 32');
  process.exit(1);
}

/**
 * JWT Authentication Middleware
 * Phase 3.8: Cookie-first, falls back to Authorization header.
 */
const authMiddleware = (req: Request, res: Response, next: NextFunction): void => {
  const token = req.cookies?.access_token ?? req.headers.authorization?.split(' ')[1];
  if (!token) {
    res.status(401).json({ error: { code: 'UNAUTHORIZED', message: 'Missing authentication token' } });
    return;
  }
  try {
    const decoded = jwt.verify(token, JWT_SECRET) as JwtPayload;
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ error: { code: 'UNAUTHORIZED', message: 'Invalid or expired token' } });
    return;
  }
};

export default authMiddleware;
