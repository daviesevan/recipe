import React, { useState } from "react";
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
import { Link } from "react-router-dom";
import { signupEmployee, loginAdmin } from "../../Api";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/context/ToastContext";
const Form = ({ method }) => {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { showErrorToast, showSuccessToast } = useToast();
  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (method === "signup") {
        try {
          const response = await signupEmployee(fullName, email, password);
          showSuccessToast(`${response.message}`, {
            duration: 4000,
            position: "top-center",
          });
          navigate("/admin/login");
        } catch (error) {
          showErrorToast(
            response.message || "Signup failed! Please try again.",
            {
              duration: 4000,
              position: "top-center",
            }
          );
        }
      }
      if (method === "login") {
        try {
          const response = await loginAdmin(email, password);
          console.log("Login response:", response);
          console.log("Login successful, about to show success toast");
          showSuccessToast(`Welcome back ${response.admin_name}`, {
            duration: 4000,
            position: "top-center",
          });
          console.log("Success toast should be visible now");
          navigate("/dashboard");
        } catch (error) {
          showErrorToast(
            response.message || "Invalid credentials! Please try again.",
            {
              duration: 4000,
              position: "top-center",
            }
          );
        }
      }
    } catch (error) {
      showErrorToast("An error occurred! Please try again.", {
        duration: 4000,
        position: "top-center",
      });
      console.error("Error during form submission:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="mx-auto max-w-sm mt-24">
      <CardHeader>
        <CardTitle className="text-2xl">
          {method === "signup" ? "Add Employee" : "Employee's Login"}
        </CardTitle>
        <CardDescription>
          {method === "signup"
            ? "Create a new employee account"
            : "Enter your credentials to login"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="grid gap-4">
          {method === "signup" && (
            <div className="grid gap-2">
              <Label htmlFor="fullName">Full Name</Label>
              <Input
                id="fullName"
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
              />
            </div>
          )}
          <div className="grid gap-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="m@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="grid gap-2">
            <div className="flex items-center">
              <Label htmlFor="password">Password</Label>
              {method === "login" && (
                <Link to="#" className="ml-auto inline-block text-sm underline">
                  Forgot your password?
                </Link>
              )}
            </div>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading
              ? "Processing..."
              : method === "signup"
              ? "Add Employee"
              : "Login"}
          </Button>
        </form>
        {method === "login" && (
          <div className="mt-4 text-center text-sm">
            Not an admin?{" "}
            <Link to="/admin/signup" className="underline">
              Signup Here
            </Link>
          </div>
        )}
        {method === "signup" && (
          <div className="mt-4 text-center text-sm">
            I already have an account?{" "}
            <Link to="/admin/login" className="underline">
              Login Here
            </Link>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default Form;
