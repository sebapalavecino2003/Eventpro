import { useNavigate } from 'react-router-dom';
import './NotFound.css';

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="not-found-page">
      <h1 className="not-found-code">404</h1>
      <p className="not-found-text">Página no encontrada</p>
      <button className="btn btn-primary" onClick={() => navigate('/dashboard')}>
        Volver al Dashboard
      </button>
    </div>
  );
}
