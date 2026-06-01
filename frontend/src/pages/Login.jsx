import { useState, useContext } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './Login.css';

const INITIAL_STATE = { email: '', password: '' };

export default function Login() {
  const [form, setForm] = useState(INITIAL_STATE);
  const [error, setError] = useState('');
  const { login, loading } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();
  const registered = location.state?.registered;

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.email.trim() || !form.password.trim()) {
      setError('Todos los campos son obligatorios.');
      return;
    }

    try {
      await login(form.email.trim().toLowerCase(), form.password);
      navigate('/dashboard');
    } catch (err) {
      const detail =
        err.response?.data?.non_field_errors?.[0] ||
        err.response?.data?.detail ||
        'Error al iniciar sesión. Verifica tus credenciales.';
      setError(detail);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <h1>Iniciar Sesión</h1>
          <p className="login-subtitle">
            Ingresa a tu panel de gestión de eventos
          </p>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          {registered && (
            <div className="form-success">
              Cuenta creada exitosamente. Ahora inicia sesión.
            </div>
          )}
          {error && <div className="form-error">{error}</div>}

          <div className="form-group">
            <label htmlFor="email">Correo electrónico</label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="tu@correo.com"
              value={form.email}
              onChange={handleChange}
              autoComplete="email"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="Tu contraseña"
              value={form.password}
              onChange={handleChange}
              autoComplete="current-password"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary login-btn"
            disabled={loading}
          >
            {loading ? 'Ingresando...' : 'Iniciar Sesión'}
          </button>
        </form>

        <div className="login-footer">
          <span>¿No tienes cuenta?</span>
          <Link to="/register">Regístrate aquí</Link>
        </div>
        <div className="login-forgot">
          <Link to="/forgot-password">¿Olvidaste tu contraseña?</Link>
        </div>
      </div>
    </div>
  );
}
