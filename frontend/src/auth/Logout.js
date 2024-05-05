import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';


const Logout = () => {
    const { handleLogout } = useAuth();
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        setLoading(false);
        handleLogout();
        navigate('/login');
    }, [handleLogout, navigate]);

    return (
        <div>
            {loading && <h1>Logging out...</h1>}
        </div>
    );
}


export default Logout;