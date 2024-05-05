import { useParams, Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { useAuth } from '../context/AuthContext';
import { getDate, getTime } from '../utils/utils';

function formatEventType(type) {
    const typeMap = {
        'conference': 'Conference',
        'workshop': 'Workshop',
        'seminar': 'Seminar',
        'hackathon': 'Hackathon',
        'competition': 'Competition',
        'training': 'Training',
        'bootcamp': 'Bootcamp',
        'webinar': 'Webinar',
        'other': 'Other'
    
    };
    return typeMap[type] || type;
}

const EventDetail = () => {
    const { token, userType } = useAuth();
    const { id } = useParams();
    const [event, setEvent] = useState({});
    const [loading, setLoading] = useState(true);
    const [eventRegistrants, setEventRegistrants] = useState([]);
    const isStaff = userType === 'staff';
   

    useEffect(() => {
        const getEvent = async () => {
            const eventsEndpoint = `/events/${id}`;

            const registrationsEndpoint = isStaff
            ? `/events/${id}/registrations`
            : null;

            try {
                const response = await axiosClient.get(eventsEndpoint);
                setEvent(response.data);
                if (registrationsEndpoint) {
                    const registrantsResponse = await axiosClient.get(registrationsEndpoint);
                    setEventRegistrants(registrantsResponse.data);
                }
                setLoading(false);
            } catch (error) {
                console.error('Error fetching event:', error);
            }
        };

        getEvent();
    }, [id, token, isStaff]);

    if (loading) {
        return <h1>Loading...</h1>
    }

    return (
        <div>
            <div>
                <h1>{event.name}</h1>
                <div>Type: {formatEventType(event.event_type)}</div>
                <div>Date: {getDate(event.event_date)}</div>
                <div>Location: {event.event_location}</div>
                <div>Time: {getTime(event.event_date)}</div>
                <div>Description: {event.description}</div>
            </div>
            {isStaff && (
                <div>
                    <h2>Registrations</h2>
                    <ul>
                      

                        {eventRegistrants.length > 0 ? eventRegistrants.map((registrant) => (
                            <>
                                <div>Number of registrants: {eventRegistrants.length}</div>
                                <li key={registrant.student.id}>
                                    <Link to={`/students/${registrant.student.id}`}>{registrant.student.user.first_name} {registrant.student.user.last_name}</Link>
                                    <div> Registration Date: {getDate(registrant.registration_date)}</div>
                                    <hr />
                                </li>
                            </>
                        )) : <div>No registrants</div>}
                    </ul>
                </div>
            )}
        </div>
    
    );
}

export default EventDetail;