import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { Link } from 'react-router-dom';
import Nav from 'react-bootstrap/Nav';
import Card from 'react-bootstrap/Card';
import Alert from 'react-bootstrap/Alert';


function activityTypeMap(tag) {
    const tagMap = {
        'interview': 'Interview',
        'phone_call': 'Phone Call',
        'test': 'Test',
        'assessment_center': 'Assessment Center'
    }
    return tagMap[tag];
}


const UpcomingApplicationActivities = () => {
    const [activities, setActivities] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activityType, setActivityType] = useState('');
    const applicationTags = [
        'interview',
        'phone_call',
        'test',
        'assessment_center'
    ];


    useEffect(() => {
        const fetchActivities = async () => {
            let endpoint = `/job-applications/upcoming-activities`;
            const params = {};
            if (activityType) {
                params.activity_type = activityType;
            }
            try {
                const response = await axiosClient.get(endpoint);
                const currentDate = new Date();
                const dateInSevenDays = currentDate.setDate(currentDate.getDate() + 7);
                setActivities(response.data.filter(activity => new Date(activity.activity_date) < dateInSevenDays && new Date(activity.activity_date) >= new Date()));
                

                setLoading(false);
            } catch (error) {
                console.error('Error fetching upcoming activities:', error);
            }
        };

        fetchActivities();
    }, [activityType]);


    const handleSelect = (eventKey) => {
        setActivityType(eventKey);
    };

    if (loading) {
        return <h1>Loading...</h1>
    }

    return (
        <>
                <Card.Title className="mb-4">Upcoming Student Activities (Next 7 days) </Card.Title>
                
                <Card className="mb-3">
                    <Card.Body>
                        <Card.Text className="text-muted">Filter by activity type</Card.Text>
                        <Nav variant="underline" activeKey={activityType} onSelect={handleSelect}>
                            <Nav.Item>
                                <Nav.Link eventKey="">All</Nav.Link>
                            </Nav.Item>
                            {applicationTags.map(tag => (
                                <Nav.Item key={tag}>
                                    <Nav.Link eventKey={tag}>{activityTypeMap(tag)}</Nav.Link>
                                </Nav.Item>
                            ))}
                        </Nav>
                    </Card.Body>
                </Card>

                {activities.length > 0 ? activities.map((activity) => (
                    <Card key={activity.id} className="mb-4 p-4">
                        <Card.Body>
                            <Card.Text>
                                <Link to={`/job-applications/${activity.id}`}>{activity.title}</Link>
                            </Card.Text>
                            <Card.Text> 
                                <Link to={`/students/${activity.job_application.student_id}`}>
                                    {activity.job_application.student.user.first_name} {activity.job_application.student.user.last_name}
                                </Link>
                            </Card.Text>
                            <Card.Text>
                                <Link to={`/students/${activity.job_application.student.student_id}`}></Link>
                            </Card.Text>
                            <Card.Text>Date: {activity.activity_date}</Card.Text>
                            <Card.Text>Type: {activityTypeMap(activity.activity_type)}</Card.Text>
                        </Card.Body>

                    </Card>
                )) : <Alert variant="info">No upcoming activities</Alert>}
        </>
    );
}

export default UpcomingApplicationActivities;