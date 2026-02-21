/**
 * Tournament Routes
 * Stub implementation - detailed routes follow
 */

const express = require('express');
const database = require('../database/db');
const authMiddleware = require('../middleware/auth');

const router = express.Router();

// GET /tournaments - List all tournaments
router.get('/', async (req, res, next) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = Math.min(parseInt(req.query.limit) || 20, 100);
    const offset = (page - 1) * limit;

    let query = 'SELECT * FROM tournaments';
    let countQuery = 'SELECT COUNT(*) as count FROM tournaments';
    let params = [];

    if (req.query.status) {
      query += ' WHERE status = ?';
      countQuery += ' WHERE status = ?';
      params.push(req.query.status);
    }

    query += ' ORDER BY scheduled_at DESC LIMIT ? OFFSET ?';
    params.push(limit, offset);

    const tournaments = await database.all(query, params);
    const countResult = await database.get(countQuery, params.slice(0, -2));

    res.json({
      tournaments,
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

// GET /tournaments/:id - Get tournament details
router.get('/:id', async (req, res, next) => {
  try {
    const tournament = await database.get(
      'SELECT * FROM tournaments WHERE id = ?',
      [req.params.id]
    );

    if (!tournament) {
      return res.status(404).json({
        error: {
          code: 'NOT_FOUND',
          message: 'Tournament not found'
        }
      });
    }

    res.json(tournament);
  } catch (err) {
    next(err);
  }
});

// POST /tournaments - Create tournament (stub)
router.post('/', authMiddleware, async (req, res, next) => {
  res.status(501).json({
    error: {
      code: 'NOT_IMPLEMENTED',
      message: 'Tournament creation not yet implemented'
    }
  });
});

module.exports = router;
