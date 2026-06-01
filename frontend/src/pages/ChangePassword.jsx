import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';
import './ChangePassword.css';

const INITIAL_STATE = {
  old_password: '',
  new_password: '',
  new_password_confirm: '',
};

export default function ChangePassword() {
  const navigate = useNavigate();
  const [form, setForm] = useState(INITIAL_STATE);
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    if (errors[e.target.name]) setErrors((prev) => ({ ...prev, [e.target.name]: '' }));
    setApiError('');
  };

  const validate = () => {
    const errs = {};
    if (!form.old_password) errs.old_password = 'Ingresa tu contraseña actual.';
    if (!form.new_password) errs.new_password = 'Ingresa una nueva contraseña.';
    if (form.new_password.length < 8) errs.new_password = 'Mínimo 8 caracteres.';
    if (!form.new_password_confirm) errs.new_password_confirm = 'Confirma la nueva contraseña.';
    if (form.new_password !== form.new_password_confirm) {
      errs.new_password_confirm = 'Las contraseñas no coinciden.';
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    setApiError('');
    setSuccess('');

    try {
      await authService.changePassword({
        old_password: form.old_password,
        new_password: form.new_password,
        new_password_confirm: form.new_password_confirm,
      });
      setSuccess('Contraseña actualizada correctamente.');
      setForm(INITIAL_STATE);
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
      setApiError(data?.detail || 'Error al cambiar la contraseña.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="change-password-page">
      <button className="btn btn-secondary" onClick={() => navigate('/profile')}>
        ← Volver al perfil
      </button>

      <div className="change-password-card">
        <h1>Cambiar Contraseña</h1>

        <form onSubmit={handleSubmit} noValidate>
          {apiError && <div className="form-error">{apiError}</div>}
          {success && <div className="form-success">{success}</div>}

          <div className="form-group">
            <label htmlFor="old_password">Contraseña actual</label>
            <input
              id="old_password"
              name="old_password"
              type="password"
              placeholder="Tu contraseña actual"
              value={form.old_password}
              onChange={handleChange}
              className={errors.old_password ? 'input-error' : ''}
            />
            {errors.old_password && <p className="error-text">{errors.old_password}</p>}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="new_password">Nueva contraseña</label>
              <input
                id="new_password"
                name="new_password"
                type="password"
                placeholder="Mínimo 8 caracteres"
                value={form.new_password}
                onChange={handleChange}
                className={errors.new_password ? 'input-error' : ''}
              />
              {errors.new_password && <p className="error-text">{errors.new_password}</p>}
            </div>

            <div className="form-group">
              <label htmlFor="new_password_confirm">Confirmar contraseña</label>
              <input
                id="new_password_confirm"
                name="new_password_confirm"
                type="password"
                placeholder="Repite la contraseña"
                value={form.new_password_confirm}
                onChange={handleChange}
                className={errors.new_password_confirm ? 'input-error' : ''}
              />
              {errors.new_password_confirm && (
                <p className="error-text">{errors.new_password_confirm}</p>
              )}
            </div>
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => navigate('/profile')}
            >
              Cancelar
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Cambiando...' : 'Cambiar Contraseña'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
