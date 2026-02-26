import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { tournamentsService } from '../services/tournaments.service';
import type { Tournament } from '../services/tournaments.service';
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
      await loadTournaments();
    } catch (err: any) {
      alert(err.response?.data?.error?.message || 'Failed to register');
    }
  };

  const handleUnregister = async (tournamentId: number) => {
    try {
      await tournamentsService.unregister(tournamentId);
      await loadTournaments();
    } catch (err: any) {
      alert(err.response?.data?.error?.message || 'Failed to unregister');
    }
  };

  if (loading) {
    return (
      <div className="text-center py-16">
        <div
          className="inline-block animate-spin rounded-full h-14 w-14 border-4 border-t-transparent"
          style={{ borderColor: 'var(--color-accent-gold)' }}
        ></div>
        <p className="mt-6 text-lg" style={{ color: 'var(--color-text-secondary)' }}>
          Loading tournaments...
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
      <div className="flex justify-between items-center mb-10">
        <h1 className="text-4xl font-bold" style={{ color: 'var(--color-text-primary)' }}>
          Tournaments
        </h1>
        {isAdmin && (
          <Link
            to="/tournaments/create"
            className="inline-flex items-center px-6 py-3 rounded-lg text-sm font-semibold transition-all btn-gold"
          >
            Create Tournament
          </Link>
        )}
      </div>

      {tournaments.length === 0 ? (
        <div className="text-center py-20 card">
          <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gold bg-opacity-10 flex items-center justify-center">
            <svg className="w-10 h-10 text-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
            </svg>
          </div>
          <p className="text-lg mb-4" style={{ color: 'var(--color-text-secondary)' }}>
            No tournaments available at the moment.
          </p>
          {isAdmin && (
            <Link
              to="/tournaments/create"
              className="inline-flex items-center px-8 py-3 rounded-lg text-sm font-semibold transition-all btn-gold"
            >
              Create the First Tournament
            </Link>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tournaments.map((tournament) => (
            <div key={tournament.id} className="card p-6">
              <div className="flex justify-between items-start mb-5">
                <h3 className="text-xl font-bold" style={{ color: 'var(--color-text-primary)' }}>
                  {tournament.name}
                </h3>
                <span
                  className={`px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wide ${
                    tournament.status === 'scheduled'
                      ? 'bg-green-900 bg-opacity-30 text-green-400 border border-green-700'
                      : tournament.status === 'in_progress'
                      ? 'bg-yellow-900 bg-opacity-30 text-yellow-400 border border-yellow-700'
                      : tournament.status === 'completed'
                      ? 'bg-gray-700 bg-opacity-30 text-gray-400 border border-gray-600'
                      : 'bg-red-900 bg-opacity-30 text-red-400 border border-red-700'
                  }`}
                >
                  {tournament.status.replace('_', ' ')}
                </span>
              </div>

              <div className="space-y-3 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>
                    Buy-in
                  </span>
                  <span className="font-semibold text-gold">
                    ${tournament.buy_in_chips.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>
                    Entry Fee
                  </span>
                  <span className="font-semibold" style={{ color: 'var(--color-text-primary)' }}>
                    ${tournament.entry_fee_usd.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>
                    Players
                  </span>
                  <span className="font-semibold" style={{ color: 'var(--color-text-primary)' }}>
                    {tournament.player_count || 0} / {tournament.max_players}
                  </span>
                </div>
                <div className="flex justify-between items-center pt-2 border-t" style={{ borderColor: 'var(--color-border)' }}>
                  <span className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>
                    Scheduled
                  </span>
                  <span className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>
                    {new Date(tournament.scheduled_at).toLocaleDateString()}
                  </span>
                </div>
              </div>

              <div className="flex gap-3">
                <Link
                  to={`/tournaments/${tournament.id}`}
                  className="flex-1 text-center px-4 py-2.5 rounded-lg text-sm font-medium transition-all btn-secondary"
                >
                  Details
                </Link>

                {isAuthenticated && tournament.status === 'scheduled' && (
                  <>
                    {tournament.is_registered ? (
                      <button
                        onClick={() => handleUnregister(tournament.id)}
                        className="flex-1 px-4 py-2.5 rounded-lg text-sm font-semibold transition-all"
                        style={{
                          backgroundColor: 'var(--color-error)',
                          color: 'var(--color-text-primary)'
                        }}
                      >
                        Leave
                      </button>
                    ) : (
                      <button
                        onClick={() => handleRegister(tournament.id)}
                        disabled={(tournament.player_count || 0) >= tournament.max_players}
                        className="flex-1 px-4 py-2.5 rounded-lg text-sm font-semibold transition-all btn-gold disabled:opacity-40 disabled:cursor-not-allowed"
                      >
                        {(tournament.player_count || 0) >= tournament.max_players ? 'Full' : 'Join'}
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
