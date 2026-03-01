import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from './AuthContext';
import { ReactNode } from 'react';

// Phase 3.8: mock authService with cookie-based methods
vi.mock('../services/auth.service', () => ({
  authService: {
    checkSession: vi.fn(() => Promise.resolve(null)),
    logout: vi.fn(() => Promise.resolve()),
  },
}));

import { authService } from '../services/auth.service';

const wrapper = ({ children }: { children: ReactNode }) =>
  <AuthProvider>{children}</AuthProvider>;

describe('AuthContext - Phase 3.8', () => {
  beforeEach(() => { vi.clearAllMocks(); });

  it('should start with isLoading true then settle to false', async () => {
    (authService.checkSession as any).mockResolvedValue(null);
    const { result } = renderHook(() => useAuth(), { wrapper });

    expect(result.current.isLoading).toBe(true);
    await waitFor(() => expect(result.current.isLoading).toBe(false));
    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('should restore session from cookie on mount', async () => {
    const sessionData = { user_id: 1, username: 'testuser', role: 'player' };
    (authService.checkSession as any).mockResolvedValue(sessionData);

    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.isLoading).toBe(false));

    expect(result.current.user).toEqual({ user_id: 1, username: 'testuser', role: 'player' });
    expect(result.current.isAuthenticated).toBe(true);
    expect(result.current.isAdmin).toBe(false);
  });

  it('should login user via context login()', async () => {
    (authService.checkSession as any).mockResolvedValue(null);
    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.isLoading).toBe(false));

    act(() => {
      result.current.login({ user_id: 2, username: 'admin', role: 'admin' });
    });

    expect(result.current.user).toEqual({ user_id: 2, username: 'admin', role: 'admin' });
    expect(result.current.isAdmin).toBe(true);
  });

  it('should logout user and clear state', async () => {
    const sessionData = { user_id: 1, username: 'testuser', role: 'player' };
    (authService.checkSession as any).mockResolvedValue(sessionData);

    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.isAuthenticated).toBe(true));

    await act(async () => { await result.current.logout(); });

    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
    expect(authService.logout).toHaveBeenCalledOnce();
  });

  it('should throw when useAuth used outside AuthProvider', () => {
    expect(() => renderHook(() => useAuth())).toThrow('useAuth must be used within an AuthProvider');
  });
});
