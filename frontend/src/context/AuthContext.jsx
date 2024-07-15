import React, { createContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      setIsAuthenticated(true);
      const decodedUser = jwtDecode(token);
      setUser(decodedUser);

      const isTokenExpired = decodedUser.exp * 1000 < Date.now();
      if (isTokenExpired) {
        handleTokenRefresh();
      }
    }
  }, []);

  const handleTokenRefresh = async () => {
    try {
      const { data } = await api.post("/auth/refresh");
      localStorage.setItem("access_token", data.access_token);
      const decodedUser = jwtDecode(data.access_token);
      setIsAuthenticated(true);
      setUser(decodedUser);
    } catch (error) {
      console.error("Failed to refresh token", error);
      logout();
    }
  };

  const login = (token) => {
    localStorage.setItem("access_token", token);
    setIsAuthenticated(true);
    const decodedUser = jwtDecode(token);
    setUser(decodedUser);
    navigate("/dashboard");
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setIsAuthenticated(false);
    setUser(null);
    navigate("/login");
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
