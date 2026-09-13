// No passcode: everyone is admin.
export default function handler(req, res) {
  res.json({ role: "admin" });
}
