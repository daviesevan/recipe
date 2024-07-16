import React from "react";
import { Link, useLocation } from "react-router-dom";
import {
  CreditCard,
  UserRoundCog,
  ChefHat,
  HeartIcon,
  Grape,
  CookingPot,
  SearchIcon,
  Beef ,
} from "lucide-react";
const Sidebar = ({ children }) => {
  const location = useLocation();

  return (
    <main className="flex min-h-[calc(100vh_-_theme(spacing.16))] flex-1 flex-col gap-4 bg-muted/40 p-4 md:gap-8 md:p-10">
      <div className="mx-auto grid w-full max-w-6xl gap-2">
        <h1 className="text-3xl font-semibold">My Kitchen</h1>
      </div>
      <div className="mx-auto grid w-full max-w-6xl items-start gap-6 md:grid-cols-[180px_1fr] lg:grid-cols-[250px_1fr]">
        <nav className="grid gap-4 text-sm text-muted-foreground">
          <Link
            to="/kitchen"
            className={
              location.pathname === "/kitchen"
                ? "font-semibold text-primary flex"
                : "flex"
            }
          >
            <UserRoundCog className="flex-shrink-0 w-4 h-auto mr-3" />
            General
          </Link>
          <Link
            to="/kitchen/subscriptions"
            className={
              location.pathname === "/kitchen/subscriptions"
                ? "font-semibold text-primary flex"
                : "flex"
            }
          >
            <CreditCard className="flex-shrink-0 w-4 h-auto mr-3" />
            Subscriptions
          </Link>
          <Link
            to="/kitchen/favourites"
            className={
              location.pathname === "/kitchen/favourites"
                ? "font-semibold text-primary flex"
                : "flex"
            }
          >
            <HeartIcon className="flex-shrink-0 w-4 h-auto mr-3" />
            Favourites
          </Link>
          <Link
            to="/kitchen/recipes"
            className={
              location.pathname === "/kitchen/recipes"
                ? "font-semibold text-primary flex"
                : "flex"
            }
          >
            <ChefHat className="flex-shrink-0 w-4 h-auto mr-3" />
            My Recipes
          </Link>
          <Link
            to="/kitchen/organizations"
            className={
              location.pathname === "/kitchen/organizations"
              ? "font-semibold text-primary flex"
              : "flex"
          }
        >
          <ChefHat className="flex-shrink-0 w-4 h-auto mr-3" />
            Organizations
          </Link>
          <Link
            to="/kitchen/advanced"
            className={
              location.pathname === "/kitchen/advanced"
              ? "font-semibold text-primary flex"
              : "flex"
          }
        >
          <ChefHat className="flex-shrink-0 w-4 h-auto mr-3" />
            Advanced
          </Link>
        </nav>
        <div className="grid gap-6">{children}</div>
      </div>
    </main>
  );
};

export default Sidebar;
