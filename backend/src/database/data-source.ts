import 'reflect-metadata';
import { DataSource } from 'typeorm';
import path from 'path';
import { User } from './entities/User';
import { Tournament } from './entities/Tournament';
import { TournamentPlayer } from './entities/TournamentPlayer';
import { Match } from './entities/Match';
import { MatchPlayer } from './entities/MatchPlayer';

const env = process.env.NODE_ENV || 'test';

let dataSourceConfig: any;

if (env === 'production') {
  // PostgreSQL for production
  // CRIT-5 FIX: Add SSL configuration for secure database connections
  dataSourceConfig = {
    type: 'postgres',
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT || '5432'),
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    entities: [User, Tournament, TournamentPlayer, Match, MatchPlayer],
    synchronize: false,
    logging: false,
    migrations: [path.join(__dirname, 'migrations/*.ts'), path.join(__dirname, 'migrations/*.js')],
    migrationsRun: true, // Automatically run migrations on startup
    // SSL configuration for production
    ssl: {
      rejectUnauthorized: true,
      ca: process.env.DB_SSL_CA || undefined,
    },
    // Connection pool settings
    extra: {
      max: 20, // Maximum number of connections in pool
      idleTimeoutMillis: 30000, // Close idle connections after 30s
      connectionTimeoutMillis: 2000, // Timeout for establishing connection
    },
  };
} else {
  // SQLite for test/development
  // CRIT-4 FIX: Disable synchronize to prevent data loss
  dataSourceConfig = {
    type: 'sqlite',
    database: process.env.DB_PATH || path.join(__dirname, '../../data/test/poker.db'),
    entities: [User, Tournament, TournamentPlayer, Match, MatchPlayer],
    synchronize: false, // Use migrations instead of auto-sync
    logging: false,
    migrations: [path.join(__dirname, 'migrations/*.ts'), path.join(__dirname, 'migrations/*.js')],
    migrationsRun: true, // Automatically run migrations on startup
  };
}

export const AppDataSource = new DataSource(dataSourceConfig);
