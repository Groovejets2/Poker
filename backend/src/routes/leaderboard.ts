import { Router, Request, Response, NextFunction } from 'express';
import { AppDataSource } from '../database/data-source';
import { User } from '../database/entities/User';
import { TournamentPlayer } from '../database/entities/TournamentPlayer';

const router = Router();

/**
 * GET /leaderboard
 * Get global leaderboard (top players by winnings)
 */
router.get('/', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const limit = Math.min(parseInt(req.query.limit as string) || 50, 100);
    const offset = parseInt(req.query.offset as string) || 0;

    const userRepository = AppDataSource.getRepository(User);

    const leaderboard = await userRepository
      .createQueryBuilder('u')
      .leftJoin('u.tournamentPlayers', 'tp')
      .select('u.id', 'user_id')
      .addSelect('u.username', 'username')
      .addSelect('COUNT(DISTINCT tp.tournament_id)', 'tournaments_played')
      .addSelect('SUM(CASE WHEN tp.finish_position = 1 THEN 1 ELSE 0 END)', 'tournament_wins')
      .addSelect('ROUND(AVG(CAST(tp.finish_position AS DECIMAL)), 2)', 'avg_finish')
      .addSelect('COALESCE(SUM(tp.prize_usd), 0)', 'total_winnings')
      .groupBy('u.id')
      .addGroupBy('u.username')
      .orderBy('total_winnings', 'DESC')
      .offset(offset)
      .limit(limit)
      .getRawMany();

    res.json({
      leaderboard: leaderboard.map((entry, idx) => ({
        rank: offset + idx + 1,
        user_id: parseInt(entry.user_id),
        username: entry.username,
        tournaments_played: parseInt(entry.tournaments_played) || 0,
        tournament_wins: parseInt(entry.tournament_wins) || 0,
        avg_finish: parseFloat(entry.avg_finish) || null,
        total_winnings: parseFloat(entry.total_winnings) || 0
      })),
      updated_at: new Date().toISOString()
    });
  } catch (err) {
    next(err);
  }
});

/**
 * GET /leaderboard/:user_id
 * Get player stats
 */
router.get('/:user_id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const userId = parseInt(req.params.user_id as string);

    const userRepository = AppDataSource.getRepository(User);

    const stats = await userRepository
      .createQueryBuilder('u')
      .leftJoin('u.tournamentPlayers', 'tp')
      .select('u.id', 'user_id')
      .addSelect('u.username', 'username')
      .addSelect('COUNT(DISTINCT tp.tournament_id)', 'tournaments_played')
      .addSelect('SUM(CASE WHEN tp.finish_position = 1 THEN 1 ELSE 0 END)', 'tournament_wins')
      .addSelect('ROUND(AVG(CAST(tp.finish_position AS DECIMAL)), 2)', 'avg_finish')
      .addSelect('COALESCE(SUM(tp.prize_usd), 0)', 'total_winnings')
      .where('u.id = :userId', { userId })
      .groupBy('u.id')
      .addGroupBy('u.username')
      .getRawOne();

    if (!stats) {
      return res.status(404).json({
        error: {
          code: 'NOT_FOUND',
          message: 'User not found'
        }
      });
    }

    res.json({
      user_id: parseInt(stats.user_id),
      username: stats.username,
      tournaments_played: parseInt(stats.tournaments_played) || 0,
      tournament_wins: parseInt(stats.tournament_wins) || 0,
      avg_finish: parseFloat(stats.avg_finish) || null,
      total_winnings: parseFloat(stats.total_winnings) || 0
    });
  } catch (err) {
    next(err);
  }
});

export default router;
