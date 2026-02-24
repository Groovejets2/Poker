import 'reflect-metadata';
import dotenv from 'dotenv';

// CRITICAL: Load environment variables BEFORE any other imports
// This ensures JWT_SECRET is available when auth modules are loaded
dotenv.config();

import express, { Express, Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
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

// Middleware
app.use(helmet());
app.use(cors({
  origin: [
    'http://localhost:3000',
    'https://openclaw-poker.local'
  ]
}));
app.use(express.json({ limit: '100kb' })); // MED-4 FIX: Add request body size limit

// Rate limiting
const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 100, // 100 requests per minute
  message: 'Too many requests, please try again later'
});
app.use(limiter);

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', message: 'OpenClaw Poker API running' });
});

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/tournaments', tournamentRoutes);
app.use('/api/matches', matchRoutes);
app.use('/api/leaderboard', leaderboardRoutes);

// Error handling middleware
app.use(errorHandler);

// CRIT-3 FIX: Wait for database initialization before starting server
async function startServer() {
  try {
    // Wait for database to be ready FIRST
    await AppDataSource.initialize();
    console.log('✓ TypeORM DataSource initialized successfully');

    // THEN start server
    app.listen(PORT, () => {
      console.log(`✓ OpenClaw Poker API running on port ${PORT}`);
      console.log(`✓ Environment: ${process.env.NODE_ENV || 'development'}`);
      console.log('✓ Database connection established');
    });
  } catch (error) {
    console.error('✗ FATAL: Error during TypeORM DataSource initialization');
    console.error(error);
    process.exit(1);
  }
}

// CRIT-3 FIX: Graceful shutdown handlers (MED-3)
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully...');
  try {
    await AppDataSource.destroy();
    console.log('✓ Database connections closed');
    process.exit(0);
  } catch (error) {
    console.error('✗ Error during shutdown:', error);
    process.exit(1);
  }
});

process.on('SIGINT', async () => {
  console.log('\nSIGINT received, shutting down gracefully...');
  try {
    await AppDataSource.destroy();
    console.log('✓ Database connections closed');
    process.exit(0);
  } catch (error) {
    console.error('✗ Error during shutdown:', error);
    process.exit(1);
  }
});

// Start the server
startServer();
