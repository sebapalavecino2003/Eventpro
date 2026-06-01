import { useState } from 'react';
import { Link } from 'react-router-dom';
import { authService } from '../services/authService';
import './ForgotPassword.css';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim()) {
      setError('Ingresa tu correo electrónico.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      await authService.forgotPassword(email.trim().toLowerCase());
      setSent(true);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.response?.data?.email?.[0] ||
        'Error al enviar el correo. Intenta de nuevo.',
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="forgot-page">
      <div className="forgot-card">
        <div className="forgot-header">
          <h1>Recuperar Contraseña</h1>
          <p className="forgot-subtitle">
            Ingresa tu correo y te enviaremos instrucciones
          </p>
        </div>

        {sent ? (
          <div className="forgot-sent">
            <p>
              Si el correo está registrado, recibirás instrucciones para
              restablecer tu contraseña.
            </p>
            <Link to="/login" className="btn btn-primary forgot-link">
              Volver a Iniciar Sesión
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} noValidate>
            {error && <div className="form-error">{error}</div>}

            <div className="form-group">
              <label htmlFor="email">Correo electrónico</label>
              <input
                id="email"
                type="email"
                placeholder="tu@correo.com"
                value={email}
                onChange={(e) => { setEmail(e.target.value); setError(''); }}
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary forgot-btn"
              disabled={loading}
            >
              {loading ? 'Enviando...' : 'Enviar Instrucciones'}
            </button>
          </form>
        )}

        <div className="forgot-footer">
          <span>¿Recordaste tu contraseña?</span>
          <Link to="/login">Inicia sesión</Link>
        </div>
      </div>
    </div>
  );
}
