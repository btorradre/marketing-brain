const META_API_VERSION = "v21.0";
const META_BASE_URL = `https://graph.facebook.com/${META_API_VERSION}`;

async function metaFetch<T>(
  endpoint: string,
  accessToken: string,
  params?: Record<string, string>
): Promise<T> {
  const url = new URL(`${META_BASE_URL}${endpoint}`);
  url.searchParams.set("access_token", accessToken);
  if (params) {
    Object.entries(params).forEach(([key, value]) =>
      url.searchParams.set(key, value)
    );
  }

  const response = await fetch(url.toString());
  const data = await response.json();

  if (data.error) {
    throw new Error(
      `Meta API Error: ${data.error.message} (code: ${data.error.code})`
    );
  }

  return data;
}

export async function getAdAccounts(accessToken: string) {
  return metaFetch<{
    data: Array<{ id: string; name: string; account_id: string }>;
  }>("/me/adaccounts", accessToken, { fields: "id,name,account_id" });
}

export async function getCampaigns(
  adAccountId: string,
  accessToken: string
) {
  return metaFetch<{ data: Array<any> }>(
    `/${adAccountId}/campaigns`,
    accessToken,
    {
      fields: "id,name,objective,status,created_time,updated_time",
      limit: "500",
    }
  );
}

export async function getAdSets(
  campaignId: string,
  accessToken: string
) {
  return metaFetch<{ data: Array<any> }>(
    `/${campaignId}/adsets`,
    accessToken,
    { fields: "id,name,status,targeting", limit: "500" }
  );
}

export async function getAds(adSetId: string, accessToken: string) {
  return metaFetch<{ data: Array<any> }>(
    `/${adSetId}/ads`,
    accessToken,
    {
      fields:
        "id,name,status,creative{id,thumbnail_url,image_url,video_id,body,title,call_to_action_type,object_story_spec}",
      limit: "500",
    }
  );
}

export async function getAdInsights(
  adId: string,
  accessToken: string,
  datePreset: string = "last_30d"
) {
  return metaFetch<{ data: Array<any> }>(`/${adId}/insights`, accessToken, {
    fields:
      "spend,impressions,reach,clicks,ctr,cpc,cpm,actions,action_values,cost_per_action_type,video_3_sec_watched_actions,video_thru_play_actions,video_avg_time_watched_actions,outbound_clicks,outbound_clicks_ctr,frequency,unique_clicks,unique_ctr",
    date_preset: datePreset,
  });
}

export async function getVideoData(
  videoId: string,
  accessToken: string
) {
  return metaFetch<{
    source: string;
    thumbnails: { data: Array<{ uri: string }> };
  }>(`/${videoId}`, accessToken, { fields: "source,thumbnails" });
}

export function getMetaOAuthUrl(): string {
  const appId = process.env.META_APP_ID;
  const redirectUri = `${process.env.NEXTAUTH_URL}/api/meta/callback`;
  const scopes =
    "ads_management,ads_read,business_management,read_insights";

  return `https://www.facebook.com/${META_API_VERSION}/dialog/oauth?client_id=${appId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${scopes}&response_type=code`;
}

export async function exchangeCodeForToken(
  code: string
): Promise<{ access_token: string; expires_in: number }> {
  const url = new URL(`${META_BASE_URL}/oauth/access_token`);
  url.searchParams.set("client_id", process.env.META_APP_ID!);
  url.searchParams.set("client_secret", process.env.META_APP_SECRET!);
  url.searchParams.set(
    "redirect_uri",
    `${process.env.NEXTAUTH_URL}/api/meta/callback`
  );
  url.searchParams.set("code", code);

  const response = await fetch(url.toString());
  return response.json();
}

export async function getLongLivedToken(
  shortToken: string
): Promise<{ access_token: string; expires_in: number }> {
  const url = new URL(`${META_BASE_URL}/oauth/access_token`);
  url.searchParams.set("grant_type", "fb_exchange_token");
  url.searchParams.set("client_id", process.env.META_APP_ID!);
  url.searchParams.set("client_secret", process.env.META_APP_SECRET!);
  url.searchParams.set("fb_exchange_token", shortToken);

  const response = await fetch(url.toString());
  return response.json();
}
