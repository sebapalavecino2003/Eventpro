import { useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { authService } from '../services/authService';
import './ForgotPassword.css';

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const [form, setForm] = useState({
    password: '',
    password_confirm: '',
  });
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    if (errors[e.target.name]) {
      setErrors((prev) => ({ ...prev, [e.target.name]: '' }));
    }
    setApiError('');
  };

  const validate = () => {
    const errs = {};
    if (!form.password) errs.password = 'Ingresa una nueva contraseña.';
    if (form.password.length < 8) errs.password = 'Mínimo 8 caracteres.';
    if (!form.password_confirm) errs.password_confirm = 'Confirma la contraseña.';
    if (form.password !== form.password_confirm) {
      errs.password_confirm = 'Las contraseñas no coinciden.';
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    setApiError('');

    try {
      await authService.resetPassword(token, form.password, form.password_confirm);
      setSuccess(true);
    } catch (err) {
      const data = err.response?.data;
      if (data && typeof data === 'object') {
        const fieldErrors = {};
        let hasField = false;
        for (const [key, msgs] of Object.entries(data)) {
          if (Array.isArray(msgs) && msgs.length > 0) {
            fieldErrors[key] = msgs[0];
            hasField = true;
          }
        }
        if (hasField) {
          setErrors(fieldErrors);
          return;
        }
      }
      setApiError(data?.error || 'Error al restablecer la contraseña.');
    } finally {
      setLoading(false);
    }
  };

  if (!token) {
    return (
      <div className="forgot-page">
        <div className="forgot-card">
          <div className="forgot-header">
            <h1>Enlace inválido</h1>
            <p className="forgot-subtitle">
              El enlace para restablecer la contraseña no es válido o ha expirado.
            </p>
          </div>
          <div className="forgot-footer">
            <Link to="/forgot-password">Solicitar un nuevo enlace</Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="forgot-page">
      <div className="forgot-card">
        <div className="forgot-header">
          <h1>Restablecer Contraseña</h1>
          <p className="forgot-subtitle">Ingresa tu nueva contraseña</p>
        </div>

        {success ? (
          <div className="forgot-sent">
            <p>Tu contraseña se ha restablecido exitosamente.</p>
            <Link to="/login" className="btn btn-primary forgot-link">
              Iniciar Sesión
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} noValidate>
            {apiError && <div className="form-error">{apiError}</div>}

            <div className="form-group">
              <label htmlFor="password">Nueva contraseña</label>
              <input
                id="password"
                name="password"
                type="password"
                placeholder="Mínimo 8 caracteres"
                value={form.password}
                onChange={handleChange}
                className={errors.password ? 'input-error' : ''}
              />
              {errors.password && <p className="error-text">{errors.password}</p>}
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
                className={errors.password_confirm ? 'input-error' : ''}
              />
              {errors.password_confirm && (
                <p className="error-text">{errors.password_confirm}</p>
              )}
            </div>

            <button
              type="submit"
              className="btn btn-primary forgot-btn"
              disabled={loading}
            >
              {loading ? 'Restableciendo...' : 'Restablecer Contraseña'}
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
