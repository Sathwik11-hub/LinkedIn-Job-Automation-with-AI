import { useState, useEffect } from 'react';

interface AuthState {
  isAuthenticated: boolean;
  user: any | null;
  token: string | null;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    token: null,
  });

  useEffect(() => {
    // Check for existing token on component mount
    const token = localStorage.getItem('access_token');
    if (token) {
      setAuthState({
        isAuthenticated: true,
        user: null, // You would typically decode the token or fetch user info
        token,
      });
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await fetch('/api/v1/auth/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        setAuthState({
          isAuthenticated: true,
          user: null, // Fetch user info separately if needed
          token: data.access_token,
        });
        return { success: true };
      } else {
        return { success: false, error: 'Login failed' };
      }
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setAuthState({
      isAuthenticated: false,
      user: null,
      token: null,
    });
  };

  const register = async (userData: any) => {
    try {
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        const data = await response.json();
        return { success: true, data };
      } else {
        const errorData = await response.json();
        return { success: false, error: errorData.detail };
      }
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  };

  return {
    ...authState,
    login,
    logout,
    register,
  };
};