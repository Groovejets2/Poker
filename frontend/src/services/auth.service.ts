import apiClient from './api';

export interface LoginCredentials { username: string; password: string; }
export interface RegisterData { username: string; email: string; password: string; }
export interface SessionData { user_id: number; username: string; role: string; }
export interface User { user_id: number; username: string; email?: string; role: string; }

interface RegisterResponse { user_id: number; username: string; message: string; }

export const authService = {
  async register(data: RegisterData): Promise<SessionData> {
    await apiClient.post<RegisterResponse>('/auth/register', data);
    return this.login({ username: data.username, password: data.password });
  },
  async login(credentials: LoginCredentials): Promise<SessionData> {
    const response = await apiClient.post<SessionData>('/auth/login', credentials);
    return response.data;
  },
  /** Phase 3.8: Restore session from httpOnly cookie */
  async checkSession(): Promise<SessionData | null> {
    try {
      const response = await apiClient.post<SessionData>('/auth/refresh');
      return response.data;
    } catch { return null; }
  },
  async logout(): Promise<void> {
    try { await apiClient.post('/auth/logout'); } catch { /* ignore */ }
  },
};
