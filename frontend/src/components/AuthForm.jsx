import { Link, useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { useState } from "react";
import api from "@/api";
import toast, { Toaster } from "react-hot-toast";

export default function AuthForm({ route, method, role = "users" }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullname, setFullname] = useState("");
  const [errors, setErrors] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const formData = {
    email,
    password,
    ...(method === "signup" && { fullname }),
  };

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    try {
      const res = await api.post(route, formData);
      if (method === "login") {
        localStorage.setItem("access_token", res.data.access_token);
        localStorage.setItem("refresh_token", res.data.refresh_token);
        navigate(role === "admin" ? "/admin/dashboard" : "/recipes");
      } else {
        if (res.data.error) {
          toast.error(`${res.data.error}`);
        } else {
          toast.success("Signup successful! Please log in.");
          navigate(role === "admin" ? "/admin/login" : "/login");
        }
      }
    } catch (error) {
      if (error.response && error.response.data && error.response.data.error) {
        setErrors(error.response.data.error);
        setTimeout(() => {
          setErrors("");
        }, 3000);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Toaster position="top-right" reverseOrder={false} />
      <div
        className={`flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8 ${
          role === "admin" ? "bg-gray-800 text-white" : "bg-white text-gray-900"
        }`}
      >
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <h2
            className={`mt-10 text-center text-2xl font-bold leading-9 tracking-tight ${
              role === "admin" ? "text-white" : "text-gray-900"
            }`}
          >
            {method === "signup"
              ? role === "admin"
                ? "Create an admin account"
                : "Create an account"
              : role === "admin"
              ? "Admin Sign in"
              : "Sign in to your account"}
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {method === "signup" && (
              <div>
                <label
                  htmlFor="fullname"
                  className={`block text-sm font-medium leading-6 ${
                    role === "admin" ? "text-white" : "text-gray-900"
                  }`}
                >
                  Full Name
                </label>
                <div className="mt-2">
                  <input
                    id="fullname"
                    name="fullname"
                    type="text"
                    value={fullname}
                    placeholder="Enter your Fullname"
                    onChange={(e) => setFullname(e.target.value)}
                    required
                    className={`mt-2 block w-full placeholder-gray-400/70 rounded-lg border ${
                      role === "admin"
                        ? "border-gray-700 bg-gray-900 text-gray-300"
                        : "border-gray-200 bg-white text-gray-700"
                    } px-5 py-2.5 focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-40`}
                  />
                </div>
              </div>
            )}

            <div>
              <label
                htmlFor="email"
                className={`block text-sm font-medium leading-6 ${
                  role === "admin" ? "text-white" : "text-gray-900"
                }`}
              >
                Email address
              </label>
              <div className="mt-2">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  placeholder="Enter your email address."
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className={`mt-2 block w-full placeholder-gray-400/70 rounded-lg border ${
                    role === "admin"
                      ? "border-gray-700 bg-gray-900 text-gray-300"
                      : "border-gray-200 bg-white text-gray-700"
                  } px-5 py-2.5 focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-40`}
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label
                  htmlFor="password"
                  className={`block text-sm font-medium leading-6 ${
                    role === "admin" ? "text-white" : "text-gray-900"
                  }`}
                >
                  Password
                </label>
                {method === "login" && (
                  <div className="text-sm">
                    <Link
                      to="/reset-password"
                      className="font-semibold text-indigo-600 hover:text-indigo-500"
                    >
                      Forgot password?
                    </Link>
                  </div>
                )}
              </div>
              <div className="mt-2">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  placeholder="********"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className={`mt-2 block w-full placeholder-gray-400/70 rounded-lg border ${
                    role === "admin"
                      ? "border-gray-700 bg-gray-900 text-gray-300"
                      : "border-gray-200 bg-white text-gray-700"
                  } px-5 py-2.5 focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-40`}
                />
              </div>
            </div>

            <div>
              <Button
                type="submit"
                className={`flex w-full justify-center rounded-md px-3 py-1.5 text-sm font-semibold leading-6 ${
                  role === "admin"
                    ? "text-gray-900 bg-white"
                    : "text-white bg-indigo-600"
                } shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2`}
              >
                {loading
                  ? "Loading..."
                  : method === "signup"
                  ? role === "admin"
                    ? "Admin Sign up"
                    : "Sign up"
                  : role === "admin"
                  ? "Admin Sign in"
                  : "Sign in"}
              </Button>
            </div>
          </form>

          <p
            className={`mt-10 text-center text-sm ${
              role === "admin" ? "text-gray-400" : "text-gray-500"
            }`}
          >
            {method === "signup" ? (
              <>
                Already have an account?
                <Link
                  to={role === "admin" ? "/admin/login" : "/login"}
                  className="text-blue-700 hover:text-blue-900"
                >
                  {" "}
                  Sign in
                </Link>
              </>
            ) : (
              <>
                Don't have an account?
                <Link
                  to={role === "admin" ? "/admin/signup" : "/signup"}
                  className="text-blue-700 hover:text-blue-900"
                >
                  {" "}
                  Sign up
                </Link>
              </>
            )}
          </p>
        </div>
      </div>
    </>
  );
}
