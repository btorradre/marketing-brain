import { requireRole, storageGet, storagePut, storageDelete, storageList } from "./_lib.js";

const OK = /^[a-z0-9][a-z0-9\-_]*$/;

export default async function handler(req, res) {
  const slug = req.query.slug || "";
  if (!OK.test(slug)) return res.status(400).json({ error: "bad slug" });
  if (req.method === "GET") {
    if (!requireRole(req, res)) return;
    const r = await storageGet(`boards/${slug}.json`);
    if (!r) return res.status(404).json({ error: "not found" });
    return res.json(await r.json());
  }
  if (req.method === "PUT") {
    if (requireRole(req, res, "admin") !== "admin") return;
    const data = req.body || {};
    data.id = slug;
    await storagePut(`boards/${slug}.json`, JSON.stringify(data, null, 1), "application/json");
    return res.json({ ok: true });
  }
  if (req.method === "DELETE") {
    if (requireRole(req, res, "admin") !== "admin") return;
    const assets = (await storageList(`assets/${slug}`)).map(o => o.path);
    await storageDelete([`boards/${slug}.json`, ...assets]);
    return res.json({ ok: true });
  }
  res.status(405).json({ error: "method" });
}
