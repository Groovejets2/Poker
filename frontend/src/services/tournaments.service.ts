import apiClient from './api';

/**
 * Tournament interface matching backend API specification
 * See: docs/specifications/OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md
 */
export interface Tournament {
  id: number;
  name: string;
  description?: string | null;
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  buy_in_chips: number;        // ✅ Backend field name
  entry_fee_usd: number;        // ✅ Backend field name
  max_players: number;
  player_count: number;
  seats_available: number;
  scheduled_at: string;         // ISO 8601
  created_at: string;           // ISO 8601
  updated_at: string;           // ISO 8601
  is_registered?: boolean;
}

export interface CreateTournamentData {
  name: string;
  buy_in_chips: number;         // ✅ Backend field name
  entry_fee_usd: number;        // ✅ Backend field name
  max_players: number;
  scheduled_at: string;
}

interface TournamentsListResponse {
  tournaments: Tournament[];
  pagination: {
    total: number;
    page: number;
    limit: number;
    pages: number;
  };
}

export const tournamentsService = {
  /**
   * Get all tournaments
   */
  async getAll(): Promise<Tournament[]> {
    const response = await apiClient.get<TournamentsListResponse>('/tournaments');
    return response.data.tournaments;
  },

  /**
   * Get tournament by ID
   * Backend returns a flat tournament object (not wrapped).
   */
  async getById(id: number): Promise<Tournament> {
    const response = await apiClient.get<Tournament>(`/tournaments/${id}`);
    return response.data;
  },

  /**
   * Create a new tournament (admin only)
   * Backend returns a flat tournament object (not wrapped).
   */
  async create(data: CreateTournamentData): Promise<Tournament> {
    const response = await apiClient.post<Tournament>('/tournaments', data);
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
