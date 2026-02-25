import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { leaderboardService } from '../services/leaderboard.service';
import type { LeaderboardPlayer } from '../services/leaderboard.service';

export const Leaderboard = () => {
  const [players, setPlayers] = useState<LeaderboardPlayer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadLeaderboard();
  }, []);

  const loadLeaderboard = async () => {
    try {
      setLoading(true);
      const data = await leaderboardService.getLeaderboard();
      setPlayers(data);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  const getRankDisplay = (index: number) => {
    if (index === 0) return <span className="text-xl font-bold text-gold-light">1ST</span>;
    if (index === 1) return <span className="text-lg font-bold" style={{ color: '#C0C0C0' }}>2ND</span>;
    if (index === 2) return <span className="text-lg font-bold" style={{ color: '#CD7F32' }}>3RD</span>;
    return <span className="text-lg font-semibold" style={{ color: 'var(--color-text-secondary)' }}>#{index + 1}</span>;
  };

  if (loading) {
    return (
      <div className="text-center py-16">
        <div
          className="inline-block animate-spin rounded-full h-14 w-14 border-4 border-t-transparent"
          style={{ borderColor: 'var(--color-accent-gold)' }}
        ></div>
        <p className="mt-6 text-lg" style={{ color: 'var(--color-text-secondary)' }}>
          Loading leaderboard...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div
        className="px-6 py-4 rounded-lg"
        style={{
          backgroundColor: 'var(--color-error-bg)',
          borderLeft: '4px solid var(--color-error)',
          color: 'var(--color-error)'
        }}
      >
        {error}
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-4xl font-bold mb-10" style={{ color: 'var(--color-text-primary)' }}>
        Global Leaderboard
      </h1>

      {players.length === 0 ? (
        <div className="text-center py-20 card">
          <p className="text-lg" style={{ color: 'var(--color-text-secondary)' }}>
            No players on the leaderboard yet.
          </p>
        </div>
      ) : (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr>
                  <th className="px-6 py-4 text-left">Rank</th>
                  <th className="px-6 py-4 text-left">Player</th>
                  <th className="px-6 py-4 text-right">Tournaments</th>
                  <th className="px-6 py-4 text-right">Wins</th>
                  <th className="px-6 py-4 text-right">Total Winnings</th>
                  <th className="px-6 py-4 text-right">Avg. Finish</th>
                  <th className="px-6 py-4 text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                {players.map((player, index) => (
                  <tr
                    key={player.user_id}
                    className={index < 3 ? 'shadow-gold' : ''}
                    style={index < 3 ? { backgroundColor: 'rgba(212, 175, 55, 0.03)' } : {}}
                  >
                    <td className="px-6 py-4">
                      {getRankDisplay(index)}
                    </td>
                    <td className="px-6 py-4">
                      <div className="font-semibold" style={{ color: 'var(--color-text-primary)' }}>
                        {player.username}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span style={{ color: 'var(--color-text-secondary)' }}>
                        {player.tournaments_played}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span className="font-semibold" style={{ color: 'var(--color-text-primary)' }}>
                        {player.tournaments_won}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span className="font-bold text-gold text-lg">
                        ${player.total_winnings.toLocaleString()}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span style={{ color: 'var(--color-text-secondary)' }}>
                        {player.avg_finish_position?.toFixed(1) || 'N/A'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <Link
                        to={`/stats/${player.user_id}`}
                        className="inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all btn-secondary"
                      >
                        View Stats
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
