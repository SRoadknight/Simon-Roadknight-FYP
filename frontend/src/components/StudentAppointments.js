import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useParams } from 'react-router-dom';
import axiosClient from '../utils/axiosClient';
import { getDate, getDuration, getTime } from '../utils/utils';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Nav from 'react-bootstrap/Nav';
import ListGroup from 'react-bootstrap/ListGroup';
import Alert from 'react-bootstrap/Alert';

const StudentAppointments = ({ showUIElements = true, limit = null }) => {
    const {id: studentId} = useParams();
    const { token, userType } = useAuth();
    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [appointmentType, setAppointmentType] = useState('');
    const [appointmentStatus, setAppointmentStatus] = useState('booked');

    useEffect(() => {
        const getAppointments = async () => {
            const isStaff = userType === 'staff';
            const params = {}; 

            let endpoint = isStaff
                ? `/students/${studentId}/appointments`
                : `/students/me/appointments`;

            if (appointmentType) {
                params.appointment_type = appointmentType;
            }

            if (appointmentStatus) {
                params.appointment_status = appointmentStatus;
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
    }, [token, studentId, userType, appointmentType, appointmentStatus, showUIElements, limit]);


    const handleUnregister = async (id) => {
        if (!window.confirm('Are you sure you want to cancel your booking for this appointment?')) {
            return;
        }
        const endpoint = `/appointments/${id}/cancel-booking`;
 

        try {
            await axiosClient.patch(endpoint);
            alert('Successfully unregistered for appointment');
            const updatedAppointments = appointments.map(appointment => {
                if (appointment.id === id) {
                    return { ...appointment, status: 'available' };
                }
                return appointment;
            }); 
            setAppointments(updatedAppointments);
        } catch (error) {
            console.error('Error unregistering for appointment:', error);
            alert('Error unregistering for appointment');
        }
    };

    const handleBooking = async (id) => {
        if (!window.confirm('Are you sure you want to book this appointment?')) {
            return;
        }
        const endpoint = `/appointments/${id}/book-appointment`;

        try {
            await axiosClient.post(endpoint);
            alert('Successfully registered for appointment');
            const updatedAppointments = appointments.map(appointment => {
                if (appointment.id === id) {
                    return { ...appointment, status: 'booked' };
                }
                return appointment;
            });
            setAppointments(updatedAppointments);
        } catch (error) {
            console.error('Error registering for appointment:', error);
            alert('Error registering for appointment');
        }
    };

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
        <>
            <Card className="mb-3">
                <Card.Header>
                    {showUIElements && <Card.Title>Booked Appointments</Card.Title>}
                    {!showUIElements &&  <Card.Title>Upcoming Appointments</Card.Title>}
                    
                    {!showUIElements && appointments.length > 0 && userType === 'staff' &&
                    <Button as={Link} to={`/students/${studentId}/appointments`} variant="secondary" className="m-2">View students appointments</Button>
                    }
                    {!showUIElements &&  appointments.length > 0 && userType === 'student' &&
                    <Button as={Link} to="/students/me/appointments" variant="secondary" className="m-2">View all my appointments</Button>
                    }
                    {userType === 'student' &&
                    <Button as={Link} to="/appointments" variant="secondary" className="m-2">Book an appointment</Button>
                    }
                </Card.Header>
            {showUIElements &&
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
                <ListGroup variant="flush">
                {appointments.length > 0 ? appointments.map((appointment) => (
                        <ListGroup.Item key={appointment.id}>
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
                            {showUIElements && userType === 'student' && appointment.status === 'booked' && (
                                <Button onClick={() => handleUnregister(appointment.id)}>Unregister</Button>
                            )}
                            {showUIElements && userType === 'student' && appointment.status === 'available' && (
                                <Button onClick={() => handleBooking(appointment.id)}>Book</Button>
                            )}
                        </ListGroup.Item>
                    
                        )): <Alert variant="info">No appointments found</Alert>}
            </ListGroup>

                </Card.Body>    

            </Card>
        </>
    );
}

export default StudentAppointments;