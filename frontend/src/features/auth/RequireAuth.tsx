import { useEffect } from 'react';
import {
  Navigate,
  useLocation,
  useNavigate,
} from 'react-router-dom';
import { useAuth0 } from "@auth0/auth0-react";
import ROUTES from '../../constants/Routes';

function RequireAuth({ children }: { children: React.ReactNode }) {

  const { isAuthenticated } = useAuth0();

  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate(ROUTES.LOGIN, { state: { from: location } });
    }
  }, [isAuthenticated, navigate, location]);

  if (!isAuthenticated) {
    return <Navigate to={ROUTES.LOGIN} replace state={{ path: location }} />
  }

  return <>{children}</>;

}

export default RequireAuth;