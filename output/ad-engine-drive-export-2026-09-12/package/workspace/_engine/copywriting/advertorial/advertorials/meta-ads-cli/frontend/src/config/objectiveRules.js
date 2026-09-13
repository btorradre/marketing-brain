/**
 * Meta Marketing API objective-to-optimization-goal mapping.
 *
 * When a campaign has a specific objective, only certain optimization goals,
 * billing events, and bid strategies are valid for its ad sets.
 *
 * Reference: Meta Marketing API v21.0 documentation
 */

export const OBJECTIVES = [
  { value: 'OUTCOME_TRAFFIC', label: 'Traffic' },
  { value: 'OUTCOME_AWARENESS', label: 'Awareness' },
  { value: 'OUTCOME_ENGAGEMENT', label: 'Engagement' },
  { value: 'OUTCOME_LEADS', label: 'Leads' },
  { value: 'OUTCOME_SALES', label: 'Sales' },
  { value: 'OUTCOME_APP_PROMOTION', label: 'App Promotion' },
];

export const ALL_OPT_GOALS = [
  { value: 'LINK_CLICKS', label: 'Link Clicks' },
  { value: 'LANDING_PAGE_VIEWS', label: 'Landing Page Views' },
  { value: 'IMPRESSIONS', label: 'Impressions' },
  { value: 'REACH', label: 'Reach' },
  { value: 'OFFSITE_CONVERSIONS', label: 'Conversions' },
  { value: 'LEAD_GENERATION', label: 'Lead Generation' },
  { value: 'POST_ENGAGEMENT', label: 'Post Engagement' },
  { value: 'THRUPLAY', label: 'ThruPlay' },
  { value: 'VALUE', label: 'Value' },
  { value: 'APP_INSTALLS', label: 'App Installs' },
  { value: 'AD_RECALL_LIFT', label: 'Ad Recall Lift' },
  { value: 'QUALITY_LEAD', label: 'Quality Lead' },
  { value: 'ENGAGED_USERS', label: 'Engaged Users' },
  { value: 'PAGE_LIKES', label: 'Page Likes' },
];

export const BID_STRATEGIES = [
  { value: 'LOWEST_COST_WITHOUT_CAP', label: 'Lowest Cost' },
  { value: 'LOWEST_COST_WITH_BID_CAP', label: 'Bid Cap' },
  { value: 'COST_CAP', label: 'Cost Cap' },
];

export const BILLING_EVENTS = ['IMPRESSIONS', 'LINK_CLICKS', 'THRUPLAY'];

export const CTA_TYPES = [
  'LEARN_MORE', 'SHOP_NOW', 'SIGN_UP', 'BOOK_TRAVEL', 'CONTACT_US',
  'DOWNLOAD', 'GET_OFFER', 'GET_QUOTE', 'SUBSCRIBE', 'WATCH_MORE',
];

/**
 * Promoted object requirements by objective.
 * Meta requires a promoted_object for certain objective+goal combos.
 *
 * Types:
 *   'pixel'  → { pixel_id, custom_event_type }
 *   'page'   → { page_id }
 *   'app'    → { application_id, object_store_url }
 *   null     → not required
 */
export const PROMOTED_OBJECT_RULES = {
  OUTCOME_SALES: {
    type: 'pixel',
    label: 'Facebook Pixel',
    fields: [
      { key: 'pixel_id', label: 'Pixel ID', placeholder: 'e.g. 123456789012345', required: true },
      {
        key: 'custom_event_type', label: 'Conversion Event', type: 'select', required: true,
        options: [
          { value: 'PURCHASE', label: 'Purchase' },
          { value: 'ADD_TO_CART', label: 'Add to Cart' },
          { value: 'INITIATED_CHECKOUT', label: 'Initiated Checkout' },
          { value: 'ADD_PAYMENT_INFO', label: 'Add Payment Info' },
          { value: 'COMPLETE_REGISTRATION', label: 'Complete Registration' },
          { value: 'LEAD', label: 'Lead' },
          { value: 'VIEW_CONTENT', label: 'View Content' },
          { value: 'SEARCH', label: 'Search' },
          { value: 'OTHER', label: 'Other' },
        ],
      },
    ],
  },
  OUTCOME_LEADS: {
    type: 'page',
    label: 'Facebook Page',
    fields: [
      { key: 'page_id', label: 'Page ID', placeholder: 'e.g. 123456789012345', required: true },
    ],
  },
  OUTCOME_APP_PROMOTION: {
    type: 'app',
    label: 'App',
    fields: [
      { key: 'application_id', label: 'App ID', placeholder: 'e.g. 123456789012345', required: true },
      { key: 'object_store_url', label: 'App Store URL', placeholder: 'https://play.google.com/store/apps/details?id=...', required: true },
    ],
  },
};

/**
 * Mapping: campaign objective → allowed optimization goals for ad sets.
 * The first goal in each array is the recommended default.
 */
export const OBJECTIVE_RULES = {
  OUTCOME_TRAFFIC: {
    optimization_goals: ['LINK_CLICKS', 'LANDING_PAGE_VIEWS', 'IMPRESSIONS', 'REACH'],
    default_goal: 'LINK_CLICKS',
    billing_events: ['IMPRESSIONS', 'LINK_CLICKS'],
    default_billing: 'IMPRESSIONS',
    description: 'Drive traffic to your website or app',
  },
  OUTCOME_AWARENESS: {
    optimization_goals: ['REACH', 'IMPRESSIONS', 'AD_RECALL_LIFT', 'THRUPLAY'],
    default_goal: 'REACH',
    billing_events: ['IMPRESSIONS'],
    default_billing: 'IMPRESSIONS',
    description: 'Maximize reach and brand awareness',
  },
  OUTCOME_ENGAGEMENT: {
    optimization_goals: ['POST_ENGAGEMENT', 'IMPRESSIONS', 'REACH', 'THRUPLAY', 'PAGE_LIKES', 'ENGAGED_USERS'],
    default_goal: 'POST_ENGAGEMENT',
    billing_events: ['IMPRESSIONS'],
    default_billing: 'IMPRESSIONS',
    description: 'Get more engagement on your posts or page',
  },
  OUTCOME_LEADS: {
    optimization_goals: ['LEAD_GENERATION', 'LINK_CLICKS', 'LANDING_PAGE_VIEWS', 'QUALITY_LEAD'],
    default_goal: 'LEAD_GENERATION',
    billing_events: ['IMPRESSIONS'],
    default_billing: 'IMPRESSIONS',
    description: 'Collect leads for your business',
  },
  OUTCOME_SALES: {
    optimization_goals: ['OFFSITE_CONVERSIONS', 'VALUE', 'LINK_CLICKS', 'LANDING_PAGE_VIEWS'],
    default_goal: 'OFFSITE_CONVERSIONS',
    billing_events: ['IMPRESSIONS'],
    default_billing: 'IMPRESSIONS',
    description: 'Drive purchases and conversions',
  },
  OUTCOME_APP_PROMOTION: {
    optimization_goals: ['APP_INSTALLS', 'LINK_CLICKS', 'OFFSITE_CONVERSIONS', 'VALUE'],
    default_goal: 'APP_INSTALLS',
    billing_events: ['IMPRESSIONS'],
    default_billing: 'IMPRESSIONS',
    description: 'Get more app installs and engagement',
  },
};

/**
 * Get valid optimization goals for a given campaign objective.
 * Returns full goal objects (value + label) filtered by what's allowed.
 */
export function getGoalsForObjective(objective) {
  const rules = OBJECTIVE_RULES[objective];
  if (!rules) return ALL_OPT_GOALS;
  return ALL_OPT_GOALS.filter(g => rules.optimization_goals.includes(g.value));
}

/**
 * Get the default optimization goal for a campaign objective.
 */
export function getDefaultGoal(objective) {
  return OBJECTIVE_RULES[objective]?.default_goal || 'LINK_CLICKS';
}

/**
 * Get valid billing events for a given campaign objective.
 */
export function getBillingEventsForObjective(objective) {
  return OBJECTIVE_RULES[objective]?.billing_events || BILLING_EVENTS;
}

/**
 * Get the default billing event for a campaign objective.
 */
export function getDefaultBilling(objective) {
  return OBJECTIVE_RULES[objective]?.default_billing || 'IMPRESSIONS';
}

/**
 * Check if a goal is valid for a given objective.
 */
export function isGoalValidForObjective(goal, objective) {
  const rules = OBJECTIVE_RULES[objective];
  if (!rules) return true;
  return rules.optimization_goals.includes(goal);
}

/**
 * Get promoted object requirement for a campaign objective.
 * Returns the rule config or null if not required.
 */
export function getPromotedObjectRule(objective) {
  return PROMOTED_OBJECT_RULES[objective] || null;
}

/**
 * Check if a campaign is using CBO (Campaign Budget Optimization).
 * Returns true if the campaign has a budget set at the campaign level.
 */
export function isCBO(campaign) {
  return !!(campaign?.daily_budget || campaign?.lifetime_budget);
}
