import { Router, Request, Response, NextFunction } from 'express';
import { AppDataSource } from '../database/data-source';
import { Tournament } from '../database/entities/Tournament';
import { TournamentPlayer } from '../database/entities/TournamentPlayer';
import { User } from '../database/entities/User';
import authMiddleware from '../middleware/auth';

const router = Router();

// GET /tournaments - List tournaments
router.get('/', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const page = parseInt(req.query.page as string) || 1;
    const limit = Math.min(parseInt(req.query.limit as string) || 20, 100);
    const offset = (page - 1) * limit;

    const tournamentRepository = AppDataSource.getRepository(Tournament);
    const tournamentPlayerRepository = AppDataSource.getRepository(TournamentPlayer);

    let query = tournamentRepository.createQueryBuilder('t');

    if (req.query.status) {
      query = query.where('t.status = :status', { status: req.query.status });
    }

    const [tournaments, total] = await query
      .orderBy('t.scheduled_at', 'DESC')
      .skip(offset)
      .take(limit)
      .getManyAndCount();

    const tournamentsWithCounts = await Promise.all(
      tournaments.map(async (t) => {
        const playerCount = await tournamentPlayerRepository.count({
          where: { tournament: { id: t.id } }
        });
        return {
          ...t,
          player_count: playerCount,
          seats_available: t.max_players - playerCount
        };
      })
    );

    res.json({
      tournaments: tournamentsWithCounts,
      pagination: {
        total,
        page,
        limit,
        pages: Math.ceil(total / limit)
      }
    });
  } catch (err) {
    next(err);
  }
});

// GET /tournaments/:id
router.get('/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const tournamentRepository = AppDataSource.getRepository(Tournament);
    const tournamentPlayerRepository = AppDataSource.getRepository(TournamentPlayer);

    const tournament = await tournamentRepository.findOne({
      where: { id: parseInt(req.params.id as string) },
      relations: ['created_by']
    });

    if (!tournament) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Tournament not found' }
      });
    }

    const players = await tournamentPlayerRepository.find({
      where: { tournament: { id: tournament.id } },
      relations: ['user']
    });

    res.json({
      ...tournament,
      players: players.map(tp => ({
        ...tp,
        username: tp.user.username
      }))
    });
  } catch (err) {
    next(err);
  }
});

// POST /tournaments/:id/register
router.post('/:id/register', authMiddleware, async (req: Request, res: Response, next: NextFunction) => {
  try {
    const tournamentId = parseInt(req.params.id as string);
    const userId = (req as any).user.user_id;

    const tournamentRepository = AppDataSource.getRepository(Tournament);
    const tournamentPlayerRepository = AppDataSource.getRepository(TournamentPlayer);

    const tournament = await tournamentRepository.findOne({
      where: { id: tournamentId }
    });

    if (!tournament) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Tournament not found' }
      });
    }

    const existing = await tournamentPlayerRepository.findOne({
      where: {
        tournament: { id: tournamentId },
        user: { id: userId }
      }
    });

    if (existing) {
      return res.status(409).json({
        error: { code: 'CONFLICT', message: 'Already registered' }
      });
    }

    const playerCount = await tournamentPlayerRepository.count({
      where: { tournament: { id: tournamentId } }
    });

    if (playerCount >= tournament.max_players) {
      return res.status(400).json({
        error: { code: 'INVALID_REQUEST', message: 'Tournament full' }
      });
    }

    const newPlayer = tournamentPlayerRepository.create({
      tournament: { id: tournamentId } as Tournament,
      user: { id: userId } as User,
      starting_stack: tournament.buy_in_chips
    });

    await tournamentPlayerRepository.save(newPlayer);

    res.json({
      success: true,
      message: 'Registered for tournament',
      tournament_id: tournamentId,
      user_id: userId,
      player_count: playerCount + 1,
      seats_available: tournament.max_players - playerCount - 1
    });
  } catch (err) {
    next(err);
  }
});

// DELETE /tournaments/:id/unregister
router.delete('/:id/unregister', authMiddleware, async (req: Request, res: Response, next: NextFunction) => {
  try {
    const tournamentId = parseInt(req.params.id as string);
    const userId = (req as any).user.user_id;

    const tournamentPlayerRepository = AppDataSource.getRepository(TournamentPlayer);

    const result = await tournamentPlayerRepository.delete({
      tournament: { id: tournamentId },
      user: { id: userId }
    });

    if (result.affected === 0) {
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

export default router;
