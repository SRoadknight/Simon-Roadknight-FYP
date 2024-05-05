import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { cleanData } from '../utils/utils';
import axiosClient from '../utils/axiosClient';
import NewApplicationActivityForm from '../forms/NewApplicationActivityForm';
import UpdateApplicationForm from '../forms/UpdateApplicationForm';
import UpdateApplicationActivityForm from '../forms/UpdateApplicationActivityForm';
import Alert from 'react-bootstrap/Alert';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Badge from 'react-bootstrap/Badge';
import { getDate } from '../utils/utils';

function formatApplicationStage(stage) {
    const stageMap = {
        'applied': 'Applied',
        'interviewing': 'Interviewing',
        'offer': 'Offered',
        'accepted': 'Accepted',
        'rejected': 'Rejected'
    };
    return stageMap[stage];
}

function formatActivityType(tag) {
    const tagMap = {
        'interview': 'Interview',
        'phone_call': 'Phone Call',
        'test': 'Test',
        'assessment_center': 'Assessment Center',
        'take_home_project': 'Take Home Project',
        'follow_up': 'Follow Up',
        'general_note': 'General Note',
        'other': 'Other'
    };
    return tagMap[tag];
}


const ApplicationDetail = () => {
    const { id: applicationId } = useParams();
    const [application, setApplication] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [selectedTags, setSelectedTags] = useState([]);
    const [filteredActivities, setFilteredActivities] = useState([]);
    const { userType } = useAuth();
    const tags = [
        'interview',
        'phone_call',
        'test',
        'assessment_center',
        'take_home_project',
        'follow_up',
        'general_note',
        'other'
    ]


    useEffect(() => {
        const fetchApplication = async () => {
            const endpoint = `/job-applications/${applicationId}`;
            try {
                const response = await axiosClient.get(endpoint);
                setApplication(response.data);
                const filteredActivities = selectedTags.length > 0
                    ? response.data.activities.filter(activity => selectedTags.includes(activity.activity_type))
                    : response.data.activities;
                setFilteredActivities(filteredActivities);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching application:', error);
                setError('Error fetching application');
                setLoading(false);
            }
        };

        fetchApplication();
    }, [applicationId, selectedTags]);


    const toggleTag = (tag) => {
        setSelectedTags(prevSelectedTags =>
            prevSelectedTags.includes(tag)
            ? prevSelectedTags.filter(t => t !== tag)
            : [...prevSelectedTags, tag]
        );
    };

    const handleSubmitNewActivity = async (newActivity) => {
        try {
            const cleanedData = cleanData(newActivity);
            let endpoint =  `/job-applications/${applicationId}/activities`;
            const response = await axiosClient.post(endpoint, cleanedData);
            const dbActivity = response.data;
            const updatedActivities = [dbActivity, ...application.activities];
            setApplication({ ...application, activities: updatedActivities });
            setFilteredActivities([dbActivity, ...filteredActivities]);
            return Promise.resolve(dbActivity)
        } catch (error) {
            console.error('Error adding activity:', error);
            setError('Error fetching application');
            return Promise.reject(error);
        }
    };

    const handleSubmitUpdateApplication = async (updatedValues) => {
        const endpoint = `/job-applications/${applicationId}`;
        try {
            const cleanedData = cleanData(updatedValues);
            const response = await axiosClient.patch(endpoint, cleanedData);
            setApplication(response.data);
        } catch (error) {
            console.error('Error updating application:', error);
            setError('Error fetching application');
        }
    };

    const handleSubmitUpdateActivity = async (updatedActivity) => {
        const endpoint = `/job-applications/activities/${updatedActivity.id}`;
        try {
            const cleanedData = cleanData(updatedActivity);
            const response = await axiosClient.patch(endpoint, cleanedData);
            const updatedActivities = application.activities.map(activity => activity.id === updatedActivity.id ? response.data : activity);
            setApplication({ ...application, activities: updatedActivities });
            setFilteredActivities(filteredActivities.map(activity => activity.id === updatedActivity.id ? response.data : activity));
        } catch (error) {
            console.error('Error updating activity:', error);
            setError('Error updating activity');
        }
    };


    const handleDeleteActivity = async (activityId) => {
        if (window.confirm('Are you sure you want to delete this activity?')) {
            const endpoint = `/job-applications/activities/${activityId}`;
            try {
                await axiosClient.delete(endpoint);
                const updatedActivities = application.activities.filter(activity => activity.id !== activityId);
                setApplication({ ...application, activities: updatedActivities });
                setFilteredActivities(filteredActivities.filter(activity => activity.id !== activityId));
            } catch (error) {
                console.error('Error deleting activity:', error);
                setError('Error deleting activity');
            }
        }
    };


    if (loading) return <div>Loading application...</div>;
    if (!application) return <Alert variant="danger">
        Application not found - <Link to="/">Go back to your profile</Link>
        </Alert>;


    return (
        <>  
        {error && <Alert variant="danger" dismissible onClose={() => setError('')}>{error}</Alert>}

        
            <Row className="mb-4">
                <Col md={6} className="mb-2">
                    <Card> 
                        <Card.Header>
                            <Card.Title>Application Details</Card.Title>
                        </Card.Header>
                        <Card.Body>
                            <Card.Text> 
                                <Link to={userType === 'student' ? '/students/me' : `/students/${application.student_id}`}>
                                    {application.student.user.first_name} {application.student.user.last_name} 
                                </Link>
                            </Card.Text>
                            <Card.Text> <strong>Stage - </strong> {formatApplicationStage(application.stage)} </Card.Text>
                            <Card.Text> <strong>Date Applied - </strong> {application.date_applied} </Card.Text>
                            {application.notes && <Card.Text> <strong>Notes - </strong> {application.notes} </Card.Text>}
                            <Card.Text> <strong>Assisted by Careers+ - </strong> {application.careers_plus_assisted ? 'Yes' : 'No'} </Card.Text>
                            <UpdateApplicationForm application={application} onFormSubmit={handleSubmitUpdateApplication}/>
                        </Card.Body>
                    </Card>
                </Col>
                <Col md={6} className="mb-2">
                    <Card>
                        <Card.Header>
                            <Card.Title>Job Details</Card.Title>
                        </Card.Header>
                        <Card.Body>
                            <Card.Text> <strong>Title - </strong> {application.job_post.title} </Card.Text>
                            <Card.Text> <strong>Company - </strong> {application.job_post.company_name} </Card.Text>
                            <Card.Text> <strong>Location - </strong> {application.job_post.location} </Card.Text>
                            <Button variant="secondary" as={Link} to={`/job-posts/${application.job_post.id}`}>View Full Job Post</Button>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            <Card className="mb-3">
                <Card.Header>
                    <Card.Title>Application Activities</Card.Title>
                </Card.Header>
                <Card.Body>
                    {tags.map(tag => (
                        <Badge
                            pill
                            key={tag}
                            bg={selectedTags.includes(tag) ? 'primary' : 'secondary'}
                            onClick={() => toggleTag(tag)}
                            style={{ cursor: 'pointer'}}
                            className="me-2"    
                        >
                            {formatActivityType(tag)} - {application.activities.filter(activity => activity.activity_type === tag).length}
                        </Badge>
                    ))}
                </Card.Body>
                <Card.Body>
                    <NewApplicationActivityForm onFormSubmit={handleSubmitNewActivity}/>
                </Card.Body>
            </Card>

            <Row xs={1} md={2} lg={3} className="g-4 mb-4">
                {filteredActivities.length > 0 && filteredActivities.map((activity) => (
                    <Col key={activity.id}>
                        <Card>
                            <Card.Header>
                                <Card.Text>{activity.title}</Card.Text>
                                <Card.Text className="text-muted">{formatActivityType(activity.activity_type)}</Card.Text>
                            </Card.Header>
                            <Card.Body>
                                {activity.activity_date && <Card.Text> {getDate(activity.activity_date)} </Card.Text>}
                                {activity.activity_time && <Card.Text> {activity.activity_time} </Card.Text>}
                                {activity.notes && <Card.Text>{activity.notes} </Card.Text>}
                                {!activity.activity_date && !activity.activity_time && !activity.notes && <Card.Text> <strong>No information</strong> </Card.Text>}
                                <UpdateApplicationActivityForm activity={activity} onFormSubmit={handleSubmitUpdateActivity} />
                                <Button onClick={() => handleDeleteActivity(activity.id)} className="m-2">Delete</Button>
                            </Card.Body>
                        </Card>
                    </Col>
                ))}
            </Row>
        </>
    );

};

export default ApplicationDetail;