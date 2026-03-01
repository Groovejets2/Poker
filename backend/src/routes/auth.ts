import { Router, Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import crypto from 'crypto';
import { AppDataSource } from '../database/data-source';
import { User } from '../database/entities/User';
import * as validators from '../utils/validation';

const router = Router();

const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) { console.error('FATAL: JWT_SECRET not set'); process.exit(1); }

const REFRESH_SECRET = process.env.REFRESH_SECRET;
if (!REFRESH_SECRET) {
  console.error('FATAL: REFRESH_SECRET environment variable is not set');
  console.error('Generate with: openssl rand -base64 32');
  process.exit(1);
}

const ACCESS_TOKEN_EXPIRY_SECS = 15 * 60;
const REFRESH_TOKEN_EXPIRY_SECS = 7 * 24 * 60 * 60;

const COOKIE_BASE = {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'strict' as const,
};

const hashToken = (token: string): string =>
  crypto.createHash('sha256').update(token).digest('hex');

const compareHashes = (a: string, b: string): boolean => {
  const bufA = Buffer.from(a, 'hex');
  const bufB = Buffer.from(b, 'hex');
  if (bufA.length !== bufB.length) return false;
  return crypto.timingSafeEqual(bufA, bufB);
};

router.post('/login', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) return res.status(400).json({ error: { code: 'INVALID_REQUEST', message: 'Username and password are required' } });

    const userRepository = AppDataSource.getRepository(User);
    const user = await userRepository.findOne({ where: { username } });
    if (!user) return res.status(401).json({ error: { code: 'UNAUTHORIZED', message: 'Invalid credentials' } });

    const passwordMatch = await bcrypt.compare(password, user.password_hash);
    if (!passwordMatch) return res.status(401).json({ error: { code: 'UNAUTHORIZED', message: 'Invalid credentials' } });

    const payload = { user_id: user.id, username: user.username, role: user.role };
    const accessToken = jwt.sign(payload, JWT_SECRET, { expiresIn: ACCESS_TOKEN_EXPIRY_SECS });
    const refreshToken = jwt.sign(payload, REFRESH_SECRET, { expiresIn: REFRESH_TOKEN_EXPIRY_SECS });

    user.refresh_token_hash = hashToken(refreshToken);
    user.refresh_token_expires_at = new Date(Date.now() + REFRESH_TOKEN_EXPIRY_SECS * 1000);
    await userRepository.save(user);

    res.cookie('access_token', accessToken, { ...COOKIE_BASE, maxAge: ACCESS_TOKEN_EXPIRY_SECS * 1000 });
    res.cookie('refresh_token', refreshToken, { ...COOKIE_BASE, maxAge: REFRESH_TOKEN_EXPIRY_SECS * 1000, path: '/api/auth' });
    res.json({ user_id: user.id, username: user.username, role: user.role });
  } catch (err) { next(err); }
});

router.post('/refresh', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const refreshToken = req.cookies?.refresh_token;
    if (!refreshToken) return res.status(401).json({ error: { code: 'UNAUTHORIZED', message: 'No refresh token' } });

    let decoded: { user_id: number; username: string; role: string };
    try { decoded = jwt.verify(refreshToken, REFRESH_SECRET) as typeof decoded; }
    catch { return res.status(401).json({ error: { code: 'UNAUTHORIZED', message: 'Invalid or expired refresh token' } }); }

    const userRepository = AppDataSource.getRepository(User);
    const user = await userRepository.findOne({ where: { id: decoded.user_id } });
    if (!user || !user.refresh_token_hash || !user.refresh_token_expires_at)
      return res.status(401).json({ error: { code: 'UNAUTHORIZED', message: 'Session not found' } });

    if (user.refresh_token_expires_at < new Date()) {
      user.refresh_token_hash = null; user.refresh_token_expires_at = null;
      await userRepository.save(user);
      return res.status(401).json({ error: { code: 'UNAUTHORIZED', message: 'Refresh token expired' } });
    }

    if (!compareHashes(hashToken(refreshToken), user.refresh_token_hash)) {
      user.refresh_token_hash = null; user.refresh_token_expires_at = null;
      await userRepository.save(user);
      return res.status(401).json({ error: { code: 'UNAUTHORIZED', message: 'Refresh token reuse detected' } });
    }

    const payload = { user_id: user.id, username: user.username, role: user.role };
    const newAccessToken = jwt.sign(payload, JWT_SECRET, { expiresIn: ACCESS_TOKEN_EXPIRY_SECS });
    const newRefreshToken = jwt.sign(payload, REFRESH_SECRET, { expiresIn: REFRESH_TOKEN_EXPIRY_SECS });
    user.refresh_token_hash = hashToken(newRefreshToken);
    user.refresh_token_expires_at = new Date(Date.now() + REFRESH_TOKEN_EXPIRY_SECS * 1000);
    await userRepository.save(user);

    res.cookie('access_token', newAccessToken, { ...COOKIE_BASE, maxAge: ACCESS_TOKEN_EXPIRY_SECS * 1000 });
    res.cookie('refresh_token', newRefreshToken, { ...COOKIE_BASE, maxAge: REFRESH_TOKEN_EXPIRY_SECS * 1000, path: '/api/auth' });
    res.json({ user_id: user.id, username: user.username, role: user.role });
  } catch (err) { next(err); }
});

router.post('/logout', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const accessToken = req.cookies?.access_token;
    if (accessToken) {
      const decoded = jwt.decode(accessToken) as { user_id?: number } | null;
      if (decoded?.user_id) {
        const userRepository = AppDataSource.getRepository(User);
        const user = await userRepository.findOne({ where: { id: decoded.user_id } });
        if (user) { user.refresh_token_hash = null; user.refresh_token_expires_at = null; await userRepository.save(user); }
      }
    }
    res.clearCookie('access_token', COOKIE_BASE);
    res.clearCookie('refresh_token', { ...COOKIE_BASE, path: '/api/auth' });
    res.json({ message: 'Logged out successfully' });
  } catch (err) { next(err); }
});

router.post('/register', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { username, email, password } = req.body;
    if (!validators.username(username)) return res.status(400).json({ error: { code: 'INVALID_REQUEST', message: 'Username: 3-32 chars, alphanumeric + underscore' } });
    if (!validators.password(password)) return res.status(400).json({ error: { code: 'INVALID_REQUEST', message: 'Password must be at least 6 characters' } });
    if (email && !validators.email(email)) return res.status(400).json({ error: { code: 'INVALID_REQUEST', message: 'Invalid email format' } });

    const passwordHash = await bcrypt.hash(password, 12);
    const userRepository = AppDataSource.getRepository(User);
    const newUser = userRepository.create({ username, email: email || null, password_hash: passwordHash });
    const savedUser = await userRepository.save(newUser);
    res.status(201).json({ user_id: savedUser.id, username: savedUser.username, message: 'User created successfully' });
  } catch (err: any) {
    if (err.message?.includes('UNIQUE constraint failed') || err.code === 'ER_DUP_ENTRY')
      return res.status(409).json({ error: { code: 'CONFLICT', message: 'Username or email already exists' } });
    next(err);
  }
});

export default router;
