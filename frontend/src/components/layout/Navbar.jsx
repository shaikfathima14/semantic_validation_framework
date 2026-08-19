import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const [profileOpen, setProfileOpen] = useState(false);
  const navigate = useNavigate();

  const isLoggedIn =
  localStorage.getItem("semanticAILoggedIn") === "true";

  const user = JSON.parse(
    localStorage.getItem("semanticAIUser") || "null"
  );

  const userName = user?.name || "Citizen";
  const userEmail = user?.email || "No email";

  const handleLogout = () => {
    localStorage.removeItem("semanticAILoggedIn");
    localStorage.removeItem("semanticAIUserName");
    

    setProfileOpen(false);
    navigate("/");
  };

  return (
    <nav className="w-full fixed top-0 left-0 z-50 bg-white/80 backdrop-blur-lg border-b border-blue-100">

      <div className="max-w-7xl mx-auto flex items-center justify-between px-8 py-4">

        {/* LOGO */}

        <Link
          to="/"
          className="text-2xl font-heading font-bold text-primary"
        >
          SemanticAI
        </Link>


        {/* NAVIGATION */}

        <div className="hidden md:flex items-center gap-8 text-gray-700 font-medium">

          <Link
            to="/"
            className="hover:text-primary transition"
          >
            Home
          </Link>

          <Link
            to="/dashboard"
            className="hover:text-primary transition"
          >
            Services
          </Link>

          <a
            href="#about"
            className="hover:text-primary transition"
          >
            About
          </a>

          <a
            href="#contact"
            className="hover:text-primary transition"
          >
            Contact
          </a>

        </div>


        {/* RIGHT SIDE */}

        <div className="flex items-center gap-4">

          {!isLoggedIn ? (

            <>
              <Link
                to="/login"
                className="px-5 py-2 rounded-full bg-white text-primary border border-primary hover:bg-blue-50 transition"
              >
                Login
              </Link>

              <Link
                to="/register"
                className="px-5 py-2 rounded-full bg-primary text-white hover:opacity-90 transition"
              >
                Register
              </Link>
            </>

          ) : (

            /* PROFILE */

            <div className="relative">

              {/* PROFILE BUTTON */}

              <button
                onClick={() => setProfileOpen(!profileOpen)}
                className="flex items-center gap-3 rounded-full hover:bg-blue-50 px-2 py-1.5 transition"
              >

                {/* AVATAR */}

                <div className="w-11 h-11 rounded-full bg-primary text-white flex items-center justify-center font-bold text-lg shadow-sm">
                  {userName.charAt(0).toUpperCase()}
                </div>

                {/* ARROW */}

                <svg
                  className={`w-4 h-4 text-gray-500 transition-transform ${
                    profileOpen ? "rotate-180" : ""
                  }`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>

              </button>


              {/* DROPDOWN */}

              {profileOpen && (

                <div className="absolute right-0 mt-3 w-72 bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">

                  {/* USER HEADER */}

                  <div className="p-5 bg-blue-50">

                    <div className="flex items-center gap-3">

                      <div className="w-12 h-12 rounded-full bg-primary text-white flex items-center justify-center font-bold text-lg">
                        {userName.charAt(0).toUpperCase()}
                      </div>

                      <div className="min-w-0">

                        <p className="font-bold text-gray-800 truncate">
                          {userName}
                        </p>

                        <p className="text-sm text-gray-500 truncate">
                          {userEmail}
                        </p>

                      </div>

                    </div>

                    <div className="flex items-center gap-2 mt-3">

                      <span className="w-2 h-2 rounded-full bg-green-500"></span>

                      <span className="text-xs text-green-600 font-medium">
                        Logged in
                      </span>

                    </div>

                  </div>


                  {/* MENU */}

                  <div className="p-2">

                    <button
                      onClick={() => {
                        setProfileOpen(false);
                        navigate("/dashboard");
                      }}
                      className="w-full text-left px-4 py-3 rounded-xl hover:bg-blue-50 text-gray-700 transition"
                    >
                      <span className="font-medium">
                        Dashboard
                      </span>
                    </button>


                    <button
                      onClick={() => {
                        setProfileOpen(false);
                        alert(
                          `Name: ${userName}\nEmail: ${userEmail}`
                        );
                      }}
                      className="w-full text-left px-4 py-3 rounded-xl hover:bg-blue-50 text-gray-700 transition"
                    >
                      <span className="font-medium">
                        My Profile
                      </span>
                    </button>


                    <div className="border-t border-gray-100 my-2"></div>


                    <button
                      onClick={handleLogout}
                      className="w-full text-left px-4 py-3 rounded-xl hover:bg-red-50 text-red-500 transition font-medium"
                    >
                      Logout
                    </button>

                  </div>

                </div>

              )}

            </div>

          )}

        </div>

      </div>

    </nav>
  );
}

export default Navbar;