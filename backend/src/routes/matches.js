/**
 * Match Routes
 */

const express = require('express');
const database = require('../database/db');
const authMiddleware = require('../middleware/auth');

const router = express.Router();

// GET /tournaments/:tournament_id/matches
router.get('/tournament/:tournament_id', async (req, res, next) => {
  try {
    const matches = await database.all(
      'SELECT m.*, u.username as winner FROM matches m LEFT JOIN users u ON m.winner_id = u.id WHERE m.tournament_id = ? ORDER BY table_number, game_number',
      [req.params.tournament_id]
    );

    res.json({
      tournament_id: req.params.tournament_id,
      matches
    });
  } catch (err) {
    next(err);
  }
});

// GET /matches/:id
router.get('/:id', async (req, res, next) => {
  try {
    const match = await database.get(
      'SELECT m.*, u.username as winner FROM matches m LEFT JOIN users u ON m.winner_id = u.id WHERE m.id = ?',
      [req.params.id]
    );

    if (!match) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Match not found' }
      });
    }

    const players = await database.all(
      'SELECT mp.*, u.username FROM match_players mp JOIN users u ON mp.user_id = u.id WHERE mp.match_id = ?',
      [req.params.id]
    );

    res.json({ ...match, players });
  } catch (err) {
    next(err);
  }
});

// POST /matches/:id/submit-score (submit match results)
router.post('/:id/submit-score', authMiddleware, async (req, res, next) => {
  try {
    const matchId = req.params.id;
    const { winner_id, results } = req.body;

    if (!winner_id || !results) {
      return res.status(400).json({
        error: { code: 'INVALID_REQUEST', message: 'Missing winner_id or results' }
      });
    }

    // Update match
    await database.run(
      'UPDATE matches SET status = ?, winner_id = ?, completed_at = CURRENT_TIMESTAMP WHERE id = ?',
      ['completed', winner_id, matchId]
    );

    // Update player stacks and positions
    for (const result of results) {
      await database.run(
        'UPDATE match_players SET ending_stack = ?, status = ? WHERE match_id = ? AND user_id = ?',
        [result.ending_stack, result.status, matchId, result.user_id]
      );
    }

    res.json({
      success: true,
      message: 'Match score submitted',
      match_id: matchId
    });
  } catch (err) {
    next(err);
  }
});

module.exports = router;
