import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function RegisterPage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });

    setError("");
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (
      !formData.name ||
      !formData.email ||
      !formData.password ||
      !formData.confirmPassword
    ) {
      setError("Please fill in all fields.");
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must contain at least 6 characters.");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    // Temporary frontend registration
    localStorage.setItem(
      "semanticAIUser",
      JSON.stringify({
        name: formData.name,
        email: formData.email,
        password: formData.password,
      })
    );

    alert("Registration successful!");

    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6 py-12">

      <div className="w-full max-w-md">

        {/* Logo */}

        <div className="text-center mb-8">

          <Link
            to="/"
            className="text-3xl font-heading font-bold text-primary"
          >
            SemanticAI
          </Link>

          <h1 className="text-3xl font-bold text-gray-800 mt-6">
            Create your account
          </h1>

          <p className="text-gray-500 mt-2">
            Join SemanticAI and validate your documents smarter.
          </p>

        </div>

        {/* Register Card */}

        <div className="bg-white rounded-3xl shadow-soft p-8">

          <form onSubmit={handleSubmit}>

            {/* Name */}

            <div className="mb-5">

              <label className="block font-medium text-gray-700 mb-2">
                Full Name
              </label>

              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Enter your full name"
                className="w-full border border-gray-200 rounded-xl px-4 py-3 outline-none focus:border-primary focus:ring-2 focus:ring-blue-100"
              />

            </div>

            {/* Email */}

            <div className="mb-5">

              <label className="block font-medium text-gray-700 mb-2">
                Email Address
              </label>

              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email"
                className="w-full border border-gray-200 rounded-xl px-4 py-3 outline-none focus:border-primary focus:ring-2 focus:ring-blue-100"
              />

            </div>

            {/* Password */}

            <div className="mb-5">

              <label className="block font-medium text-gray-700 mb-2">
                Password
              </label>

              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Create a password"
                className="w-full border border-gray-200 rounded-xl px-4 py-3 outline-none focus:border-primary focus:ring-2 focus:ring-blue-100"
              />

            </div>

            {/* Confirm Password */}

            <div className="mb-5">

              <label className="block font-medium text-gray-700 mb-2">
                Confirm Password
              </label>

              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="Confirm your password"
                className="w-full border border-gray-200 rounded-xl px-4 py-3 outline-none focus:border-primary focus:ring-2 focus:ring-blue-100"
              />

            </div>

            {/* Error */}

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 rounded-xl px-4 py-3 mb-5 text-sm">
                {error}
              </div>
            )}

            {/* Register Button */}

            <button
              type="submit"
              className="w-full bg-primary text-white py-3 rounded-xl font-semibold hover:opacity-90 transition"
            >
              Create Account
            </button>

          </form>

          {/* Login */}

          <p className="text-center text-gray-500 mt-6">

            Already have an account?{" "}

            <Link
              to="/login"
              className="text-primary font-semibold hover:underline"
            >
              Login
            </Link>

          </p>

          {/* Home */}

          <div className="text-center mt-4">

            <Link
              to="/"
              className="text-sm text-gray-500 hover:text-primary"
            >
              ← Back to Home
            </Link>

          </div>

        </div>

      </div>

    </div>
  );
}

export default RegisterPage;