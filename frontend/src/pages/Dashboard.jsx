import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between font-sans">
      <header className="border-b border-slate-900 bg-slate-900/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <span className="font-bold text-xl tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
            Dashboard
          </span>
          <div className="flex items-center gap-4">
            <span className="text-sm text-slate-400">
              Logged in as: <strong className="text-slate-200">{user?.email}</strong> ({user?.role})
            </span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-xs font-semibold uppercase tracking-wider bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12 flex-grow flex flex-col justify-center items-center">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold mb-4">Welcome to Aegis Motion</h1>
          <p className="text-slate-400 max-w-md">
            This is your workspace. Your injury risk detection modules, video uploads, and history will be visible here.
          </p>
        </div>
      </main>

      <footer className="border-t border-slate-900 bg-slate-950/80 py-6 text-center text-xs text-slate-500">
        © 2026 Aegis Motion. All rights reserved.
      </footer>
    </div>
  );
}
