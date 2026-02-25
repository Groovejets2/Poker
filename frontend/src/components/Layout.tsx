import { Link, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Layout = () => {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <div className="min-h-screen flex flex-col">
      {/* Navigation */}
      <nav className="border-b" style={{
        backgroundColor: 'var(--color-bg-secondary)',
        borderColor: 'var(--color-border)'
      }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20">
            {/* Logo and main navigation */}
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Link to="/" className="text-3xl font-bold text-gold tracking-tight hover:text-gold-light transition-colors">
                  OpenClaw Poker
                </Link>
              </div>
              <div className="hidden sm:ml-12 sm:flex sm:space-x-8">
                <Link
                  to="/tournaments"
                  className="inline-flex items-center px-1 pt-1 text-sm font-medium transition-colors"
                  style={{ color: 'var(--color-text-secondary)' }}
                  onMouseEnter={(e) => e.currentTarget.style.color = 'var(--color-text-primary)'}
                  onMouseLeave={(e) => e.currentTarget.style.color = 'var(--color-text-secondary)'}
                >
                  Tournaments
                </Link>
                <Link
                  to="/leaderboard"
                  className="inline-flex items-center px-1 pt-1 text-sm font-medium transition-colors"
                  style={{ color: 'var(--color-text-secondary)' }}
                  onMouseEnter={(e) => e.currentTarget.style.color = 'var(--color-text-primary)'}
                  onMouseLeave={(e) => e.currentTarget.style.color = 'var(--color-text-secondary)'}
                >
                  Leaderboard
                </Link>
              </div>
            </div>

            {/* User menu */}
            <div className="flex items-center">
              {isAuthenticated ? (
                <div className="flex items-center space-x-6">
                  <span className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>
                    Welcome, <span className="font-semibold text-gold">{user?.username}</span>
                    {user?.role === 'admin' && (
                      <span
                        className="ml-3 inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide"
                        style={{
                          backgroundColor: 'var(--color-accent-gold)',
                          color: 'var(--color-bg-primary)'
                        }}
                      >
                        Admin
                      </span>
                    )}
                  </span>
                  <button
                    onClick={logout}
                    className="inline-flex items-center px-5 py-2 rounded-lg text-sm font-medium transition-all btn-secondary"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <div className="flex items-center space-x-4">
                  <Link
                    to="/login"
                    className="inline-flex items-center px-5 py-2 rounded-lg text-sm font-medium transition-all btn-secondary"
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="inline-flex items-center px-6 py-2.5 rounded-lg text-sm font-semibold transition-all btn-gold"
                  >
                    Register
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Main content */}
      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <Outlet />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t mt-auto" style={{
        backgroundColor: 'var(--color-bg-secondary)',
        borderColor: 'var(--color-border)'
      }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-sm" style={{ color: 'var(--color-text-tertiary)' }}>
            &copy; 2026 OpenClaw Poker Platform. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};
