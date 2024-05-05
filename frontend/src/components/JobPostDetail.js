import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useParams } from 'react-router-dom';
import axiosClient from '../utils/axiosClient';
import { cleanData } from '../utils/utils';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import ApplicationForm from '../forms/ApplicationForm';
import UpdateJobPostForm from '../forms/UpdateJobPostForm';
import Alert from 'react-bootstrap/Alert';


function jobPostStatusMap(status) {
    const statusMap = {
        'ongoing': 'Ongoing',
        'closed': 'Closed',
        'removed': 'Removed'
    };
    return statusMap[status];
}

function stageMap(stage) {
    const stageMap = {
        'applied': 'Applied',
        'interview': 'Interview',
        'offer': 'Offer',
        'rejected': 'Rejected'
    };
    return stageMap[stage];
}

function jobTypeMap(jobType) {
    const jobTypeMap = {
        'placement/internship': 'Placement/Internship',
        'graduate': 'Graduate'
    };
    return jobTypeMap[jobType];
}

const JobPostDetail = () => {
    const { userType } = useAuth();
    const { id:jobPostId } = useParams();
    const [jobPost, setJobPost] = useState(null);
    const [loading, setLoading] = useState(true);
    const [hasApplied, setHasApplied] = useState(false);
    const [applicationId, setApplicationId] = useState('');
    const [applicants, setApplicants] = useState([]);
    const [error, setError] = useState('');


    useEffect(() => {   
        const fetchJobPost = async () => {
            const jobPostEndpoint = `/job-posts/${jobPostId}`;
            const studentApplicationsEndpoints = `/students/me/job-applications`;
            if (userType === 'staff') {
                const jobApplicationsEndpoint = `/job-posts/${jobPostId}/applications`;
                try {
                    const jobPostResponse = await axiosClient.get(jobPostEndpoint);
                    const jobApplicationsResponse = await axiosClient.get(jobApplicationsEndpoint);
                    setJobPost(jobPostResponse.data);
                    setApplicants(jobApplicationsResponse.data);
                    setLoading(false);
                } catch (error) {
                    console.error('Error fetching job post:', error);
                    setError('Error fetching job post');
                    setLoading(false);
                }
                return;
            } else {
                try {
                    const jobPostResponse = await axiosClient.get(jobPostEndpoint);
                    setJobPost(jobPostResponse.data);
                    let applicationId = null;
                    const studentApplicationsResponse = await axiosClient.get(studentApplicationsEndpoints);
                    studentApplicationsResponse.data.forEach(application => {
                        if (application.job_post.id === jobPostResponse.data.id) {
                            setHasApplied(true);
                            applicationId = application.id;
                        }
                    });
                    setApplicationId(applicationId);
                    setLoading(false);
                } catch (error) {
                    console.error('Error fetching job post:', error);
                    setError('Error fetching job post');
                    setLoading(false);
                }
            }

        };

        fetchJobPost();
    }, [jobPostId, userType]);

    const handleApplicationSubmit = async (newApplication) => {
     

        const cleanedData = cleanData(newApplication);
        const endpoint = `/job-posts/${jobPostId}/applications`;

        try {
            const response = await axiosClient.post(endpoint, cleanedData);
            setHasApplied(true);
            setApplicationId(response.data.id);
        } catch (error) {
            console.error('Error applying for job:', error);
        }
    };
    

    const handleSubmitUpdateJobPost = async (updatedJobPost) => {
        const endpoint = `/job-posts/${jobPostId}`;

        try {
            const cleanedData = cleanData(updatedJobPost);
            const response = await axiosClient.patch(endpoint, cleanedData);
            setJobPost(response.data);
        } catch (error) {
            console.error('Error updating job post:', error);
            setError('Error updating job post');
        }
    };
    

  

    if (loading) {
        return <div>Loading job post...</div>;
    }

    if (!jobPost) {
        return <div>Job post not found</div>;
    }

    return (
        <>
        {error && <Alert variant="danger">{error}</Alert>}
            <Card className="mb-4">
                <Card.Header>
                    <Card.Title>{jobPost.title}</Card.Title>
                    <Card.Text className="text-muted">{jobPost.location}</Card.Text>
                </Card.Header>
                <Card.Body>
                    <Card.Text>{jobPost.company_name}</Card.Text>
                    <Card.Text>{jobPost.description}</Card.Text>
                    
                    <Card.Text>{jobPost.salary}</Card.Text>
                    <Card.Text>{jobTypeMap(jobPost.job_type)}</Card.Text>
                    {/* tick or cross displayed for hiring multiple or not */}
                    <Card.Text>Hiring multiple candidates {jobPost.hiring_multiple_candidates ?  '✓' : '✗'}</Card.Text>
                    <Card.Text>{jobPost.degree_required}</Card.Text>
                    <Card.Text>{jobPost.deadline}</Card.Text>
                    <Card.Text as ="a" href={jobPost.website_url}>{jobPost.website_url}</Card.Text>
                    <Card.Text>{jobPostStatusMap(jobPost.status)}</Card.Text>
                    {userType === 'student' ? (
                        !hasApplied ? (
                            <ApplicationForm onFormSubmit={handleApplicationSubmit} />
                    ) : (
                        <Button variant="secondary" className="m-2" as={Link} to={`/applications/${applicationId}`}>View Application</Button>
                    )
                    ) : (
                        <UpdateJobPostForm jobPost={jobPost} onFormSubmit={handleSubmitUpdateJobPost} />
                    )}
                </Card.Body>
            </Card>

            {userType === 'staff' && 
            
            <>
                <Card.Title className="mb-4">Applicants</Card.Title>
                {applicants.length > 0 ? applicants.map(applicant => (
                    <Card key={applicant.id} className="mb-3">
                        <Card.Header>
                            <Card.Title as={Link} to={`/students/${applicant.student_id}`}>{applicant.student.user.first_name} {applicant.student.user.last_name}</Card.Title>
                        </Card.Header>
                        <Card.Body>
                            <Card.Text><strong>Date applied - </strong>{applicant.date_applied}</Card.Text>
                            <Card.Text><strong>Stage - </strong>{stageMap(applicant.stage)}</Card.Text>
                            <Button as={Link} to={`/applications/${applicant.id}`} variant="secondary">View Full Application</Button>
                        </Card.Body>
                    </Card>
                )) : <Alert variant="info">No applicants</Alert>}
            </>
                
            }

            </>
    );
};

export default JobPostDetail;