import React from "react";
import {
  Activity,
  ArrowUpRight,
  CircleUser,
  PieChart,
  DollarSign,
  Menu,
  Package2,
  Search,
  Users,
  Hash,
} from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import Navbar from "../../components/Navbar";
import Cards from "../../components/reports/Cards";
import CardDetails from "../../components/reports/CardDetails";
import Transactions from "@/components/tables/Transactions";

const Dashboard = () => {
  return (
    <>
      <Navbar />
      <main className="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-8">
        <div className="grid gap-4 md:grid-cols-2 md:gap-8 lg:grid-cols-4">
          <CardDetails
            endpoint="/admin/analytics/total-users"
            title="Total Users"
            icon={<Users className="h-4 w-4 text-muted-foreground" />}
            dataKey="total_users"
            subtitle="No. of users in our database"
          />
          <CardDetails
            endpoint="/admin/analytics/yearly-revenue"
            title="Total Revenue"
            icon={<DollarSign className="h-4 w-4 text-muted-foreground" />}
            dataKey="yearly_revenue"
            subtitle="This years' revenue"
          />
          <CardDetails
            endpoint="/admin/analytics/users-by-subscription"
            title="Users by Subscription"
            icon={<PieChart className="h-4 w-4 text-muted-foreground" />}
            dataKey="users_by_subscription"
            subtitle="No. of subscribed users"
          />
          <CardDetails
            endpoint="/admin/analytics/recipe-count"
            title="Recipe Count"
            icon={<Hash className="h-4 w-4 text-muted-foreground" />}
            dataKey="recipe_count"
            subtitle="Total recipes in the database"
          />
          <div className="grid gap-2">
            <Transactions />
          </div>
        </div>
      </main>
    </>
  );
};

export default Dashboard;
