/**
 * SQLite Database Setup
 * Initialize schema and connection pool
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const DB_PATH = process.env.DB_PATH || path.join(__dirname, '../../poker.db');

let db = null;

const database = {
  /**
   * Initialize database connection and create schema
   */
  initialize: () => {
    db = new sqlite3.Database(DB_PATH, (err) => {
      if (err) {
        console.error('Database connection error:', err);
        process.exit(1);
      }
      console.log('Connected to SQLite database at', DB_PATH);
    });

    db.serialize(() => {
      // Users table
      db.run(`
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT UNIQUE NOT NULL,
          email TEXT UNIQUE,
          password_hash TEXT NOT NULL,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          CHECK(LENGTH(username) >= 3)
        )
      `);

      // Tournaments table
      db.run(`
        CREATE TABLE IF NOT EXISTS tournaments (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          description TEXT,
          status TEXT DEFAULT 'draft' CHECK(status IN ('draft', 'scheduled', 'in_progress', 'completed', 'cancelled')),
          buy_in_chips INTEGER NOT NULL,
          entry_fee_usd REAL NOT NULL DEFAULT 0,
          max_players INTEGER NOT NULL DEFAULT 8,
          scheduled_at DATETIME NOT NULL,
          created_by INTEGER NOT NULL,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY(created_by) REFERENCES users(id)
        )
      `);

      // Tournament players table
      db.run(`
        CREATE TABLE IF NOT EXISTS tournament_players (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          tournament_id INTEGER NOT NULL,
          user_id INTEGER NOT NULL,
          status TEXT DEFAULT 'registered' CHECK(status IN ('registered', 'active', 'eliminated', 'withdrew')),
          starting_stack INTEGER NOT NULL DEFAULT 10000,
          current_stack INTEGER,
          finish_position INTEGER,
          prize_usd REAL,
          joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          UNIQUE(tournament_id, user_id),
          FOREIGN KEY(tournament_id) REFERENCES tournaments(id) ON DELETE CASCADE,
          FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
      `);

      // Matches table
      db.run(`
        CREATE TABLE IF NOT EXISTS matches (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          tournament_id INTEGER NOT NULL,
          table_number INTEGER NOT NULL,
          game_number INTEGER NOT NULL,
          status TEXT DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'in_progress', 'completed', 'cancelled')),
          winner_id INTEGER,
          pot_total INTEGER,
          hand_count INTEGER DEFAULT 0,
          scheduled_at DATETIME,
          started_at DATETIME,
          completed_at DATETIME,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          UNIQUE(tournament_id, table_number, game_number),
          FOREIGN KEY(tournament_id) REFERENCES tournaments(id) ON DELETE CASCADE,
          FOREIGN KEY(winner_id) REFERENCES users(id)
        )
      `);

      // Match players table
      db.run(`
        CREATE TABLE IF NOT EXISTS match_players (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          match_id INTEGER NOT NULL,
          user_id INTEGER NOT NULL,
          position INTEGER NOT NULL,
          starting_stack INTEGER NOT NULL,
          ending_stack INTEGER,
          status TEXT DEFAULT 'active' CHECK(status IN ('active', 'folded', 'eliminated', 'won')),
          UNIQUE(match_id, user_id),
          FOREIGN KEY(match_id) REFERENCES matches(id) ON DELETE CASCADE,
          FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
      `);

      // Create indexes for performance
      db.run('CREATE INDEX IF NOT EXISTS idx_tournaments_status ON tournaments(status)');
      db.run('CREATE INDEX IF NOT EXISTS idx_tournaments_scheduled ON tournaments(scheduled_at)');
      db.run('CREATE INDEX IF NOT EXISTS idx_tournament_players_tournament ON tournament_players(tournament_id)');
      db.run('CREATE INDEX IF NOT EXISTS idx_matches_tournament ON matches(tournament_id)');
      db.run('CREATE INDEX IF NOT EXISTS idx_matches_status ON matches(status)');
      db.run('CREATE INDEX IF NOT EXISTS idx_match_players_match ON match_players(match_id)');

      console.log('Database schema initialized');
    });
  },

  /**
   * Get database connection
   */
  getDb: () => db,

  /**
   * Run query (for non-SELECT operations)
   */
  run: (sql, params = []) => {
    return new Promise((resolve, reject) => {
      db.run(sql, params, function(err) {
        if (err) reject(err);
        else resolve({ id: this.lastID, changes: this.changes });
      });
    });
  },

  /**
   * Get single row
   */
  get: (sql, params = []) => {
    return new Promise((resolve, reject) => {
      db.get(sql, params, (err, row) => {
        if (err) reject(err);
        else resolve(row);
      });
    });
  },

  /**
   * Get all rows
   */
  all: (sql, params = []) => {
    return new Promise((resolve, reject) => {
      db.all(sql, params, (err, rows) => {
        if (err) reject(err);
        else resolve(rows || []);
      });
    });
  },

  /**
   * Close database connection
   */
  close: () => {
    return new Promise((resolve, reject) => {
      if (db) {
        db.close((err) => {
          if (err) reject(err);
          else resolve();
        });
      } else {
        resolve();
      }
    });
  }
};

module.exports = database;
