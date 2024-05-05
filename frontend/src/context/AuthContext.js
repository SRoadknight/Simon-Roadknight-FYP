import { createContext, useContext, useEffect, useState } from 'react';
import { decodeJWT } from '../utils/jwtUtils';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userType, setUserType] = useState('');
    const [loading, setLoading] = useState(true);


    useEffect(() => {
        setLoading(true);
        if (token) {
            try {
                const decoded = decodeJWT(token);
                setIsAuthenticated(true);
                setUserType(decoded.user_type);
            } catch (error) {
                console.error("Error decoding token:", error);
                setIsAuthenticated(false);
                setUserType('');
            }
        } else {
            setIsAuthenticated(false);
            setUserType('');
        }
        setLoading(false);
    }, [token]);

    const handleLogin = (newToken) => {
        localStorage.setItem('token', newToken);
        setToken(newToken);
        const decodedToken = decodeJWT(newToken);
        setIsAuthenticated(true);
        setUserType(decodedToken.user_type);
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setIsAuthenticated(false);
        setUserType('');
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, userType, token, handleLogin, handleLogout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);