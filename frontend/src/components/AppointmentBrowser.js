import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getDate, getDuration, getTime } from '../utils/utils';
import axiosClient from '../utils/axiosClient';
import Card from 'react-bootstrap/Card';
import Nav from 'react-bootstrap/Nav';
import ListGroup from 'react-bootstrap/ListGroup';
import Alert from 'react-bootstrap/Alert';

const AppointmentBrowser = () => {
    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [appointmentType, setAppointmentType] = useState('');

    useEffect(() => {
        const getAppointments = async () => {
            let endpoint = `/appointments`;
            const params = {};
            params.appointment_status = 'available'

            if (appointmentType) {
                params.appointment_type = appointmentType;
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
    }, [appointmentType]);

    const handleSelect = (selectedKey) => {
        setAppointmentType(selectedKey);
    }
    

    if (loading) {
        return <h1>Loading...</h1>
    }

    return (
        <>
            <Card className="mb-3">
                <Card.Header>
                    <Card.Title>Appointments</Card.Title>
                </Card.Header>
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
                        </ListGroup.Item>
                    
                        )): <Alert variant="info">No appointments found</Alert>}
            </ListGroup>

                </Card.Body>    
            </Card>
        </>
    );
}

export default AppointmentBrowser;