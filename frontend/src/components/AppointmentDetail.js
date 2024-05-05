import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { useAuth } from '../context/AuthContext';
import { getDate, getDuration, getTime } from '../utils/utils';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';

function formatAppointmentType(type) {
    const typeMap = {
        'group': 'Group',
        'one_on_one': 'One on One',
        'drop_in': 'Drop In',
        'workshop': 'Workshop',
        'seminar': 'Seminar'
    };
    return typeMap[type] || type;
};

const AppointmentDetail = () => {
    const { token, userType } = useAuth();
    const { id } = useParams();
    const [appointment, setAppointment] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [booked, setBooked] = useState(false);

    useEffect(() => {
        const getAppointment = async () => {
            const endpoint = `/appointments/${id}`;
            try {
                const response = await axiosClient.get(endpoint);
                setAppointment(response.data);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching appointment:', error);
                setError(error?.response?.data?.detail || 'Error fetching appointment');
            }
        };

        getAppointment();
    }, [id, token]);

    const handleBooking = async () => {
        const endpoint = `/appointments/${id}/book-appointment`;


        try {
            await axiosClient.post(endpoint);
            setAppointment({ ...appointment, status: 'booked' });
            setBooked(true);
        } catch (error) {
            setError(error.response.data.detail || 'Error booking appointment')
        }
    };

    if (loading) {
        return <h1>Loading...</h1>;
    }


    return (
        <div>
            <h1>Appointment Detail</h1>
            {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
            {booked && <Alert variant="success" onClose={() => setBooked(false)} dismissible>Successfully registered for appointment</Alert>}
            <h2>{appointment.name}</h2>
            <div> Status: {appointment.status}</div>
            <div> Type: {formatAppointmentType(appointment.type)}</div>
            <div> Description: {appointment.description}</div>
            <div>Date: {getDate(appointment.app_start_time)}</div>
            <div>Time: {getTime(appointment.app_start_time)}</div>
            <div>Duration: {getDuration(appointment.app_start_time, appointment.app_end_time)}</div>
            <div>Location: {appointment.location}</div>
            <ul>
                {appointment.skills.map((skillItem, index) => (
                    <li key={index}> 
                        {skillItem.skill.name}
                    </li>
                ))}
            </ul> 
            {appointment.status === 'available' && userType === 'student' && (
                <Button variant="primary" className="mb-3" onClick={handleBooking}>Book Appointment</Button>
            )}
        </div>
        
    );
};

export default AppointmentDetail;