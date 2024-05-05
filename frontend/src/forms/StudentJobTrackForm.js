import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';



const StudentJobTrackForm = ({ onFormSubmit }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [error, setError] = useState(null);
    const [validated, setValidated] = useState(false);

    // State variables for form inputs (application data)
    const [stage, setStage] = useState('applied');
    const [dateApplied, setDateApplied] = useState('');
    const [assistedByCareers, setAssistedByCareers] = useState(false);

    // State variables for form inputs (job post data)
    const [title, setTitle] = useState('');
    const [companyName, setCompanyName] = useState('');
    const [description, setDescription] = useState('');
    const [location, setLocation] = useState('');
    const [salary, setSalary] = useState('');
    const [jobType, setJobType] = useState('graduate');
    const [hiringMultipleCandidates, setHiringMultipleCandidates] = useState(false);
    const [degreeRequired, setDegreeRequired] = useState('All grades');
    const [deadline, setDeadline] = useState('');
    const [websiteUrl, setWebsiteUrl] = useState('');
    const [jobStatus, setJobStatus] = useState('ongoing');


    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const resetForm = () => {
        setStage('applied');
        setDateApplied('');
        setAssistedByCareers(false);
        setTitle('');
        setCompanyName('');
        setDescription('');
        setLocation('');
        setSalary('');
        setJobType('graduate');
        setHiringMultipleCandidates(false);
        setDegreeRequired('All grades');
        setDeadline('');
        setWebsiteUrl('');
        setJobStatus('ongoing');
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null)
        const form = event.currentTarget;
        if (!form.checkValidity()) {
            event.stopPropagation();
            setValidated(true);
        } else {
            const postData = {
                stage: stage,
                date_applied: dateApplied === '' ? null : dateApplied,
                title,
                company_name: companyName,
                description,
                location,
                salary,
                job_type: jobType,
                hiring_multiple_candidates: hiringMultipleCandidates,
                degree_required: degreeRequired,
                deadline: deadline === '' ? null : deadline,
                website_url: websiteUrl,
                status: jobStatus,
                careers_plus_assisted: assistedByCareers
            };
            
            onFormSubmit(postData)
                .then (() => {
                    resetForm();
                    closeModal();
                    setValidated(false);
                })
                .catch((error) => {
                    setError(error?.response?.data?.message || 'An error occurred. Please try again.');
                });
        }

    };



    return (
        <>

        <Button onClick={openModal} className="m-2">Track external job application</Button>
        <Modal show={isModalOpen} onHide={closeModal}>
            <Modal.Header closeButton>
                <Modal.Title>Job post and application information</Modal.Title>
            </Modal.Header>
            
                <Form noValidate validated={validated} onSubmit={handleSubmit}>
                <Modal.Body>
                    <Form.Group className="mb-3">
                        <Form.Label>Stage</Form.Label>
                        <Form.Select aria-label="Select stage" value={stage} onChange={(event) => setStage(event.target.value)}>
                            <option value="applied">Applied</option>
                            <option value="interviewing">Interviewing</option>
                            <option value="offer">Offer</option>
                            <option value="accepted">Accepted</option>
                            <option value="rejected">Rejected</option>
                        </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Date Applied</Form.Label>
                        <Form.Control type="date" value={dateApplied} onChange={(event) => setDateApplied(event.target.value)} />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Title</Form.Label>
                        <Form.Control type="text" placeholder="Title" value={title} onChange={(event) => setTitle(event.target.value)} required minLength="3" />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Company Name</Form.Label>
                        <Form.Control 
                            type="text" 
                            placeholder="Company Name" 
                            value={companyName} 
                            onChange={(event) => setCompanyName(event.target.value)} 
                            required
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Description</Form.Label>
                        <Form.Control as="textarea" 
                            placeholder="Description" 
                            value={description} onChange={(event) => setDescription(event.target.value)} 
                            required
                            minLength="10"
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Location</Form.Label>
                        <Form.Control type="text" placeholder="Location" value={location} onChange={(event) => setLocation(event.target.value)} required/>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Salary</Form.Label>
                        <Form.Control type="text" placeholder="Salary" value={salary} onChange={(event) => setSalary(event.target.value)} />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Job Type</Form.Label>
                        <Form.Select aria-label="Select job type" value={jobType} onChange={(event) => setJobType(event.target.value)} required>
                            <option value="graduate">Graduate Job</option>
                            <option value="placement/internship">Placement / Internship</option>
                        </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Degree Required</Form.Label>
                        <Form.Select aria-label="Select degree required" value={degreeRequired} onChange={(event) => setDegreeRequired(event.target.value)} required>
                            <option value="All grades">All grades</option>
                            <option value="2:2 and above">2:2 and above</option>
                            <option value="2:1 and above">2:1 and above</option>
                            <option value="First">First class</option>
                            <option value="Master's and above">Master's and above</option>
                            <option value="2:2 and above (expected)">2:2 and above (expected)</option>
                            <option value="2:1 and above (expected)">2:1 and above (expected)</option>
                            <option value="First (expected)">First class (expected)</option>
                        </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Deadline</Form.Label>
                        <Form.Control type="date" value={deadline} onChange={(event) => setDeadline(event.target.value)} />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Website URL</Form.Label>
                        <Form.Control type="url" placeholder="Website URL" value={websiteUrl} onChange={(event) => setWebsiteUrl(event.target.value)} />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Job Status</Form.Label>
                        <Form.Select aria-label="Select job status" value={jobStatus} onChange={(event) => setJobStatus(event.target.value)}>
                            <option value="ongoing">Ongoing</option>
                            <option value="closed">Closed</option>
                        </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Check type="checkbox" label="Assisted by Careers+" checked={assistedByCareers} onChange={(event) => setAssistedByCareers(event.target.checked)} />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Check type="checkbox" label="Hiring Multiple Candidates" checked={hiringMultipleCandidates} onChange={(event) => setHiringMultipleCandidates(event.target.checked)} />
                    </Form.Group>
                    </Modal.Body>
                    <Modal.Footer>
                <Modal.Body>
                {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
                </Modal.Body>
                <Button variant="secondary" onClick={closeModal}>Close</Button>
                <Button variant="primary" type="submit">Submit</Button>
            </Modal.Footer>
                </Form>
          
          
        </Modal>
    </>
    )
};

export default StudentJobTrackForm;
