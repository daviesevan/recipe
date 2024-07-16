import React, { useContext, useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { AuthContext } from "@/context/AuthContext";
import { useToast } from "@/context/ToastContext";
import { api } from "@/Api";

const GeneralSettings = () => {
  const { userSettings, setUserSettings } = useContext(AuthContext);
  const [email, setEmail] = useState(userSettings?.email || "");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(true);

  const { showErrorToast, showSuccessToast } = useToast();

  const updateProfile = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.put("/user/settings/", { email, password });
      setUserSettings({ ...userSettings, email });
      showSuccessToast("Profile updated successfully!", {
        duration: 4000,
        position: "top-right",
      });
    } catch (error) {
      showErrorToast("Failed to update profile", {
        duration: 4000,
        position: "top-right",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (userSettings) {
      setEmail(userSettings.email);
    }
  }, [userSettings]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Update your personal info</CardTitle>
        <CardDescription>
          Used to identify your store in the marketplace.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={updateProfile}>
          <Input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
          />
          <Input
            className="mt-2"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            type="password"
          />
        </form>
      </CardContent>
      <CardFooter className="border-t px-6 py-4">
        <Button type="submit" disabled={loading}>
          Update Profile
        </Button>
      </CardFooter>
    </Card>
  );
};

export default GeneralSettings;
