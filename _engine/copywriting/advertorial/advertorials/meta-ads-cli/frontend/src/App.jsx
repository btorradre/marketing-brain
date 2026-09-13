import { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import ToastContainer from './components/Toast';
import Dashboard from './pages/Dashboard';
import Campaigns from './pages/Campaigns';
import AdSets from './pages/AdSets';
import Ads from './pages/Ads';
import BulkLaunch from './pages/BulkLaunch';
import Settings from './pages/Settings';
import Login from './pages/Login';
import { api } from './api/client';
import { useToast } from './hooks/useToast';
import { useAuth } from './contexts/AuthContext';
import { Loader } from 'lucide-react';

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'var(--bg-primary)',
      }}>
        <Loader size={24} style={{ animation: 'spin 1s linear infinite', color: 'var(--accent)' }} />
      </div>
    );
  }

  if (!user) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  const { toasts, addToast } = useToast();
  const { user, loading } = useAuth();
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    if (!user) return;
    api.getTokenStatus()
      .then((res) => setConnected(res.valid))
      .catch(() => setConnected(false));
  }, [user]);

  const handleTokenRefreshed = () => {
    api.getTokenStatus()
      .then((res) => setConnected(res.valid))
      .catch(() => setConnected(false));
  };

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'var(--bg-primary)',
      }}>
        <Loader size={24} style={{ animation: 'spin 1s linear infinite', color: 'var(--accent)' }} />
      </div>
    );
  }

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" replace /> : <Login />} />
      <Route path="*" element={
        <ProtectedRoute>
          <div className="app-layout">
            <Sidebar connected={connected} addToast={addToast} onTokenRefreshed={handleTokenRefreshed} />
            <main className="main-content">
              <Routes>
                <Route path="/" element={<Dashboard addToast={addToast} />} />
                <Route path="/campaigns" element={<Campaigns addToast={addToast} />} />
                <Route path="/adsets" element={<AdSets addToast={addToast} />} />
                <Route path="/ads" element={<Ads addToast={addToast} />} />
                <Route path="/bulk" element={<BulkLaunch addToast={addToast} />} />
                <Route path="/settings" element={<Settings addToast={addToast} onTokenRefreshed={handleTokenRefreshed} />} />
              </Routes>
            </main>
            <ToastContainer toasts={toasts} />
          </div>
        </ProtectedRoute>
      } />
    </Routes>
  );
}
