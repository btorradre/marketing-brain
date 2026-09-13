import { useState, useEffect } from 'react';
import { Settings as SettingsIcon, CheckCircle, AlertCircle, RefreshCw, ChevronDown, Loader } from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../contexts/AuthContext';

export default function Settings({ addToast, onTokenRefreshed }) {
  const { user } = useAuth();
  const [config, setConfig] = useState(null);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [accounts, setAccounts] = useState([]);
  const [loadingAccounts, setLoadingAccounts] = useState(false);
  const [selectingAccount, setSelectingAccount] = useState(false);

  useEffect(() => { loadConfig(); loadAccounts(); }, []);

  async function loadConfig() {
    setLoading(true);
    try {
      const [configRes, healthRes] = await Promise.all([
        api.getConfig().catch(() => null),
        api.health().catch(() => null),
      ]);
      setConfig(configRes);
      setHealth(healthRes);
    } catch (err) {
      addToast('Failed to load config', 'error');
    } finally {
      setLoading(false);
    }
  }

  async function loadAccounts() {
    setLoadingAccounts(true);
    try {
      const result = await api.getAccounts();
      setAccounts(result.accounts || []);
    } catch {
      // No accounts yet — that's fine
      setAccounts([]);
    }
    setLoadingAccounts(false);
  }

  async function handleSelectAccount(accountId) {
    setSelectingAccount(true);
    try {
      await api.selectAccount(accountId);
      addToast('Ad account selected', 'success');
      await loadAccounts();
      await loadConfig();
      onTokenRefreshed?.();
    } catch (e) {
      addToast(e.message || 'Failed to select account', 'error');
    }
    setSelectingAccount(false);
  }

  const selectedAccount = accounts.find(a => a.is_selected);

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Settings</h2>
          <p>Account and connection settings</p>
        </div>
        <button className="btn btn-secondary" onClick={() => { loadConfig(); loadAccounts(); }}>
          <RefreshCw size={14} />
          Refresh
        </button>
      </div>

      <div style={{ display: 'grid', gap: 20, maxWidth: 700 }}>
        {/* User Info */}
        <div className="card">
          <div className="card-header">
            <h3>Account</h3>
          </div>
          <div style={{ display: 'grid', gap: 12 }}>
            <div className="flex justify-between items-center" style={{ padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
              <span className="text-sm text-muted">Email</span>
              <span className="text-sm">{user?.email || '—'}</span>
            </div>
            <div className="flex justify-between items-center" style={{ padding: '8px 0' }}>
              <span className="text-sm text-muted">User ID</span>
              <span className="text-sm font-mono" style={{ fontSize: 11 }}>{user?.id?.substring(0, 8) || '—'}...</span>
            </div>
          </div>
        </div>

        {/* Connection Status */}
        <div className="card">
          <div className="card-header">
            <h3>Meta Connection</h3>
            {config?.connected ? (
              <span style={{ color: 'var(--success)', fontSize: 13, display: 'flex', alignItems: 'center', gap: 6 }}>
                <CheckCircle size={14} /> Connected
              </span>
            ) : (
              <span style={{ color: 'var(--error)', fontSize: 13, display: 'flex', alignItems: 'center', gap: 6 }}>
                <AlertCircle size={14} /> Not Connected
              </span>
            )}
          </div>

          <div style={{ display: 'grid', gap: 12 }}>
            <div className="flex justify-between items-center" style={{ padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
              <span className="text-sm text-muted">Backend API</span>
              <span className="text-sm">{health ? 'Running' : 'Not running'}</span>
            </div>
            <div className="flex justify-between items-center" style={{ padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
              <span className="text-sm text-muted">Meta API Connected</span>
              <span className="text-sm">{config?.connected ? 'Yes' : 'No'}</span>
            </div>
            <div className="flex justify-between items-center" style={{ padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
              <span className="text-sm text-muted">Ad Account</span>
              <span className="text-sm font-mono">{config?.ad_account_id || '—'}</span>
            </div>
            <div className="flex justify-between items-center" style={{ padding: '8px 0' }}>
              <span className="text-sm text-muted">API Version</span>
              <span className="text-sm font-mono">{config?.api_version || '—'}</span>
            </div>
          </div>
        </div>

        {/* Ad Account Selector */}
        {accounts.length > 0 && (
          <div className="card">
            <div className="card-header">
              <h3>Ad Account</h3>
              {selectedAccount && (
                <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                  Current: {selectedAccount.meta_account_name || selectedAccount.meta_account_id}
                </span>
              )}
            </div>

            <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 12 }}>
              Select which ad account to manage. All campaigns, ad sets, and ads will use this account.
            </p>

            <div style={{ display: 'grid', gap: 8 }}>
              {accounts.map(account => (
                <div
                  key={account.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-sm)',
                    border: `1px solid ${account.is_selected ? 'var(--accent)' : 'var(--border)'}`,
                    background: account.is_selected ? 'var(--accent-subtle)' : 'transparent',
                    cursor: selectingAccount ? 'not-allowed' : 'pointer',
                    transition: 'border-color 0.15s, background 0.15s',
                  }}
                  onClick={() => !selectingAccount && !account.is_selected && handleSelectAccount(account.meta_account_id)}
                >
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 500 }}>{account.meta_account_name || account.meta_account_id}</div>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)', fontFamily: 'monospace' }}>{account.meta_account_id}</div>
                  </div>
                  {account.is_selected ? (
                    <CheckCircle size={16} style={{ color: 'var(--accent)' }} />
                  ) : (
                    <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>Select</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* No accounts message */}
        {!loadingAccounts && accounts.length === 0 && config?.connected && (
          <div className="card" style={{ textAlign: 'center', padding: '32px 20px' }}>
            <AlertCircle size={24} style={{ color: 'var(--warning)', marginBottom: 8 }} />
            <p style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 4 }}>
              No ad accounts found
            </p>
            <p style={{ fontSize: 12, color: 'var(--text-muted)' }}>
              Your Meta account may not have any ad accounts. Create one in Meta Business Manager.
            </p>
          </div>
        )}

        {/* Not connected message */}
        {!loading && !config?.connected && (
          <div className="card" style={{ textAlign: 'center', padding: '32px 20px' }}>
            <AlertCircle size={24} style={{ color: 'var(--text-muted)', marginBottom: 8 }} />
            <p style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 4 }}>
              No Meta account connected
            </p>
            <p style={{ fontSize: 12, color: 'var(--text-muted)' }}>
              Click the connection status in the sidebar to connect your Meta account via Facebook.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
