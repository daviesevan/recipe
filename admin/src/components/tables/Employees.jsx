import React, { useEffect, useState } from "react";
import { api } from "@/Api";
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
import { useToast } from "@/context/ToastContext";

const Employees = () => {
  const [employees, setEmployees] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const perPage = 3;

  const { showSuccessToast, showErrorToast, showWarningToast } = useToast();

  useEffect(() => {
    fetchEmployees();
  }, [currentPage]);

  const fetchEmployees = async () => {
    setIsLoading(true);
    try {
      const response = await api.get("/employees/", {
        params: {
          page: currentPage,
          per_page: perPage,
        },
      });
      setEmployees(response.data.employees);
      setCurrentPage(response.data.current_page);
      setTotalPages(response.data.total_pages);
    } catch (error) {
      console.error("Error fetching employees:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSetAdmin = async (id) => {
    try {
      await api.post(`/employees/${id}/set_admin`);
      showSuccessToast("Operation was successful!", {
        duration: 4000,
        position: "top-right",
      });
      fetchEmployees();
    } catch (error) {
      showErrorToast("Error setting admin!", {
        duration: 4000,
        position: "top-right",
      });
      console.error("Error setting admin:", error);
    }
  };

  const handleRevokeAdmin = async (id) => {
    try {
      await api.post(`/employees/${id}/revoke_admin`);
      showSuccessToast("Operation was successful!", {
        duration: 4000,
        position: "top-right",
      });
      fetchEmployees();
    } catch (error) {
      showErrorToast("Error setting admin!", {
        duration: 4000,
        position: "top-right",
      });
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
            <Loader loading={true} />
          ) : (
            <>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    {/* <TableHead>Email</TableHead> */}
                    <TableHead>Role</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {employees.map((employee) => (
                    <TableRow key={employee.id}>
                      <TableCell>{employee.fullname}</TableCell>
                      {/* <TableCell>{employee.email}</TableCell> */}
                      <TableCell>
                        <Badge variant="outline">
                          {employee.isAdmin ? "Admin" : "Employee"}
                        </Badge>
                      </TableCell>
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
              <div className="flex justify-between items-center mt-4">
                <Button
                  disabled={currentPage <= 1}
                  onClick={() => setCurrentPage(currentPage - 1)}
                >
                  Previous
                </Button>
                <span>
                  Page {currentPage} of {totalPages}
                </span>
                <Button
                  disabled={currentPage >= totalPages}
                  onClick={() => setCurrentPage(currentPage + 1)}
                >
                  Next
                </Button>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </>
  );
};

export default Employees;
