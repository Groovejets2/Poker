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
    const leaderboard = response.data.leaderboard || response.data;

    // Map backend field names to frontend field names
    return leaderboard.map((player: any) => ({
      ...player,
      tournaments_won: player.tournament_wins || player.tournaments_won || 0,
      avg_finish_position: player.avg_finish || player.avg_finish_position,
    }));
  },

  /**
   * Get player statistics
   */
  async getPlayerStats(userId: number): Promise<PlayerStats> {
    const response = await apiClient.get(`/leaderboard/${userId}`);
    return response.data;
  },
};
