import React, { useEffect, useState, useCallback } from "react";
import { useLocation, Link } from "react-router-dom";
import api from "@/api";
import toast, { Toaster } from "react-hot-toast";
import Spinner from "@/components/Spinner";

const PaymentConfirmation = () => {
  const location = useLocation();
  const [paymentDetails, setPaymentDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getQueryParams = useCallback((search) => {
    return new URLSearchParams(search);
  }, []);

  const verifyPayment = useCallback(async (reference) => {
    try {
      const response = await api.post("/payment/verify", { reference });
      setPaymentDetails(response.data.paymentDetails);
    } catch (error) {
      console.error("Payment verification failed:", error);
      setError("Payment verification failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const queryParams = getQueryParams(location.search);
    const reference = queryParams.get("reference");

    console.log("Extracted reference:", reference);

    if (!reference) {
      setError("Reference is required");
      setLoading(false);
      return;
    }

    verifyPayment(reference);
  }, [location.search, getQueryParams, verifyPayment]);

  useEffect(() => {
    if (error) {
      toast.error(error);
    }
  }, [error]);

  if (loading) {
    return <Spinner loading={loading} />;
  }

  if (!paymentDetails) {
    return (
      <div>
        <Toaster position="top-center" reverseOrder={false} />
        Payment verification failed. Please try again.
      </div>
    );
  }

  // Log payment details for debugging
  console.log(paymentDetails);

  const {
    paid_at,
    channel,
    amount,
    currency,
    status,
    card_type,
    last4,
    fees,
    reference,
  } = paymentDetails;
  const formattedPaidAt = paid_at
    ? new Date(paid_at).toLocaleDateString()
    : "N/A";
  const formattedAmount = amount ? (amount / 100).toFixed(2) : "N/A";
  const formattedFees = fees ? (fees / 100).toFixed(2) : "N/A";

  return (
    <>
      {" "}
      <Toaster position="top-center" reverseOrder={false} />
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
                {formattedPaidAt}
              </dd>
            </dl>
            <dl className="sm:flex items-center justify-between gap-4">
              <dt className="font-normal mb-1 sm:mb-0 text-gray-500 dark:text-gray-400">
                Payment Method
              </dt>
              <dd className="font-medium text-gray-900 dark:text-white sm:text-end">
                {channel}
              </dd>
            </dl>
            <dl className="sm:flex items-center justify-between gap-4">
              <dt className="font-normal mb-1 sm:mb-0 text-gray-500 dark:text-gray-400">
                Amount Paid
              </dt>
              <dd className="font-medium text-gray-900 dark:text-white sm:text-end">
                {formattedAmount} {currency}
              </dd>
            </dl>
            <dl className="sm:flex items-center justify-between gap-4">
              <dt className="font-normal mb-1 sm:mb-0 text-gray-500 dark:text-gray-400">
                Status
              </dt>
              <dd className="font-medium text-gray-900 dark:text-white sm:text-end">
                {status}
              </dd>
            </dl>
            <dl className="sm:flex items-center justify-between gap-4">
              <dt className="font-normal mb-1 sm:mb-0 text-gray-500 dark:text-gray-400">
                Card Type
              </dt>
              <dd className="font-medium text-gray-900 dark:text-white sm:text-end">
                {card_type} ending in {last4}
              </dd>
            </dl>
            <dl className="sm:flex items-center justify-between gap-4">
              <dt className="font-normal mb-1 sm:mb-0 text-gray-500 dark:text-gray-400">
                Fees
              </dt>
              <dd className="font-medium text-gray-900 dark:text-white sm:text-end">
                {formattedFees} {currency}
              </dd>
            </dl>
          </div>
          <div className="flex items-center space-x-4">
            <Link
              to="/recipes"
              className="py-2.5 px-5 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-primary-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
            >
              Return to home
            </Link>
          </div>
        </div>
      </section>
    </>
  );
};

export default PaymentConfirmation;
