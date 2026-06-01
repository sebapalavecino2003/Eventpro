import { createContext, useState, useCallback } from 'react';
import { authService } from '../services/authService';

// eslint-disable-next-line react-refresh/only-export-components
export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('user');
    return stored ? JSON.parse(stored) : null;
  });

  const [loading, setLoading] = useState(false);

  const isAuthenticated = !!localStorage.getItem('access_token') && !!user;

  const login = useCallback(async (email, password) => {
    setLoading(true);
    try {
      const { data } = await authService.login(email, password);
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      localStorage.setItem('user', JSON.stringify(data.user));
      setUser(data.user);
      return data.user;
    } finally {
      setLoading(false);
    }
  }, []);

  const register = useCallback(async (formData) => {
    setLoading(true);
    try {
      const { data } = await authService.register(formData);
      return data;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    const refresh = localStorage.getItem('refresh_token');
    if (refresh) {
      try {
        await authService.logout(refresh);
      } catch {
        /* ignore */
      }
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setUser(null);
  }, []);

  const updateUser = useCallback((userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  }, []);

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
