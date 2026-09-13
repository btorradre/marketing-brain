import { useState, useEffect } from 'react';
import {
  Rocket,
  Upload,
  CheckCircle,
  FileJson,
  Play,
  AlertCircle,
  Plus,
  Trash2,
  ChevronDown,
  ChevronRight,
  Megaphone,
  Target,
  Image,
  Copy,
  Code,
  Layers,
  Info,
  AlertTriangle,
  Loader,
} from 'lucide-react';
import { api } from '../api/client';
import {
  OBJECTIVES,
  ALL_OPT_GOALS,
  BID_STRATEGIES,
  CTA_TYPES,
  OBJECTIVE_RULES,
  PROMOTED_OBJECT_RULES,
  getGoalsForObjective,
  getDefaultGoal,
  getBillingEventsForObjective,
  getDefaultBilling,
  getPromotedObjectRule,
} from '../config/objectiveRules';

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
  };
}

function makeAdSet(objective) {
  return {
    _key: Math.random().toString(36).slice(2),
    _open: true,
    name: '',
    daily_budget: '',
    billing_event: getDefaultBilling(objective || 'OUTCOME_TRAFFIC'),
    optimization_goal: getDefaultGoal(objective || 'OUTCOME_TRAFFIC'),
    bid_strategy: 'LOWEST_COST_WITHOUT_CAP',
    status: 'PAUSED',
    countries: 'US',
    age_min: '18',
    age_max: '65',
    // promoted_object fields (used dynamically based on objective)
    pixel_id: '',
    custom_event_type: 'PURCHASE',
    promoted_page_id: '',
    application_id: '',
    object_store_url: '',
    ads: [makeAd()],
  };
}

function makeCampaign() {
  const objective = 'OUTCOME_TRAFFIC';
  return {
    _key: Math.random().toString(36).slice(2),
    _open: true,
    name: '',
    objective,
    daily_budget: '',
    status: 'PAUSED',
    special_ad_categories: [],
    ad_sets: [makeAdSet(objective)],
  };
}

function buildPromotedObject(adset, objective) {
  const rule = PROMOTED_OBJECT_RULES[objective];
  if (!rule) return undefined;

  if (rule.type === 'pixel' && adset.pixel_id) {
    return { pixel_id: adset.pixel_id, custom_event_type: adset.custom_event_type || 'PURCHASE' };
  }
  if (rule.type === 'page' && adset.promoted_page_id) {
    return { page_id: adset.promoted_page_id };
  }
  if (rule.type === 'app' && adset.application_id) {
    const po = { application_id: adset.application_id };
    if (adset.object_store_url) po.object_store_url = adset.object_store_url;
    return po;
  }
  return undefined;
}

function buildPayload(campaigns) {
  return {
    campaigns: campaigns.map(c => {
      const campPayload = {
        name: c.name,
        objective: c.objective,
        status: c.status,
        special_ad_categories: c.special_ad_categories,
      };
      // Only set campaign budget if CBO
      if (c.daily_budget) {
        campPayload.daily_budget = parseInt(c.daily_budget);
      }

      const isCBO = !!c.daily_budget;

      campPayload.ad_sets = c.ad_sets.map(as => {
        const adsetPayload = {
          name: as.name,
          billing_event: as.billing_event,
          optimization_goal: as.optimization_goal,
          bid_strategy: as.bid_strategy,
          status: as.status,
          targeting: {
            geo_locations: { countries: as.countries.split(',').map(s => s.trim()).filter(Boolean) },
            age_min: parseInt(as.age_min) || 18,
            age_max: parseInt(as.age_max) || 65,
          },
        };

        // Only include ad-set budget for ABO
        if (!isCBO && as.daily_budget) {
          adsetPayload.daily_budget = parseInt(as.daily_budget);
        }

        // Build promoted_object
        const po = buildPromotedObject(as, c.objective);
        if (po) adsetPayload.promoted_object = po;

        adsetPayload.ads = as.ads.map(ad => ({
          name: ad.name,
          page_id: ad.page_id,
          link: ad.link,
          message: ad.message,
          headline: ad.headline,
          description: ad.description,
          call_to_action_type: ad.call_to_action_type,
          status: ad.status,
        }));

        return adsetPayload;
      });

      return campPayload;
    }),
  };
}

export default function BulkLaunch({ addToast }) {
  const [step, setStep] = useState(0);
  const [campaigns, setCampaigns] = useState([makeCampaign()]);
  const [mode, setMode] = useState('visual');
  const [jsonInput, setJsonInput] = useState('');
  const [results, setResults] = useState(null);
  const [launching, setLaunching] = useState(false);

  // ── Pixels & Pages data (for dropdowns) ──
  const [pixels, setPixels] = useState([]);
  const [pixelsLoading, setPixelsLoading] = useState(false);
  const [pixelsFetched, setPixelsFetched] = useState(false);
  const [pages, setPages] = useState([]);
  const [pagesLoading, setPagesLoading] = useState(false);
  const [pagesFetched, setPagesFetched] = useState(false);

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

  // Fetch pages eagerly (every ad needs a page) and pixels when needed
  useEffect(() => {
    loadPages();
    const needsPixel = campaigns.some(c => getPromotedObjectRule(c.objective)?.type === 'pixel');
    if (needsPixel) loadPixels();
  }, [campaigns.map(c => c.objective).join(',')]);

  // ── Campaign CRUD ──
  function updateCampaign(idx, field, value) {
    setCampaigns(prev => prev.map((c, i) => {
      if (i !== idx) return c;

      const updated = { ...c, [field]: value };

      // When objective changes, cascade defaults to all child ad sets
      if (field === 'objective') {
        const newGoal = getDefaultGoal(value);
        const newBilling = getDefaultBilling(value);
        const validGoals = OBJECTIVE_RULES[value]?.optimization_goals || [];

        updated.ad_sets = c.ad_sets.map(as => {
          const goalValid = validGoals.includes(as.optimization_goal);
          const billingValid = getBillingEventsForObjective(value).includes(as.billing_event);
          return {
            ...as,
            optimization_goal: goalValid ? as.optimization_goal : newGoal,
            billing_event: billingValid ? as.billing_event : newBilling,
          };
        });
      }

      return updated;
    }));
  }

  function removeCampaign(idx) {
    setCampaigns(prev => prev.filter((_, i) => i !== idx));
  }
  function duplicateCampaign(idx) {
    setCampaigns(prev => {
      const copy = JSON.parse(JSON.stringify(prev[idx]));
      copy._key = Math.random().toString(36).slice(2);
      copy.name = copy.name + ' (copy)';
      copy.ad_sets.forEach(as => {
        as._key = Math.random().toString(36).slice(2);
        as.ads.forEach(ad => { ad._key = Math.random().toString(36).slice(2); });
      });
      return [...prev.slice(0, idx + 1), copy, ...prev.slice(idx + 1)];
    });
  }

  // ── Ad Set CRUD ──
  function updateAdSet(cIdx, asIdx, field, value) {
    setCampaigns(prev => prev.map((c, ci) => ci !== cIdx ? c : {
      ...c,
      ad_sets: c.ad_sets.map((as, ai) => ai === asIdx ? { ...as, [field]: value } : as),
    }));
  }
  function addAdSet(cIdx) {
    setCampaigns(prev => prev.map((c, ci) => ci !== cIdx ? c : {
      ...c, ad_sets: [...c.ad_sets, makeAdSet(c.objective)],
    }));
  }
  function removeAdSet(cIdx, asIdx) {
    setCampaigns(prev => prev.map((c, ci) => ci !== cIdx ? c : {
      ...c, ad_sets: c.ad_sets.filter((_, i) => i !== asIdx),
    }));
  }

  // ── Ad CRUD ──
  function updateAd(cIdx, asIdx, adIdx, field, value) {
    setCampaigns(prev => prev.map((c, ci) => ci !== cIdx ? c : {
      ...c,
      ad_sets: c.ad_sets.map((as, ai) => ai !== asIdx ? as : {
        ...as,
        ads: as.ads.map((ad, adi) => adi === adIdx ? { ...ad, [field]: value } : ad),
      }),
    }));
  }
  function addAd(cIdx, asIdx) {
    setCampaigns(prev => prev.map((c, ci) => ci !== cIdx ? c : {
      ...c,
      ad_sets: c.ad_sets.map((as, ai) => ai !== asIdx ? as : {
        ...as, ads: [...as.ads, makeAd()],
      }),
    }));
  }
  function removeAd(cIdx, asIdx, adIdx) {
    setCampaigns(prev => prev.map((c, ci) => ci !== cIdx ? c : {
      ...c,
      ad_sets: c.ad_sets.map((as, ai) => ai !== asIdx ? as : {
        ...as, ads: as.ads.filter((_, i) => i !== adIdx),
      }),
    }));
  }

  // ── Validation ──
  function validate() {
    const errors = [];
    campaigns.forEach((c, ci) => {
      if (!c.name.trim()) errors.push(`Campaign ${ci + 1}: Name is required`);
      const rules = OBJECTIVE_RULES[c.objective];
      const poRule = getPromotedObjectRule(c.objective);
      c.ad_sets.forEach((as, ai) => {
        if (!as.name.trim()) errors.push(`Campaign ${ci + 1} → Ad Set ${ai + 1}: Name is required`);
        if (rules && !rules.optimization_goals.includes(as.optimization_goal)) {
          errors.push(`Campaign ${ci + 1} → Ad Set ${ai + 1}: "${as.optimization_goal}" is not valid for ${c.objective.replace('OUTCOME_', '')} campaigns`);
        }
        // Validate promoted object
        if (poRule) {
          if (poRule.type === 'pixel' && !as.pixel_id) {
            errors.push(`Campaign ${ci + 1} → Ad Set ${ai + 1}: Pixel ID is required for ${c.objective.replace('OUTCOME_', '')} campaigns`);
          }
          if (poRule.type === 'page' && !as.promoted_page_id) {
            errors.push(`Campaign ${ci + 1} → Ad Set ${ai + 1}: Page ID is required for ${c.objective.replace('OUTCOME_', '')} campaigns`);
          }
          if (poRule.type === 'app' && !as.application_id) {
            errors.push(`Campaign ${ci + 1} → Ad Set ${ai + 1}: App ID is required for ${c.objective.replace('OUTCOME_', '')} campaigns`);
          }
        }
        as.ads.forEach((ad, adi) => {
          if (!ad.name.trim()) errors.push(`Campaign ${ci + 1} → Ad Set ${ai + 1} → Ad ${adi + 1}: Name is required`);
          if (!ad.page_id.trim()) errors.push(`Campaign ${ci + 1} → Ad Set ${ai + 1} → Ad ${adi + 1}: Page ID is required`);
          if (!ad.link.trim()) errors.push(`Campaign ${ci + 1} → Ad Set ${ai + 1} → Ad ${adi + 1}: URL is required`);
        });
      });
    });
    return errors;
  }

  function handleContinue() {
    if (mode === 'json') {
      try {
        const data = JSON.parse(jsonInput);
        if (!data.campaigns) { addToast('JSON must have a "campaigns" key', 'error'); return; }
        setStep(1);
        return;
      } catch { addToast('Invalid JSON', 'error'); return; }
    }
    const errors = validate();
    if (errors.length > 0) {
      addToast(errors[0], 'error');
      return;
    }
    setStep(1);
  }

  function getPayload() {
    if (mode === 'json') return JSON.parse(jsonInput);
    return buildPayload(campaigns);
  }

  async function handleLaunch() {
    setStep(2);
    setLaunching(true);
    try {
      const result = await api.executeBulk(getPayload());
      setResults(result);
      setStep(3);
      if (result.errors?.length === 0) {
        addToast('Bulk launch completed successfully!');
      } else {
        addToast(`Launched with ${result.errors?.length || 0} errors`, 'warning');
      }
    } catch (err) {
      addToast(err.message, 'error');
      setStep(1);
    } finally {
      setLaunching(false);
    }
  }

  function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const data = JSON.parse(event.target.result);
        if (data.campaigns) {
          const imported = data.campaigns.map(c => {
            const objective = c.objective || 'OUTCOME_TRAFFIC';
            return {
              ...makeCampaign(),
              name: c.name || '',
              objective,
              daily_budget: c.daily_budget ? String(c.daily_budget) : '',
              status: c.status || 'PAUSED',
              special_ad_categories: c.special_ad_categories || [],
              ad_sets: (c.ad_sets || []).map(as => ({
                ...makeAdSet(objective),
                name: as.name || '',
                daily_budget: as.daily_budget ? String(as.daily_budget) : '',
                billing_event: as.billing_event || getDefaultBilling(objective),
                optimization_goal: as.optimization_goal || getDefaultGoal(objective),
                bid_strategy: as.bid_strategy || 'LOWEST_COST_WITHOUT_CAP',
                status: as.status || 'PAUSED',
                countries: as.targeting?.geo_locations?.countries?.join(', ') || 'US',
                age_min: String(as.targeting?.age_min || 18),
                age_max: String(as.targeting?.age_max || 65),
                pixel_id: as.promoted_object?.pixel_id || '',
                custom_event_type: as.promoted_object?.custom_event_type || 'PURCHASE',
                promoted_page_id: as.promoted_object?.page_id || '',
                application_id: as.promoted_object?.application_id || '',
                object_store_url: as.promoted_object?.object_store_url || '',
                ads: (as.ads || []).map(ad => ({
                  ...makeAd(),
                  ...ad,
                })),
              })),
            };
          });
          setCampaigns(imported);
          setMode('visual');
          addToast(`Imported ${imported.length} campaign(s)`);
        }
      } catch {
        addToast('Invalid JSON file', 'error');
      }
    };
    reader.readAsText(file);
    e.target.value = '';
  }

  function reset() {
    setStep(0);
    setResults(null);
  }

  function countObjects() {
    const payload = getPayload();
    let c = 0, as = 0, ads = 0;
    for (const camp of payload?.campaigns || []) {
      c++;
      for (const adset of camp.ad_sets || []) {
        as++;
        ads += (adset.ads || []).length;
      }
    }
    return { campaigns: c, adsets: as, ads };
  }

  const steps = [
    { label: 'Build', completed: step > 0, active: step === 0 },
    { label: 'Review', completed: step > 1, active: step === 1 },
    { label: 'Launch', completed: step > 2, active: step === 2 },
    { label: 'Results', completed: step === 3, active: step === 3 },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Bulk Launch</h2>
          <p>Build and deploy entire campaign structures at once</p>
        </div>
        <div className="flex gap-2">
          {step > 0 && step < 3 && (
            <button className="btn btn-secondary" onClick={reset}>Start Over</button>
          )}
        </div>
      </div>

      {/* Steps */}
      <div className="steps-container">
        {steps.map((s, i) => (
          <div key={i} style={{ display: 'contents' }}>
            <div className={`step ${s.active ? 'active' : ''} ${s.completed ? 'completed' : ''}`}>
              <div className="step-number">
                {s.completed ? <CheckCircle size={14} /> : i + 1}
              </div>
              {s.label}
            </div>
            {i < steps.length - 1 && <div className="step-connector" />}
          </div>
        ))}
      </div>

      {/* ── Step 0: Build ── */}
      {step === 0 && (
        <div>
          {/* Mode toggle + actions bar */}
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            marginBottom: 16,
          }}>
            <div className="flex gap-2">
              <button
                className={`btn btn-sm ${mode === 'visual' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setMode('visual')}
              >
                <Layers size={14} />
                Visual Builder
              </button>
              <button
                className={`btn btn-sm ${mode === 'json' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => {
                  setJsonInput(JSON.stringify(buildPayload(campaigns), null, 2));
                  setMode('json');
                }}
              >
                <Code size={14} />
                JSON
              </button>
            </div>
            <div className="flex gap-2">
              <label className="btn btn-secondary btn-sm" style={{ cursor: 'pointer' }}>
                <Upload size={14} />
                Import JSON
                <input type="file" accept=".json" onChange={handleFileUpload} style={{ display: 'none' }} />
              </label>
            </div>
          </div>

          {mode === 'visual' ? (
            <div>
              {campaigns.map((camp, ci) => {
                const objectiveRules = OBJECTIVE_RULES[camp.objective];
                const availableGoals = getGoalsForObjective(camp.objective);
                const availableBilling = getBillingEventsForObjective(camp.objective);
                const poRule = getPromotedObjectRule(camp.objective);
                const campIsCBO = !!camp.daily_budget;

                return (
                <div key={camp._key} style={{
                  background: 'var(--bg-card)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius-lg)',
                  marginBottom: 16,
                  overflow: 'hidden',
                }}>
                  {/* Campaign header */}
                  <div
                    style={{
                      display: 'flex', alignItems: 'center', gap: 12,
                      padding: '14px 20px',
                      background: 'var(--bg-secondary)',
                      borderBottom: camp._open ? '1px solid var(--border)' : 'none',
                      cursor: 'pointer',
                    }}
                    onClick={() => updateCampaign(ci, '_open', !camp._open)}
                  >
                    {camp._open ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                    <Megaphone size={16} style={{ color: 'var(--accent)' }} />
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: 13, fontWeight: 600 }}>
                        {camp.name || `Campaign ${ci + 1}`}
                      </div>
                      <div className="text-xs text-muted">
                        {OBJECTIVES.find(o => o.value === camp.objective)?.label || 'Traffic'}
                        {campIsCBO ? ' · CBO' : ' · ABO'}
                        {' · '}{camp.ad_sets.length} ad set{camp.ad_sets.length !== 1 ? 's' : ''}
                        {' · '}{camp.ad_sets.reduce((sum, as) => sum + as.ads.length, 0)} ad{camp.ad_sets.reduce((sum, as) => sum + as.ads.length, 0) !== 1 ? 's' : ''}
                      </div>
                    </div>
                    <div className="flex gap-2" onClick={e => e.stopPropagation()}>
                      <button className="btn btn-ghost btn-sm" onClick={() => duplicateCampaign(ci)} title="Duplicate">
                        <Copy size={14} />
                      </button>
                      {campaigns.length > 1 && (
                        <button className="btn btn-ghost btn-sm" onClick={() => removeCampaign(ci)} title="Remove" style={{ color: 'var(--error)' }}>
                          <Trash2 size={14} />
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Campaign body */}
                  {camp._open && (
                    <div style={{ padding: 20 }}>
                      {/* Campaign fields */}
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: 12, marginBottom: 12 }}>
                        <div className="form-group" style={{ margin: 0 }}>
                          <label>Campaign Name</label>
                          <input
                            type="text"
                            value={camp.name}
                            onChange={e => updateCampaign(ci, 'name', e.target.value)}
                            placeholder="e.g. Summer Sale 2026"
                          />
                        </div>
                        <div className="form-group" style={{ margin: 0 }}>
                          <label>Objective</label>
                          <select value={camp.objective} onChange={e => updateCampaign(ci, 'objective', e.target.value)}>
                            {OBJECTIVES.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
                          </select>
                        </div>
                        <div className="form-group" style={{ margin: 0 }}>
                          <label>Campaign Budget (CBO)</label>
                          <input
                            type="number"
                            value={camp.daily_budget}
                            onChange={e => updateCampaign(ci, 'daily_budget', e.target.value)}
                            placeholder="Leave empty for ABO"
                          />
                          <div className="hint" style={{ fontSize: 11 }}>
                            {camp.daily_budget ? `CBO: $${(camp.daily_budget / 100).toFixed(2)}/day` : 'ABO — set budget per ad set'}
                          </div>
                        </div>
                        <div className="form-group" style={{ margin: 0 }}>
                          <label>Status</label>
                          <select value={camp.status} onChange={e => updateCampaign(ci, 'status', e.target.value)}>
                            <option value="PAUSED">Paused</option>
                            <option value="ACTIVE">Active</option>
                          </select>
                        </div>
                      </div>

                      {/* Objective rules info */}
                      {objectiveRules && (
                        <div style={{
                          display: 'flex',
                          alignItems: 'flex-start',
                          gap: 10,
                          padding: '10px 14px',
                          marginBottom: 16,
                          background: 'var(--accent-subtle)',
                          border: '1px solid var(--accent)',
                          borderRadius: 'var(--radius-sm)',
                          fontSize: 12,
                        }}>
                          <Info size={14} style={{ color: 'var(--accent)', flexShrink: 0, marginTop: 1 }} />
                          <div>
                            <strong style={{ color: 'var(--accent)' }}>
                              {OBJECTIVES.find(o => o.value === camp.objective)?.label} Objective
                            </strong>
                            <span style={{ color: 'var(--text-secondary)', marginLeft: 6 }}>
                              — {objectiveRules.description}
                            </span>
                            {poRule && (
                              <div style={{ color: 'var(--warning, #f59e0b)', marginTop: 4 }}>
                                ⚠ Requires {poRule.label} as promoted object on each ad set
                              </div>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Ad Sets */}
                      {camp.ad_sets.map((adset, ai) => (
                        <div key={adset._key} style={{
                          border: '1px solid var(--border)',
                          borderRadius: 'var(--radius-md)',
                          marginBottom: 12,
                          overflow: 'hidden',
                        }}>
                          {/* Ad Set header */}
                          <div
                            style={{
                              display: 'flex', alignItems: 'center', gap: 10,
                              padding: '10px 16px',
                              background: 'var(--bg-primary)',
                              borderBottom: adset._open ? '1px solid var(--border)' : 'none',
                              cursor: 'pointer',
                            }}
                            onClick={() => updateAdSet(ci, ai, '_open', !adset._open)}
                          >
                            {adset._open ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                            <Target size={14} style={{ color: '#818cf8' }} />
                            <div style={{ flex: 1, fontSize: 13, fontWeight: 500 }}>
                              {adset.name || `Ad Set ${ai + 1}`}
                              <span className="text-xs text-muted" style={{ marginLeft: 8 }}>
                                {!campIsCBO && adset.daily_budget ? `$${(adset.daily_budget / 100).toFixed(2)}/day` : campIsCBO ? 'CBO' : 'No budget'} · {adset.ads.length} ad{adset.ads.length !== 1 ? 's' : ''} · {ALL_OPT_GOALS.find(g => g.value === adset.optimization_goal)?.label || adset.optimization_goal}
                              </span>
                            </div>
                            <div onClick={e => e.stopPropagation()}>
                              {camp.ad_sets.length > 1 && (
                                <button className="btn btn-ghost btn-sm" onClick={() => removeAdSet(ci, ai)} style={{ color: 'var(--error)' }}>
                                  <Trash2 size={13} />
                                </button>
                              )}
                            </div>
                          </div>

                          {adset._open && (
                            <div style={{ padding: 16 }}>
                              {/* Ad Set fields */}
                              <div style={{ display: 'grid', gridTemplateColumns: campIsCBO ? '1fr' : '1fr 1fr', gap: 12, marginBottom: 12 }}>
                                <div className="form-group" style={{ margin: 0 }}>
                                  <label>Ad Set Name</label>
                                  <input
                                    type="text"
                                    value={adset.name}
                                    onChange={e => updateAdSet(ci, ai, 'name', e.target.value)}
                                    placeholder="e.g. US Women 25-45"
                                  />
                                </div>
                                {/* Only show budget for ABO */}
                                {!campIsCBO && (
                                  <div className="form-group" style={{ margin: 0 }}>
                                    <label>Daily Budget (cents)</label>
                                    <input
                                      type="number"
                                      value={adset.daily_budget}
                                      onChange={e => updateAdSet(ci, ai, 'daily_budget', e.target.value)}
                                      placeholder="e.g. 2000 = $20/day"
                                    />
                                    {adset.daily_budget && (
                                      <div className="hint">= ${(adset.daily_budget / 100).toFixed(2)}/day</div>
                                    )}
                                  </div>
                                )}
                              </div>

                              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12, marginBottom: 12 }}>
                                <div className="form-group" style={{ margin: 0 }}>
                                  <label>Optimization Goal</label>
                                  <select value={adset.optimization_goal} onChange={e => updateAdSet(ci, ai, 'optimization_goal', e.target.value)}>
                                    {availableGoals.map(g => <option key={g.value} value={g.value}>{g.label}</option>)}
                                  </select>
                                </div>
                                <div className="form-group" style={{ margin: 0 }}>
                                  <label>Billing Event</label>
                                  <select value={adset.billing_event} onChange={e => updateAdSet(ci, ai, 'billing_event', e.target.value)}>
                                    {availableBilling.map(b => <option key={b} value={b}>{b}</option>)}
                                  </select>
                                </div>
                                <div className="form-group" style={{ margin: 0 }}>
                                  <label>Bid Strategy</label>
                                  <select value={adset.bid_strategy} onChange={e => updateAdSet(ci, ai, 'bid_strategy', e.target.value)}>
                                    {BID_STRATEGIES.map(b => <option key={b.value} value={b.value}>{b.label}</option>)}
                                  </select>
                                </div>
                              </div>

                              <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 12, marginBottom: 12 }}>
                                <div className="form-group" style={{ margin: 0 }}>
                                  <label>Status</label>
                                  <select value={adset.status} onChange={e => updateAdSet(ci, ai, 'status', e.target.value)} style={{ maxWidth: 200 }}>
                                    <option value="PAUSED">Paused</option>
                                    <option value="ACTIVE">Active</option>
                                  </select>
                                </div>
                              </div>

                              {/* Promoted Object — required for Sales, Leads, App */}
                              {poRule && (
                                <div style={{
                                  background: 'var(--bg-primary)',
                                  border: '1px solid var(--warning, #f59e0b)',
                                  borderRadius: 'var(--radius-sm)',
                                  padding: 12,
                                  marginBottom: 12,
                                }}>
                                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--warning, #f59e0b)', marginBottom: 10 }}>
                                    <AlertTriangle size={12} />
                                    Promoted Object (required)
                                  </div>

                                  {poRule.type === 'pixel' && (
                                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                                      <div className="form-group" style={{ margin: 0 }}>
                                        <label>Pixel</label>
                                        {pixels.length > 0 ? (
                                          <select value={adset.pixel_id} onChange={e => updateAdSet(ci, ai, 'pixel_id', e.target.value)}>
                                            <option value="">Select a pixel...</option>
                                            {pixels.map(p => <option key={p.id} value={p.id}>{p.name} (ID: {p.id})</option>)}
                                          </select>
                                        ) : pixelsLoading ? (
                                          <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 0' }}>
                                            <Loader size={14} style={{ animation: 'spin 1s linear infinite', color: 'var(--text-muted)' }} />
                                            <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Loading pixels...</span>
                                          </div>
                                        ) : (
                                          <input type="text" value={adset.pixel_id} onChange={e => updateAdSet(ci, ai, 'pixel_id', e.target.value)} placeholder="e.g. 123456789012345" />
                                        )}
                                      </div>
                                      <div className="form-group" style={{ margin: 0 }}>
                                        <label>Conversion Event</label>
                                        <select
                                          value={adset.custom_event_type}
                                          onChange={e => updateAdSet(ci, ai, 'custom_event_type', e.target.value)}
                                        >
                                          <option value="PURCHASE">Purchase</option>
                                          <option value="ADD_TO_CART">Add to Cart</option>
                                          <option value="INITIATED_CHECKOUT">Initiated Checkout</option>
                                          <option value="ADD_PAYMENT_INFO">Add Payment Info</option>
                                          <option value="COMPLETE_REGISTRATION">Complete Registration</option>
                                          <option value="LEAD">Lead</option>
                                          <option value="VIEW_CONTENT">View Content</option>
                                          <option value="SEARCH">Search</option>
                                          <option value="OTHER">Other</option>
                                        </select>
                                      </div>
                                    </div>
                                  )}

                                  {poRule.type === 'page' && (
                                    <div className="form-group" style={{ margin: 0 }}>
                                      <label>Facebook Page</label>
                                      {pages.length > 0 ? (
                                        <select value={adset.promoted_page_id} onChange={e => updateAdSet(ci, ai, 'promoted_page_id', e.target.value)}>
                                          <option value="">Select a page...</option>
                                          {pages.map(p => <option key={p.id} value={p.id}>{p.name} (ID: {p.id})</option>)}
                                        </select>
                                      ) : pagesLoading ? (
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 0' }}>
                                          <Loader size={14} style={{ animation: 'spin 1s linear infinite', color: 'var(--text-muted)' }} />
                                          <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Loading pages...</span>
                                        </div>
                                      ) : (
                                        <input type="text" value={adset.promoted_page_id} onChange={e => updateAdSet(ci, ai, 'promoted_page_id', e.target.value)} placeholder="e.g. 123456789012345" />
                                      )}
                                    </div>
                                  )}

                                  {poRule.type === 'app' && (
                                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                                      <div className="form-group" style={{ margin: 0 }}>
                                        <label>App ID</label>
                                        <input
                                          type="text"
                                          value={adset.application_id}
                                          onChange={e => updateAdSet(ci, ai, 'application_id', e.target.value)}
                                          placeholder="e.g. 123456789012345"
                                        />
                                      </div>
                                      <div className="form-group" style={{ margin: 0 }}>
                                        <label>App Store URL</label>
                                        <input
                                          type="text"
                                          value={adset.object_store_url}
                                          onChange={e => updateAdSet(ci, ai, 'object_store_url', e.target.value)}
                                          placeholder="https://play.google.com/..."
                                        />
                                      </div>
                                    </div>
                                  )}
                                </div>
                              )}

                              {/* Targeting */}
                              <div style={{
                                background: 'var(--bg-primary)',
                                border: '1px solid var(--border)',
                                borderRadius: 'var(--radius-sm)',
                                padding: 12,
                                marginBottom: 16,
                              }}>
                                <div style={{ fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: 10 }}>
                                  Audience Targeting
                                </div>
                                <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: 12 }}>
                                  <div className="form-group" style={{ margin: 0 }}>
                                    <label>Countries</label>
                                    <input
                                      type="text"
                                      value={adset.countries}
                                      onChange={e => updateAdSet(ci, ai, 'countries', e.target.value)}
                                      placeholder="US, CA, GB"
                                    />
                                  </div>
                                  <div className="form-group" style={{ margin: 0 }}>
                                    <label>Age Range</label>
                                    <div className="flex gap-2 items-center">
                                      <input type="number" value={adset.age_min} onChange={e => updateAdSet(ci, ai, 'age_min', e.target.value)} style={{ width: 70 }} min="18" max="65" />
                                      <span className="text-muted text-xs">to</span>
                                      <input type="number" value={adset.age_max} onChange={e => updateAdSet(ci, ai, 'age_max', e.target.value)} style={{ width: 70 }} min="18" max="65" />
                                    </div>
                                  </div>
                                </div>
                              </div>

                              {/* Ads inside this ad set */}
                              <div style={{ fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: 8 }}>
                                Ads ({adset.ads.length})
                              </div>

                              {adset.ads.map((ad, adi) => (
                                <div key={ad._key} style={{
                                  background: 'var(--bg-primary)',
                                  border: '1px solid var(--border)',
                                  borderLeft: '3px solid var(--success)',
                                  borderRadius: 'var(--radius-sm)',
                                  padding: 14,
                                  marginBottom: 8,
                                }}>
                                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                                    <div className="flex items-center gap-2">
                                      <Image size={13} style={{ color: 'var(--success)' }} />
                                      <span style={{ fontSize: 12, fontWeight: 600 }}>{ad.name || `Ad ${adi + 1}`}</span>
                                    </div>
                                    {adset.ads.length > 1 && (
                                      <button className="btn btn-ghost btn-sm" onClick={() => removeAd(ci, ai, adi)} style={{ color: 'var(--error)' }}>
                                        <Trash2 size={12} />
                                      </button>
                                    )}
                                  </div>

                                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 10 }}>
                                    <div className="form-group" style={{ margin: 0 }}>
                                      <label>Ad Name</label>
                                      <input type="text" value={ad.name} onChange={e => updateAd(ci, ai, adi, 'name', e.target.value)} placeholder="e.g. Hero Image A" />
                                    </div>
                                    <div className="form-group" style={{ margin: 0 }}>
                                      <label>Facebook Page</label>
                                      {pages.length > 0 ? (
                                        <select value={ad.page_id} onChange={e => updateAd(ci, ai, adi, 'page_id', e.target.value)}>
                                          <option value="">Select a page...</option>
                                          {pages.map(p => <option key={p.id} value={p.id}>{p.name} (ID: {p.id})</option>)}
                                        </select>
                                      ) : pagesLoading ? (
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 0' }}>
                                          <Loader size={14} style={{ animation: 'spin 1s linear infinite', color: 'var(--text-muted)' }} />
                                          <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Loading pages...</span>
                                        </div>
                                      ) : (
                                        <input type="text" value={ad.page_id} onChange={e => updateAd(ci, ai, adi, 'page_id', e.target.value)} placeholder="Page ID" />
                                      )}
                                    </div>
                                  </div>

                                  <div className="form-group" style={{ margin: '0 0 10px' }}>
                                    <label>Destination URL</label>
                                    <input type="url" value={ad.link} onChange={e => updateAd(ci, ai, adi, 'link', e.target.value)} placeholder="https://yoursite.com/landing" />
                                  </div>

                                  <div className="form-group" style={{ margin: '0 0 10px' }}>
                                    <label>Primary Text</label>
                                    <textarea
                                      value={ad.message}
                                      onChange={e => updateAd(ci, ai, adi, 'message', e.target.value)}
                                      placeholder="The main text above your ad..."
                                      style={{ minHeight: 60 }}
                                    />
                                  </div>

                                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 10 }}>
                                    <div className="form-group" style={{ margin: 0 }}>
                                      <label>Headline</label>
                                      <input type="text" value={ad.headline} onChange={e => updateAd(ci, ai, adi, 'headline', e.target.value)} placeholder="Bold headline" />
                                    </div>
                                    <div className="form-group" style={{ margin: 0 }}>
                                      <label>Description</label>
                                      <input type="text" value={ad.description} onChange={e => updateAd(ci, ai, adi, 'description', e.target.value)} placeholder="Short description" />
                                    </div>
                                    <div className="form-group" style={{ margin: 0 }}>
                                      <label>CTA Button</label>
                                      <select value={ad.call_to_action_type} onChange={e => updateAd(ci, ai, adi, 'call_to_action_type', e.target.value)}>
                                        {CTA_TYPES.map(c => <option key={c} value={c}>{c.replace(/_/g, ' ')}</option>)}
                                      </select>
                                    </div>
                                  </div>
                                </div>
                              ))}

                              <button className="btn btn-ghost btn-sm" onClick={() => addAd(ci, ai)} style={{ marginTop: 4 }}>
                                <Plus size={13} />
                                Add Ad Variation
                              </button>
                            </div>
                          )}
                        </div>
                      ))}

                      <button className="btn btn-secondary btn-sm" onClick={() => addAdSet(ci)} style={{ marginTop: 4 }}>
                        <Plus size={13} />
                        Add Ad Set
                      </button>
                    </div>
                  )}
                </div>
              )})}

              <button
                className="btn btn-secondary"
                onClick={() => setCampaigns(prev => [...prev, makeCampaign()])}
                style={{ width: '100%', justifyContent: 'center', padding: '14px', marginBottom: 16 }}
              >
                <Plus size={16} />
                Add Another Campaign
              </button>
            </div>
          ) : (
            <div className="card">
              <textarea
                className="json-editor"
                value={jsonInput}
                onChange={e => setJsonInput(e.target.value)}
                spellCheck={false}
                style={{ minHeight: 400 }}
              />
            </div>
          )}

          {/* Bottom action bar */}
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            padding: '16px 20px',
            background: 'var(--bg-card)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-lg)',
          }}>
            <div className="text-sm text-muted">
              {(() => {
                try {
                  const c = countObjects();
                  return `${c.campaigns} campaign${c.campaigns !== 1 ? 's' : ''} · ${c.adsets} ad set${c.adsets !== 1 ? 's' : ''} · ${c.ads} ad${c.ads !== 1 ? 's' : ''}`;
                } catch { return 'Configure your campaigns above'; }
              })()}
            </div>
            <button className="btn btn-primary btn-lg" onClick={handleContinue}>
              Review & Launch
            </button>
          </div>
        </div>
      )}

      {/* ── Step 1: Review ── */}
      {step === 1 && (
        <div className="card">
          <div className="card-header">
            <h3>Review Before Launch</h3>
          </div>

          {(() => {
            const counts = countObjects();
            return (
              <div className="stats-grid" style={{ marginBottom: 24 }}>
                <div className="stat-card">
                  <div className="label"><Megaphone size={14} /> Campaigns</div>
                  <div className="value">{counts.campaigns}</div>
                </div>
                <div className="stat-card">
                  <div className="label"><Target size={14} /> Ad Sets</div>
                  <div className="value">{counts.adsets}</div>
                </div>
                <div className="stat-card">
                  <div className="label"><Image size={14} /> Ads</div>
                  <div className="value">{counts.ads}</div>
                </div>
              </div>
            );
          })()}

          {getPayload().campaigns.map((camp, ci) => (
            <div key={ci} style={{ marginBottom: 16 }}>
              <div style={{
                padding: '12px 16px',
                background: 'var(--bg-primary)',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border)',
                marginBottom: 8,
                display: 'flex', alignItems: 'center', gap: 10,
              }}>
                <Megaphone size={16} style={{ color: 'var(--accent)' }} />
                <div>
                  <div style={{ fontWeight: 600, fontSize: 13 }}>{camp.name}</div>
                  <div className="text-xs text-muted">
                    {OBJECTIVES.find(o => o.value === camp.objective)?.label || camp.objective} · {camp.status}
                    {camp.daily_budget ? ` · CBO $${(camp.daily_budget / 100).toFixed(2)}/day` : ' · ABO'}
                  </div>
                </div>
              </div>

              {(camp.ad_sets || []).map((adset, ai) => (
                <div key={ai} style={{ marginLeft: 28, marginBottom: 8 }}>
                  <div style={{
                    padding: '10px 14px',
                    background: 'var(--bg-primary)',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--border)',
                    borderLeft: '3px solid var(--accent)',
                    marginBottom: 4,
                    display: 'flex', alignItems: 'center', gap: 10,
                  }}>
                    <Target size={14} style={{ color: '#818cf8' }} />
                    <div>
                      <div style={{ fontWeight: 500, fontSize: 13 }}>{adset.name}</div>
                      <div className="text-xs text-muted">
                        {adset.daily_budget ? `$${(adset.daily_budget / 100).toFixed(2)}/day` : camp.daily_budget ? 'CBO' : 'No budget'} · {adset.targeting?.geo_locations?.countries?.join(', ')} · Ages {adset.targeting?.age_min}-{adset.targeting?.age_max} · {ALL_OPT_GOALS.find(g => g.value === adset.optimization_goal)?.label || adset.optimization_goal}
                        {adset.promoted_object && (
                          <> · Pixel: {adset.promoted_object.pixel_id || adset.promoted_object.page_id || adset.promoted_object.application_id}</>
                        )}
                      </div>
                    </div>
                  </div>

                  {(adset.ads || []).map((ad, adi) => (
                    <div key={adi} style={{
                      marginLeft: 28,
                      padding: '8px 14px',
                      background: 'var(--bg-primary)',
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid var(--border)',
                      borderLeft: '3px solid var(--success)',
                      marginBottom: 4,
                      display: 'flex', alignItems: 'center', gap: 10,
                    }}>
                      <Image size={13} style={{ color: 'var(--success)' }} />
                      <div>
                        <div style={{ fontWeight: 500, fontSize: 12 }}>{ad.name}</div>
                        <div className="text-xs text-muted">
                          {ad.headline || 'No headline'} · {ad.call_to_action_type?.replace(/_/g, ' ')}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          ))}

          <div className="mt-4 flex justify-between">
            <button className="btn btn-secondary" onClick={() => setStep(0)}>Back to Edit</button>
            <button className="btn btn-primary btn-lg" onClick={handleLaunch}>
              <Rocket size={16} />
              Launch All
            </button>
          </div>
        </div>
      )}

      {/* ── Step 2: Launching ── */}
      {step === 2 && (
        <div className="card">
          <div className="empty-state">
            <div style={{
              width: 64, height: 64, borderRadius: '50%',
              background: 'var(--accent-subtle)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              margin: '0 auto 16px',
              animation: 'pulse 1.5s ease-in-out infinite',
            }}>
              <Rocket size={28} style={{ color: 'var(--accent)' }} />
            </div>
            <h3>Launching campaigns...</h3>
            <p>Creating your campaigns, ad sets, and ads. This may take a moment.</p>
          </div>
        </div>
      )}

      {/* ── Step 3: Results ── */}
      {step === 3 && results && (
        <div className="card">
          <div className="card-header">
            <h3>Launch Results</h3>
            <button className="btn btn-primary" onClick={reset}>
              <Play size={14} />
              New Launch
            </button>
          </div>

          {results.created?.length > 0 && (
            <div style={{ marginBottom: 20 }}>
              <h4 style={{ fontSize: 13, fontWeight: 600, color: 'var(--success)', marginBottom: 8 }}>
                <CheckCircle size={14} style={{ verticalAlign: -2 }} /> Created ({results.created.length})
              </h4>
              <table>
                <thead>
                  <tr><th>Type</th><th>Name</th><th>ID</th></tr>
                </thead>
                <tbody>
                  {results.created.map((obj, i) => (
                    <tr key={i}>
                      <td><span className="badge active">{obj.type}</span></td>
                      <td style={{ fontWeight: 500 }}>{obj.name}</td>
                      <td className="font-mono text-xs">{obj.id}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {results.errors?.length > 0 && (
            <div>
              <h4 style={{ fontSize: 13, fontWeight: 600, color: 'var(--error)', marginBottom: 8 }}>
                <AlertCircle size={14} style={{ verticalAlign: -2 }} /> Errors ({results.errors.length})
              </h4>
              {results.errors.map((err, i) => (
                <div key={i} style={{
                  padding: '10px 14px',
                  background: 'var(--error-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  marginBottom: 6, fontSize: 13,
                }}>
                  <strong>[{err.type}] {err.name}:</strong>
                  {(err.errors || []).map((e, j) => (
                    <div key={j} className="text-xs" style={{ marginTop: 4 }}>{e}</div>
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
