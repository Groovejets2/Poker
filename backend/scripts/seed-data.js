/**
 * Seed Data Script - Populate test database
 * Run: node scripts/seed-data.js
 */

const bcrypt = require('bcryptjs');
const database = require('../src/database/db');

async function seedData() {
  try {
    console.log('Seeding test data...');

    // Create test users
    const users = [
      { username: 'player1', email: 'player1@test.local', password: 'password123' },
      { username: 'player2', email: 'player2@test.local', password: 'password123' },
      { username: 'player3', email: 'player3@test.local', password: 'password123' },
      { username: 'player4', email: 'player4@test.local', password: 'password123' },
      { username: 'player5', email: 'player5@test.local', password: 'password123' }
    ];

    const userIds = [];
    for (const user of users) {
      const hash = await bcrypt.hash(user.password, 12);
      const result = await database.run(
        'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
        [user.username, user.email, hash]
      );
      userIds.push(result.id);
      console.log(`Created user: ${user.username} (ID: ${result.id})`);
    }

    // Create test tournaments
    const now = new Date();
    const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);

    const tournaments = [
      {
        name: 'Saturday Afternoon',
        buy_in_chips: 10000,
        entry_fee_usd: 5.00,
        max_players: 4,
        scheduled_at: tomorrow.toISOString(),
        created_by: userIds[0]
      },
      {
        name: 'High Stakes Championship',
        buy_in_chips: 50000,
        entry_fee_usd: 25.00,
        max_players: 8,
        scheduled_at: new Date(tomorrow.getTime() + 24 * 60 * 60 * 1000).toISOString(),
        created_by: userIds[0]
      }
    ];

    const tournamentIds = [];
    for (const t of tournaments) {
      const result = await database.run(
        'INSERT INTO tournaments (name, buy_in_chips, entry_fee_usd, max_players, scheduled_at, created_by, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
        [t.name, t.buy_in_chips, t.entry_fee_usd, t.max_players, t.scheduled_at, t.created_by, 'scheduled']
      );
      tournamentIds.push(result.id);
      console.log(`Created tournament: ${t.name} (ID: ${result.id})`);
    }

    // Register players to tournaments
    for (let i = 0; i < tournamentIds.length; i++) {
      const numPlayers = (i === 0) ? 3 : 5;
      for (let j = 0; j < numPlayers; j++) {
        await database.run(
          'INSERT INTO tournament_players (tournament_id, user_id, starting_stack, status) VALUES (?, ?, ?, ?)',
          [tournamentIds[i], userIds[j], tournaments[i].buy_in_chips, 'registered']
        );
      }
      console.log(`Registered ${numPlayers} players to tournament ${tournamentIds[i]}`);
    }

    console.log('\n✓ Test data seeded successfully');
    console.log('\nTest Users:');
    users.forEach((u, idx) => {
      console.log(`  ${u.username} / password123`);
    });

    process.exit(0);
  } catch (err) {
    console.error('Seed error:', err);
    process.exit(1);
  }
}

database.initialize();
setTimeout(seedData, 500);
