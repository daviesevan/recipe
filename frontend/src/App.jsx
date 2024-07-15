import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import Login from "./pages/auth/Login";
import Signup from "./pages/auth/Signup";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoutes from "./components/auth/ProtectedRoutes";
import Settings from "./pages/settings/Settings";
import SettingsLayout from "./layouts/SettingsLayout";

const App = () => {
  return (
    <>
      <BrowserRouter>
        <AuthProvider>
          <Navbar />
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/login" element={<Login />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoutes>
                  <Dashboard />
                </ProtectedRoutes>
              }
            />
            <Route
              path="/settings/*"
              element={
                <ProtectedRoutes>
                  <SettingsLayout />
                </ProtectedRoutes>
              }
            />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </>
  );
};

export default App;
