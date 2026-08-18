'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { fetchApi } from './api';

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: 'SOLVER' | 'POSTER' | 'BOTH' | 'ADMIN' | 'MODERATOR';
  status: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, pass: string) => Promise<void>;
  register: (payload: any) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    try {
      const token = localStorage.getItem('sb_access_token');
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }
      const data = await fetchApi('/auth/me/');
      setUser(data);
    } catch (e) {
      localStorage.removeItem('sb_access_token');
      localStorage.removeItem('sb_refresh_token');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = async (email: string, password: string) => {
    const data = await fetchApi('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    localStorage.setItem('sb_access_token', data.access_token);
    localStorage.setItem('sb_refresh_token', data.refresh_token);
    setUser(data.user);
  };

  const register = async (payload: any) => {
    const data = await fetchApi('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    localStorage.setItem('sb_access_token', data.access_token);
    localStorage.setItem('sb_refresh_token', data.refresh_token);
    setUser(data.user);
  };

  const logout = () => {
    localStorage.removeItem('sb_access_token');
    localStorage.removeItem('sb_refresh_token');
    setUser(null);
    window.location.href = '/';
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
