import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Megaphone,
  Target,
  Image,
  Rocket,
  Settings,
  Zap,
  LogOut,
} from 'lucide-react';
import TokenManager from './TokenManager';
import { useAuth } from '../contexts/AuthContext';

const navItems = [
  { section: 'Overview' },
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },

  { section: 'Manage' },
  { path: '/campaigns', label: 'Campaigns', icon: Megaphone },
  { path: '/adsets', label: 'Ad Sets', icon: Target },
  { path: '/ads', label: 'Ads', icon: Image },

  { section: 'Launch' },
  { path: '/bulk', label: 'Bulk Launch', icon: Rocket },

  { section: 'System' },
  { path: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar({ connected, addToast, onTokenRefreshed }) {
  const { user, signOut } = useAuth();

  const handleLogout = async () => {
    await signOut();
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h1>
          <Zap size={20} />
          <span>Velocity Ads</span>
        </h1>
        <p>Campaign Manager</p>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item, i) => {
          if (item.section) {
            return (
              <div key={i} className="sidebar-section">
                {item.section}
              </div>
            );
          }
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `nav-item ${isActive ? 'active' : ''}`
              }
            >
              <Icon size={18} />
              {item.label}
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <TokenManager addToast={addToast} onTokenRefreshed={onTokenRefreshed} />

        {/* User info + logout */}
        {user && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '8px 12px',
            borderTop: '1px solid var(--border)',
            marginTop: 4,
          }}>
            <span style={{
              flex: 1,
              fontSize: 11,
              color: 'var(--text-muted)',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
            }}>
              {user.email}
            </span>
            <button
              onClick={handleLogout}
              title="Sign out"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 4,
                background: 'none',
                border: 'none',
                color: 'var(--text-muted)',
                cursor: 'pointer',
                padding: '4px 6px',
                borderRadius: 'var(--radius-sm)',
                fontSize: 11,
                transition: 'color 0.15s, background 0.15s',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.color = 'var(--error)';
                e.currentTarget.style.background = 'var(--error-subtle)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.color = 'var(--text-muted)';
                e.currentTarget.style.background = 'none';
              }}
            >
              <LogOut size={14} />
            </button>
          </div>
        )}
      </div>
    </aside>
  );
}
