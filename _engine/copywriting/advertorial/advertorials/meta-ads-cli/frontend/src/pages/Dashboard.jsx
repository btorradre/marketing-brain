import { useState, useEffect } from 'react';
import {
  Megaphone,
  Target,
  Image,
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  RefreshCw,
} from 'lucide-react';
import { api } from '../api/client';
import StatusBadge from '../components/StatusBadge';

export default function Dashboard({ addToast }) {
  const [campaigns, setCampaigns] = useState([]);
  const [adsets, setAdsets] = useState([]);
  const [ads, setAds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    setLoading(true);
    try {
      const [campRes, adsetRes, adRes] = await Promise.all([
        api.listCampaigns({ limit: 10 }),
        api.listAdSets({ limit: 10 }),
        api.listAds({ limit: 10 }),
      ]);
      setCampaigns(campRes.campaigns || []);
      setAdsets(adsetRes.adsets || []);
      setAds(adRes.ads || []);
    } catch (err) {
      addToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  }

  const activeCampaigns = campaigns.filter(c => c.status === 'ACTIVE').length;
  const activeAdsets = adsets.filter(a => a.status === 'ACTIVE').length;
  const activeAds = ads.filter(a => a.status === 'ACTIVE').length;

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Dashboard</h2>
          <p>Overview of your Meta ad account</p>
        </div>
        <button className="btn btn-secondary" onClick={loadData} disabled={loading}>
          <RefreshCw size={14} className={loading ? 'spin' : ''} />
          Refresh
        </button>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="label">
            <Megaphone size={14} />
            Total Campaigns
          </div>
          <div className="value">{campaigns.length}</div>
          <div className="change positive">
            <ArrowUpRight size={12} /> {activeCampaigns} active
          </div>
        </div>

        <div className="stat-card">
          <div className="label">
            <Target size={14} />
            Total Ad Sets
          </div>
          <div className="value">{adsets.length}</div>
          <div className="change positive">
            <ArrowUpRight size={12} /> {activeAdsets} active
          </div>
        </div>

        <div className="stat-card">
          <div className="label">
            <Image size={14} />
            Total Ads
          </div>
          <div className="value">{ads.length}</div>
          <div className="change positive">
            <ArrowUpRight size={12} /> {activeAds} active
          </div>
        </div>

        <div className="stat-card">
          <div className="label">
            <Activity size={14} />
            API Status
          </div>
          <div className="value" style={{ fontSize: 18, color: 'var(--success)' }}>
            Connected
          </div>
          <div className="change" style={{ color: 'var(--text-muted)' }}>
            v21.0
          </div>
        </div>
      </div>

      {/* Recent Campaigns Table */}
      <div className="card">
        <div className="card-header">
          <h3>Recent Campaigns</h3>
          <span className="text-xs text-muted">{campaigns.length} total</span>
        </div>
        <div className="table-container">
          {campaigns.length === 0 ? (
            <div className="empty-state">
              <Megaphone size={40} />
              <h3>No campaigns yet</h3>
              <p>Create your first campaign to get started</p>
            </div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Campaign</th>
                  <th>Objective</th>
                  <th>Status</th>
                  <th>Budget</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {campaigns.map(camp => (
                  <tr key={camp.id}>
                    <td>
                      <div>{camp.name}</div>
                      <div className="text-xs text-muted font-mono">{camp.id}</div>
                    </td>
                    <td className="text-xs">{camp.objective}</td>
                    <td><StatusBadge status={camp.status} /></td>
                    <td>
                      {camp.daily_budget
                        ? `$${(camp.daily_budget / 100).toFixed(2)}/day`
                        : camp.lifetime_budget
                        ? `$${(camp.lifetime_budget / 100).toFixed(2)} lifetime`
                        : 'CBO'
                      }
                    </td>
                    <td className="text-xs text-muted">
                      {camp.created ? new Date(camp.created).toLocaleDateString() : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
