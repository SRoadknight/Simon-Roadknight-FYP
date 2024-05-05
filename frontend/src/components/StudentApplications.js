import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { staffOrStudentRoute } from '../utils/utils';
import Card from 'react-bootstrap/Card';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import StudentJobTrackForm from '../forms/StudentJobTrackForm';
import { cleanData } from '../utils/utils';

const StudentApplications = ({ showUIElements = true, limit = null }) => {
    const { id: studentId } = useParams();
    const [applications, setApplications] = useState([]);
    const [error, setError] = useState('');
    const { token, userType } = useAuth();
    const [applicationStage, setApplicationStage] = useState('');

    useEffect(() => {
        const isStaff = userType === 'staff';
        const params = {};
        let endpoint = isStaff 
        ? `/students/${studentId}/job-applications`
        : `/students/me/job-applications`;
        if (applicationStage) {
            params.stage = applicationStage;
        }
        const fetchApplications = async () => {
            try {
                const response = await axiosClient.get(endpoint, {params});
                setApplications(response.data);
                limit && setApplications(response.data.slice(0, limit));
            } catch (error) {
                console.error('Error fetching student applications:', error);
                setError('Error fetching student applications');
            }
        };

        fetchApplications();
    }, [token, studentId, userType, applicationStage, showUIElements, limit]);

    const handleSelect = (eventKey) => {
        setApplicationStage(eventKey);
    };

    const handleSubmitNewExternalApplication = async (newApplication) => {
        let endpoint = userType === 'staff' ? `/students/${studentId}/job-posts` : `/students/job-posts`;

        try {
            const cleanedData = cleanData(newApplication);
            const response = await axiosClient.post(endpoint, cleanedData);
            const dbApplication = response.data;
            setApplications([dbApplication, ...applications]);
            return Promise.resolve(dbApplication);
        } catch (error) {
            console.error('Error posting job:', error);
            setError("Error creating job and application. Please try again.")
            return Promise.reject(error);
        }
    }; 



    return (
        <>
            <Card className="mb-3">
                <Card.Header>
                    <Card.Title>
                        {showUIElements ? 'Applications' : 'Recent Applications'}
                    </Card.Title>
                </Card.Header>
                <Card.Body>
                    {error && <Alert variant="danger">{error}</Alert>}
                    <StudentJobTrackForm onFormSubmit={handleSubmitNewExternalApplication} />
                    {!showUIElements && applications.length > 0 && 
                        <Link to={staffOrStudentRoute(userType, studentId, 'applications')}>
                            <Button variant="secondary" className="m-2">
                                {userType === 'staff' ? 'View student\'s applications' : 'View all my applications'}
                            </Button>
                        </Link>
                    }
                    <Button variant="secondary" className="m-2" as ={Link} to="/job-posts">Browse jobs</Button>
                

            {showUIElements &&
            <>
                <Card.Text className="text-muted mx-2 mt-2">Filter by stage</Card.Text>
                <Nav variant="underline" activeKey={applicationStage} onSelect={handleSelect}>
                    <Nav.Item>
                        <Nav.Link eventKey="">All</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="applied">Applied</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="interviewing">Interviewing</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="offer">Offered</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="accepted">Accepted</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="rejected">Rejected</Nav.Link>
                    </Nav.Item>

                </Nav>
                
            </>}
                </Card.Body>
            </Card>
                {applications.length > 0 ? applications.map((application) => (
                    <Card key={application.id} className="mb-4 p-4">
                        <Card.Body>
                            <Card.Text>
                            <Link to={`/job-posts/${application.job_post_id}`}>{application.job_post.title}</Link>
                            </Card.Text>
                       
                            <Card.Text>Date applied: {application.date_applied}</Card.Text>
                            <Card.Text>Company: {application.job_post.company_name}</Card.Text>
                            <Card.Text>Stage: {application.stage}</Card.Text>
                        </Card.Body>
                        <Card.Body>
                        <Button variant="secondary" as={Link} to={`/applications/${application.id}`}>View application</Button>
                        </Card.Body>
                    </Card>
                )) : <Alert variant="info">No applications found</Alert>}

        </>
    );
};

export default StudentApplications;