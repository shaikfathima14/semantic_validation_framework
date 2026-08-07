import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="w-full fixed top-0 left-0 z-50 bg-white/70 backdrop-blur-lg border-b border-blue-100">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-8 py-4">

        <Link
          to="/"
          className="text-2xl font-heading font-bold text-primary"
        >
          SemanticAI
        </Link>

        <div className="hidden md:flex items-center gap-8 text-gray-700 font-medium">
          <a href="#">Home</a>
          <a href="#">Services</a>
          <a href="#">About</a>
          <a href="#">Contact</a>
        </div>

        <div className="flex gap-3">
          <button className="px-5 py-2 rounded-full bg-white text-primary border border-primary hover:bg-blue-50 transition">
            Login
          </button>

          <button className="px-5 py-2 rounded-full bg-primary text-white hover:opacity-90 transition">
            Register
          </button>
        </div>

      </div>
    </nav>
  );
}

export default Navbar;