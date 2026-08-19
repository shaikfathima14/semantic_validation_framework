import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    setError("");

    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }

    const storedUser = localStorage.getItem("semanticAIUser");

    if (!storedUser) {
      setError("No account found. Please register first.");
      return;
    }

    const user = JSON.parse(storedUser);

    if (user.email !== email || user.password !== password) {
      setError("Invalid email or password.");
      return;
    }

    localStorage.setItem(
      "semanticAILoggedIn",
      "true"
    );

    localStorage.setItem(
      "semanticAIUserName",
      user.name
    );

    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6">

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
            Welcome back
          </h1>

          <p className="text-gray-500 mt-2">
            Login to continue to your dashboard.
          </p>

        </div>

        {/* Login Card */}

        <div className="bg-white rounded-3xl shadow-soft p-8">

          <form onSubmit={handleSubmit}>

            {/* Email */}

            <div className="mb-5">

              <label className="block font-medium text-gray-700 mb-2">
                Email Address
              </label>

              <input
                type="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  setError("");
                }}
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
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  setError("");
                }}
                placeholder="Enter your password"
                className="w-full border border-gray-200 rounded-xl px-4 py-3 outline-none focus:border-primary focus:ring-2 focus:ring-blue-100"
              />

            </div>

            {/* Error */}

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 rounded-xl px-4 py-3 mb-5 text-sm">
                {error}
              </div>
            )}

            {/* Login */}

            <button
              type="submit"
              className="w-full bg-primary text-white py-3 rounded-xl font-semibold hover:opacity-90 transition"
            >
              Login
            </button>

          </form>

          {/* Register */}

          <p className="text-center text-gray-500 mt-6">

            Don't have an account?{" "}

            <Link
              to="/register"
              className="text-primary font-semibold hover:underline"
            >
              Register
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

export default LoginPage;