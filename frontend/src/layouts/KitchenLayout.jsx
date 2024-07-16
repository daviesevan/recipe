import React from "react";
import { Routes, Route } from "react-router-dom";
import Sidebar from "@/components/Sidebar";
import GeneralSettings from "@/pages/settings/GeneralSettings";
import Breadcrumps from "@/components/Breadcrumps";
import Subscriptions from "@/pages/settings/Subscriptions";

const KitchenLayout = () => {
  return (
    <Sidebar>
      <div className="mx-auto grid w-full max-w-6xl gap-2">
        <Breadcrumps />
      </div>
      <Routes>
        <Route path="/" element={<GeneralSettings />} />
        <Route path="general" element={<GeneralSettings />} />
        <Route path="subscriptions" element={<Subscriptions />} />
      </Routes>
    </Sidebar>
  );
};

export default KitchenLayout;
