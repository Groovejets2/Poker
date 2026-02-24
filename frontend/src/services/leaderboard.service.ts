import apiClient from './api';

export interface LeaderboardPlayer {
  user_id: number;
  username: string;
  tournaments_played: number;
  tournaments_won: number;
  total_winnings: number;
  avg_finish_position: number;
}

export interface PlayerStats {
  user_id: number;
  username: string;
  tournaments_played: number;
  tournaments_won: number;
  total_winnings: number;
  avg_finish_position: number;
  recent_tournaments?: Array<{
    tournament_id: number;
    tournament_name: string;
    finish_position: number;
    payout: number;
  }>;
}

export const leaderboardService = {
  /**
   * Get global leaderboard
   */
  async getLeaderboard(): Promise<LeaderboardPlayer[]> {
    const response = await apiClient.get('/leaderboard');
    return response.data;
  },

  /**
   * Get player statistics
   */
  async getPlayerStats(userId: number): Promise<PlayerStats> {
    const response = await apiClient.get(`/leaderboard/${userId}`);
    return response.data;
  },
};
