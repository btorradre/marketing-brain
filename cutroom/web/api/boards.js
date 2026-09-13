import { requireRole, storageList, storageGet, storagePut, loadProjects, slugify } from "./_lib.js";

export default async function handler(req, res) {
  if (req.method === "GET") {
    if (!requireRole(req, res)) return;
    const objs = await storageList("boards");
    const boards = await Promise.all(objs.map(async (o) => {
      const slug = o.path.replace(/^boards\//, "").replace(/\.json$/, "");
      try {
        const b = await (await storageGet(o.path)).json();
        return { id: slug, title: b.title || slug, project: b.project || "general",
                 cards: (b.cards || []).length, updated: new Date(o.updated).getTime() / 1000 };
      } catch { return null; }
    }));
    return res.json(boards.filter(Boolean).sort((a, b) => b.updated - a.updated));
  }
  if (req.method === "POST") {
    if (requireRole(req, res, "admin") !== "admin") return;
    const title = req.body?.title || "Untitled board";
    let project = req.body?.project || "general";
    if (!(project in (await loadProjects()))) project = "general";
    let slug = slugify(title);
    const existing = new Set((await storageList("boards")).map(o => o.path));
    let base = slug, i = 2;
    while (existing.has(`boards/${slug}.json`)) slug = `${base}-${i++}`;
    const board = { id: slug, title, project, created: new Date().toISOString().slice(0, 10),
                    cards: req.body?.cards || [], edges: req.body?.edges || [] };
    await storagePut(`boards/${slug}.json`, JSON.stringify(board, null, 1), "application/json");
    return res.json({ id: slug });
  }
  res.status(405).json({ error: "method" });
}
