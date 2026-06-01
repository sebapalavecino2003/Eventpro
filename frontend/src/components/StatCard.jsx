import './StatCard.css';

export default function StatCard({ title, value, icon, color }) {
  return (
    <div className="stat-card" style={{ '--stat-color': color || 'var(--color-primary)' }}>
      <div className="stat-card-icon">{icon}</div>
      <div className="stat-card-info">
        <span className="stat-card-value">{value}</span>
        <span className="stat-card-title">{title}</span>
      </div>
    </div>
  );
}
