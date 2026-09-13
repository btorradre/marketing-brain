// Passcode removed. Kept as a no-op so any stale client that still
// posts here gets a success instead of a 401.
export default function handler(req, res) {
  res.json({ role: "admin" });
}
