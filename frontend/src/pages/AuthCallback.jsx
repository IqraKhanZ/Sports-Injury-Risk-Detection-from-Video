import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Loader2, ShieldAlert } from 'lucide-react';
import './AuthCallback.css';

export default function AuthCallback({ login }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [processed, setProcessed] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (processed) return;

    const params = new URLSearchParams(location.search);
    const token = params.get('token');
    const role = params.get('role');
    const fullname = params.get('fullname');
    const email = params.get('email');
    const err = params.get('error');

    if (err) {
      setProcessed(true);
      setError(decodeURIComponent(err));
      setTimeout(() => navigate('/'), 4000);
      return;
    }

    if (token && email) {
      setProcessed(true);
      
      // Normalize role
      let normalizedRole = 'Athlete';
      if (role) {
        const r = decodeURIComponent(role).trim().toLowerCase();
        if (r === 'coach') normalizedRole = 'Coach';
        else if (r === 'physiotherapist' || r === 'physio') normalizedRole = 'Physiotherapist';
        else if (r.includes('scientist')) normalizedRole = 'Sports Scientist';
        else if (r.includes('admin')) normalizedRole = 'Administrator';
        else normalizedRole = 'Athlete';
      }

      const decodedEmail = decodeURIComponent(email).toLowerCase();
      const decodedName = fullname ? decodeURIComponent(fullname) : decodedEmail.split('@')[0];

      const authData = {
        access_token: token,
        token_type: 'bearer',
        role: normalizedRole,
        fullname: decodedName,
        email: decodedEmail,
      };
      
      login(authData);
      
      setTimeout(() => {
        navigate('/dashboard', { replace: true });
      }, 50);
    } else if (params.toString()) {
      setProcessed(true);
      setError('Invalid authorization callback data.');
      setTimeout(() => navigate('/'), 3000);
    }
  }, [location, login, navigate, processed]);

  return (
    <div className="callback-container">
      <div className="callback-card animate-scale-in">
        {error ? (
          <div className="callback-error-content">
            <ShieldAlert size={48} className="error-icon" />
            <h2>Authentication Failed</h2>
            <p className="error-msg">{error}</p>
            <p className="redirect-text">Redirecting you to the home page...</p>
          </div>
        ) : (
          <div className="callback-loading-content">
            <Loader2 size={48} className="spinner" />
            <h2>Completing Sign In</h2>
            <p>Syncing your profile credentials, please wait...</p>
          </div>
        )}
      </div>
    </div>
  );
}
