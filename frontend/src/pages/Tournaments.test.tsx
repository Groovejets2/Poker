import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Tournaments } from './Tournaments';
import { AuthProvider } from '../context/AuthContext';
import * as tournamentsService from '../services/tournaments.service';

// Mock tournaments service
vi.mock('../services/tournaments.service', () => ({
  tournamentsService: {
    getAll: vi.fn(),
    register: vi.fn(),
    unregister: vi.fn(),
  },
}));

// Mock AuthContext with different states
vi.mock('../context/AuthContext', async () => {
  const actual = await vi.importActual('../context/AuthContext');
  return {
    ...actual,
    useAuth: vi.fn(() => ({
      isAuthenticated: false,
      isAdmin: false,
      user: null,
    })),
  };
});

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      <AuthProvider>{component}</AuthProvider>
    </BrowserRouter>
  );
};

describe('Tournaments Component', () => {
  const mockTournaments = [
    {
      id: 1,
      name: 'Test Tournament 1',
      buy_in: 100,
      entry_fee: 10,
      max_players: 10,
      scheduled_at: '2026-03-01T10:00:00Z',
      status: 'scheduled' as const,
      player_count: 5,
      is_registered: false,
    },
    {
      id: 2,
      name: 'Test Tournament 2',
      buy_in: 200,
      entry_fee: 20,
      max_players: 20,
      scheduled_at: '2026-03-02T10:00:00Z',
      status: 'in_progress' as const,
      player_count: 15,
      is_registered: false,
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should display loading state initially', () => {
    vi.mocked(tournamentsService.tournamentsService.getAll).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    renderWithProviders(<Tournaments />);

    expect(screen.getByText(/loading tournaments/i)).toBeInTheDocument();
  });

  it('should render tournaments list', async () => {
    vi.mocked(tournamentsService.tournamentsService.getAll).mockResolvedValue(
      mockTournaments
    );

    renderWithProviders(<Tournaments />);

    await waitFor(() => {
      expect(screen.getByText('Test Tournament 1')).toBeInTheDocument();
      expect(screen.getByText('Test Tournament 2')).toBeInTheDocument();
    });
  });

  it('should display tournament details correctly', async () => {
    vi.mocked(tournamentsService.tournamentsService.getAll).mockResolvedValue([
      mockTournaments[0],
    ]);

    renderWithProviders(<Tournaments />);

    await waitFor(() => {
      expect(screen.getByText('Test Tournament 1')).toBeInTheDocument();
      expect(screen.getByText(/buy-in:/i)).toBeInTheDocument();
      expect(screen.getByText('$100')).toBeInTheDocument();
      expect(screen.getByText(/entry fee:/i)).toBeInTheDocument();
      expect(screen.getByText('$10')).toBeInTheDocument();
      expect(screen.getByText(/5\/10/i)).toBeInTheDocument(); // player count
    });
  });

  it('should display error message on failure', async () => {
    const errorMessage = 'Failed to load tournaments';
    vi.mocked(tournamentsService.tournamentsService.getAll).mockRejectedValue({
      response: {
        data: {
          error: {
            message: errorMessage,
          },
        },
      },
    });

    renderWithProviders(<Tournaments />);

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  it('should show empty state when no tournaments', async () => {
    vi.mocked(tournamentsService.tournamentsService.getAll).mockResolvedValue([]);

    renderWithProviders(<Tournaments />);

    await waitFor(() => {
      expect(
        screen.getByText(/no tournaments available at the moment/i)
      ).toBeInTheDocument();
    });
  });

  it('should display tournament status badges', async () => {
    vi.mocked(tournamentsService.tournamentsService.getAll).mockResolvedValue(
      mockTournaments
    );

    renderWithProviders(<Tournaments />);

    await waitFor(() => {
      expect(screen.getByText('scheduled')).toBeInTheDocument();
      expect(screen.getByText('in_progress')).toBeInTheDocument();
    });
  });
});
