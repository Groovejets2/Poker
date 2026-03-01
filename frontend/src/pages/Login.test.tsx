import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Login } from './Login';
import { AuthProvider } from '../context/AuthContext';
import * as authServiceModule from '../services/auth.service';

// Phase 3.8: mock authService without localStorage methods
vi.mock('../services/auth.service', () => ({
  authService: {
    login: vi.fn(),
    checkSession: vi.fn(() => Promise.resolve(null)),
    logout: vi.fn(() => Promise.resolve()),
  },
}));

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return { ...actual, useNavigate: () => mockNavigate };
});

const renderWithProviders = (component: React.ReactElement) =>
  render(<BrowserRouter><AuthProvider>{component}</AuthProvider></BrowserRouter>);

describe('Login Component - Phase 3.8', () => {
  beforeEach(() => { vi.clearAllMocks(); });

  it('should render login form', async () => {
    renderWithProviders(<Login />);
    await waitFor(() => {
      expect(screen.getByText('Welcome Back')).toBeInTheDocument();
    });
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('should handle successful login and navigate', async () => {
    // Phase 3.8: login returns SessionData (no token)
    const mockSession = { user_id: 1, username: 'testuser', role: 'player' };
    vi.mocked(authServiceModule.authService.login).mockResolvedValue(mockSession);

    renderWithProviders(<Login />);
    await waitFor(() => expect(screen.getByLabelText(/username/i)).toBeInTheDocument());

    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => expect(mockNavigate).toHaveBeenCalledWith('/tournaments'));
  });

  it('should display error on failed login', async () => {
    vi.mocked(authServiceModule.authService.login).mockRejectedValue({
      response: { data: { error: { message: 'Invalid credentials' } } },
    });

    renderWithProviders(<Login />);
    await waitFor(() => expect(screen.getByLabelText(/username/i)).toBeInTheDocument());

    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'bad' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'wrongpass' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => expect(screen.getByText('Invalid credentials')).toBeInTheDocument());
  });
});
