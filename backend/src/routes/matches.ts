import { Router, Request, Response, NextFunction } from 'express';
import { AppDataSource } from '../database/data-source';
import { Match } from '../database/entities/Match';
import { MatchPlayer } from '../database/entities/MatchPlayer';
import { User } from '../database/entities/User';
import authMiddleware from '../middleware/auth';

const router = Router();

/**
 * GET /matches/tournament/:tournament_id
 * List all matches for a tournament
 */
router.get('/tournament/:tournament_id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const tournamentId = parseInt(req.params.tournament_id);

    const matchRepository = AppDataSource.getRepository(Match);

    const matches = await matchRepository
      .createQueryBuilder('m')
      .leftJoinAndSelect('m.winner', 'u')
      .where('m.tournament.id = :tournamentId', { tournamentId })
      .orderBy('m.table_number', 'ASC')
      .addOrderBy('m.game_number', 'ASC')
      .getMany();

    const matchesWithWinner = matches.map(match => ({
      ...match,
      winner: match.winner ? match.winner.username : null
    }));

    res.json({
      tournament_id: tournamentId,
      matches: matchesWithWinner
    });
  } catch (err) {
    next(err);
  }
});

/**
 * GET /matches/:id
 * Get match details with players
 */
router.get('/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const matchId = parseInt(req.params.id);

    const matchRepository = AppDataSource.getRepository(Match);
    const matchPlayerRepository = AppDataSource.getRepository(MatchPlayer);

    const match = await matchRepository.findOne({
      where: { id: matchId },
      relations: ['winner']
    });

    if (!match) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Match not found' }
      });
    }

    const players = await matchPlayerRepository.find({
      where: { match: { id: matchId } },
      relations: ['user']
    });

    const playersWithUsername = players.map(mp => ({
      ...mp,
      username: mp.user.username
    }));

    res.json({
      ...match,
      winner: match.winner ? match.winner.username : null,
      players: playersWithUsername
    });
  } catch (err) {
    next(err);
  }
});

/**
 * POST /matches/:id/submit-score
 * Submit match results (authenticated)
 */
router.post('/:id/submit-score', authMiddleware, async (req: Request, res: Response, next: NextFunction) => {
  try {
    const matchId = parseInt(req.params.id);
    const { winner_id, results } = req.body;

    if (!winner_id || !results) {
      return res.status(400).json({
        error: { code: 'INVALID_REQUEST', message: 'Missing winner_id or results' }
      });
    }

    const matchRepository = AppDataSource.getRepository(Match);
    const matchPlayerRepository = AppDataSource.getRepository(MatchPlayer);

    // Get the match
    const match = await matchRepository.findOne({
      where: { id: matchId }
    });

    if (!match) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Match not found' }
      });
    }

    // Update match status and winner
    match.status = 'completed';
    match.winner = { id: winner_id } as User;
    match.completed_at = new Date();

    await matchRepository.save(match);

    // Update player stacks and positions
    for (const result of results) {
      const matchPlayer = await matchPlayerRepository.findOne({
        where: {
          match: { id: matchId },
          user: { id: result.user_id }
        }
      });

      if (matchPlayer) {
        matchPlayer.ending_stack = result.ending_stack;
        matchPlayer.status = result.status;
        await matchPlayerRepository.save(matchPlayer);
      }
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

export default router;
