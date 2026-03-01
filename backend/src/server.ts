import 'reflect-metadata';
import dotenv from 'dotenv';
dotenv.config();

import express, { Express, Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import cookieParser from 'cookie-parser';
import rateLimit from 'express-rate-limit';
import { AppDataSource } from './database/data-source';
import authRoutes from './routes/auth';
import tournamentRoutes from './routes/tournaments';
import matchRoutes from './routes/matches';
import leaderboardRoutes from './routes/leaderboard';
import authMiddleware from './middleware/auth';
import errorHandler from './middleware/errorHandler';

const app: Express = express();
const PORT = process.env.PORT || 5000;

// Phase 3.8: CORS origins from env var or defaults
const corsOrigins = process.env.CORS_ORIGIN
  ? process.env.CORS_ORIGIN.split(',').map((o) => o.trim())
  : ['http://localhost:3000', 'http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175', 'https://openclaw-poker.local'];

app.use(helmet());
app.use(cors({ origin: corsOrigins, credentials: true }));
app.use(express.json({ limit: '100kb' }));
app.use(cookieParser());

const limiter = rateLimit({ windowMs: 60 * 1000, max: 100, message: 'Too many requests, please try again later' });
app.use(limiter);

app.get('/health', (_req: Request, res: Response) => res.json({ status: 'ok', message: 'OpenClaw Poker API running' }));

app.use('/api/auth', authRoutes);
app.use('/api/tournaments', tournamentRoutes);
app.use('/api/matches', matchRoutes);
app.use('/api/leaderboard', leaderboardRoutes);
app.use(errorHandler);

async function startServer() {
  try {
    await AppDataSource.initialize();
    console.log('\u2713 TypeORM DataSource initialized successfully');
    app.listen(PORT, () => {
      console.log('\u2713 OpenClaw Poker API running on port ' + PORT);
      console.log('\u2713 Environment: ' + (process.env.NODE_ENV || 'development'));
      console.log('\u2713 Database connection established');
    });
  } catch (error) {
    console.error('\u2717 FATAL: Error during TypeORM DataSource initialization');
    console.error(error); process.exit(1);
  }
}

process.on('SIGTERM', async () => {
  try { await AppDataSource.destroy(); process.exit(0); }
  catch (error) { console.error('\u2717 Error during shutdown:', error); process.exit(1); }
});

process.on('SIGINT', async () => {
  try { await AppDataSource.destroy(); process.exit(0); }
  catch (error) { console.error('\u2717 Error during shutdown:', error); process.exit(1); }
});

startServer();
