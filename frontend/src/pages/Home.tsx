import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        Welcome to OpenClaw Poker
      </h1>
      <p className="text-xl text-gray-600 mb-8">
        Compete in tournaments, climb the leaderboard, and become a poker champion!
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">🏆 Tournaments</h2>
          <p className="text-gray-600 mb-4">
            Join competitive poker tournaments and test your skills against other players.
          </p>
          <Link
            to="/tournaments"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            View Tournaments
          </Link>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">📊 Leaderboard</h2>
          <p className="text-gray-600 mb-4">
            See who's on top and track your ranking among all players.
          </p>
          <Link
            to="/leaderboard"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            View Leaderboard
          </Link>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">👤 Your Stats</h2>
          <p className="text-gray-600 mb-4">
            Track your performance, wins, and earnings across all tournaments.
          </p>
          {isAuthenticated ? (
            <Link
              to="/stats"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              View Your Stats
            </Link>
          ) : (
            <Link
              to="/login"
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              Login to View Stats
            </Link>
          )}
        </div>
      </div>

      {!isAuthenticated && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Ready to get started?
          </h3>
          <p className="text-gray-600 mb-4">
            Create an account to join tournaments and compete with players worldwide.
          </p>
          <Link
            to="/register"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            Create Account
          </Link>
        </div>
      )}
    </div>
  );
};
