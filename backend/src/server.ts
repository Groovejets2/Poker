import 'reflect-metadata';
import express, { Express, Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import dotenv from 'dotenv';
import { AppDataSource } from './database/data-source';
import authRoutes from './routes/auth';
import tournamentRoutes from './routes/tournaments';
import matchRoutes from './routes/matches';
import leaderboardRoutes from './routes/leaderboard';
import authMiddleware from './middleware/auth';
import errorHandler from './middleware/errorHandler';

dotenv.config();

const app: Express = express();
const PORT = process.env.PORT || 5000;

// Initialize TypeORM DataSource
AppDataSource.initialize()
  .then(() => {
    console.log('TypeORM DataSource initialized successfully');
  })
  .catch((error) => {
    console.error('Error during TypeORM DataSource initialization:', error);
    process.exit(1);
  });

// Middleware
app.use(helmet());
app.use(cors({
  origin: [
    'http://localhost:3000',
    'https://openclaw-poker.local'
  ]
}));
app.use(express.json());

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

// Start server
app.listen(PORT, () => {
  console.log(`OpenClaw Poker API running on port ${PORT}`);
});
