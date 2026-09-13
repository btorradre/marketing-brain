import Anthropic from "@anthropic-ai/sdk";
import { requireRole, storageGet, storagePut } from "./_lib.js";

const AI_SCHEMA = {
  type: "object",
  properties: {
    reply: { type: "string" },
    cards: {
      type: "array",
      items: {
        type: "object",
        properties: {
          type: { type: "string", enum: ["note", "label", "lane"] },
          x: { type: "integer" }, y: { type: "integer" },
          w: { type: "integer" }, h: { type: "integer" },
          title: { type: "string" }, text: { type: "string" },
          color: { type: "string" }, size: { type: "integer" },
        },
        required: ["type", "x", "y", "w", "h", "title", "text", "color", "size"],
        additionalProperties: false,
      },
    },
  },
  required: ["reply", "cards"],
  additionalProperties: false,
};

const AI_SYSTEM = `You are the AI layer of Cutroom, an internal Milanote-style whiteboard a direct-response marketing team uses for creative briefs and reference-ad storyboards.

You receive the full JSON of the current board plus an instruction from a team member. Respond with \`reply\` (one or two sentences to the user) and \`cards\` (new cards to add — empty if the instruction is a pure question).

Card types you may create:
- note: sticky card. title = short bold header (may be ""), text = body, color = background hex. Palette: "#f7f5ee" neutral, "#fdf3c9" script/idea yellow, "#f3dcE8" emotion pink, "#dff2e1" DO green, "#f9d9d4" DON'T red. Typical w 260-320, h ≈ 26 + 19 per ~34-char line of text (+24 if titled).
- label: floating headline. text = the words, size = font px (22 section, 34 title). h ≈ size + 14. color "" for default, or a hex.
- lane: dashed container rectangle behind a group. title = uppercase tab text. Draw it AROUND cards it should visually group (place it first in your list; it renders behind).

Coordinates are absolute pixels on an infinite canvas; y grows downward. Never overlap existing cards: the board summary includes the current bounding box — place new content below it (bounds.bottom + 80) unless the instruction says otherwise, laying cards out left-to-right in columns ~300px apart. For fields that don't apply, use "" for strings and 0 for size.

Ground everything in what is actually on the board; never invent studies, statistics, or citations. Write in plain direct-response language, no em dashes.`;

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });
  if (requireRole(req, res, "admin") !== "admin") return;
  const slug = req.body?.board || "";
  const prompt = (req.body?.prompt || "").trim();
  if (!/^[a-z0-9][a-z0-9\-_]*$/.test(slug) || !prompt)
    return res.status(400).json({ error: "need board and prompt" });
  const r = await storageGet(`boards/${slug}.json`);
  if (!r) return res.status(404).json({ error: "board not found" });
  const board = await r.json();
  const cards = board.cards || [];
  const bounds = cards.length ? {
    left: Math.min(...cards.map(c => c.x)), top: Math.min(...cards.map(c => c.y)),
    right: Math.max(...cards.map(c => c.x + c.w)), bottom: Math.max(...cards.map(c => c.y + c.h)),
  } : { left: 0, top: 0, right: 0, bottom: 0 };

  const client = new Anthropic();
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 16000,
    system: AI_SYSTEM,
    output_config: { format: { type: "json_schema", schema: AI_SCHEMA } },
    messages: [{
      role: "user",
      content: `BOARD JSON:\n${JSON.stringify({ title: board.title, bounds, cards })}\n\nINSTRUCTION:\n${prompt}`,
    }],
  });
  if (response.stop_reason === "refusal")
    return res.status(400).json({ error: "The AI declined this request." });
  const text = response.content.find(b => b.type === "text")?.text || "{}";
  const result = JSON.parse(text);
  let added = 0;
  for (const c of result.cards || []) {
    const card = {};
    for (const [k, v] of Object.entries(c)) {
      if (v !== "" && v !== 0 || k === "x" || k === "y") card[k] = v;
    }
    card.id = "ai" + Math.random().toString(36).slice(2, 10);
    board.cards = board.cards || [];
    board.cards.push(card);
    added++;
  }
  if (added) await storagePut(`boards/${slug}.json`, JSON.stringify(board, null, 1), "application/json");
  res.json({ reply: result.reply || "", added });
}
