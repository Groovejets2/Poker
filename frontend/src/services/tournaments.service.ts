import apiClient from './api';

export interface Tournament {
  id: number;
  name: string;
  buy_in: number;
  entry_fee: number;
  max_players: number;
  scheduled_at: string;
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  player_count?: number;
  is_registered?: boolean;
}

export interface CreateTournamentData {
  name: string;
  buy_in: number;
  entry_fee: number;
  max_players: number;
  scheduled_at: string;
}

export const tournamentsService = {
  /**
   * Get all tournaments
   */
  async getAll(): Promise<Tournament[]> {
    const response = await apiClient.get('/tournaments');
    return response.data;
  },

  /**
   * Get tournament by ID
   */
  async getById(id: number): Promise<Tournament> {
    const response = await apiClient.get(`/tournaments/${id}`);
    return response.data;
  },

  /**
   * Create a new tournament (admin only)
   */
  async create(data: CreateTournamentData): Promise<Tournament> {
    const response = await apiClient.post('/tournaments', data);
    return response.data;
  },

  /**
   * Register for a tournament
   */
  async register(tournamentId: number): Promise<void> {
    await apiClient.post(`/tournaments/${tournamentId}/register`);
  },

  /**
   * Unregister from a tournament
   */
  async unregister(tournamentId: number): Promise<void> {
    await apiClient.delete(`/tournaments/${tournamentId}/unregister`);
  },
};
