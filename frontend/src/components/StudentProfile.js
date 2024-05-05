import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { useAuth } from '../context/AuthContext';
import StudentApplications from './StudentApplications';
import StudentEvents from './StudentEvents';
import StudentDegrees from './StudentDegrees';
import { useParams } from 'react-router-dom';
import StudentAppointments from './StudentAppointments';
import { cleanData } from '../utils/utils';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import ListGroup from 'react-bootstrap/ListGroup';
import Col from 'react-bootstrap/Col';
import StudentActivties from './StudentActivities';
import StudentInfoUpdateForm from '../forms/StudentInfoUpdateForm';
import Alert from 'react-bootstrap/Alert';
import StudentInteractions from './StudentInteractions';


function careerConfidenceLevelMap(level) {
    const levelMap = {
        very_low: 'Very Low',
        low: 'Low',
        medium: 'Medium',
        high: 'High',
        very_high: 'Very High'
    }
    return levelMap[level] || null;
}

function employmentStatusMap(status) {
    const statusMap = {
        unemployed : 'Unemployed',
        casual_work : 'Casual Work',
        related_work : 'Related Work',
        related_work_graduate : 'Related Work (Graduate)',
        graduate_scheme : 'Graduate Scheme',
        graduate_level_work  : 'Graduate Level Work',
        internsip : 'Internship',
        placement_year : 'Placement Year',
        self_employed : 'Self Employed',
        other : 'Other'
    }
    return statusMap[status] || null;
}

const StudentProfile = () => {
    const { id: studentId } = useParams();
    const [profileData, setProfileData] = useState(null);
    const [error, setError] = useState('');
    const { userType } = useAuth();


    useEffect(() => {
        const isStaff = userType === 'staff';
        const endpoint = isStaff
            ? `/students/${studentId}`
            : `/students/me`;
        const fetchProfile = async () => {
            try {
                const response = await axiosClient.get(endpoint);
                setProfileData(response.data);
            } catch (error) {
                console.error('Error fetching student profile:', error);
                setError('Error fetching student profile');
            }
        };
        fetchProfile();
    }, [studentId, userType]);


    const handleSubmitUpdateStudentProfile = async (updatedProfileData) => {
        const isStaff = userType === 'staff';
        const endpoint = isStaff
            ? `/students/${studentId}`
            : `/students/me`;

        try {
            setError('');
            let cleanedData = cleanData(updatedProfileData);
            if (!cleanedData.about) {
                cleanedData.about = null;
            }
            const response = await axiosClient.patch(endpoint, cleanedData);
            setProfileData(response.data);
        } catch (error) {
            console.error('Error updating student profile:', error);
            setError('Error updating student profile');
        }
    };


    if (!profileData) {
        return <div>Loading student profile...</div>;
    }

    

    return (
        <>
            {error && <Alert variant="danger" dismissible onClose={() => setError('')} >{error}</Alert>}
                <Row>
                    <Col lg={8}>
            <Card className="mb-4">
                <Card.Header>
                    <Card.Title>Student Info</Card.Title>
                </Card.Header>
                <Card.Body>
                    <Card.Text> <strong>Student ID - </strong> {profileData.id}</Card.Text>
                    <Card.Text><strong>Email - </strong>  {profileData.user.email_address}</Card.Text>   
                </Card.Body>
                <ListGroup variant="flush">
                    <ListGroup.Item>Career confidence level: {profileData.career_confidence_level === null ? 'No confidence level available' : careerConfidenceLevelMap(profileData.career_confidence_level)}</ListGroup.Item>
                    <ListGroup.Item>Career options confidence level: {profileData.career_options_confidence_level === null ? 'No confidence level available' : careerConfidenceLevelMap(profileData.career_options_confidence_level)}</ListGroup.Item>
                    <ListGroup.Item> Current employment status: {employmentStatusMap(profileData.current_employment_status)}</ListGroup.Item>
                    <ListGroup.Item> Casual work experience: {profileData.casual_work_experience ? 'Yes' : 'No'}</ListGroup.Item>
                    <ListGroup.Item> Internship experience: {profileData.internship_experience ? 'Yes' : 'No'}</ListGroup.Item>
                    <ListGroup.Item> Related work experience: {profileData.related_work_experience ? 'Yes' : 'No'}</ListGroup.Item>
                    <ListGroup.Item> Placement year: {profileData.placement_year ? 'Yes' : 'No'}</ListGroup.Item>
                </ListGroup>
                <Card.Body>
                    <Card.Title>About</Card.Title>
                    <Card.Text> {profileData.about === null || profileData.about === '' ? 'No about information' : profileData.about} </Card.Text>
                </Card.Body>
                <Card.Body>
                    <Card.Title>Other Information</Card.Title>
                    <Card.Text> {profileData.other_academic_info === null || profileData.other_academic_info === '' ? 'No other academic information available' : profileData.other_academic_info} </Card.Text>
                    <StudentInfoUpdateForm student={profileData} onFormSubmit={handleSubmitUpdateStudentProfile} />
                </Card.Body>
                   
            </Card>    
            </Col> 
                <Col>
                <StudentDegrees />
                </Col>
            </Row>
        
            <Row>
            <Col lg={6}>
            <StudentApplications studentId={studentId} showUIElements={false} limit={5}/>
            </Col>
            <Col lg={6}>
            <StudentActivties studentId={studentId} showUIElements={false} limit={12}/>
            </Col>
            </Row>

            <Row>
                <Col>
                    <StudentInteractions studentId={studentId} showUIElements={false} limit={6}/>
                </Col>
            </Row>
            
            <Row>
            <Col>
            <StudentAppointments studentId={studentId} showUIElements={false} limit={5}/>
            </Col>
            <Col>
            <StudentEvents studentId={studentId} showUIElements={false} limit={5}/>
            </Col>
            </Row>     
        </>
    );
};

export default StudentProfile;