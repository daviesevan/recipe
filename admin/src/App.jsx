import { useState } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Login from "./pages/auth/Login";
import Signup from "./pages/auth/Signup";
import Dashboard from "./pages/dashboard/dashboard";
import ProtectedRoutes from "./components/ProtectedRoutes";

const Logout = () => {
  localStorage.clear();
  return <Login />;
};
const Signin = () => {
  localStorage.clear();
  return <Login />;
};
// const Register = () => {
//   // localStorage.clear();
//   return <Signup />;
// };

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/admin/login" element={<Signin />} />
          <Route path="/admin/signup" element={<Signup />} />
          <Route path="/logout" element={<Logout />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoutes>
                <Dashboard />
              </ProtectedRoutes>
            }
          />
          <Route
            path="/admin/signup"
            element={
              <ProtectedRoutes>
                <Signup />
              </ProtectedRoutes>
            }
          />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
