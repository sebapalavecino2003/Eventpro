import { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { authService } from '../services/authService';
import './Profile.css';

export default function Profile() {
  const { user, updateUser } = useContext(AuthContext);
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    phone: user?.phone || '',
  });
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');
    try {
      const { data } = await authService.updateProfile(form);
      updateUser(data);
      setMessage('Perfil actualizado correctamente.');
      setEditing(false);
    } catch {
      setError('Error al actualizar perfil.');
    }
  };

  return (
    <div className="profile-page">
      <div className="profile-card">
        <div className="profile-avatar">
          {user?.first_name?.charAt(0)?.toUpperCase() || 'U'}
        </div>
        <h1 className="profile-name">
          {user?.first_name} {user?.last_name}
        </h1>
        <p className="profile-email">{user?.email}</p>
        <p className="profile-role">{user?.role === 'admin' ? 'Administrador' : 'Organizador'}</p>

        <div className="profile-actions">
          <button
            className="btn btn-primary"
            onClick={() => setEditing(!editing)}
          >
            {editing ? 'Cancelar' : 'Editar Perfil'}
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => navigate('/change-password')}
            style={{ marginLeft: '8px' }}
          >
            Cambiar Contraseña
          </button>
        </div>

        {editing && (
          <form className="profile-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Nombre</label>
              <input
                className="input"
                name="first_name"
                value={form.first_name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Apellido</label>
              <input
                className="input"
                name="last_name"
                value={form.last_name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Teléfono</label>
              <input
                className="input"
                name="phone"
                value={form.phone}
                onChange={handleChange}
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Guardar Cambios
            </button>
            {message && <p className="form-success">{message}</p>}
            {error && <p className="form-error">{error}</p>}
          </form>
        )}
      </div>
    </div>
  );
}
