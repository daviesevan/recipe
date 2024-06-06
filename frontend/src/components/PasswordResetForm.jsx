import { useState } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import api from "@/api";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

const PasswordResetForm = () => {
  const [step, setStep] = useState(1);
  const [email, setEmail] = useState("");
  const [resetCode, setResetCode] = useState("");
  const [loading, isLoading] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm();
  const navigate = useNavigate();

  const handlePrevStep = () => {
    setStep((prevStep) => prevStep - 1);
  };

  const handleNextStep = () => {
    setStep((prevStep) => prevStep + 1);
  };

  const onSubmitEmail = async (data) => {
    isLoading(true);
    try {
      await api.post("/auth/forgot-password", { email: data.email });
      setEmail(data.email);
      handleNextStep();
    } catch (error) {
      setError("email", { type: "manual", message: error.response.data.error });
    } finally {
      isLoading(false);
    }
  };

  const onSubmitCode = (data) => {
    isLoading(true);
    setResetCode(data.resetCode);
    isLoading(false);
    handleNextStep();
  };

  const onSubmitPassword = async (data) => {
    isLoading(true);
    try {
      await api.post("/auth/reset-password", {
        email,
        reset_code: resetCode,
        new_password: data.newPassword,
      });
      toast.success("Password reset successfully");
      setTimeout(() => {
        navigate("/login");
      }, 2000);
    } catch (error) {
      setError("newPassword", {
        type: "manual",
        message: error.response.data.error,
      });
    }
  };

  return (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      {step === 1 && (
        <>
          <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form onSubmit={handleSubmit(onSubmitEmail)}>
              <label className="block text-sm text-gray-500 dark:text-gray-300">
                  Email address
                </label>
                <Input
                  type="email"
                  className="mt-2 block w-full placeholder-gray-400/70 rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-gray-700 focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-40 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:focus:border-blue-300"
                  placeholder="Enter your email..."
                  {...register("email", { required: "Email is required" })}
                />
                {errors.email && (
                  <p className="mt-3 text-xs text-red-400">
                    {errors.email.message}
                  </p>
                )}
              <Button type="submit" className="mt-3">
                {loading ? "Loading..." : "Send Reset Code"}
              </Button>
            </form>
          </div>
        </>
      )}

      {step === 2 && (
        <>
          <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form onSubmit={handleSubmit(onSubmitCode)}>
              <div>
                <label className="block text-sm text-gray-500 dark:text-gray-300">
                  Reset Code (Check Email)
                </label>
                <Input
                  type="text"
                  className="mt-2 block w-full placeholder-gray-400/70 rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-gray-700 focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-40 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:focus:border-blue-300"
                  {...register("resetCode", {
                    required: "Reset code is required",
                  })}
                />
                {errors.resetCode && (
                  <p className="mt-3 text-xs text-red-400">
                    {errors.resetCode.message}
                  </p>
                )}
              </div>
              <div className="flex justify-between">
                <Button onClick={handlePrevStep} variant={"outline"} className="mt-3">
                  Back
                </Button>
                <Button type="submit" className="mt-3">
                  {loading ? "Loading..." : "Verify Code"}
                </Button>
              </div>
            </form>
          </div>
        </>
      )}

      {step === 3 && (
        <>
          <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form onSubmit={handleSubmit(onSubmitPassword)}>
              <div>
                <label className="block text-sm text-gray-500 dark:text-gray-300">
                  New Password
                </label>
                <Input
                  type="password"
                  className="mt-2 block w-full placeholder-gray-400/70 rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-gray-700 focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-40 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:focus:border-blue-300"
                  {...register("newPassword", {
                    required: "New password is required",
                  })}
                />
                {errors.newPassword && (
                  <p className="mt-3 text-xs text-red-400">
                    {errors.newPassword.message}
                  </p>
                )}
              </div>
              <div className="flex justify-between">
                <Button onClick={handlePrevStep} variant={"outline"} className="mt-3">
                  Back
                </Button>
                <Button type="submit" className="mt-3">
                  {loading ? "Loading..." : "Reset Password"}
                </Button>
              </div>
            </form>
          </div>
        </>
      )}
    </div>
  );
};

export default PasswordResetForm;