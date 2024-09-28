import {
  Navigate,
  useLocation,
} from 'react-router-dom';
import { useAuth0 } from "@auth0/auth0-react";
import ROUTES from '../../constants/Routes';

function RequireAuth({ children }: { children: React.ReactNode }) {

  const { isLoading, isAuthenticated } = useAuth0();
  const location = useLocation();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to={ROUTES.LOGIN} replace state={{ path: location }} />
  }

  return <>{children}</>;

}

export default RequireAuth;