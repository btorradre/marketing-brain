import { useState, useEffect } from 'react';
import {
  Plus, Target, RefreshCw, Search, Pencil, Info, AlertTriangle,
  Layers, Image, Trash2, Copy, CheckCircle, AlertCircle, Rocket,
  Upload, Loader, X, Film,
} from 'lucide-react';
import { api } from '../api/client';
import Modal from '../components/Modal';
import StatusBadge from '../components/StatusBadge';
import {
  OBJECTIVES,
  ALL_OPT_GOALS,
  BID_STRATEGIES,
  BILLING_EVENTS,
  CTA_TYPES,
  OBJECTIVE_RULES,
  getGoalsForObjective,
  getDefaultGoal,
  getBillingEventsForObjective,
  getDefaultBilling,
  getPromotedObjectRule,
  isCBO,
} from '../config/objectiveRules';

const defaultForm = {
  name: '',
  campaign_id: '',
  daily_budget: '',
  billing_event: 'IMPRESSIONS',
  optimization_goal: 'LINK_CLICKS',
  bid_strategy: 'LOWEST_COST_WITHOUT_CAP',
  status: 'PAUSED',
  countries: 'US',
  age_min: '18',
  age_max: '65',
  pixel_id: '',
  custom_event_type: 'PURCHASE',
  page_id: '',
  application_id: '',
  object_store_url: '',
};

function makeAd() {
  return {
    _key: Math.random().toString(36).slice(2),
    name: '',
    page_id: '',
    link: '',
    message: '',
    headline: '',
    description: '',
    call_to_action_type: 'LEARN_MORE',
    status: 'PAUSED',
    // Media fields
    media_type: '',       // '' | 'image' | 'video'
    image_hash: '',
    video_id: '',
    media_preview: '',    // object URL for thumbnail
    media_uploading: false,
    media_filename: '',
  };
}

export default function AdSets({ addToast }) {
  const [adsets, setAdsets] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [showUpdate, setShowUpdate] = useState(null);
  const [form, setForm] = useState({ ...defaultForm });
  const [updateForm, setUpdateForm] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [campaignFilter, setCampaignFilter] = useState('');
  const [search, setSearch] = useState('');

  // ── Bulk Ads state ──
  const [bulkAdTarget, setBulkAdTarget] = useState(null);
  const [bulkAds, setBulkAds] = useState([]);
  const [bulkSubmitting, setBulkSubmitting] = useState(false);
  const [bulkResults, setBulkResults] = useState(null);

  // ── Pixels & Pages data (for dropdowns) ──
  const [pixels, setPixels] = useState([]);
  const [pixelsLoading, setPixelsLoading] = useState(false);
  const [pixelsFetched, setPixelsFetched] = useState(false);
  const [pages, setPages] = useState([]);
  const [pagesLoading, setPagesLoading] = useState(false);
  const [pagesFetched, setPagesFetched] = useState(false);

  useEffect(() => {
    loadData();
  }, [campaignFilter]);

  async function loadData() {
    setLoading(true);
    try {
      const params = {};
      if (campaignFilter) params.campaign_id = campaignFilter;
      const [adsetRes, campRes] = await Promise.all([
        api.listAdSets(params),
        api.listCampaigns({}),
      ]);
      setAdsets(adsetRes.adsets || []);
      setCampaigns(campRes.campaigns || []);
    } catch (err) {
      addToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  }

  async function loadPixels() {
    if (pixelsFetched) return;
    setPixelsLoading(true);
    try {
      const res = await api.listPixels();
      setPixels(res.pixels || []);
      setPixelsFetched(true);
    } catch (err) {
      console.error('Failed to load pixels:', err);
    } finally {
      setPixelsLoading(false);
    }
  }

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

  function getSelectedCampaign() {
    return campaigns.find(c => c.id === form.campaign_id) || null;
  }

  function handleCampaignChange(campaignId) {
    const camp = campaigns.find(c => c.id === campaignId);
    const objective = camp?.objective;
    if (objective && OBJECTIVE_RULES[objective]) {
      setForm(prev => ({
        ...prev,
        campaign_id: campaignId,
        optimization_goal: getDefaultGoal(objective),
        billing_event: getDefaultBilling(objective),
        daily_budget: isCBO(camp) ? '' : prev.daily_budget,
      }));
    } else {
      setForm(prev => ({ ...prev, campaign_id: campaignId }));
    }
  }

  async function handleCreate(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      const camp = getSelectedCampaign();
      const objective = camp?.objective;
      const promotedRule = getPromotedObjectRule(objective);
      const payload = {
        name: form.name,
        campaign_id: form.campaign_id,
        billing_event: form.billing_event,
        optimization_goal: form.optimization_goal,
        bid_strategy: form.bid_strategy,
        status: form.status,
        targeting: {
          geo_locations: { countries: form.countries.split(',').map(c => c.trim()) },
          age_min: parseInt(form.age_min) || 18,
          age_max: parseInt(form.age_max) || 65,
        },
      };
      if (!isCBO(camp) && form.daily_budget) {
        payload.daily_budget = parseInt(form.daily_budget);
      }
      if (promotedRule) {
        const po = {};
        if (promotedRule.type === 'pixel') {
          if (form.pixel_id) po.pixel_id = form.pixel_id;
          if (form.custom_event_type) po.custom_event_type = form.custom_event_type;
        } else if (promotedRule.type === 'page') {
          if (form.page_id) po.page_id = form.page_id;
        } else if (promotedRule.type === 'app') {
          if (form.application_id) po.application_id = form.application_id;
          if (form.object_store_url) po.object_store_url = form.object_store_url;
        }
        if (Object.keys(po).length > 0) payload.promoted_object = po;
      }
      await api.createAdSet(payload);
      addToast('Ad set created successfully');
      setShowCreate(false);
      setForm({ ...defaultForm });
      loadData();
    } catch (err) {
      addToast(err.message, 'error');
    } finally {
      setSubmitting(false);
    }
  }

  async function handleUpdate(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      const updates = {};
      if (updateForm.status) updates.status = updateForm.status;
      if (updateForm.daily_budget) updates.daily_budget = parseInt(updateForm.daily_budget);
      if (updateForm.name) updates.name = updateForm.name;
      await api.updateAdSet(showUpdate, updates);
      addToast('Ad set updated successfully');
      setShowUpdate(null);
      loadData();
    } catch (err) {
      addToast(err.message, 'error');
    } finally {
      setSubmitting(false);
    }
  }

  function openUpdate(adset) {
    setUpdateForm({ name: adset.name, status: adset.status, daily_budget: adset.daily_budget || '' });
    setShowUpdate(adset.id);
  }

  // ── Bulk Ads CRUD ──
  function openBulkAds(adset) {
    setBulkAdTarget(adset);
    setBulkAds([makeAd()]);
    setBulkResults(null);
  }

  function closeBulkAds() {
    // Revoke all object URLs to prevent memory leaks
    bulkAds.forEach(ad => {
      if (ad.media_preview) URL.revokeObjectURL(ad.media_preview);
    });
    setBulkAdTarget(null);
    setBulkAds([]);
    setBulkResults(null);
  }

  function updateBulkAd(idx, field, value) {
    setBulkAds(prev => prev.map((ad, i) => i === idx ? { ...ad, [field]: value } : ad));
  }

  function addBulkAd() {
    setBulkAds(prev => [...prev, makeAd()]);
  }

  function removeBulkAd(idx) {
    setBulkAds(prev => {
      const ad = prev[idx];
      if (ad.media_preview) URL.revokeObjectURL(ad.media_preview);
      return prev.filter((_, i) => i !== idx);
    });
  }

  function duplicateBulkAd(idx) {
    setBulkAds(prev => {
      const src = prev[idx];
      const copy = {
        ...src,
        _key: Math.random().toString(36).slice(2),
        name: src.name ? src.name + ' (copy)' : '',
        // Keep image_hash/video_id (reusable), but don't share the preview URL
        media_preview: src.media_preview || '',
        media_uploading: false,
      };
      return [...prev.slice(0, idx + 1), copy, ...prev.slice(idx + 1)];
    });
  }

  // ── Media Upload ──
  async function handleMediaUpload(idx, file) {
    if (!file) return;

    const isImage = file.type.startsWith('image/');
    const isVideo = file.type.startsWith('video/');

    if (!isImage && !isVideo) {
      addToast('Please select an image or video file', 'error');
      return;
    }

    // Client-side size validation
    const maxSize = isImage ? 30 * 1024 * 1024 : 1024 * 1024 * 1024; // 30MB images, 1GB videos
    if (file.size > maxSize) {
      addToast(`File too large. Max ${isImage ? '30 MB' : '1 GB'}.`, 'error');
      return;
    }

    // Set preview + loading state immediately
    const previewUrl = URL.createObjectURL(file);
    setBulkAds(prev => prev.map((ad, i) =>
      i === idx ? {
        ...ad,
        media_preview: previewUrl,
        media_uploading: true,
        media_type: isImage ? 'image' : 'video',
        media_filename: file.name,
      } : ad
    ));

    try {
      const result = await api.uploadMedia(file);
      setBulkAds(prev => prev.map((ad, i) =>
        i === idx ? {
          ...ad,
          media_uploading: false,
          media_type: result.type,
          image_hash: result.image_hash || '',
          video_id: result.video_id || '',
        } : ad
      ));
    } catch (err) {
      addToast(`Upload failed: ${err.message}`, 'error');
      setBulkAds(prev => prev.map((ad, i) =>
        i === idx ? {
          ...ad,
          media_preview: '',
          media_uploading: false,
          media_type: '',
          media_filename: '',
          image_hash: '',
          video_id: '',
        } : ad
      ));
      URL.revokeObjectURL(previewUrl);
    }
  }

  function removeMedia(idx) {
    setBulkAds(prev => prev.map((ad, i) => {
      if (i === idx) {
        if (ad.media_preview) URL.revokeObjectURL(ad.media_preview);
        return { ...ad, media_type: '', image_hash: '', video_id: '', media_preview: '', media_uploading: false, media_filename: '' };
      }
      return ad;
    }));
  }

  async function handleBulkAdsLaunch() {
    const errors = [];
    bulkAds.forEach((ad, i) => {
      if (!ad.name.trim()) errors.push(`Ad ${i + 1}: Name is required`);
      if (!ad.page_id.trim()) errors.push(`Ad ${i + 1}: Page ID is required`);
      if (!ad.link.trim()) errors.push(`Ad ${i + 1}: Destination URL is required`);
      if (ad.media_uploading) errors.push(`Ad ${i + 1}: Media is still uploading`);
    });
    if (errors.length > 0) {
      addToast(errors[0], 'error');
      return;
    }

    setBulkSubmitting(true);
    try {
      const payload = bulkAds.map(ad => {
        const adPayload = {
          name: ad.name,
          page_id: ad.page_id,
          link: ad.link,
          message: ad.message,
          headline: ad.headline,
          description: ad.description,
          call_to_action_type: ad.call_to_action_type,
          status: ad.status,
        };
        if (ad.media_type === 'image' && ad.image_hash) {
          adPayload.image_hash = ad.image_hash;
        }
        if (ad.media_type === 'video' && ad.video_id) {
          adPayload.video_id = ad.video_id;
        }
        return adPayload;
      });
      const result = await api.bulkCreateAds(bulkAdTarget.id, payload);
      setBulkResults(result);
      if (!result.errors || result.errors.length === 0) {
        addToast(`${result.created?.length || 0} ads created successfully!`);
      } else {
        addToast(`${result.created?.length || 0} created, ${result.errors.length} failed`, 'warning');
      }
    } catch (err) {
      addToast(err.message, 'error');
    } finally {
      setBulkSubmitting(false);
    }
  }

  const filtered = adsets.filter(a =>
    a.name.toLowerCase().includes(search.toLowerCase())
  );

  function getCampaignName(id) {
    const c = campaigns.find(c => c.id === id);
    return c ? c.name : id;
  }

  const selectedCampaign = getSelectedCampaign();
  const selectedObjective = selectedCampaign?.objective || null;
  const campaignIsCBO = isCBO(selectedCampaign);
  const availableGoals = selectedObjective ? getGoalsForObjective(selectedObjective) : ALL_OPT_GOALS;
  const availableBillingEvents = selectedObjective ? getBillingEventsForObjective(selectedObjective) : BILLING_EVENTS;
  const objectiveRules = selectedObjective ? OBJECTIVE_RULES[selectedObjective] : null;
  const promotedObjectRule = getPromotedObjectRule(selectedObjective);

  // Fetch pixels/pages when promoted object rule changes
  useEffect(() => {
    if (promotedObjectRule?.type === 'pixel') loadPixels();
    if (promotedObjectRule?.type === 'page') loadPages();
  }, [promotedObjectRule?.type]);

  // Fetch pages when bulk ads modal opens (every ad needs a page)
  useEffect(() => {
    if (bulkAdTarget) loadPages();
  }, [bulkAdTarget]);

  // ── Media upload zone component (used per ad card) ──
  function renderMediaZone(ad, idx) {
    if (ad.media_preview) {
      // Uploaded / uploading state
      return (
        <div className="form-group" style={{ margin: '0 0 10px' }}>
          <label>Creative {ad.media_type === 'video' ? '(Video)' : '(Image)'}</label>
          <div style={{ position: 'relative', display: 'inline-block', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border)', overflow: 'hidden' }}>
            {ad.media_type === 'video' ? (
              <div style={{ position: 'relative', width: 220, height: 130, background: '#000' }}>
                <video
                  src={ad.media_preview}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                  muted
                />
                {!ad.media_uploading && (
                  <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', pointerEvents: 'none' }}>
                    <Film size={28} style={{ color: 'rgba(255,255,255,0.8)' }} />
                  </div>
                )}
              </div>
            ) : (
              <img src={ad.media_preview} alt="Preview" style={{ display: 'block', maxWidth: 220, maxHeight: 130, objectFit: 'cover' }} />
            )}

            {/* Upload spinner overlay */}
            {ad.media_uploading && (
              <div style={{ position: 'absolute', inset: 0, background: 'rgba(0,0,0,0.55)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Loader size={22} style={{ color: 'white', animation: 'spin 1s linear infinite' }} />
              </div>
            )}

            {/* Remove button */}
            {!ad.media_uploading && (
              <button
                type="button"
                onClick={() => removeMedia(idx)}
                style={{
                  position: 'absolute', top: 4, right: 4,
                  background: 'rgba(0,0,0,0.6)', border: 'none', borderRadius: '50%',
                  width: 22, height: 22, display: 'flex', alignItems: 'center', justifyContent: 'center',
                  cursor: 'pointer',
                }}
              >
                <X size={12} style={{ color: 'white' }} />
              </button>
            )}

            {/* Type badge + hash/ID */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '4px 8px', background: 'var(--bg-secondary)' }}>
              <span style={{
                fontSize: 9, fontWeight: 700, letterSpacing: '0.05em',
                padding: '1px 5px', borderRadius: 3,
                background: ad.media_type === 'video' ? 'var(--accent)' : 'var(--success)',
                color: 'white',
              }}>
                {ad.media_type === 'video' ? 'VIDEO' : 'IMAGE'}
              </span>
              <span className="font-mono" style={{ fontSize: 10, color: 'var(--text-muted)' }}>
                {ad.media_uploading
                  ? 'Uploading...'
                  : ad.media_type === 'video'
                    ? (ad.video_id || '').slice(0, 16)
                    : (ad.image_hash || '').slice(0, 16)
                }
              </span>
            </div>
          </div>
        </div>
      );
    }

    // Empty dropzone state
    return (
      <div className="form-group" style={{ margin: '0 0 10px' }}>
        <label>Creative</label>
        <div
          style={{
            border: '2px dashed var(--border)', borderRadius: 'var(--radius-sm)',
            padding: '14px 20px', textAlign: 'center', cursor: 'pointer',
            transition: 'border-color 0.15s',
          }}
          onClick={() => document.getElementById(`media-input-${ad._key}`).click()}
          onDragOver={e => { e.preventDefault(); e.currentTarget.style.borderColor = 'var(--accent)'; }}
          onDragLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; }}
          onDrop={e => {
            e.preventDefault();
            e.currentTarget.style.borderColor = 'var(--border)';
            const file = e.dataTransfer.files[0];
            if (file) handleMediaUpload(idx, file);
          }}
        >
          <Upload size={18} style={{ color: 'var(--text-muted)', marginBottom: 4 }} />
          <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
            Click or drag image / video here
          </div>
          <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 2 }}>
            JPG, PNG, WebP, MP4, MOV — Images max 30 MB, Videos max 1 GB
          </div>
        </div>
        <input
          id={`media-input-${ad._key}`}
          type="file"
          accept="image/jpeg,image/png,image/webp,image/gif,video/mp4,video/quicktime,video/x-msvideo,video/webm"
          style={{ display: 'none' }}
          onChange={e => {
            const file = e.target.files[0];
            if (file) handleMediaUpload(idx, file);
            e.target.value = '';
          }}
        />
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Ad Sets</h2>
          <p>Manage audience targeting, budgets, and scheduling</p>
        </div>
        <div className="flex gap-2">
          <button className="btn btn-secondary" onClick={loadData}>
            <RefreshCw size={14} />
          </button>
          <button className="btn btn-primary" onClick={() => setShowCreate(true)}>
            <Plus size={14} />
            New Ad Set
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-3 mb-4">
        <div style={{ position: 'relative', flex: 1, maxWidth: 300 }}>
          <Search size={14} style={{ position: 'absolute', left: 12, top: 11, color: 'var(--text-muted)' }} />
          <input type="text" placeholder="Search ad sets..." value={search} onChange={e => setSearch(e.target.value)} style={{ paddingLeft: 34 }} />
        </div>
        <select value={campaignFilter} onChange={e => setCampaignFilter(e.target.value)} style={{ width: 250 }}>
          <option value="">All Campaigns</option>
          {campaigns.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>

      {/* Table */}
      <div className="card">
        <div className="table-container">
          {filtered.length === 0 ? (
            <div className="empty-state">
              <Target size={40} />
              <h3>No ad sets found</h3>
              <p>Create an ad set to define your audience and budget</p>
            </div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Ad Set</th>
                  <th>Campaign</th>
                  <th>Status</th>
                  <th>Budget</th>
                  <th>Bid Strategy</th>
                  <th>Goal</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {filtered.map(adset => (
                  <tr key={adset.id}>
                    <td>
                      <div style={{ fontWeight: 500 }}>{adset.name}</div>
                      <div className="text-xs text-muted font-mono">{adset.id}</div>
                    </td>
                    <td>
                      <div style={{ fontSize: 12 }}>{getCampaignName(adset.campaign_id)}</div>
                      <div className="text-xs font-mono text-muted">{adset.campaign_id}</div>
                    </td>
                    <td><StatusBadge status={adset.status} /></td>
                    <td>
                      {adset.daily_budget ? `$${(adset.daily_budget / 100).toFixed(2)}/day`
                        : adset.lifetime_budget ? `$${(adset.lifetime_budget / 100).toFixed(2)}`
                        : '—'}
                    </td>
                    <td className="text-xs">{(adset.bid_strategy || '').replace(/_/g, ' ').toLowerCase()}</td>
                    <td className="text-xs">{(adset.optimization_goal || '').replace(/_/g, ' ').toLowerCase()}</td>
                    <td>
                      <div className="flex gap-1">
                        <button className="btn btn-ghost btn-sm" onClick={() => openBulkAds(adset)} title="Bulk create ads">
                          <Layers size={14} />
                        </button>
                        <button className="btn btn-ghost btn-sm" onClick={() => openUpdate(adset)} title="Edit ad set">
                          <Pencil size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Create Ad Set Modal */}
      {showCreate && (
        <Modal title="Create Ad Set" onClose={() => setShowCreate(false)} footer={
          <>
            <button className="btn btn-secondary" onClick={() => setShowCreate(false)}>Cancel</button>
            <button className="btn btn-primary" onClick={handleCreate} disabled={submitting}>
              {submitting ? 'Creating...' : 'Create Ad Set'}
            </button>
          </>
        }>
          <form onSubmit={handleCreate}>
            <div className="form-group">
              <label>Campaign</label>
              <select value={form.campaign_id} onChange={e => handleCampaignChange(e.target.value)} required>
                <option value="">Select a campaign...</option>
                {campaigns.map(c => (
                  <option key={c.id} value={c.id}>
                    {c.name} — {(c.objective || '').replace('OUTCOME_', '')}{isCBO(c) ? ' (CBO)' : ''}
                  </option>
                ))}
              </select>
            </div>

            {selectedObjective && objectiveRules && (
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: 10, padding: '10px 14px', marginBottom: 16, background: 'var(--accent-subtle)', border: '1px solid var(--accent)', borderRadius: 'var(--radius-sm)', fontSize: 12 }}>
                <Info size={14} style={{ color: 'var(--accent)', flexShrink: 0, marginTop: 1 }} />
                <div>
                  <strong style={{ color: 'var(--accent)' }}>
                    {OBJECTIVES.find(o => o.value === selectedObjective)?.label} Campaign
                    {campaignIsCBO && <span style={{ marginLeft: 6, opacity: 0.8 }}>(CBO — budget set at campaign level)</span>}
                  </strong>
                  <div style={{ color: 'var(--text-secondary)', marginTop: 2 }}>
                    {objectiveRules.description}. Optimization goals and billing events have been filtered to match this objective.
                  </div>
                </div>
              </div>
            )}

            <div className="form-group">
              <label>Ad Set Name</label>
              <input type="text" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} placeholder="e.g. US Women 25-45" required />
            </div>

            <div className="form-grid">
              {!campaignIsCBO && (
                <div className="form-group">
                  <label>Daily Budget (cents)</label>
                  <input type="number" value={form.daily_budget} onChange={e => setForm({ ...form, daily_budget: e.target.value })} placeholder="e.g. 2000 = $20.00" />
                  <div className="hint">{form.daily_budget ? `= $${(form.daily_budget / 100).toFixed(2)}/day` : ''}</div>
                </div>
              )}
              <div className="form-group">
                <label>Status</label>
                <select value={form.status} onChange={e => setForm({ ...form, status: e.target.value })}>
                  <option value="PAUSED">Paused</option>
                  <option value="ACTIVE">Active</option>
                </select>
              </div>
            </div>

            <div className="form-grid">
              <div className="form-group">
                <label>Optimization Goal</label>
                <select value={form.optimization_goal} onChange={e => setForm({ ...form, optimization_goal: e.target.value })}>
                  {availableGoals.map(g => <option key={g.value} value={g.value}>{g.label}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label>Billing Event</label>
                <select value={form.billing_event} onChange={e => setForm({ ...form, billing_event: e.target.value })}>
                  {availableBillingEvents.map(b => <option key={b} value={b}>{b}</option>)}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Bid Strategy</label>
              <select value={form.bid_strategy} onChange={e => setForm({ ...form, bid_strategy: e.target.value })}>
                {BID_STRATEGIES.map(b => <option key={b.value} value={b.value}>{b.label}</option>)}
              </select>
            </div>

            {promotedObjectRule && (
              <div style={{ borderTop: '1px solid var(--border)', margin: '16px 0', paddingTop: 16 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
                  <AlertTriangle size={14} style={{ color: 'var(--warning, #f59e0b)' }} />
                  <h4 style={{ fontSize: 13, fontWeight: 600, margin: 0 }}>
                    Promoted Object <span style={{ color: 'var(--error)', fontWeight: 400 }}>(required)</span>
                  </h4>
                </div>
                <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 12 }}>
                  {selectedObjective === 'OUTCOME_SALES' && 'Sales campaigns require a Meta Pixel to track conversions.'}
                  {selectedObjective === 'OUTCOME_LEADS' && 'Lead campaigns require a Facebook Page ID for lead forms.'}
                  {selectedObjective === 'OUTCOME_APP_PROMOTION' && 'App campaigns require your app ID and store URL.'}
                </div>
                {promotedObjectRule.fields.map(field => (
                  <div className="form-group" key={field.key}>
                    <label>{field.label}</label>
                    {field.type === 'select' ? (
                      <select value={form[field.key] || field.options[0]?.value} onChange={e => setForm({ ...form, [field.key]: e.target.value })}>
                        {field.options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
                      </select>
                    ) : field.key === 'pixel_id' && pixels.length > 0 ? (
                      <select value={form.pixel_id} onChange={e => setForm({ ...form, pixel_id: e.target.value })} required={field.required}>
                        <option value="">Select a pixel...</option>
                        {pixels.map(p => <option key={p.id} value={p.id}>{p.name} (ID: {p.id})</option>)}
                      </select>
                    ) : field.key === 'pixel_id' && pixelsLoading ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 0' }}>
                        <Loader size={14} style={{ animation: 'spin 1s linear infinite', color: 'var(--text-muted)' }} />
                        <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Loading pixels...</span>
                      </div>
                    ) : field.key === 'page_id' && pages.length > 0 ? (
                      <select value={form.page_id} onChange={e => setForm({ ...form, page_id: e.target.value })} required={field.required}>
                        <option value="">Select a page...</option>
                        {pages.map(p => <option key={p.id} value={p.id}>{p.name} (ID: {p.id})</option>)}
                      </select>
                    ) : field.key === 'page_id' && pagesLoading ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 0' }}>
                        <Loader size={14} style={{ animation: 'spin 1s linear infinite', color: 'var(--text-muted)' }} />
                        <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Loading pages...</span>
                      </div>
                    ) : (
                      <input type="text" value={form[field.key] || ''} onChange={e => setForm({ ...form, [field.key]: e.target.value })} placeholder={field.placeholder || ''} required={field.required} />
                    )}
                  </div>
                ))}
              </div>
            )}

            <div style={{ borderTop: '1px solid var(--border)', margin: '16px 0', paddingTop: 16 }}>
              <h4 style={{ fontSize: 13, fontWeight: 600, marginBottom: 12 }}>Targeting</h4>
            </div>
            <div className="form-grid">
              <div className="form-group">
                <label>Countries (comma-separated)</label>
                <input type="text" value={form.countries} onChange={e => setForm({ ...form, countries: e.target.value })} placeholder="US, CA, GB" />
              </div>
              <div className="form-group">
                <label>Age Range</label>
                <div className="flex gap-2 items-center">
                  <input type="number" value={form.age_min} onChange={e => setForm({ ...form, age_min: e.target.value })} style={{ width: 80 }} min="18" max="65" />
                  <span className="text-muted">to</span>
                  <input type="number" value={form.age_max} onChange={e => setForm({ ...form, age_max: e.target.value })} style={{ width: 80 }} min="18" max="65" />
                </div>
              </div>
            </div>
          </form>
        </Modal>
      )}

      {/* Update Ad Set Modal */}
      {showUpdate && (
        <Modal title="Update Ad Set" onClose={() => setShowUpdate(null)} footer={
          <>
            <button className="btn btn-secondary" onClick={() => setShowUpdate(null)}>Cancel</button>
            <button className="btn btn-primary" onClick={handleUpdate} disabled={submitting}>
              {submitting ? 'Updating...' : 'Save Changes'}
            </button>
          </>
        }>
          <form onSubmit={handleUpdate}>
            <div className="form-group">
              <label>Ad Set ID</label>
              <input type="text" value={showUpdate} disabled />
            </div>
            <div className="form-group">
              <label>Name</label>
              <input type="text" value={updateForm.name} onChange={e => setUpdateForm({ ...updateForm, name: e.target.value })} />
            </div>
            <div className="form-grid">
              <div className="form-group">
                <label>Status</label>
                <select value={updateForm.status} onChange={e => setUpdateForm({ ...updateForm, status: e.target.value })}>
                  <option value="PAUSED">Paused</option>
                  <option value="ACTIVE">Active</option>
                </select>
              </div>
              <div className="form-group">
                <label>Daily Budget (cents)</label>
                <input type="number" value={updateForm.daily_budget} onChange={e => setUpdateForm({ ...updateForm, daily_budget: e.target.value })} placeholder="e.g. 2000" />
              </div>
            </div>
          </form>
        </Modal>
      )}

      {/* ── Bulk Create Ads Modal ── */}
      {bulkAdTarget && (
        <Modal
          title={bulkResults ? 'Bulk Create Ads — Results' : 'Bulk Create Ads'}
          className="modal-wide"
          onClose={closeBulkAds}
          footer={
            bulkResults ? (
              <>
                <button className="btn btn-secondary" onClick={() => { setBulkResults(null); setBulkAds([makeAd()]); }}>
                  <Plus size={14} /> Create More
                </button>
                <button className="btn btn-primary" onClick={closeBulkAds}>Done</button>
              </>
            ) : (
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                <span className="text-sm text-muted">
                  {bulkAds.length} ad{bulkAds.length !== 1 ? 's' : ''} ready to launch
                </span>
                <div className="flex gap-2">
                  <button className="btn btn-secondary" onClick={closeBulkAds}>Cancel</button>
                  <button className="btn btn-primary" onClick={handleBulkAdsLaunch} disabled={bulkSubmitting}>
                    {bulkSubmitting ? 'Launching...' : (
                      <><Rocket size={14} /> Launch {bulkAds.length} Ad{bulkAds.length !== 1 ? 's' : ''}</>
                    )}
                  </button>
                </div>
              </div>
            )
          }
        >
          {/* Ad set info banner */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 14px', marginBottom: 20, background: 'var(--accent-subtle)', border: '1px solid var(--accent)', borderRadius: 'var(--radius-sm)', fontSize: 12 }}>
            <Target size={14} style={{ color: 'var(--accent)', flexShrink: 0 }} />
            <div>
              <strong style={{ color: 'var(--accent)' }}>{bulkAdTarget.name}</strong>
              <span className="text-muted" style={{ marginLeft: 8 }}>{bulkAdTarget.id}</span>
              <div style={{ color: 'var(--text-secondary)', marginTop: 2 }}>
                Campaign: {getCampaignName(bulkAdTarget.campaign_id)}
                {bulkAdTarget.optimization_goal && ` · ${bulkAdTarget.optimization_goal.replace(/_/g, ' ').toLowerCase()}`}
                {bulkAdTarget.daily_budget && ` · $${(bulkAdTarget.daily_budget / 100).toFixed(2)}/day`}
              </div>
            </div>
          </div>

          {/* Results view */}
          {bulkResults ? (
            <div>
              {bulkResults.created?.length > 0 && (
                <div style={{ marginBottom: 20 }}>
                  <h4 style={{ fontSize: 13, fontWeight: 600, color: 'var(--success)', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
                    <CheckCircle size={14} /> Created ({bulkResults.created.length})
                  </h4>
                  <table>
                    <thead><tr><th>Name</th><th>Ad ID</th></tr></thead>
                    <tbody>
                      {bulkResults.created.map((obj, i) => (
                        <tr key={i}>
                          <td style={{ fontWeight: 500 }}>{obj.name}</td>
                          <td className="font-mono text-xs">{obj.id}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
              {bulkResults.errors?.length > 0 && (
                <div>
                  <h4 style={{ fontSize: 13, fontWeight: 600, color: 'var(--error)', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
                    <AlertCircle size={14} /> Failed ({bulkResults.errors.length})
                  </h4>
                  {bulkResults.errors.map((err, i) => (
                    <div key={i} style={{ padding: '10px 14px', background: 'var(--error-subtle, rgba(239,68,68,0.1))', borderRadius: 'var(--radius-sm)', marginBottom: 6, fontSize: 13 }}>
                      <strong>{err.name}:</strong>
                      {(err.errors || []).map((e, j) => <div key={j} className="text-xs" style={{ marginTop: 4 }}>{e}</div>)}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            /* Build view — ad cards */
            <div>
              {bulkAds.map((ad, idx) => (
                <div key={ad._key} style={{
                  background: 'var(--bg-primary)', border: '1px solid var(--border)',
                  borderLeft: '3px solid var(--success)', borderRadius: 'var(--radius-sm)',
                  padding: 14, marginBottom: 10,
                }}>
                  {/* Card header */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                    <div className="flex items-center gap-2">
                      <Image size={13} style={{ color: 'var(--success)' }} />
                      <span style={{ fontSize: 12, fontWeight: 600 }}>{ad.name || `Ad ${idx + 1}`}</span>
                      {ad.media_type && (
                        <span style={{
                          fontSize: 9, fontWeight: 700, letterSpacing: '0.05em',
                          padding: '1px 5px', borderRadius: 3,
                          background: ad.media_type === 'video' ? 'var(--accent)' : 'var(--success)',
                          color: 'white',
                        }}>
                          {ad.media_type === 'video' ? 'VIDEO' : 'IMAGE'}
                        </span>
                      )}
                    </div>
                    <div className="flex gap-1">
                      <button className="btn btn-ghost btn-sm" onClick={() => duplicateBulkAd(idx)} title="Duplicate"><Copy size={12} /></button>
                      {bulkAds.length > 1 && (
                        <button className="btn btn-ghost btn-sm" onClick={() => removeBulkAd(idx)} style={{ color: 'var(--error)' }} title="Remove"><Trash2 size={12} /></button>
                      )}
                    </div>
                  </div>

                  {/* Row 1: Name + Page ID */}
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 10 }}>
                    <div className="form-group" style={{ margin: 0 }}>
                      <label>Ad Name</label>
                      <input type="text" value={ad.name} onChange={e => updateBulkAd(idx, 'name', e.target.value)} placeholder="e.g. Hero Image A" />
                    </div>
                    <div className="form-group" style={{ margin: 0 }}>
                      <label>Facebook Page</label>
                      {pages.length > 0 ? (
                        <select value={ad.page_id} onChange={e => updateBulkAd(idx, 'page_id', e.target.value)}>
                          <option value="">Select a page...</option>
                          {pages.map(p => <option key={p.id} value={p.id}>{p.name} (ID: {p.id})</option>)}
                        </select>
                      ) : pagesLoading ? (
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 0' }}>
                          <Loader size={14} style={{ animation: 'spin 1s linear infinite', color: 'var(--text-muted)' }} />
                          <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Loading pages...</span>
                        </div>
                      ) : (
                        <input type="text" value={ad.page_id} onChange={e => updateBulkAd(idx, 'page_id', e.target.value)} placeholder="Page ID" />
                      )}
                    </div>
                  </div>

                  {/* Row 2: URL */}
                  <div className="form-group" style={{ margin: '0 0 10px' }}>
                    <label>Destination URL</label>
                    <input type="url" value={ad.link} onChange={e => updateBulkAd(idx, 'link', e.target.value)} placeholder="https://yoursite.com/landing" />
                  </div>

                  {/* Row 3: Media upload zone */}
                  {renderMediaZone(ad, idx)}

                  {/* Row 4: Primary text */}
                  <div className="form-group" style={{ margin: '0 0 10px' }}>
                    <label>Primary Text</label>
                    <textarea value={ad.message} onChange={e => updateBulkAd(idx, 'message', e.target.value)} placeholder="The main text above your ad..." style={{ minHeight: 60 }} />
                  </div>

                  {/* Row 5: Headline + Description + CTA + Status */}
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 100px', gap: 10 }}>
                    <div className="form-group" style={{ margin: 0 }}>
                      <label>Headline</label>
                      <input type="text" value={ad.headline} onChange={e => updateBulkAd(idx, 'headline', e.target.value)} placeholder="Bold headline" />
                    </div>
                    <div className="form-group" style={{ margin: 0 }}>
                      <label>Description</label>
                      <input type="text" value={ad.description} onChange={e => updateBulkAd(idx, 'description', e.target.value)} placeholder="Short description" />
                    </div>
                    <div className="form-group" style={{ margin: 0 }}>
                      <label>CTA Button</label>
                      <select value={ad.call_to_action_type} onChange={e => updateBulkAd(idx, 'call_to_action_type', e.target.value)}>
                        {CTA_TYPES.map(c => <option key={c} value={c}>{c.replace(/_/g, ' ')}</option>)}
                      </select>
                    </div>
                    <div className="form-group" style={{ margin: 0 }}>
                      <label>Status</label>
                      <select value={ad.status} onChange={e => updateBulkAd(idx, 'status', e.target.value)}>
                        <option value="PAUSED">Paused</option>
                        <option value="ACTIVE">Active</option>
                      </select>
                    </div>
                  </div>
                </div>
              ))}

              <button className="btn btn-secondary btn-sm" onClick={addBulkAd} style={{ marginTop: 4 }}>
                <Plus size={13} /> Add Ad Variation
              </button>
            </div>
          )}
        </Modal>
      )}
    </div>
  );
}
