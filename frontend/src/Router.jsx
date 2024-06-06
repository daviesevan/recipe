import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import ProtectedRoutes from "./components/ProtectedRoutes";
import Recipes from "./pages/Recipes";
import PasswordResetPage from "./pages/PasswordResetPage";

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
      </Routes>
    </BrowserRouter>
  );
};

export default Router;
