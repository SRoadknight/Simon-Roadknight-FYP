import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { Link } from 'react-router-dom';

const StaffBrowser = () => {
    const [staff, setStaff] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchStaff = async () => {
            try {
                const response = await axiosClient.get('/staff');
                setStaff(response.data);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching staff:', error);
                setError(error);
            }
        };
        fetchStaff();
    }, []);

    if (loading) {
        return <h1>Loading...</h1>
    }

    if (error) {
        return <div>Error fetching staff: {error.message}</div>;
    }

    return (
        <>
           {staff.length > 0 ? staff.map((staffMember) => {
                return (
                     <div key={staffMember.id}>
                          <h2>{staffMember.user.first_name} {staffMember.user.last_name}</h2>
                          <div>Staff ID: {staffMember.id}</div>
                          <div>Email: {staffMember.user.email_address}</div>
                          <Link to={`/staff/${staffMember.id}/appointments`}>View Appointments</Link>
                     </div>
                )
              }) : <div>No staff found</div>}
        </>
    )
}


export default StaffBrowser;