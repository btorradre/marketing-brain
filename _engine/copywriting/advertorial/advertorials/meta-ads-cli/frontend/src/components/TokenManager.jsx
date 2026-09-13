import { useState, useEffect, useCallback } from 'react';
import { Key, RefreshCw, X, CheckCircle, AlertTriangle, XCircle, Loader, LogIn } from 'lucide-react';
import { api } from '../api/client';

export default function TokenManager({ addToast, onTokenRefreshed }) {
  const [status, setStatus] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [shortToken, setShortToken] = useState('');
  const [exchanging, setExchanging] = useState(false);
  const [checking, setChecking] = useState(true);
  const [connecting, setConnecting] = useState(false);

  const checkStatus = async () => {
    setChecking(true);
    try {
      const result = await api.getTokenStatus();
      setStatus(result);
    } catch {
      setStatus({ valid: false, error: 'No Meta account connected' });
    }
    setChecking(false);
  };

  useEffect(() => {
    checkStatus();
  }, []);

  // Listen for OAuth callback message from popup window
  const handleOAuthMessage = useCallback(async (event) => {
    if (event.data?.type === 'META_TOKEN_REFRESHED') {
      setConnecting(false);
      addToast(`Connected! Token valid for ~${event.data.days} days`, 'success');
      await checkStatus();
      onTokenRefreshed?.();
      setShowModal(false);
    }
  }, [addToast, onTokenRefreshed]);

  useEffect(() => {
    window.addEventListener('message', handleOAuthMessage);
    return () => window.removeEventListener('message', handleOAuthMessage);
  }, [handleOAuthMessage]);

  const handleOAuthConnect = async () => {
    setConnecting(true);
    try {
      const result = await api.getOAuthUrl();
      // Open Facebook OAuth in a popup
      const w = 600, h = 700;
      const left = window.screenX + (window.outerWidth - w) / 2;
      const top = window.screenY + (window.outerHeight - h) / 2;
      const popup = window.open(
        result.url,
        'meta_oauth',
        `width=${w},height=${h},left=${left},top=${top},toolbar=no,menubar=no`
      );

      // Poll for popup close (in case user closes without completing)
      const pollTimer = setInterval(() => {
        if (popup?.closed) {
          clearInterval(pollTimer);
          setConnecting(false);
          checkStatus();
        }
      }, 1000);
    } catch (e) {
      addToast(e.message || 'Failed to start OAuth flow', 'error');
      setConnecting(false);
    }
  };

  const handleExchange = async () => {
    if (!shortToken.trim()) return;
    setExchanging(true);
    try {
      const result = await api.exchangeToken(shortToken.trim());
      addToast(result.message || 'Token exchanged successfully!', 'success');
      setShortToken('');
      setShowModal(false);
      await checkStatus();
      onTokenRefreshed?.();
    } catch (e) {
      addToast(e.message || 'Token exchange failed', 'error');
    }
    setExchanging(false);
  };

  // Determine status indicator
  let statusColor = 'var(--text-muted)';
  let statusIcon = <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} />;
  let statusText = 'Checking...';

  if (!checking && status) {
    if (!status.valid) {
      statusColor = 'var(--error)';
      statusIcon = <XCircle size={14} />;
      statusText = status.error?.includes('No Meta') ? 'Not Connected' : 'Token Expired';
    } else if (status.expires_in_days !== null && status.expires_in_days <= 7) {
      statusColor = 'var(--warning)';
      statusIcon = <AlertTriangle size={14} />;
      statusText = `Expires in ${status.expires_in_days}d`;
    } else if (status.valid) {
      statusColor = 'var(--success)';
      statusIcon = <CheckCircle size={14} />;
      statusText = status.expires_in_days !== null ? `Valid (${status.expires_in_days}d)` : 'Connected';
    }
  }

  return (
    <>
      {/* Inline status badge */}
      <div
        onClick={() => setShowModal(true)}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '8px 12px',
          borderRadius: 'var(--radius-sm)',
          cursor: 'pointer',
          color: statusColor,
          fontSize: 12,
          fontWeight: 500,
          transition: 'background 0.15s',
          background: 'transparent',
        }}
        onMouseEnter={(e) => e.currentTarget.style.background = 'var(--bg-card-hover)'}
        onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
        title="Click to manage Meta connection"
      >
        {statusIcon}
        <span>{statusText}</span>
        <Key size={12} style={{ marginLeft: 'auto', opacity: 0.5 }} />
      </div>

      {/* Modal */}
      {showModal && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 9999,
          }}
          onClick={(e) => e.target === e.currentTarget && setShowModal(false)}
        >
          <div
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius-lg)',
              padding: 28,
              width: '100%',
              maxWidth: 520,
              boxShadow: 'var(--shadow-lg)',
            }}
          >
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 16, fontWeight: 600 }}>
                <Key size={18} />
                Meta Connection
              </h3>
              <button
                onClick={() => setShowModal(false)}
                style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', padding: 4 }}
              >
                <X size={18} />
              </button>
            </div>

            {/* Current Status */}
            <div
              style={{
                padding: 14,
                borderRadius: 'var(--radius-md)',
                background: !status?.valid ? 'var(--error-subtle)' : status?.expires_in_days <= 7 ? 'var(--warning-subtle)' : 'var(--success-subtle)',
                border: `1px solid ${!status?.valid ? 'var(--error)' : status?.expires_in_days <= 7 ? 'var(--warning)' : 'var(--success)'}33`,
                marginBottom: 20,
                fontSize: 13,
              }}
            >
              <div style={{ fontWeight: 600, marginBottom: 4, color: statusColor }}>
                {statusIcon} {' '} {statusText}
              </div>
              {status?.error && (
                <div style={{ color: 'var(--text-secondary)', fontSize: 12 }}>{status.error}</div>
              )}
              {status?.valid && status?.expires_at && (
                <div style={{ color: 'var(--text-secondary)', fontSize: 12 }}>
                  Expires: {new Date(status.expires_at).toLocaleDateString()} ({status.expires_in_days} days remaining)
                </div>
              )}
              {status?.meta_user_name && (
                <div style={{ color: 'var(--text-secondary)', fontSize: 12, marginTop: 4 }}>
                  Meta User: {status.meta_user_name}
                </div>
              )}
            </div>

            {/* ── Connect with Facebook (OAuth) ── */}
            <button
              onClick={handleOAuthConnect}
              disabled={connecting}
              style={{
                width: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 10,
                padding: '12px 16px',
                background: connecting ? 'var(--bg-input)' : '#1877F2',
                color: connecting ? 'var(--text-muted)' : '#fff',
                border: 'none',
                borderRadius: 'var(--radius-sm)',
                cursor: connecting ? 'not-allowed' : 'pointer',
                fontSize: 14,
                fontWeight: 600,
                marginBottom: 20,
                transition: 'opacity 0.15s',
              }}
              onMouseEnter={(e) => { if (!connecting) e.currentTarget.style.opacity = '0.9'; }}
              onMouseLeave={(e) => { e.currentTarget.style.opacity = '1'; }}
            >
              {connecting ? (
                <><Loader size={16} style={{ animation: 'spin 1s linear infinite' }} /> Connecting...</>
              ) : (
                <><LogIn size={16} /> {status?.valid ? 'Reconnect with Facebook' : 'Connect with Facebook'}</>
              )}
            </button>

            {/* Divider */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
              <div style={{ flex: 1, height: 1, background: 'var(--border)' }} />
              <span style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: 1 }}>or paste manually</span>
              <div style={{ flex: 1, height: 1, background: 'var(--border)' }} />
            </div>

            {/* Manual Exchange Form */}
            <div style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', fontSize: 12, fontWeight: 500, marginBottom: 6, color: 'var(--text-muted)' }}>
                Token from{' '}
                <a
                  href="https://developers.facebook.com/tools/explorer/"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: 'var(--accent)' }}
                >
                  Graph API Explorer
                </a>
              </label>
              <textarea
                value={shortToken}
                onChange={(e) => setShortToken(e.target.value)}
                placeholder="EAA..."
                rows={2}
                style={{
                  width: '100%',
                  background: 'var(--bg-input)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '8px 10px',
                  color: 'var(--text-primary)',
                  fontSize: 11,
                  fontFamily: 'monospace',
                  resize: 'vertical',
                  outline: 'none',
                }}
                onFocus={(e) => e.target.style.borderColor = 'var(--border-focus)'}
                onBlur={(e) => e.target.style.borderColor = 'var(--border)'}
              />
            </div>

            {/* Manual Exchange Actions */}
            <div style={{ display: 'flex', gap: 10 }}>
              <button
                onClick={handleExchange}
                disabled={!shortToken.trim() || exchanging}
                style={{
                  flex: 1,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 8,
                  padding: '8px 14px',
                  background: shortToken.trim() && !exchanging ? 'var(--accent)' : 'var(--bg-input)',
                  color: shortToken.trim() && !exchanging ? '#fff' : 'var(--text-muted)',
                  border: 'none',
                  borderRadius: 'var(--radius-sm)',
                  cursor: shortToken.trim() && !exchanging ? 'pointer' : 'not-allowed',
                  fontSize: 12,
                  fontWeight: 600,
                }}
              >
                {exchanging ? (
                  <><Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> Exchanging...</>
                ) : (
                  <><RefreshCw size={14} /> Exchange for 60-Day Token</>
                )}
              </button>

              <button
                onClick={checkStatus}
                disabled={checking}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6,
                  padding: '8px 12px',
                  background: 'var(--bg-input)',
                  color: 'var(--text-secondary)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius-sm)',
                  cursor: checking ? 'not-allowed' : 'pointer',
                  fontSize: 12,
                }}
                title="Re-check token status"
              >
                <RefreshCw size={14} style={checking ? { animation: 'spin 1s linear infinite' } : {}} />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
