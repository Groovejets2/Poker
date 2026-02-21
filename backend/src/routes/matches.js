/**
 * Match Routes
 */

const express = require('express');
const database = require('../database/db');

const router = express.Router();

// GET /matches/:id - Get match details
router.get('/:id', async (req, res, next) => {
  try {
    const match = await database.get(
      'SELECT * FROM matches WHERE id = ?',
      [req.params.id]
    );

    if (!match) {
      return res.status(404).json({
        error: {
          code: 'NOT_FOUND',
          message: 'Match not found'
        }
      });
    }

    const players = await database.all(
      'SELECT * FROM match_players WHERE match_id = ?',
      [req.params.id]
    );

    res.json({ ...match, players });
  } catch (err) {
    next(err);
  }
});

module.exports = router;
