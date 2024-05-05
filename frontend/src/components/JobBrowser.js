import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axiosClient from '../utils/axiosClient';
import Card from 'react-bootstrap/Card';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';

const JobBrowser = () => {
    const [jobPosts, setJobPosts] = useState([]);
    const [recomnendations, setRecommendations] = useState([]);
    const [error, setError] = useState('');
    const { token, userType } = useAuth();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const isStaff = userType === 'staff';

                if (isStaff) {
                    const jobPostsEndpoint = '/job-posts';
                    try {
                        const response = await axiosClient.get(jobPostsEndpoint);
                        setJobPosts(response.data);
                    } catch (error) {
                        setError('Error fetching data');
                    }
                    return;
                }


                const recommendationsEndpoint = '/students/me/recommended-jobs';
                const jobPostsEndpoint = '/job-posts';
                const applicationsEndpoint = '/students/me/job-applications';

                const [recommendationsResponse, jobPostsResponse, applicationsResponse] = await Promise.all([
                    axiosClient.get(recommendationsEndpoint),
                    axiosClient.get(jobPostsEndpoint),
                    axiosClient.get(applicationsEndpoint)
                ]);

                const recommendationsWithApplications = recommendationsResponse.data.map(recommendation => ({
                    ...recommendation,
                    application: applicationsResponse.data.find(application => application.job_post_id === recommendation.id)
                }));

                const jobPostsWithApplications = jobPostsResponse.data.map(jobPost => ({
                    ...jobPost,
                    application: applicationsResponse.data.find(application => application.job_post_id === jobPost.id)
                }));

                setRecommendations(recommendationsWithApplications);
                setJobPosts(jobPostsWithApplications);

            } catch (error) {
                setError('Error fetching data');
            }
        };
        fetchData();
    }, [token, userType]);

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <>
        
            {userType === 'student' && 
            <>
            <Card.Title className="mb-4">Recommended Jobs</Card.Title>
            {recomnendations.length > 0 ? recomnendations.map(recomendation => (
            <Card key={recomendation.id} className="mb-3 p-4">
                <Card.Text as={Link} to={`/job-posts/${recomendation.id}`}>{recomendation.title}</Card.Text>
                <Card.Text>Company: {recomendation.company_name}</Card.Text>
                <Card.Text>Location: {recomendation.location}</Card.Text>
                <Card.Text>Salary: {recomendation.salary}</Card.Text>
                <Card.Text>Deadline: {recomendation.deadline}</Card.Text>
                {recomendation.application && <Button as ={Link} to={`/applications/${recomendation.application.id}`} variant="primary">View Application</Button>}
            </Card>
            )) : <Alert variant="info" className="mb-4">No recommendations right now. Update your "about" information or contact the careers team.</Alert>}
            </>
            }


            <Card.Title className="mb-4">All Jobs</Card.Title>
             
            {jobPosts.length > 0 ? jobPosts.map(jobPost => (
                <Card key={jobPost.id} className="mb-3 p-4">
                    <Card.Body>
                        <Card.Text as={Link} to={`/job-posts/${jobPost.id}`}>{jobPost.title}</Card.Text>
                        <Card.Text>Company: {jobPost.company_name}</Card.Text>
                        <Card.Text>Location: {jobPost.location}</Card.Text>
                        <Card.Text>Salary: {jobPost.salary}</Card.Text>
                        <Card.Text>Deadline: {jobPost.deadline}</Card.Text>
                        {jobPost.application && <Button as ={Link} to={`/applications/${jobPost.application.id}`} variant="primary">View Application</Button>}
                    </Card.Body>
                </Card>
            )) : <Alert variant="info" className="mb-4">No job posts</Alert>}
        </>

    );
}

export default JobBrowser;