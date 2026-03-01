import { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { authService } from '../services/auth.service';
import type { SessionData } from '../services/auth.service';

interface User { user_id: number; username: string; email?: string; role: string; }

interface AuthContextType {
  user: User | null; isAuthenticated: boolean; isLoading: boolean;
  login: (sessionData: SessionData) => void; logout: () => Promise<void>; isAdmin: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    authService.checkSession()
      .then((s) => { if (s) setUser({ user_id: s.user_id, username: s.username, role: s.role }); })
      .finally(() => setIsLoading(false));
  }, []);

  const login = (s: SessionData) => setUser({ user_id: s.user_id, username: s.username, role: s.role });
  const logout = async () => { await authService.logout(); setUser(null); };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, isLoading, login, logout, isAdmin: user?.role === 'admin' }}>
      {children}
    </AuthContext.Provider>
  );
};
