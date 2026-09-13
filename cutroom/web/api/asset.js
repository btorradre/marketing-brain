import { requireRole, storageGet, storagePut, slugify } from "./_lib.js";

export default async function handler(req, res) {
  if (req.method === "GET") {
    if (!requireRole(req, res)) return;
    const path = (req.query.path || "").replace(/\.\./g, "");
    const r = await storageGet(`assets/${path}`);
    if (!r) return res.status(404).json({ error: "not found" });
    res.setHeader("Content-Type", r.headers.get("content-type") || "application/octet-stream");
    res.setHeader("Cache-Control", "private, max-age=86400");
    return res.send(Buffer.from(await r.arrayBuffer()));
  }
  if (req.method === "POST") {
    if (requireRole(req, res, "admin") !== "admin") return;
    const board = slugify(req.query.board || "misc");
    const name = (req.query.name || "file.png").replace(/[^A-Za-z0-9._\-]/g, "_");
    const stamp = Date.now().toString(36);
    const path = `${board}/${stamp}-${name}`;
    const chunks = [];
    for await (const chunk of req) chunks.push(chunk);
    await storagePut(`assets/${path}`, Buffer.concat(chunks),
      req.headers["content-type"] || "application/octet-stream");
    return res.json({ src: `/assets/${path}` });
  }
  res.status(405).json({ error: "method" });
}

export const config = { api: { bodyParser: false } };
