import { supabase } from '../lib/supabase';

const API_BASE = '/api';

/** Safely convert an error item (string or object) to a readable string. */
function errorToString(e) {
  if (typeof e === 'string') return e;
  if (e && typeof e === 'object') {
    // Handle bulk error objects with nested errors array: {index, name, errors: [...]}
    if (Array.isArray(e.errors) && e.errors.length > 0) {
      const prefix = e.name ? `${e.name}: ` : '';
      return prefix + e.errors.map(errorToString).join(', ');
    }
    return e.error_user_msg || e.error_user_title || e.message || e.error || JSON.stringify(e);
  }
  return String(e);
}

/** Format an errors array into a single readable message. */
function formatErrors(errors, fallback) {
  if (!Array.isArray(errors) || errors.length === 0) return fallback;
  return errors.map(errorToString).join(', ');
}

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;

  // Get current Supabase session and attach JWT
  const { data: { session } } = await supabase.auth.getSession();
  const headers = { 'Content-Type': 'application/json' };
  if (session?.access_token) {
    headers['Authorization'] = `Bearer ${session.access_token}`;
  }

  const config = { headers, ...options };

  if (config.body && typeof config.body === 'object') {
    config.body = JSON.stringify(config.body);
  }

  const res = await fetch(url, config);

  // Handle 401 — sign out and redirect to login
  if (res.status === 401) {
    await supabase.auth.signOut();
    window.location.href = '/login';
    throw new Error('Session expired — please log in again');
  }

  const data = await res.json();

  if (!res.ok) {
    throw new Error(formatErrors(data.errors, data.error || `API error: ${res.status}`));
  }

  return data;
}

export const api = {
  // Config
  getConfig: () => request('/config'),

  // Campaigns
  listCampaigns: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/campaigns${qs ? '?' + qs : ''}`);
  },
  createCampaign: (data) => request('/campaigns', { method: 'POST', body: data }),

  // Ad Sets
  listAdSets: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/adsets${qs ? '?' + qs : ''}`);
  },
  createAdSet: (data) => request('/adsets', { method: 'POST', body: data }),
  updateAdSet: (id, data) => request(`/adsets/${id}`, { method: 'PATCH', body: data }),

  // Pixels & Pages
  listPixels: () => request('/pixels'),
  listPages: () => request('/pages'),

  // Ads
  listAds: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/ads${qs ? '?' + qs : ''}`);
  },
  createAd: (data) => request('/ads', { method: 'POST', body: data }),
  bulkCreateAds: (adsetId, ads) => request(`/adsets/${adsetId}/bulk-ads`, { method: 'POST', body: { ads } }),

  // Media Upload (uses FormData, bypasses JSON request helper)
  uploadMedia: async (file) => {
    const { data: { session } } = await supabase.auth.getSession();
    const headers = {};
    if (session?.access_token) {
      headers['Authorization'] = `Bearer ${session.access_token}`;
    }
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch('/api/media/upload', { method: 'POST', body: formData, headers });
    if (res.status === 401) {
      await supabase.auth.signOut();
      window.location.href = '/login';
      throw new Error('Session expired');
    }
    const data = await res.json();
    if (!res.ok) {
      throw new Error(formatErrors(data.errors, `Upload failed: ${res.status}`));
    }
    return data;
  },

  // Bulk
  executeBulk: (data) => request('/bulk', { method: 'POST', body: data }),

  // Token Management
  getTokenStatus: () => request('/token/status'),
  exchangeToken: (shortToken) => request('/token/exchange', { method: 'POST', body: { short_token: shortToken } }),
  getOAuthUrl: () => request('/token/oauth-url'),

  // Ad Accounts
  getAccounts: () => request('/accounts'),
  selectAccount: (accountId) => request('/accounts/select', { method: 'POST', body: { meta_account_id: accountId } }),

  // Health (public — no auth needed)
  health: () => request('/health'),
};
