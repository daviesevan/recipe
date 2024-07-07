import { api } from "@/Api";
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { MoreHorizontal } from "lucide-react";
import Loader from "../Loader";

const Employees = () => {
  const [employees, setEmployees] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    setIsLoading(true);
    try {
      const response = await api.get("/employees/");
      setEmployees(response.data);
    } catch (error) {
      console.error("Error fetching employees:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSetAdmin = async (id) => {
    try {
      await api.post(`/employees/${id}/set_admin`);
      fetchEmployees();
    } catch (error) {
      console.error("Error setting admin:", error);
    }
  };

  const handleRevokeAdmin = async (id) => {
    try {
      await api.post(`/employees/${id}/revoke_admin`);
      fetchEmployees();
    } catch (error) {
      console.error("Error revoking admin:", error);
    }
  };

  return (
    <>
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Employees</CardTitle>
          <CardDescription>
            Manage your employees and view their performance.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <Loader />
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  {/* <TableHead>Admin</TableHead> */}
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {employees.map((employee) => (
                  <TableRow key={employee.id}>
                    <TableCell>{employee.fullname}</TableCell>
                    <TableCell>{employee.email}</TableCell>
                    {/* <TableCell>
                      <Badge variant="outline">
                        {employee.isAdmin ? "Admin" : "Employee"}
                      </Badge>
                    </TableCell> */}
                    <TableCell>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button
                            aria-haspopup="true"
                            size="icon"
                            variant="ghost"
                          >
                            <MoreHorizontal className="h-4 w-4" />
                            <span className="sr-only">Toggle menu</span>
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuLabel>Actions</DropdownMenuLabel>
                          <DropdownMenuItem
                            onClick={() =>
                              employee.isAdmin
                                ? handleRevokeAdmin(employee.id)
                                : handleSetAdmin(employee.id)
                            }
                          >
                            {employee.isAdmin ? "Revoke Admin" : "Set Admin"}
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </>
  );
};

export default Employees;
