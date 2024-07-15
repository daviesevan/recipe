import React, { createContext, useContext, useState } from "react";

const NavbarContext = createContext();

export const NavbarProvider = ({ children }) => {
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <NavbarContext.Provider value={{ searchQuery, setSearchQuery }}>
      {children}
    </NavbarContext.Provider>
  );
};

export const useNavbarContext = () => useContext(NavbarContext);
