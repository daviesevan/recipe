import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { loginUser, signupUser } from "@/Api";
import { useToast } from "@/context/ToastContext";
import { AuthContext } from "@/context/AuthContext";

const Form = ({ formType }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    fullname: "",
    email: "",
    password: "",
  });
  const { showSuccessToast, showErrorToast } = useToast();
  const navigate = useNavigate();
  const {login} = useContext(AuthContext)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      if (formType === "signup") {
        await signupUser(formData.fullname, formData.email, formData.password);
        showSuccessToast("Signup successful!", {
          duration: 4000,
          position: "bottom-right",
        });
        navigate("/login");
      } else if (formType === "login") {
        const response = await loginUser(formData.email, formData.password);
        login(response.access_token);
        showSuccessToast("Login successful!", {
          duration: 4000,
          position: "bottom-right",
        });
        navigate('/dashboard')
      }
    } catch (error) {
      setError(error.message);
      showErrorToast("Something went wrong!",{
        duration: 4000,
        position: 'bottom-right'
      })
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="mx-auto max-w-sm mt-24">
      <CardHeader>
        <CardTitle className="text-2xl">
          {formType === "signup" ? "Sign Up" : "Login"}
        </CardTitle>
        <CardDescription>
          {formType === "signup"
            ? "Create a new account."
            : "Enter your email below to login to your account."}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4">
            {formType === "signup" && (
              <div className="grid gap-2">
                <Label htmlFor="fullname">Full Name</Label>
                <Input
                  id="fullname"
                  name="fullname"
                  type="text"
                  placeholder="John Doe"
                  value={formData.fullname}
                  onChange={handleChange}
                  required
                />
              </div>
            )}
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="m@example.com"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="grid gap-2">
              <div className="flex items-center">
                <Label htmlFor="password">Password</Label>
                {formType === "login" && (
                  <Link
                    to="/forgot-password"
                    className="ml-auto inline-block text-sm underline"
                  >
                    Forgot your password?
                  </Link>
                )}
              </div>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="********"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading
                ? "Loading..."
                : formType === "signup"
                ? "Sign Up"
                : "Login"}
            </Button>
            {formType === "login" && (
              <Button variant="outline" className="w-full">
                Login with Google
              </Button>
            )}
          </div>
          <div className="mt-4 text-center text-sm">
            {formType === "signup" ? (
              <>
                Already have an account?{" "}
                <Link to="/login" className="underline">
                  Log in
                </Link>
              </>
            ) : (
              <>
                Don&apos;t have an account?{" "}
                <Link to="/signup" className="underline">
                  Sign up
                </Link>
              </>
            )}
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default Form;
