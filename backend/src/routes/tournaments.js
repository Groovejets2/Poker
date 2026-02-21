/**
 * Tournament Routes
 */

const express = require('express');
const database = require('../database/db');
const authMiddleware = require('../middleware/auth');
const validators = require('../utils/validation');

const router = express.Router();

// GET /tournaments - List tournaments
router.get('/', async (req, res, next) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = Math.min(parseInt(req.query.limit) || 20, 100);
    const offset = (page - 1) * limit;

    let query = 'SELECT t.*, COUNT(tp.id) as player_count FROM tournaments t LEFT JOIN tournament_players tp ON t.id = tp.tournament_id WHERE 1=1';
    let countQuery = 'SELECT COUNT(*) as count FROM tournaments WHERE 1=1';
    let params = [];

    if (req.query.status) {
      query += ' AND t.status = ?';
      countQuery += ' AND status = ?';
      params.push(req.query.status);
    }

    query += ' GROUP BY t.id ORDER BY scheduled_at DESC LIMIT ? OFFSET ?';
    params.push(limit, offset);

    const tournaments = await database.all(query, params);
    const countResult = await database.get(countQuery, params.slice(0, -2));

    res.json({
      tournaments: tournaments.map(t => ({
        ...t,
        seats_available: t.max_players - t.player_count
      })),
      pagination: {
        total: countResult.count,
        page,
        limit,
        pages: Math.ceil(countResult.count / limit)
      }
    });
  } catch (err) {
    next(err);
  }
});

// GET /tournaments/:id
router.get('/:id', async (req, res, next) => {
  try {
    const tournament = await database.get(
      'SELECT * FROM tournaments WHERE id = ?',
      [req.params.id]
    );

    if (!tournament) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Tournament not found' }
      });
    }

    const players = await database.all(
      'SELECT tp.*, u.username FROM tournament_players tp JOIN users u ON tp.user_id = u.id WHERE tp.tournament_id = ?',
      [req.params.id]
    );

    res.json({ ...tournament, players });
  } catch (err) {
    next(err);
  }
});

// POST /tournaments/:id/register
router.post('/:id/register', authMiddleware, async (req, res, next) => {
  try {
    const tournamentId = req.params.id;
    const userId = req.user.user_id;

    const tournament = await database.get(
      'SELECT * FROM tournaments WHERE id = ?',
      [tournamentId]
    );

    if (!tournament) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Tournament not found' }
      });
    }

    const existing = await database.get(
      'SELECT id FROM tournament_players WHERE tournament_id = ? AND user_id = ?',
      [tournamentId, userId]
    );

    if (existing) {
      return res.status(409).json({
        error: { code: 'CONFLICT', message: 'Already registered' }
      });
    }

    const playerCount = await database.get(
      'SELECT COUNT(*) as count FROM tournament_players WHERE tournament_id = ?',
      [tournamentId]
    );

    if (playerCount.count >= tournament.max_players) {
      return res.status(400).json({
        error: { code: 'INVALID_REQUEST', message: 'Tournament full' }
      });
    }

    await database.run(
      'INSERT INTO tournament_players (tournament_id, user_id, starting_stack) VALUES (?, ?, ?)',
      [tournamentId, userId, tournament.buy_in_chips]
    );

    res.json({
      success: true,
      message: 'Registered for tournament',
      tournament_id: tournamentId,
      user_id: userId,
      player_count: playerCount.count + 1,
      seats_available: tournament.max_players - playerCount.count - 1
    });
  } catch (err) {
    next(err);
  }
});

// DELETE /tournaments/:id/unregister
router.delete('/:id/unregister', authMiddleware, async (req, res, next) => {
  try {
    const tournamentId = req.params.id;
    const userId = req.user.user_id;

    const result = await database.run(
      'DELETE FROM tournament_players WHERE tournament_id = ? AND user_id = ?',
      [tournamentId, userId]
    );

    if (result.changes === 0) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Registration not found' }
      });
    }

    res.json({
      success: true,
      message: 'Unregistered from tournament',
      tournament_id: tournamentId,
      user_id: userId
    });
  } catch (err) {
    next(err);
  }
});

module.exports = router;
