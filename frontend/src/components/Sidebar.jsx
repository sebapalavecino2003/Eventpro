import { useLocation, useNavigate } from 'react-router-dom';
import './Sidebar.css';

const LINKS = [
  { path: '/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/events', label: 'Eventos', icon: '📅' },
  { path: '/calendar', label: 'Calendario', icon: '🗓️' },
];

export default function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <span className="sidebar-logo">EP</span>
        <span className="sidebar-title">EventPro</span>
      </div>

      <nav className="sidebar-nav">
        {LINKS.map((link) => {
          const active = location.pathname === link.path ||
            (link.path !== '/dashboard' && location.pathname.startsWith(link.path));
          return (
            <button
              key={link.path}
              className={`sidebar-link ${active ? 'active' : ''}`}
              onClick={() => navigate(link.path)}
            >
              <span className="sidebar-icon">{link.icon}</span>
              <span className="sidebar-label">{link.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
