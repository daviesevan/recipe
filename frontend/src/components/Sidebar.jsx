import React from "react";
import { Link, useLocation } from "react-router-dom";

const Sidebar = ({ children }) => {
  const location = useLocation();

  return (
    <main className="flex min-h-[calc(100vh_-_theme(spacing.16))] bg-gray-50 flex-1 flex-col gap-4 bg-muted/40 p-4 md:gap-8 md:p-10">
      <div className="mx-auto grid w-full max-w-6xl gap-2">
        <h1 className="text-3xl font-semibold">Settings</h1>
      </div>
      <div className="mx-auto grid w-full max-w-6xl items-start gap-6 md:grid-cols-[180px_1fr] lg:grid-cols-[250px_1fr]">
        <nav className="grid gap-4 text-sm text-muted-foreground">
          <Link
            to="/settings"
            className={
              location.pathname === "/settings"
                ? "font-semibold text-primary"
                : ""
            }
          >
            General
          </Link>
          <Link
            to="/settings/security"
            className={
              location.pathname === "/settings/security"
                ? "font-semibold text-primary"
                : ""
            }
          >
            Security
          </Link>
          <Link
            to="/settings/integrations"
            className={
              location.pathname === "/settings/integrations"
                ? "font-semibold text-primary"
                : ""
            }
          >
            Integrations
          </Link>
          <Link
            to="/settings/support"
            className={
              location.pathname === "/settings/support"
                ? "font-semibold text-primary"
                : ""
            }
          >
            Support
          </Link>
          <Link
            to="/settings/organizations"
            className={
              location.pathname === "/settings/organizations"
                ? "font-semibold text-primary"
                : ""
            }
          >
            Organizations
          </Link>
          <Link
            to="/settings/advanced"
            className={
              location.pathname === "/settings/advanced"
                ? "font-semibold text-primary"
                : ""
            }
          >
            Advanced
          </Link>
        </nav>
        <div className="grid gap-6">{children}</div>
      </div>
    </main>
  );
};

export default Sidebar;
