import {useState, useEffect} from 'react';
import { useAuth } from '../context/AuthContext';
import { useParams, Link } from 'react-router-dom';
import axiosClient from '../utils/axiosClient';
import Badge from 'react-bootstrap/Badge';
import Card from 'react-bootstrap/Card';
import StudentActivityForm from '../forms/StudentActivityForm';
import { getDate } from '../utils/utils';
import Row from 'react-bootstrap/Row';
import Alert from 'react-bootstrap/Alert';
import { staffOrStudentRoute } from '../utils/utils';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';


function formatActivityType(tag) {
    const tagMap = {
        'cv_review': 'CV Review',
        'mock_interview': 'Mock Interview',
        'networking': 'Networking',
        'job_search': 'Job Search',
        'application_support': 'Application Support',
        'career_development': 'Career Development',
        'psychometric_test_practice': 'Psychometric Test Practice',
        'assessment_centre_practice': 'Assessment Centre Practice',
        'other': 'Other'
    }
    return tagMap[tag];
}

const StudentActivities = ({ showUIElements = true, limit = null }) => {
    const {id: studentId} = useParams();
    const { userType } = useAuth();
    const [activities, setActivities] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedActivityTags, setSelectedActivityTags] = useState([]);
    const [filteredActivities, setFilteredActivities] = useState([]);
    const activityTags = [
        'cv_review',
        'mock_interview',
        'networking',
        'job_search',
        'application_support',
        'career_development',
        'psychometric_test_practice',
        'assessment_centre_practice',
        'other'
    ];
    const [colSize, setColSize] = useState('');


    useEffect(() => {
        setColSize(showUIElements ? 3 : 2);
        const isStaff = userType === 'staff';
        let endpoint = isStaff
            ? `/students/${studentId}/activities`
            : `/students/me/activities`;
        

        const getActivities = async () => {
            try {
                const response = await axiosClient.get(endpoint);
                const data = limit ? response.data.slice(0, limit) : response.data;
                setActivities(data);

                const filteredData = selectedActivityTags.length > 0
                    ? data.filter(activity => selectedActivityTags.includes(activity.activity_type))
                    : data;
                setFilteredActivities(filteredData);
                setLoading(false);

            } catch (error) {
                console.error('Error fetching activities:', error);
            }   
        };

        getActivities();
    }, [userType, showUIElements, limit, studentId, selectedActivityTags]);

    const toggleActivityTag = (tag) => {
        setSelectedActivityTags(prevSelectedActivityTags => 
            prevSelectedActivityTags.includes(tag)
            ? prevSelectedActivityTags.filter(t => t !== tag)
            : [...prevSelectedActivityTags, tag]
        );
    };

    const addActivity = (newActivity) => { 
        const data = limit ? [newActivity, ...activities.slice(0, limit - 1)] : [newActivity, ...activities];
        setActivities(data);
        const filteredData = selectedActivityTags.length > 0
            ? data.filter(activity => selectedActivityTags.includes(activity.activity_type))
            : data;
        setFilteredActivities(filteredData);
    };



    if (loading) {
        return <h1>Loading...</h1>
    }

    return (
        <>
            <Card className="mb-3">
                <Card.Header>
                    {showUIElements && <Card.Title>Activities</Card.Title>}
                    {!showUIElements && <Card.Title>Recent Activities</Card.Title>}
                </Card.Header>
                {showUIElements && 
                <Card.Body>
                    {activityTags.map(tag => (
                        <Badge
                            pill
                            key={tag}
                            bg={selectedActivityTags.includes(tag) ? 'primary' : 'secondary'}
                            onClick={() => toggleActivityTag(tag)}
                            style={{ cursor: 'pointer'}}
                            className="me-2"
                        >   
                            {formatActivityType(tag)} - {activities.filter(activity => activity.activity_type === tag).length}
                        </Badge>
                    ))}
                </Card.Body>}
                <Card.Body>
                    <StudentActivityForm onFormSubmit={addActivity}/>
                    {!showUIElements && activities.length > 0 &&
                        <Link to={staffOrStudentRoute(userType, studentId, 'activities')}>
                            <Button variant="secondary" className="m-2">
                                {userType === 'staff' ? 'View student\'s activities' : 'View all my activities'}
                            </Button>
                        </Link>}
                </Card.Body>
                </Card>
                        
                <Row xs={1} md={2} lg={colSize} className="g-4 mb-4">
                    {filteredActivities.length > 0 && filteredActivities.map((activity) => (
                        <Col key={activity.id}>
                        <Card className="mb-4 p-4">
                            <Card.Header>
                            <Card.Text>{activity.title}</Card.Text>
                            <Card.Text className="text-muted">{formatActivityType(activity.activity_type)}</Card.Text>
                            </Card.Header>
                            <Card.Body>
                            <Card.Text>{activity.description}</Card.Text>
                            <Card.Text>{activity.activity_date ? getDate(activity.activity_date) : 'No date'}</Card.Text>
                            </Card.Body>
                        </Card>
                        </Col>
                        
                        
                    ))}
                </Row>
                {filteredActivities.length === 0 && <Alert variant="info">No activities found</Alert>}
                    
           </>

    );
}

export default StudentActivities;
