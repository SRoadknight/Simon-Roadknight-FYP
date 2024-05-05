import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useParams } from 'react-router-dom';
import axiosClient from '../utils/axiosClient';
import { getDate, getDuration, getTime } from '../utils/utils';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Nav from 'react-bootstrap/Nav';
import Alert from 'react-bootstrap/Alert';

const StaffAppointments = ({ showUIElements = true, limit = null }) => {
    const {id: staffId} = useParams();
    const { token, userType } = useAuth();
    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [appointmentType, setAppointmentType] = useState('');
    const [appointmentStatus, setAppointmentStatus] = useState('booked');

    useEffect(() => {
        const getAppointments = async () => {
            const isStaff = userType === 'staff';
            const params = {};
            let endpoint = '';
            if (!showUIElements && !isStaff) {
                endpoint = `/staff/${staffId}/appointments`
                params.appointment_status = 'available';
            } else if (!showUIElements && isStaff) {
                endpoint = `/staff/me/appointments`
                params.appointment_status = 'booked';
            } else {
                endpoint = isStaff
                ? `/staff/me/appointments`
                : `/staff/${staffId}/appointments`;

                params.appointment_status = 'available';

                if (isStaff) {
                    if (appointmentType) {
                        params.appointment_type = appointmentType;
                    }
                    if (appointmentStatus) {
                        params.appointment_status = appointmentStatus;
                    }
                }
            }
            try {
                const response = await axiosClient.get(endpoint, {params});
                setAppointments(response.data);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching appointments:', error);
            }   
        };

        getAppointments();
    }, [token, staffId, userType, appointmentType, appointmentStatus, showUIElements, limit]);


    const handleSelect = (selectedKey, event) => {
        const navId = event.target.id;
        if (navId.startsWith('type-')) {
            setAppointmentType(selectedKey);
        } else if (navId.startsWith('status-')) {
            setAppointmentStatus(selectedKey);
        }
    };



    if (loading) {
        return <h1>Loading...</h1>
    }

    return (
        <div>
            <Card className="mb-3">
                <Card.Header>
                    {showUIElements && <Card.Title>Appointments</Card.Title>}
                    {!showUIElements &&  userType === 'staff' && <Card.Title>Upcoming Appointments</Card.Title>}
                    {!showUIElements &&  userType === 'student' && <Card.Title>Available Appointments</Card.Title>}
                </Card.Header>
            {showUIElements && userType === 'staff' &&
                    <>
                    <Card.Body>
                    <Nav variant="underline" activeKey={appointmentType} onSelect={handleSelect}>
                        <Nav.Item>
                            <Nav.Link eventKey="" id="type-all">All Types</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="one_on_one" id="type-one_on_one">One on One</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="group" id="type-group">Group</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="other" id="type-other">Other</Nav.Link>
                        </Nav.Item>
                    </Nav>
                    </Card.Body>
                    <Card.Body>
                    <Nav variant="underline" activeKey={appointmentStatus} onSelect={handleSelect}>
                        <Nav.Item>
                            <Nav.Link eventKey="" id="status-all">All Statuses</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="booked" id="status-booked">Booked</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="available" id="status-available">Available</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="complete" id="status-complete">Completed</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="cancelled" id="status-cancelled">Cancelled</Nav.Link>
                        </Nav.Item>
                    </Nav>
                    </Card.Body>
                    </>
            
            }
                <Card.Body>
                <ul>
                {appointments.length > 0 ? appointments.map((appointment) => {
                    return (
                        <li key={appointment.id}>
                            <Link to={`/appointments/${appointment.id}`}>
                                {appointment.name} 
                            </Link>
                            <div>
                                Date: {getDate(appointment.app_start_time)}
                            </div>
                            <div>
                                Time: {getTime(appointment.app_start_time)} - {getTime(appointment.app_end_time)}
                            </div>
                            <div>
                                Duration: {getDuration(appointment.app_start_time, appointment.app_end_time)}
                            </div>
                        </li>
                    );
                }): <Alert variant="info">No appointments found</Alert>}
            </ul>

                </Card.Body>    
               
                <Card.Footer>
                    {showUIElements && userType === 'student' && 
                    <Button as={Link} to="/appointments" variant="secondary" className="m-2">All available appointments</Button>}
                    {!showUIElements && userType === 'student' && 
                    <Button as={Link} to={`/staff/${staffId}/appointments`} variant="secondary" className="m-2">View staff members available appointments</Button>}
                    {!showUIElements && userType === 'staff' && 
                    <Button as={Link} to="/staff/me/appointments" variant="secondary" className="m-2">View all my appointments</Button>}
                </Card.Footer>
               

            </Card>
        </div>
    );
}

export default StaffAppointments;