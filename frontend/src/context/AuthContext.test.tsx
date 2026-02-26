import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { AuthProvider, useAuth } from './AuthContext';
import { ReactNode } from 'react';

// Mock authService
vi.mock('../services/auth.service', () => ({
  authService: {
    getUser: vi.fn(() => null),
    isAuthenticated: vi.fn(() => false),
    storeAuth: vi.fn(),
    logout: vi.fn(),
  },
}));

describe('AuthContext', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('should provide initial auth state', () => {
    const wrapper = ({ children }: { children: ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );

    const { result } = renderHook(() => useAuth(), { wrapper });

    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.isAdmin).toBe(false);
  });

  it('should login user successfully', () => {
    const wrapper = ({ children }: { children: ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );

    const { result } = renderHook(() => useAuth(), { wrapper });

    const mockAuthResponse = {
      token: 'test-token',
      user_id: 1,
      username: 'testuser',
      role: 'player',
      expires_in: 3600,
    };

    act(() => {
      result.current.login(mockAuthResponse);
    });

    expect(result.current.user).toEqual({
      user_id: 1,
      username: 'testuser',
      role: 'player',
    });
    expect(result.current.isAuthenticated).toBe(true);
    expect(result.current.isAdmin).toBe(false);
  });

  it('should identify admin users', () => {
    const wrapper = ({ children }: { children: ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );

    const { result } = renderHook(() => useAuth(), { wrapper });

    const mockAdminAuth = {
      token: 'admin-token',
      user_id: 2,
      username: 'admin',
      role: 'admin',
      expires_in: 3600,
    };

    act(() => {
      result.current.login(mockAdminAuth);
    });

    expect(result.current.isAdmin).toBe(true);
  });

  it('should logout user successfully', () => {
    const wrapper = ({ children }: { children: ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );

    const { result } = renderHook(() => useAuth(), { wrapper });

    const mockAuthResponse = {
      token: 'test-token',
      user_id: 1,
      username: 'testuser',
      role: 'player',
      expires_in: 3600,
    };

    act(() => {
      result.current.login(mockAuthResponse);
    });

    expect(result.current.isAuthenticated).toBe(true);

    act(() => {
      result.current.logout();
    });

    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('should throw error when useAuth is used outside AuthProvider', () => {
    expect(() => {
      renderHook(() => useAuth());
    }).toThrow('useAuth must be used within an AuthProvider');
  });
});
