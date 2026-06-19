import React, { useState } from "react";
import API from "../services/api";
import { Link } from "react-router-dom";
import "./Auth.css";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const response = await API.post("/users/forgot-password", { email: email.trim() });
      // Backend now tells us if the email was actually found
      if (response.data.email_found === false) {
        setError("No account found with this email address. Please check your email or register a new account.");
      } else {
        setSent(true);
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Something went wrong. Please try again later."
      );
    } finally {
      setLoading(false);
    }
  };

  if (sent) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <div className="success-icon">📧</div>
          <h2>Check Your Email</h2>
          <p className="auth-subtitle">
            We've sent a password reset link to <strong>{email}</strong>.
            Check your inbox (and spam folder). The link expires in 1 hour.
          </p>
          <p className="auth-footer">
            <Link to="/">Back to Login</Link>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="success-icon">🔐</div>
        <h2>Forgot Password</h2>
        <p className="auth-subtitle">
          Enter the email address associated with your account and we'll send you a link to reset your password.
        </p>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Email Address</label>
            <input
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              id="forgot-email-input"
            />
          </div>
          <button type="submit" disabled={loading} className="auth-btn" id="forgot-submit-btn">
            {loading ? "Sending..." : "Send Reset Link"}
          </button>
        </form>

        <p className="auth-footer">
          Remembered your password? <Link to="/">Login here</Link>
        </p>
      </div>
    </div>
  );
}

export default ForgotPassword;
