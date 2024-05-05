import { useAuth } from '../context/AuthContext';
import { Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute = ({ allowedUserTypes, children }) => {
    const { isAuthenticated, userType } = useAuth();


    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    if (allowedUserTypes && !allowedUserTypes.includes(userType)) {
        return <Navigate to="/" replace />;
    }

    return children ? children : <Outlet />;
};

export default ProtectedRoute;


