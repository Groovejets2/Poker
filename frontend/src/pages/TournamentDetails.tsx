import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { tournamentsService, Tournament } from '../services/tournaments.service';
import { useAuth } from '../context/AuthContext';

export const TournamentDetails = () => {
  const { id } = useParams<{ id: string }>();
  const [tournament, setTournament] = useState<Tournament | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      loadTournament(parseInt(id));
    }
  }, [id]);

  const loadTournament = async (tournamentId: number) => {
    try {
      setLoading(true);
      const data = await tournamentsService.getById(tournamentId);
      setTournament(data);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to load tournament');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    if (!id) return;
    try {
      await tournamentsService.register(parseInt(id));
      await loadTournament(parseInt(id));
    } catch (err: any) {
      alert(err.response?.data?.error?.message || 'Failed to register');
    }
  };

  const handleUnregister = async () => {
    if (!id) return;
    try {
      await tournamentsService.unregister(parseInt(id));
      await loadTournament(parseInt(id));
    } catch (err: any) {
      alert(err.response?.data?.error?.message || 'Failed to unregister');
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="mt-4 text-gray-600">Loading tournament...</p>
      </div>
    );
  }

  if (error || !tournament) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
        {error || 'Tournament not found'}
      </div>
    );
  }

  return (
    <div>
      <button
        onClick={() => navigate('/tournaments')}
        className="mb-6 inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
      >
        ← Back to Tournaments
      </button>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <div className="flex justify-between items-start mb-6">
          <h1 className="text-3xl font-bold text-gray-900">{tournament.name}</h1>
          <span
            className={`px-3 py-1 text-sm font-medium rounded-full ${
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

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Buy-in</h3>
            <p className="text-2xl font-bold text-gray-900">${tournament.buy_in}</p>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Entry Fee</h3>
            <p className="text-2xl font-bold text-gray-900">${tournament.entry_fee}</p>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Players</h3>
            <p className="text-2xl font-bold text-gray-900">
              {tournament.player_count || 0} / {tournament.max_players}
            </p>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Scheduled Time</h3>
            <p className="text-2xl font-bold text-gray-900">
              {new Date(tournament.scheduled_at).toLocaleString()}
            </p>
          </div>
        </div>

        {isAuthenticated && tournament.status === 'scheduled' && (
          <div className="flex gap-4">
            {tournament.is_registered ? (
              <button
                onClick={handleUnregister}
                className="flex-1 px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
              >
                Unregister from Tournament
              </button>
            ) : (
              <button
                onClick={handleRegister}
                disabled={(tournament.player_count || 0) >= tournament.max_players}
                className="flex-1 px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {(tournament.player_count || 0) >= tournament.max_players
                  ? 'Tournament Full'
                  : 'Register for Tournament'}
              </button>
            )}
          </div>
        )}

        {!isAuthenticated && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
            <p className="text-gray-700">
              Please{' '}
              <button
                onClick={() => navigate('/login')}
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                login
              </button>{' '}
              to register for this tournament.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
