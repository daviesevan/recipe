import { useState } from "react";
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
import api from "@/api";

export default function AdminAuthForm({ route, method }) {
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post(route, formData);
      console.log(response.data);
      // Handle successful response (e.g., store tokens, redirect, etc.)
    } catch (error) {
      console.error(error);
      // Handle error (e.g., show error message)
    }
  };

  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>{method === "login" ? "Login" : "Add New Admin"}</CardTitle>
        <CardDescription>
          {method === "login"
            ? "Enter your credentials to access your account"
            : "Create a new admin account"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          {method === "signup" && (
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="fullName">Full Name</Label>
                <Input
                  id="fullName"
                  name="fullName"
                  placeholder="John Doe"
                  value={formData.fullName}
                  onChange={handleChange}
                />
              </div>
            </div>
          )}
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="john@example.com"
                value={formData.email}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
              />
            </div>
          </div>
          <Button className="w-full mt-6" type="submit">
            {method === "login" ? "Login" : "Create Admin"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}