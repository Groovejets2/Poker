/**
 * Leaderboard Routes
 */

const express = require('express');
const database = require('../database/db');

const router = express.Router();

// GET /leaderboard - Get global leaderboard
router.get('/', async (req, res, next) => {
  try {
    const limit = Math.min(parseInt(req.query.limit) || 50, 100);
    const offset = parseInt(req.query.offset) || 0;

    // Simplified leaderboard query
    const leaderboard = await database.all(`
      SELECT 
        u.id as user_id,
        u.username,
        COUNT(DISTINCT tp.tournament_id) as tournaments_played,
        SUM(CASE WHEN tp.finish_position = 1 THEN 1 ELSE 0 END) as tournament_wins,
        ROUND(AVG(CAST(tp.finish_position AS FLOAT)), 2) as avg_finish,
        COALESCE(SUM(tp.prize_usd), 0) as total_winnings
      FROM users u
      LEFT JOIN tournament_players tp ON u.id = tp.user_id
      GROUP BY u.id, u.username
      ORDER BY total_winnings DESC
      LIMIT ? OFFSET ?
    `, [limit, offset]);

    res.json({
      leaderboard: leaderboard.map((entry, idx) => ({
        rank: offset + idx + 1,
        ...entry
      })),
      updated_at: new Date().toISOString()
    });
  } catch (err) {
    next(err);
  }
});

// GET /leaderboard/:user_id - Get player stats
router.get('/:user_id', async (req, res, next) => {
  try {
    const stats = await database.get(`
      SELECT 
        u.id as user_id,
        u.username,
        COUNT(DISTINCT tp.tournament_id) as tournaments_played,
        SUM(CASE WHEN tp.finish_position = 1 THEN 1 ELSE 0 END) as tournament_wins,
        ROUND(AVG(CAST(tp.finish_position AS FLOAT)), 2) as avg_finish,
        COALESCE(SUM(tp.prize_usd), 0) as total_winnings
      FROM users u
      LEFT JOIN tournament_players tp ON u.id = tp.user_id
      WHERE u.id = ?
      GROUP BY u.id, u.username
    `, [req.params.user_id]);

    if (!stats) {
      return res.status(404).json({
        error: {
          code: 'NOT_FOUND',
          message: 'User not found'
        }
      });
    }

    res.json(stats);
  } catch (err) {
    next(err);
  }
});

module.exports = router;
