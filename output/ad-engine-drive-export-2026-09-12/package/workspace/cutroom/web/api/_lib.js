// Shared helpers for Cutroom serverless functions.
const SUPA = process.env.SUPABASE_URL?.replace(/\/$/, "");
const KEY = process.env.SUPABASE_SECRET_KEY;
const BUCKET = "cutroom";

export const supaHeaders = { apikey: KEY, Authorization: `Bearer ${KEY}` };

export async function storageGet(path) {
  const r = await fetch(`${SUPA}/storage/v1/object/${BUCKET}/${path}`, { headers: supaHeaders });
  if (!r.ok) return null;
  return r;
}

export async function storagePut(path, body, contentType) {
  const r = await fetch(`${SUPA}/storage/v1/object/${BUCKET}/${path}`, {
    method: "POST",
    headers: { ...supaHeaders, "Content-Type": contentType, "x-upsert": "true" },
    body,
  });
  if (!r.ok) throw new Error(`storage put ${path}: ${r.status} ${await r.text()}`);
}

export async function storageDelete(prefixes) {
  await fetch(`${SUPA}/storage/v1/object/${BUCKET}`, {
    method: "DELETE",
    headers: { ...supaHeaders, "Content-Type": "application/json" },
    body: JSON.stringify({ prefixes }),
  });
}

export async function storageList(prefix) {
  const out = [];
  const r = await fetch(`${SUPA}/storage/v1/object/list/${BUCKET}`, {
    method: "POST",
    headers: { ...supaHeaders, "Content-Type": "application/json" },
    body: JSON.stringify({ prefix, limit: 1000, offset: 0, sortBy: { column: "name", order: "asc" } }),
  });
  if (!r.ok) return out;
  for (const e of await r.json()) {
    const name = (prefix ? prefix + "/" : "") + e.name;
    if (e.id === null) out.push(...(await storageList(name)));
    else out.push({ path: name, updated: e.updated_at || e.created_at });
  }
  return out;
}

// Cutroom is open: no passcode, every visitor gets full admin rights.
// Signatures are kept so existing call sites work unchanged.
export function role() {
  return "admin";
}

export function requireRole() {
  return "admin";
}

export function slugify(s) {
  return (s || "").toLowerCase().trim().replace(/[^a-z0-9\-_ ]/g, "").replace(/[\s_]+/g, "-").slice(0, 60) || "board";
}

export async function loadProjects() {
  const r = await storageGet("projects.json");
  const projects = r ? await r.json() : {};
  if (!projects.general) projects.general = { name: "General", created: new Date().toISOString().slice(0, 10) };
  return projects;
}

export async function saveProjects(projects) {
  await storagePut("projects.json", JSON.stringify(projects, null, 1), "application/json");
}
