import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { authStore } from '../stores/AuthStore';

export const useAuth = (requireAuth = false) => {
  const navigate = useNavigate();

  useEffect(() => {
    if (requireAuth && !authStore.isAuthenticated) {
      navigate('/login');
    }
  }, [requireAuth, navigate]);

  return {
    user: authStore.user,
    isAuthenticated: authStore.isAuthenticated,
    isMentor: authStore.isMentor,
    isLoading: authStore.isLoading,
  };
};

export default useAuth;

