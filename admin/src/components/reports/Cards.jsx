import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const Cards = ({ title, icon, children }) => {
  return (
    <Card x-chunk="dashboard-01-chunk-0">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
};

export default Cards;
