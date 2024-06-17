import { useState, useEffect } from "react";
import api from "@/api";
import toast, { Toaster } from "react-hot-toast";
import { Card, CardHeader, CardContent, CardTitle } from "../../components/ui/card";

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get("/admin/analytics/all");
        setData(response.data);
      } catch (err) {
        setError(err.message);
        toast.error("Failed to fetch data");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Toaster position="top-right" reverseOrder={false} />
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Total Users</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{data.total_users}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Verified Users</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{data.verified_users}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Total Admins</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{data.total_admins}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Payments in Last 30 Days</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{data.payments_count}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Monthly Active Users</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{data.monthly_active_users}</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
