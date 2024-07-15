import Sidebar from "@/components/Sidebar";
import GeneralSettings from "@/pages/settings/GeneralSettings";
import React from "react";
import { Routes, Route } from "react-router-dom";

const SettingsLayout = () => {
  return (
    <Sidebar>
      <Routes>
        <Route path="/" element={<GeneralSettings />} />
        <Route path="general" element={<GeneralSettings />} />
      </Routes>
    </Sidebar>
  );
};

export default SettingsLayout;
