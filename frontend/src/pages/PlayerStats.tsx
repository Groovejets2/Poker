import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { leaderboardService } from '../services/leaderboard.service';
import type { PlayerStats as PlayerStatsType } from '../services/leaderboard.service';
import { useAuth } from '../context/AuthContext';

export const PlayerStats = () => {
  const { userId } = useParams<{ userId: string }>();
  const { user } = useAuth();
  const [stats, setStats] = useState<PlayerStatsType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // If no userId in params, use logged in user's ID
  const targetUserId = userId ? parseInt(userId) : user?.user_id;

  useEffect(() => {
    if (targetUserId) {
      loadPlayerStats(targetUserId);
    } else {
      setError('Please log in to view stats');
      setLoading(false);
    }
  }, [targetUserId]);

  const loadPlayerStats = async (playerId: number) => {
    try {
      setLoading(true);
      const data = await leaderboardService.getPlayerStats(playerId);
      setStats(data);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to load player stats');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="mt-4 text-gray-600">Loading player stats...</p>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
        {error || 'Player not found'}
      </div>
    );
  }

  return (
    <div>
      <button
        onClick={() => navigate('/leaderboard')}
        className="mb-6 inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
      >
        ← Back to Leaderboard
      </button>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">{stats.username}'s Stats</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-blue-50 p-6 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Tournaments Played</h3>
            <p className="text-3xl font-bold text-blue-600">{stats.tournaments_played}</p>
          </div>

          <div className="bg-green-50 p-6 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Tournaments Won</h3>
            <p className="text-3xl font-bold text-green-600">{stats.tournament_wins}</p>
          </div>

          <div className="bg-yellow-50 p-6 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Total Winnings</h3>
            <p className="text-3xl font-bold text-yellow-600">
              ${stats.total_winnings.toFixed(2)}
            </p>
          </div>

          <div className="bg-purple-50 p-6 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Avg. Finish Position</h3>
            <p className="text-3xl font-bold text-purple-600">
              {stats.avg_finish?.toFixed(1) || 'N/A'}
            </p>
          </div>
        </div>

        {stats.tournaments_played > 0 && (
          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Win Rate</p>
              <p className="text-2xl font-bold text-gray-900">
                {((stats.tournament_wins / stats.tournaments_played) * 100).toFixed(1)}%
              </p>
            </div>

            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Avg. Winnings per Tournament</p>
              <p className="text-2xl font-bold text-gray-900">
                ${(stats.total_winnings / stats.tournaments_played).toFixed(2)}
              </p>
            </div>

            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Total Tournaments</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats.tournaments_played}
              </p>
            </div>
          </div>
        )}
      </div>

      {stats.recent_tournaments && stats.recent_tournaments.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Recent Tournaments</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Tournament
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Finish Position
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Payout
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {stats.recent_tournaments.map((tournament) => (
                  <tr key={tournament.tournament_id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {tournament.tournament_name}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {tournament.finish_position === 1 && '🥇 '}
                        {tournament.finish_position === 2 && '🥈 '}
                        {tournament.finish_position === 3 && '🥉 '}
                        #{tournament.finish_position}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-green-600">
                        ${tournament.payout.toFixed(2)}
                      </div>
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
