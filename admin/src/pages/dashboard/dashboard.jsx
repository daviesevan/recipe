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
import Navbar from "../../components/Navbar";
import CardDetails from "../../components/reports/CardDetails";
import Transactions from "@/components/tables/Transactions";
import Employees from "@/components/tables/Employees";
import Loader from "@/components/Loader";

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
          </div>
          <div className="grid gap-4 md:gap-8 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <Transactions />
          </div>
          <div className="lg:col-span-1">
            <Employees />
          </div>
        </div>
      </main>
    </>
  );
};

export default Dashboard;
