import apiClient from './api';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

/**
 * Auth response matching backend API specification
 * See: docs/specifications/OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md
 */
export interface AuthResponse {
  token: string;
  user_id: number;       // ✅ Backend field name
  username: string;
  role: string;
  expires_in: number;
}

/**
 * User object for local storage
 */
export interface User {
  user_id: number;       // ✅ Backend field name
  username: string;
  email?: string;
  role: string;
}

interface RegisterResponse {
  user_id: number;
  username: string;
  message: string;
}

export const authService = {
  /**
   * Register a new user
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await apiClient.post<RegisterResponse>('/auth/register', data);

    // Backend doesn't return token on register, so we need to login
    return this.login({ username: data.username, password: data.password });
  },

  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/login', credentials);
    return response.data;
  },

  /**
   * Store auth data in localStorage
   */
  storeAuth(authData: AuthResponse): void {
    localStorage.setItem('auth_token', authData.token);

    const user: User = {
      user_id: authData.user_id,
      username: authData.username,
      role: authData.role,
    };

    localStorage.setItem('user', JSON.stringify(user));
  },

  /**
   * Get stored user data
   */
  getUser(): User | null {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  /**
   * Logout user
   */
  logout(): void {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  },
};
