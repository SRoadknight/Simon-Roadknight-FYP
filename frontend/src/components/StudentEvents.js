import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useParams } from 'react-router-dom';
import axiosClient from '../utils/axiosClient';
import { getDate, getDuration, getTime } from '../utils/utils';
import Card from 'react-bootstrap/Card';
import Nav from 'react-bootstrap/Nav';
import ListGroup from 'react-bootstrap/ListGroup';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';

const StudentEvents = ({ showUIElements = true, limit = null }) => {
    const {id: studentId} = useParams();
    const { token, userType } = useAuth();
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [eventType, setEventType] = useState('');
    const [eventStatus, setEventStatus] = useState('upcoming');

    useEffect(() => {
        const getEvents = async () => {
            const isStaff = userType === 'staff';
            let endpoint = isStaff
                ? `/students/${studentId}/events`
                : `/students/me/events`;

            const params = {};

            if (eventType) {
                params.event_type = eventType;
            }
            if (eventStatus) {
                params.event_status = eventStatus;
            }

            try {
                const response = await axiosClient.get(endpoint, { params });
                setEvents(response.data);
                setLoading(false);

            } catch (error) {
                console.error('Error fetching events:', error);
            }
        };

        getEvents();
    }, [token, eventStatus, studentId, userType, eventType, showUIElements, limit]);


    const handleUnregister = async (id) => {
        if (!window.confirm('Are you sure you want to unregister for this event?')) {
            return;
        }
        const endpoint = `/events/${id}/unregister`;

        try {
            const updatedEvents = events.filter(event => event.id !== id);
            await axiosClient.delete(endpoint);
            setEvents(updatedEvents);

        } catch (error) {
            console.error('Error unregistering for event:', error);
        }
    }


    const handleSelect = (selectedKey, event) => {
        const navId = event.target.id;
        if (navId.startsWith('type-')) {
            setEventType(selectedKey);
        } else if (navId.startsWith('status-')) {
            setEventStatus(selectedKey);
        }
    };

    if (loading) {
        return <h1>Loading...</h1>
    }

    return (
        <> 
            <Card className="mb-3">
                <Card.Header>
                    {showUIElements && <Card.Title>Registered Events</Card.Title>}
                    {!showUIElements &&  <Card.Title>Upcoming Events</Card.Title>}
                    
                    {!showUIElements && userType === 'staff' &&
                    <Card.Text>
                        <Button as={Link} to={`/students/${studentId}/events`} className="m-2">View students events</Button>
                    </Card.Text>}
                    {!showUIElements && userType === 'student' &&
                        <Button as={Link} to="/students/me/events" className="m-2" variant="secondary">View my registered events</Button>
                    }
                    {!showUIElements && userType === 'student' &&
                    <Button as={Link} to="/events" className="m-2" variant="secondary">Register for events</Button>
                    }
                </Card.Header>
                {showUIElements && 
                <>
                    <Card.Body>
                    <Nav variant="underline" defaultActiveKey={eventType} onSelect={handleSelect}>
                        <Nav.Item>
                            <Nav.Link  eventKey="" id="type-all">All Event Types</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="workshop" id="type-workshop">Workshops</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="hackathon" id="type-hackathon">Hackathons</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="other" id="type-other">Other</Nav.Link>
                        </Nav.Item>
                    </Nav>
                    <Nav variant="underline" defaultActiveKey={eventStatus} onSelect={handleSelect}>
                        <Nav.Item>
                            <Nav.Link eventKey="" id="status-all">All Statuses</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="upcoming" id="status-upcoming">Upcoming</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="complete" id="status-complete">Complete</Nav.Link>
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
                        {events.length > 0 ? events.map((event) => (
                            <ListGroup.Item key={event.id}>
                                <Link to={`/events/${event.id}`}>{event.name}</Link>
                                <div>Date: {getDate(event.event_start_time)}</div>
                                <div>Location: {event.event_location}</div>
                                <div>Time: {getTime(event.event_start_time)}</div>
                                <div>Duration: {getDuration(event.event_start_time, event.event_end_time)}</div>
                                {showUIElements && event.status === 'upcoming' && (
                                    <Button onClick={() => handleUnregister(event.id)} className="m-2">Unregister</Button>
                                )}
                            </ListGroup.Item>
                        )) : <Alert variant="info">No events found</Alert>}
                    </ListGroup>
                </Card.Body>
            </Card>
        </>
    );
}

export default StudentEvents;