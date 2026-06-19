import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("token");
  const isDashboard = location.pathname === "/dashboard";

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <nav className="navbar" id="main-navbar">
      <Link to={isLoggedIn ? "/dashboard" : "/"} className="navbar-brand" id="navbar-brand">
        <div className="navbar-logo" id="navbar-logo">
          <svg
            width="32"
            height="32"
            viewBox="0 0 32 32"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <rect width="32" height="32" rx="8" fill="url(#logoGrad)" />
            <path
              d="M12 10L7 16L12 22"
              stroke="white"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M20 10L25 16L20 22"
              stroke="white"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M17 9L15 23"
              stroke="rgba(255,255,255,0.6)"
              strokeWidth="2"
              strokeLinecap="round"
            />
            <defs>
              <linearGradient
                id="logoGrad"
                x1="0"
                y1="0"
                x2="32"
                y2="32"
                gradientUnits="userSpaceOnUse"
              >
                <stop stopColor="#6366f1" />
                <stop offset="1" stopColor="#8b5cf6" />
              </linearGradient>
            </defs>
          </svg>
        </div>
        <span className="navbar-title">DSA Tracker</span>
      </Link>

      <div className="navbar-links" id="navbar-links">
        {isDashboard && isLoggedIn ? (
          <button onClick={handleLogout} className="nav-logout-btn" id="nav-logout">
            Logout
          </button>
        ) : (
          !isLoggedIn && (
            <>
              <Link
                to="/"
                className={`nav-link ${location.pathname === "/" ? "active" : ""}`}
                id="nav-login"
              >
                Login
              </Link>
              <Link
                to="/register"
                className={`nav-link nav-link-register ${location.pathname === "/register" ? "active" : ""}`}
                id="nav-register"
              >
                Register
              </Link>
            </>
          )
        )}
      </div>
    </nav>
  );
}

export default Navbar;
