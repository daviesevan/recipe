import { refreshapi } from "@/Api";
import { jwtDecode } from "jwt-decode";
import React, { useEffect, useState } from "react";
import { Navigate, useLocation } from "react-router-dom";

const ProtectedRoutes = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setIsLoading] = useState(true); // Initialized to true to show loading initially
  const [isRefreshing, setIsRefreshing] = useState(false);
  const location = useLocation(); // Use useLocation to get the current location

  const refreshToken = async () => {
    setIsRefreshing(true);
    try {
      const res = await refreshapi.post("/admin/refresh", {});
      if (res.data.access_token) {
        localStorage.setItem("access_token", res.data.access_token);
        console.log("New Access Token");
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.log("Error in refresh token request:", error);
      setIsAuthenticated(false);
    } finally {
      setIsRefreshing(false);
    }
  };

  const authenticate = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setIsAuthenticated(false);
      setIsLoading(false);
      return;
    }
    try {
      const decoded = jwtDecode(token);
      console.log("Decoded token:", decoded);
      const tokenExpiration = decoded.exp;
      const now = Date.now() / 1000;
      if (tokenExpiration < now) {
        await refreshToken();
      } else {
        setIsAuthenticated(true);
        scheduleTokenRefresh((tokenExpiration - now - 60) * 1000);
      }
    } catch (error) {
      console.error("Error decoding token:", error);
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  const scheduleTokenRefresh = (timeout) => {
    if (!isRefreshing) {
      setTimeout(async () => {
        await refreshToken();
      }, timeout);
    }
  };

  useEffect(() => {
    authenticate();
  }, []);

  if (loading) {
    return <div>Loading...</div>; 
  }

  if (!isAuthenticated) {
    return <Navigate to="/admin/login" state={{ from: location.pathname }} replace />;
  }

  return children;
};

export default ProtectedRoutes;