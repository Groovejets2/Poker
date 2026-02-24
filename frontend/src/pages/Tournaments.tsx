import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { tournamentsService, Tournament } from '../services/tournaments.service';
import { useAuth } from '../context/AuthContext';

export const Tournaments = () => {
  const [tournaments, setTournaments] = useState<Tournament[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { isAuthenticated, isAdmin } = useAuth();

  useEffect(() => {
    loadTournaments();
  }, []);

  const loadTournaments = async () => {
    try {
      setLoading(true);
      const data = await tournamentsService.getAll();
      setTournaments(data);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to load tournaments');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (tournamentId: number) => {
    try {
      await tournamentsService.register(tournamentId);
      // Reload tournaments to update registration status
      await loadTournaments();
    } catch (err: any) {
      alert(err.response?.data?.error?.message || 'Failed to register');
    }
  };

  const handleUnregister = async (tournamentId: number) => {
    try {
      await tournamentsService.unregister(tournamentId);
      // Reload tournaments to update registration status
      await loadTournaments();
    } catch (err: any) {
      alert(err.response?.data?.error?.message || 'Failed to unregister');
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="mt-4 text-gray-600">Loading tournaments...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Tournaments</h1>
        {isAdmin && (
          <Link
            to="/tournaments/create"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            Create Tournament
          </Link>
        )}
      </div>

      {tournaments.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow-sm border border-gray-200">
          <p className="text-gray-500 text-lg">No tournaments available at the moment.</p>
          {isAdmin && (
            <Link
              to="/tournaments/create"
              className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              Create the first tournament
            </Link>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tournaments.map((tournament) => (
            <div
              key={tournament.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
            >
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-semibold text-gray-900">{tournament.name}</h3>
                <span
                  className={`px-2 py-1 text-xs font-medium rounded-full ${
                    tournament.status === 'scheduled'
                      ? 'bg-green-100 text-green-800'
                      : tournament.status === 'in_progress'
                      ? 'bg-yellow-100 text-yellow-800'
                      : tournament.status === 'completed'
                      ? 'bg-gray-100 text-gray-800'
                      : 'bg-red-100 text-red-800'
                  }`}
                >
                  {tournament.status}
                </span>
              </div>

              <div className="space-y-2 mb-4">
                <p className="text-sm text-gray-600">
                  <span className="font-medium">Buy-in:</span> ${tournament.buy_in}
                </p>
                <p className="text-sm text-gray-600">
                  <span className="font-medium">Entry Fee:</span> ${tournament.entry_fee}
                </p>
                <p className="text-sm text-gray-600">
                  <span className="font-medium">Players:</span> {tournament.player_count || 0}/
                  {tournament.max_players}
                </p>
                <p className="text-sm text-gray-600">
                  <span className="font-medium">Scheduled:</span>{' '}
                  {new Date(tournament.scheduled_at).toLocaleString()}
                </p>
              </div>

              <div className="flex gap-2">
                <Link
                  to={`/tournaments/${tournament.id}`}
                  className="flex-1 text-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  View Details
                </Link>

                {isAuthenticated && tournament.status === 'scheduled' && (
                  <>
                    {tournament.is_registered ? (
                      <button
                        onClick={() => handleUnregister(tournament.id)}
                        className="flex-1 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
                      >
                        Unregister
                      </button>
                    ) : (
                      <button
                        onClick={() => handleRegister(tournament.id)}
                        disabled={
                          (tournament.player_count || 0) >= tournament.max_players
                        }
                        className="flex-1 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {(tournament.player_count || 0) >= tournament.max_players
                          ? 'Full'
                          : 'Register'}
                      </button>
                    )}
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
