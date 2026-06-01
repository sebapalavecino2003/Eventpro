import { useContext } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import MainLayout from '../layouts/MainLayout';
import Loading from './Loading';

export default function ProtectedRoute({ children }) {
  const { user, loading } = useContext(AuthContext);
  const location = useLocation();

  if (loading) return <Loading text="Verificando sesión..." />;

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <MainLayout>{children}</MainLayout>;
}
