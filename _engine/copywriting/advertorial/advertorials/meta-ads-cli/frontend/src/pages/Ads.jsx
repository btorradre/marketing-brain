import { useState, useEffect } from 'react';
import { Plus, Image, RefreshCw, Search, ExternalLink, Loader } from 'lucide-react';
import { api } from '../api/client';
import Modal from '../components/Modal';
import StatusBadge from '../components/StatusBadge';

const CTA_TYPES = [
  'LEARN_MORE', 'SHOP_NOW', 'SIGN_UP', 'BOOK_TRAVEL', 'CONTACT_US',
  'DOWNLOAD', 'GET_OFFER', 'GET_QUOTE', 'SUBSCRIBE', 'WATCH_MORE',
];

const defaultForm = {
  name: '',
  adset_id: '',
  status: 'PAUSED',
  page_id: '',
  link: '',
  message: '',
  headline: '',
  description: '',
  call_to_action_type: 'LEARN_MORE',
  image_hash: '',
  creative_id: '',
};

export default function Ads({ addToast }) {
  const [ads, setAds] = useState([]);
  const [adsets, setAdsets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({ ...defaultForm });
  const [submitting, setSubmitting] = useState(false);
  const [adsetFilter, setAdsetFilter] = useState('');
  const [search, setSearch] = useState('');
  const [useExistingCreative, setUseExistingCreative] = useState(false);

  // ── Pages data (for dropdown) ──
  const [pages, setPages] = useState([]);
  const [pagesLoading, setPagesLoading] = useState(false);
  const [pagesFetched, setPagesFetched] = useState(false);

  async function loadPages() {
    if (pagesFetched) return;
    setPagesLoading(true);
    try {
      const res = await api.listPages();
      setPages(res.pages || []);
      setPagesFetched(true);
    } catch (err) {
      console.error('Failed to load pages:', err);
    } finally {
      setPagesLoading(false);
    }
  }

  useEffect(() => { loadData(); loadPages(); }, [adsetFilter]);

  async function loadData() {
    setLoading(true);
    try {
      const params = {};
      if (adsetFilter) params.adset_id = adsetFilter;
      const [adRes, adsetRes] = await Promise.all([
        api.listAds(params),
        api.listAdSets({}),
      ]);
      setAds(adRes.ads || []);
      setAdsets(adsetRes.adsets || []);
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
      const payload = {
        name: form.name,
        adset_id: form.adset_id,
        status: form.status,
      };

      if (useExistingCreative) {
        payload.creative_id = form.creative_id;
      } else {
        payload.page_id = form.page_id;
        payload.link = form.link;
        payload.message = form.message;
        payload.headline = form.headline;
        payload.description = form.description;
        payload.call_to_action_type = form.call_to_action_type;
        if (form.image_hash) payload.image_hash = form.image_hash;
      }

      await api.createAd(payload);
      addToast('Ad created successfully');
      setShowCreate(false);
      setForm({ ...defaultForm });
      loadData();
    } catch (err) {
      addToast(err.message, 'error');
    } finally {
      setSubmitting(false);
    }
  }

  const filtered = ads.filter(a =>
    a.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Ads</h2>
          <p>Manage ad creatives and copy</p>
        </div>
        <div className="flex gap-2">
          <button className="btn btn-secondary" onClick={loadData}>
            <RefreshCw size={14} />
          </button>
          <button className="btn btn-primary" onClick={() => setShowCreate(true)}>
            <Plus size={14} />
            New Ad
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-3 mb-4">
        <div style={{ position: 'relative', flex: 1, maxWidth: 300 }}>
          <Search size={14} style={{ position: 'absolute', left: 12, top: 11, color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search ads..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ paddingLeft: 34 }}
          />
        </div>
        <select
          value={adsetFilter}
          onChange={e => setAdsetFilter(e.target.value)}
          style={{ width: 250 }}
        >
          <option value="">All Ad Sets</option>
          {adsets.map(a => (
            <option key={a.id} value={a.id}>{a.name} ({a.id})</option>
          ))}
        </select>
      </div>

      {/* Table */}
      <div className="card">
        <div className="table-container">
          {filtered.length === 0 ? (
            <div className="empty-state">
              <Image size={40} />
              <h3>No ads found</h3>
              <p>Create an ad with your creative and copy</p>
            </div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Ad</th>
                  <th>Ad Set</th>
                  <th>Campaign</th>
                  <th>Status</th>
                  <th>Creative</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map(ad => (
                  <tr key={ad.id}>
                    <td>
                      <div style={{ fontWeight: 500 }}>{ad.name}</div>
                      <div className="text-xs text-muted font-mono">{ad.id}</div>
                    </td>
                    <td className="text-xs font-mono">{ad.adset_id}</td>
                    <td className="text-xs font-mono">{ad.campaign_id}</td>
                    <td><StatusBadge status={ad.status} /></td>
                    <td className="text-xs font-mono">{ad.creative_id || '—'}</td>
                    <td className="text-xs text-muted">
                      {ad.created ? new Date(ad.created).toLocaleDateString() : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Create Ad Modal */}
      {showCreate && (
        <Modal
          title="Create Ad"
          onClose={() => setShowCreate(false)}
          footer={
            <>
              <button className="btn btn-secondary" onClick={() => setShowCreate(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleCreate} disabled={submitting}>
                {submitting ? 'Creating...' : 'Create Ad'}
              </button>
            </>
          }
        >
          <form onSubmit={handleCreate}>
            <div className="form-group">
              <label>Ad Name</label>
              <input
                type="text"
                value={form.name}
                onChange={e => setForm({ ...form, name: e.target.value })}
                placeholder="e.g. Hero Image - Version A"
                required
              />
            </div>

            <div className="form-grid">
              <div className="form-group">
                <label>Ad Set</label>
                <select
                  value={form.adset_id}
                  onChange={e => setForm({ ...form, adset_id: e.target.value })}
                  required
                >
                  <option value="">Select ad set...</option>
                  {adsets.map(a => (
                    <option key={a.id} value={a.id}>{a.name}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Status</label>
                <select value={form.status} onChange={e => setForm({ ...form, status: e.target.value })}>
                  <option value="PAUSED">Paused</option>
                  <option value="ACTIVE">Active</option>
                </select>
              </div>
            </div>

            {/* Creative toggle */}
            <div className="tabs" style={{ marginBottom: 16 }}>
              <button
                type="button"
                className={`tab ${!useExistingCreative ? 'active' : ''}`}
                onClick={() => setUseExistingCreative(false)}
              >
                New Creative
              </button>
              <button
                type="button"
                className={`tab ${useExistingCreative ? 'active' : ''}`}
                onClick={() => setUseExistingCreative(true)}
              >
                Existing Creative
              </button>
            </div>

            {useExistingCreative ? (
              <div className="form-group">
                <label>Creative ID</label>
                <input
                  type="text"
                  value={form.creative_id}
                  onChange={e => setForm({ ...form, creative_id: e.target.value })}
                  placeholder="Enter existing creative ID"
                />
              </div>
            ) : (
              <>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Facebook Page</label>
                    {pages.length > 0 ? (
                      <select value={form.page_id} onChange={e => setForm({ ...form, page_id: e.target.value })}>
                        <option value="">Select a page...</option>
                        {pages.map(p => <option key={p.id} value={p.id}>{p.name} (ID: {p.id})</option>)}
                      </select>
                    ) : pagesLoading ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 0' }}>
                        <Loader size={14} style={{ animation: 'spin 1s linear infinite', color: 'var(--text-muted)' }} />
                        <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Loading pages...</span>
                      </div>
                    ) : (
                      <input type="text" value={form.page_id} onChange={e => setForm({ ...form, page_id: e.target.value })} placeholder="Your Page ID" />
                    )}
                  </div>
                  <div className="form-group">
                    <label>Destination URL</label>
                    <input
                      type="url"
                      value={form.link}
                      onChange={e => setForm({ ...form, link: e.target.value })}
                      placeholder="https://yoursite.com/landing"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Primary Text</label>
                  <textarea
                    value={form.message}
                    onChange={e => setForm({ ...form, message: e.target.value })}
                    placeholder="The main text above your ad..."
                  />
                </div>

                <div className="form-grid">
                  <div className="form-group">
                    <label>Headline</label>
                    <input
                      type="text"
                      value={form.headline}
                      onChange={e => setForm({ ...form, headline: e.target.value })}
                      placeholder="Bold headline text"
                    />
                  </div>
                  <div className="form-group">
                    <label>Description</label>
                    <input
                      type="text"
                      value={form.description}
                      onChange={e => setForm({ ...form, description: e.target.value })}
                      placeholder="Additional description"
                    />
                  </div>
                </div>

                <div className="form-grid">
                  <div className="form-group">
                    <label>Call to Action</label>
                    <select
                      value={form.call_to_action_type}
                      onChange={e => setForm({ ...form, call_to_action_type: e.target.value })}
                    >
                      {CTA_TYPES.map(c => (
                        <option key={c} value={c}>{c.replace(/_/g, ' ')}</option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Image Hash (optional)</label>
                    <input
                      type="text"
                      value={form.image_hash}
                      onChange={e => setForm({ ...form, image_hash: e.target.value })}
                      placeholder="Pre-uploaded image hash"
                    />
                  </div>
                </div>
              </>
            )}
          </form>
        </Modal>
      )}
    </div>
  );
}
