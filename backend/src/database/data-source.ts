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
    migrations: ['src/database/migrations/*.ts'],
  };
} else {
  // SQLite for test/development
  dataSourceConfig = {
    type: 'sqlite',
    database: process.env.DB_PATH || path.join(__dirname, '../../data/test/poker.db'),
    entities: [User, Tournament, TournamentPlayer, Match, MatchPlayer],
    synchronize: true,
    logging: false,
    migrations: ['src/database/migrations/*.ts'],
  };
}

export const AppDataSource = new DataSource(dataSourceConfig);
