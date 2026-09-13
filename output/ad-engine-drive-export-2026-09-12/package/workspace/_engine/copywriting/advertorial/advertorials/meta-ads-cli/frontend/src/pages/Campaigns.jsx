import { useState, useEffect } from 'react';
import { Plus, Megaphone, RefreshCw, Search } from 'lucide-react';
import { api } from '../api/client';
import Modal from '../components/Modal';
import StatusBadge from '../components/StatusBadge';
import { OBJECTIVES } from '../config/objectiveRules';

const defaultForm = {
  name: '',
  objective: 'OUTCOME_TRAFFIC',
  status: 'PAUSED',
  daily_budget: '',
  buying_type: 'AUCTION',
  special_ad_categories: [],
};

export default function Campaigns({ addToast }) {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ ...defaultForm });
  const [submitting, setSubmitting] = useState(false);
  const [statusFilter, setStatusFilter] = useState('');
  const [search, setSearch] = useState('');

  useEffect(() => { loadCampaigns(); }, [statusFilter]);

  async function loadCampaigns() {
    setLoading(true);
    try {
      const params = {};
      if (statusFilter) params.status = statusFilter;
      const res = await api.listCampaigns(params);
      setCampaigns(res.campaigns || []);
    } catch (err) {
      addToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = { ...form };
      if (payload.daily_budget) {
        payload.daily_budget = parseInt(payload.daily_budget);
      } else {
        delete payload.daily_budget;
      }
      await api.createCampaign(payload);
      addToast('Campaign created successfully');
      setShowModal(false);
      setForm({ ...defaultForm });
      loadCampaigns();
    } catch (err) {
      addToast(err.message, 'error');
    } finally {
      setSubmitting(false);
    }
  }

  const filtered = campaigns.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Campaigns</h2>
          <p>Manage your advertising campaigns</p>
        </div>
        <div className="flex gap-2">
          <button className="btn btn-secondary" onClick={loadCampaigns}>
            <RefreshCw size={14} />
          </button>
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>
            <Plus size={14} />
            New Campaign
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-3 mb-4">
        <div style={{ position: 'relative', flex: 1, maxWidth: 300 }}>
          <Search size={14} style={{ position: 'absolute', left: 12, top: 11, color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search campaigns..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ paddingLeft: 34 }}
          />
        </div>
        <select
          value={statusFilter}
          onChange={e => setStatusFilter(e.target.value)}
          style={{ width: 150 }}
        >
          <option value="">All Statuses</option>
          <option value="ACTIVE">Active</option>
          <option value="PAUSED">Paused</option>
          <option value="ARCHIVED">Archived</option>
        </select>
      </div>

      {/* Table */}
      <div className="card">
        <div className="table-container">
          {filtered.length === 0 ? (
            <div className="empty-state">
              <Megaphone size={40} />
              <h3>No campaigns found</h3>
              <p>{campaigns.length === 0 ? 'Create your first campaign to get started' : 'Try adjusting your filters'}</p>
            </div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Campaign</th>
                  <th>Objective</th>
                  <th>Status</th>
                  <th>Budget</th>
                  <th>Buying Type</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map(camp => (
                  <tr key={camp.id}>
                    <td>
                      <div style={{ fontWeight: 500 }}>{camp.name}</div>
                      <div className="text-xs text-muted font-mono">{camp.id}</div>
                    </td>
                    <td>
                      <span className="text-xs">
                        {camp.objective?.replace('OUTCOME_', '')}
                      </span>
                    </td>
                    <td><StatusBadge status={camp.status} /></td>
                    <td>
                      {camp.daily_budget
                        ? `$${(camp.daily_budget / 100).toFixed(2)}/day`
                        : camp.lifetime_budget
                        ? `$${(camp.lifetime_budget / 100).toFixed(2)}`
                        : '—'
                      }
                    </td>
                    <td className="text-xs">{camp.buying_type || 'AUCTION'}</td>
                    <td className="text-xs text-muted">
                      {camp.created ? new Date(camp.created).toLocaleDateString() : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Create Campaign Modal */}
      {showModal && (
        <Modal
          title="Create Campaign"
          onClose={() => setShowModal(false)}
          footer={
            <>
              <button className="btn btn-secondary" onClick={() => setShowModal(false)}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={handleCreate} disabled={submitting}>
                {submitting ? 'Creating...' : 'Create Campaign'}
              </button>
            </>
          }
        >
          <form onSubmit={handleCreate}>
            <div className="form-group">
              <label>Campaign Name</label>
              <input
                type="text"
                value={form.name}
                onChange={e => setForm({ ...form, name: e.target.value })}
                placeholder="e.g. Summer Sale - Traffic"
                required
              />
            </div>

            <div className="form-grid">
              <div className="form-group">
                <label>Objective</label>
                <select
                  value={form.objective}
                  onChange={e => setForm({ ...form, objective: e.target.value })}
                >
                  {OBJECTIVES.map(o => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Status</label>
                <select
                  value={form.status}
                  onChange={e => setForm({ ...form, status: e.target.value })}
                >
                  <option value="PAUSED">Paused</option>
                  <option value="ACTIVE">Active</option>
                </select>
              </div>
            </div>

            <div className="form-grid">
              <div className="form-group">
                <label>Daily Budget (cents)</label>
                <input
                  type="number"
                  value={form.daily_budget}
                  onChange={e => setForm({ ...form, daily_budget: e.target.value })}
                  placeholder="e.g. 5000 = $50.00"
                />
                <div className="hint">
                  {form.daily_budget ? `= $${(form.daily_budget / 100).toFixed(2)}/day` : 'Leave empty for ad set level budgets'}
                </div>
              </div>

              <div className="form-group">
                <label>Buying Type</label>
                <select
                  value={form.buying_type}
                  onChange={e => setForm({ ...form, buying_type: e.target.value })}
                >
                  <option value="AUCTION">Auction</option>
                  <option value="RESERVED">Reserved</option>
                </select>
              </div>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
}
