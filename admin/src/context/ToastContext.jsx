import React, { createContext, useContext } from "react";
import { Toaster, toast } from "react-hot-toast";

const ToastContext = createContext();

export const useToast = () => {
  return useContext(ToastContext);
};

export const ToastProvider = ({ children }) => {
  const showToast = (message, options) => {
    toast(message, options);
  };

  const showSuccessToast = (message, options) => {
    toast.success(message, options);
  };

  const showErrorToast = (message, options) => {
    toast.error(message, options);
  };

  const showWarningToast = (message, options) => {
    toast(message, {
      ...options,
      style: { background: "orange", color: "white" },
    });
  };

  return (
    <ToastContext.Provider
      value={{ showToast, showSuccessToast, showErrorToast, showWarningToast }}
    >
      {children}
      <Toaster />
    </ToastContext.Provider>
  );
};
