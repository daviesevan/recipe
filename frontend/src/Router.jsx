import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import ProtectedRoutes from "./components/ProtectedRoutes";
import Recipes from "./pages/Recipes";
import PasswordResetPage from "./pages/PasswordResetPage";
import Signuppage from "./pages/admin/Signup.page";
import DashboardPage from "./pages/admin/Dashboard.page";
import AdminLoginPage from "./pages/admin/Login.page";

const Logout = () => {
  localStorage.clear();
  return <LoginPage />;
};

const Signup = () => {
  localStorage.clear();
  return <SignupPage />;
};

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/admin/login" element={<AdminLoginPage />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/reset-password" element={<PasswordResetPage />} />
        <Route
          path="/recipes"
          element={
            <ProtectedRoutes>
              <Recipes />
            </ProtectedRoutes>
          }
        />
        <Route
          path="/admin/signup"
          element={
            <ProtectedRoutes>
              <Signuppage />
            </ProtectedRoutes>
          }
        />
        <Route
          path="/admin/dashboard"
          element={
            <ProtectedRoutes>
              <DashboardPage />
            </ProtectedRoutes>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};

export default Router;
