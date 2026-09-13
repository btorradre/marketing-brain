export default function StatusBadge({ status }) {
  const s = (status || '').toLowerCase();
  return <span className={`badge ${s}`}>{status}</span>;
}
