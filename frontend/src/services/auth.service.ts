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

export interface AuthResponse {
  token: string;
  user: {
    id: number;
    username: string;
    email: string;
    role: string;
  };
}

export const authService = {
  /**
   * Register a new user
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await apiClient.post('/auth/register', data);

    // Backend doesn't return token on register, so we need to login
    if (!response.data.token) {
      // Auto-login after registration
      return this.login({ username: data.username, password: data.password });
    }

    // Map backend response to frontend format
    return {
      token: response.data.token,
      user: {
        id: response.data.user_id,
        username: response.data.username,
        email: data.email,
        role: response.data.role || 'player',
      },
    };
  },

  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiClient.post('/auth/login', credentials);

    // Map backend response to frontend format
    return {
      token: response.data.token,
      user: {
        id: response.data.user_id,
        username: response.data.username,
        email: response.data.email || '',
        role: response.data.role || 'player',
      },
    };
  },

  /**
   * Store auth data in localStorage
   */
  storeAuth(authData: AuthResponse): void {
    localStorage.setItem('auth_token', authData.token);
    localStorage.setItem('user', JSON.stringify(authData.user));
  },

  /**
   * Get stored user data
   */
  getUser() {
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
