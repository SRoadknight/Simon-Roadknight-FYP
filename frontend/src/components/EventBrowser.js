import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getDate, getTime } from '../utils/utils';
import axiosClient from '../utils/axiosClient';
import Card from 'react-bootstrap/Card';
import Nav from 'react-bootstrap/Nav';
import ListGroup from 'react-bootstrap/ListGroup';
import { getDuration } from '../utils/utils';


const EventBrowser = () => {
    const { token } = useAuth();
    const [events, setEvents] = useState([]);
    const [error, setError] = useState('');
    const [eventType, setEventType] = useState('');
    const [eventStatus, setEventStatus] = useState('upcoming');

    useEffect(() => {
        const fetchEvents = async () => {
            let endpoint = `/events`;
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
            } catch (error) {
                console.error('Error fetching events:', error);
                setError('Error fetching events');
            }
        }
        fetchEvents();
    }, [token, eventStatus, eventType]);

    const handleSelect = (selectedKey, event) => {
        const navId = event.target.id;
        if (navId.startsWith('type-')) {
            setEventType(selectedKey);
        } else if (navId.startsWith('status-')) {
            setEventStatus(selectedKey);
        }
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <> 
            <Card className="mb-3">
                <Card.Header>
                    <Card.Title>Events</Card.Title>
                </Card.Header>
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
                    </Card.Body>
                    <Card.Body>
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

                <Card.Body>
                    <ListGroup variant="flush">
                        {events.length > 0 ? events.map((event) => (
                            <ListGroup.Item key={event.id}>
                                <Link to={`/events/${event.id}`}>{event.name}</Link>
                                <div>Date: {getDate(event.event_start_time)}</div>
                                <div>Location: {event.event_location}</div>
                                <div>Time: {getTime(event.event_start_time)}</div>
                                <div>Duration: {getDuration(event.event_start_time, event.event_end_time)}</div>
                            </ListGroup.Item>
                        )) : <div>No events found</div>}
                    </ListGroup>
                </Card.Body>
            </Card>
        </>
    );
}

export default EventBrowser;