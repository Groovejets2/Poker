import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="text-center">
      <div className="mb-16">
        <h1 className="text-6xl font-bold mb-6" style={{ color: 'var(--color-text-primary)' }}>
          Welcome to <span className="text-gold">OpenClaw Poker</span>
        </h1>
        <p className="text-xl max-w-3xl mx-auto" style={{ color: 'var(--color-text-secondary)' }}>
          Compete in high-stakes tournaments, climb the leaderboard, and establish yourself as a poker champion in our premium gaming platform.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
        {/* Tournaments Card */}
        <div className="card p-8 group">
          <div className="mb-4">
            <div className="w-16 h-16 mx-auto rounded-full bg-gold bg-opacity-10 flex items-center justify-center">
              <svg className="w-8 h-8 text-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
              </svg>
            </div>
          </div>
          <h2 className="text-2xl font-bold mb-3" style={{ color: 'var(--color-text-primary)' }}>
            Tournaments
          </h2>
          <p className="mb-6" style={{ color: 'var(--color-text-secondary)' }}>
            Join competitive poker tournaments and test your skills against elite players from around the world.
          </p>
          <Link
            to="/tournaments"
            className="inline-flex items-center px-6 py-2.5 rounded-lg text-sm font-semibold transition-all btn-gold"
          >
            View Tournaments
          </Link>
        </div>

        {/* Leaderboard Card */}
        <div className="card p-8 group">
          <div className="mb-4">
            <div className="w-16 h-16 mx-auto rounded-full bg-gold bg-opacity-10 flex items-center justify-center">
              <svg className="w-8 h-8 text-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
          <h2 className="text-2xl font-bold mb-3" style={{ color: 'var(--color-text-primary)' }}>
            Leaderboard
          </h2>
          <p className="mb-6" style={{ color: 'var(--color-text-secondary)' }}>
            Track your ranking and see who dominates at the top of our global player rankings.
          </p>
          <Link
            to="/leaderboard"
            className="inline-flex items-center px-6 py-2.5 rounded-lg text-sm font-semibold transition-all btn-gold"
          >
            View Leaderboard
          </Link>
        </div>

        {/* Stats Card */}
        <div className="card p-8 group">
          <div className="mb-4">
            <div className="w-16 h-16 mx-auto rounded-full bg-gold bg-opacity-10 flex items-center justify-center">
              <svg className="w-8 h-8 text-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
          </div>
          <h2 className="text-2xl font-bold mb-3" style={{ color: 'var(--color-text-primary)' }}>
            Your Statistics
          </h2>
          <p className="mb-6" style={{ color: 'var(--color-text-secondary)' }}>
            Track your performance, victories, and earnings across all tournament appearances.
          </p>
          {isAuthenticated ? (
            <Link
              to="/stats"
              className="inline-flex items-center px-6 py-2.5 rounded-lg text-sm font-semibold transition-all btn-gold"
            >
              View Your Stats
            </Link>
          ) : (
            <Link
              to="/login"
              className="inline-flex items-center px-6 py-2.5 rounded-lg text-sm font-medium transition-all btn-secondary"
            >
              Login to View Stats
            </Link>
          )}
        </div>
      </div>

      {!isAuthenticated && (
        <div className="card p-10 max-w-2xl mx-auto shadow-gold">
          <h3 className="text-2xl font-bold mb-3" style={{ color: 'var(--color-text-primary)' }}>
            Ready to Join the Elite?
          </h3>
          <p className="text-lg mb-8" style={{ color: 'var(--color-text-secondary)' }}>
            Create an account to participate in exclusive tournaments and compete with the world's finest poker players.
          </p>
          <Link
            to="/register"
            className="inline-flex items-center px-10 py-4 rounded-lg text-base font-bold transition-all btn-gold shadow-gold-lg"
          >
            Create Your Account
          </Link>
        </div>
      )}
    </div>
  );
};
