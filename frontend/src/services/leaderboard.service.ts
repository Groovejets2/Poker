import apiClient from './api';

/**
 * Leaderboard interfaces matching backend API specification
 * See: docs/specifications/OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md
 */
export interface LeaderboardPlayer {
  rank: number;
  user_id: number;                // ✅ Backend field name
  username: string;
  tournaments_played: number;
  tournament_wins: number;        // ✅ Backend field name (not tournaments_won)
  avg_finish: number | null;      // ✅ Backend field name (not avg_finish_position)
  total_winnings: number;
}

export interface PlayerStats {
  user_id: number;                // ✅ Backend field name
  username: string;
  tournaments_played: number;
  tournament_wins: number;        // ✅ Backend field name
  avg_finish: number | null;      // ✅ Backend field name
  total_winnings: number;
}

interface LeaderboardResponse {
  leaderboard: LeaderboardPlayer[];
  updated_at: string;
}

interface PlayerStatsResponse {
  player: PlayerStats;
}

export const leaderboardService = {
  /**
   * Get global leaderboard
   */
  async getLeaderboard(): Promise<LeaderboardPlayer[]> {
    const response = await apiClient.get<LeaderboardResponse>('/leaderboard');
    return response.data.leaderboard;
  },

  /**
   * Get player statistics
   */
  async getPlayerStats(userId: number): Promise<PlayerStats> {
    const response = await apiClient.get<PlayerStatsResponse>(`/leaderboard/${userId}`);
    return response.data.player;
  },
};
