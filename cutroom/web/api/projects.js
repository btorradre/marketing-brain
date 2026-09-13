import { requireRole, loadProjects, saveProjects, storageList, storageGet, storagePut, slugify } from "./_lib.js";

export default async function handler(req, res) {
  if (req.method === "GET") {
    if (!requireRole(req, res)) return;
    const projects = await loadProjects();
    const counts = {};
    for (const o of await storageList("boards")) {
      try {
        const b = await (await storageGet(o.path)).json();
        const p = b.project || "general";
        counts[p] = (counts[p] || 0) + 1;
      } catch {}
    }
    return res.json(Object.entries(projects).map(([id, p]) => ({
      id, name: p.name || id, created: p.created || "", boards: counts[id] || 0,
    })));
  }
  if (req.method === "POST") {
    if (requireRole(req, res, "admin") !== "admin") return;
    const name = (req.body?.name || "").trim();
    if (!name) return res.status(400).json({ error: "need name" });
    const slug = slugify(name);
    const projects = await loadProjects();
    if (projects[slug]) return res.status(409).json({ error: "exists", id: slug });
    projects[slug] = { name, created: new Date().toISOString().slice(0, 10) };
    await saveProjects(projects);
    return res.json({ id: slug });
  }
  if (req.method === "DELETE") {
    if (requireRole(req, res, "admin") !== "admin") return;
    const slug = req.query.slug || "";
    if (slug === "general") return res.status(400).json({ error: "cannot delete General" });
    const projects = await loadProjects();
    delete projects[slug];
    await saveProjects(projects);
    for (const o of await storageList("boards")) {
      try {
        const b = await (await storageGet(o.path)).json();
        if ((b.project || "general") === slug) {
          b.project = "general";
          await storagePut(o.path, JSON.stringify(b, null, 1), "application/json");
        }
      } catch {}
    }
    return res.json({ ok: true });
  }
  res.status(405).json({ error: "method" });
}
