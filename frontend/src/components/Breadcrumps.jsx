import { Link, useLocation } from "react-router-dom";
import React from "react";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";

const Breadcrumps = () => {
  const location = useLocation();
  console.log(location);

  let currentLink = "";
  const crumbs = location.pathname
    .split("/")
    .filter((crumb) => crumb !== "")
    .map((crumb, index, array) => {
      currentLink = currentLink + `/${crumb}`;
      if (index === array.length - 1) {
        return (
          <BreadcrumbItem key={crumb}>
            <BreadcrumbPage>{crumb}</BreadcrumbPage>
          </BreadcrumbItem>
        );
      } else {
        return (
          <BreadcrumbItem key={crumb}>
            <BreadcrumbLink asChild>
              <Link to={currentLink}>{crumb}</Link>
            </BreadcrumbLink>
            <BreadcrumbSeparator />
          </BreadcrumbItem>
        );
      }
    });

  return (
    <Breadcrumb className="hidden md:flex">
      <BreadcrumbList>{crumbs}</BreadcrumbList>
    </Breadcrumb>
  );
};

export default Breadcrumps;
