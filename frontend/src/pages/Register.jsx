import { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './Register.css';

const INITIAL_STATE = {
  first_name: '',
  last_name: '',
  email: '',
  username: '',
  password: '',
  password_confirm: '',
};

export default function Register() {
  const [form, setForm] = useState(INITIAL_STATE);
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState('');
  const { register, loading } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    if (errors[e.target.name]) {
      setErrors((prev) => ({ ...prev, [e.target.name]: '' }));
    }
    setApiError('');
  };

  const validate = () => {
    const errs = {};

    if (!form.first_name.trim()) errs.first_name = 'El nombre es obligatorio.';
    if (!form.last_name.trim()) errs.last_name = 'Los apellidos son obligatorios.';
    if (!form.email.trim()) errs.email = 'El correo electrónico es obligatorio.';
    if (!form.username.trim()) errs.username = 'El nombre de usuario es obligatorio.';
    if (form.username.trim().length < 4) errs.username = 'Mínimo 4 caracteres.';
    if (!form.password) errs.password = 'La contraseña es obligatoria.';
    if (form.password.length < 8) errs.password = 'Mínimo 8 caracteres.';
    if (!form.password_confirm) errs.password_confirm = 'Confirma tu contraseña.';
    if (form.password !== form.password_confirm) {
      errs.password_confirm = 'Las contraseñas no coinciden.';
    }

    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      await register(form);
      navigate('/login', { state: { registered: true } });
    } catch (err) {
      const data = err.response?.data;
      if (data && typeof data === 'object' && !Array.isArray(data)) {
        const fieldErrors = {};
        let hasFieldError = false;
        for (const [key, msgs] of Object.entries(data)) {
          if (Array.isArray(msgs) && msgs.length > 0) {
            fieldErrors[key] = msgs[0];
            hasFieldError = true;
          }
        }
        if (hasFieldError) {
          setErrors(fieldErrors);
          return;
        }
      }
      setApiError(
        data?.detail || 'Error al registrar. Intenta de nuevo.',
      );
    }
  };

  return (
    <div className="register-page">
      <div className="register-card">
        <div className="register-header">
          <h1>Crear Cuenta</h1>
          <p className="register-subtitle">
            Regístrate para gestionar tus eventos
          </p>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          {apiError && <div className="form-error">{apiError}</div>}

          <div className="register-row">
            <div className="form-group">
              <label htmlFor="first_name">Nombres</label>
              <input
                id="first_name"
                name="first_name"
                type="text"
                placeholder="Tu nombre"
                value={form.first_name}
                onChange={handleChange}
                disabled={loading}
                className={errors.first_name ? 'input-error' : ''}
              />
              {errors.first_name && (
                <p className="error-text">{errors.first_name}</p>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="last_name">Apellidos</label>
              <input
                id="last_name"
                name="last_name"
                type="text"
                placeholder="Tus apellidos"
                value={form.last_name}
                onChange={handleChange}
                disabled={loading}
                className={errors.last_name ? 'input-error' : ''}
              />
              {errors.last_name && (
                <p className="error-text">{errors.last_name}</p>
              )}
            </div>
          </div>

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
              className={errors.email ? 'input-error' : ''}
            />
            {errors.email && <p className="error-text">{errors.email}</p>}
          </div>

          <div className="form-group">
            <label htmlFor="username">Nombre de usuario</label>
            <input
              id="username"
              name="username"
              type="text"
              placeholder="usuario123"
              value={form.username}
              onChange={handleChange}
              autoComplete="username"
              disabled={loading}
              className={errors.username ? 'input-error' : ''}
            />
            {errors.username && (
              <p className="error-text">{errors.username}</p>
            )}
          </div>

          <div className="register-row">
            <div className="form-group">
              <label htmlFor="password">Contraseña</label>
              <input
                id="password"
                name="password"
                type="password"
                placeholder="Mínimo 8 caracteres"
                value={form.password}
                onChange={handleChange}
                autoComplete="new-password"
                disabled={loading}
                className={errors.password ? 'input-error' : ''}
              />
              {errors.password && (
                <p className="error-text">{errors.password}</p>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="password_confirm">Confirmar contraseña</label>
              <input
                id="password_confirm"
                name="password_confirm"
                type="password"
                placeholder="Repite la contraseña"
                value={form.password_confirm}
                onChange={handleChange}
                autoComplete="new-password"
                disabled={loading}
                className={errors.password_confirm ? 'input-error' : ''}
              />
              {errors.password_confirm && (
                <p className="error-text">{errors.password_confirm}</p>
              )}
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary register-btn"
            disabled={loading}
          >
            {loading ? 'Registrando...' : 'Crear Cuenta'}
          </button>
        </form>

        <div className="register-footer">
          <span>¿Ya tienes cuenta?</span>
          <Link to="/login">Inicia sesión aquí</Link>
        </div>
      </div>
    </div>
  );
}
