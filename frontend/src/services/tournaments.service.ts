import apiClient from './api';

export interface Tournament {
  id: number;
  name: string;
  buy_in: number;
  buy_in_chips?: number;
  entry_fee: number;
  entry_fee_usd?: number;
  max_players: number;
  scheduled_at: string;
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  player_count?: number;
  seats_available?: number;
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
    const tournaments = response.data.tournaments || response.data;

    // Map backend field names to frontend field names
    return tournaments.map((t: any) => ({
      ...t,
      buy_in: t.buy_in_chips || t.buy_in,
      entry_fee: t.entry_fee_usd || t.entry_fee,
    }));
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
