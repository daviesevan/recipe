import React, { useEffect, useState } from "react";
import { useLocation, Link } from "react-router-dom";
import api from "@/api";

const PaymentConfirmation = () => {
  const location = useLocation();
  const [paymentDetails, setPaymentDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retryCount, setRetryCount] = useState(0);
  const maxRetries = 2; // Maximum number of retries
  const retryInterval = 3000; // Retry interval in milliseconds

  // Helper function to extract query parameters
  const getQueryParams = (search) => {
    return new URLSearchParams(search);
  };

  useEffect(() => {
    const queryParams = getQueryParams(location.search);
    const reference = queryParams.get("reference");

    if (!reference) {
      console.error("Reference is required");
      return;
    }

    const verifyPayment = async () => {
      try {
        const response = await api.post("/payment/verify", { reference });
        setPaymentDetails(response.data);
      } catch (error) {
        if (retryCount < maxRetries) {
          setTimeout(() => setRetryCount(retryCount + 1), retryInterval);
        } else {
          console.error("Payment verification failed:", error);
        }
      } finally {
        setLoading(false);
      }
    };

    verifyPayment();
  }, [location.search, retryCount]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!paymentDetails) {
    return <div>Payment verification failed. Please try again.</div>;
  }

  return (
    <section className="bg-white py-8 antialiased dark:bg-gray-900 md:py-16">
      <div className="mx-auto max-w-2xl px-4 2xl:px-0">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl mb-2">
          Thanks for your order!
        </h2>
        <p className="text-gray-500 dark:text-gray-400 mb-6 md:mb-8">
          Your order{" "}
          <span className="font-medium text-gray-900 dark:text-white">
            #{reference}
          </span>{" "}
          has been processed successfully. We will notify you by email with
          further details.
        </p>
        <div className="space-y-4 sm:space-y-2 rounded-lg border border-gray-100 bg-gray-50 p-6 dark:border-gray-700 dark:bg-gray-800 mb-6 md:mb-8">
          <dl className="sm:flex items-center justify-between gap-4">
            <dt className="font-normal mb-1 sm:mb-0 text-gray-500 dark:text-gray-400">
              Date
            </dt>
            <dd className="font-medium text-gray-900 dark:text-white sm:text-end">
              {new Date().toLocaleDateString()}
            </dd>
          </dl>
          <dl className="sm:flex items-center justify-between gap-4">
            <dt className="font-normal mb-1 sm:mb-0 text-gray-500 dark:text-gray-400">
              Payment Method
            </dt>
            <dd className="font-medium text-gray-900 dark:text-white sm:text-end">
              Paystack
            </dd>
          </dl>
          <dl className="sm:flex items-center justify-between gap-4">
            <dt className="font-normal mb-1 sm:mb-0 text-gray-500 dark:text-gray-400">
              Name
            </dt>
            <dd className="font-medium text-gray-900 dark:text-white sm:text-end">
              {paymentDetails.user.fullname}
            </dd>
          </dl>
          <dl className="sm:flex items-center justify-between gap-4">
            <dt className="font-normal mb-1 sm:mb-0 text-gray-500 dark:text-gray-400">
              Email
            </dt>
            <dd className="font-medium text-gray-900 dark:text-white sm:text-end">
              {paymentDetails.user.email}
            </dd>
          </dl>
        </div>
        <div className="flex items-center space-x-4">
          <Link
            to="/"
            className="text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-primary-600 dark:hover:bg-primary-700 focus:outline-none dark:focus:ring-primary-800"
          >
            Track your order
          </Link>
          <Link
            to="/recipes"
            className="py-2.5 px-5 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-primary-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
          >
            Return to home
          </Link>
        </div>
      </div>
    </section>
  );
};

export default PaymentConfirmation;
