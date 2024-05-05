import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

const UpdateJobPostForm = ({ jobPost, onFormSubmit }) => {
    const [formValues, setFormValues] = useState(jobPost);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormValues({ ...formValues, [name]: value });
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        onFormSubmit(formValues);
        closeModal();
    };

    return (


        <>
            <Button variant="primary" onClick={openModal}>Update Job Post</Button>
            <Modal show={isModalOpen} onHide={closeModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Update Job Post</Modal.Title>
                </Modal.Header>
                <Form onSubmit={handleSubmit}>
                    <Modal.Body>
                        <Form.Group controlId="title">
                            <Form.Label>Title</Form.Label>
                            <Form.Control
                                type="text"
                                name="title"
                                value={formValues.title}
                                onChange={handleChange}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="company_name">
                            <Form.Label>Company Name</Form.Label>
                            <Form.Control
                                type="text"
                                name="company_name"
                                value={formValues.company_name}
                                onChange={handleChange}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="description">
                            <Form.Label>Description</Form.Label>
                            <Form.Control
                                as="textarea"
                                name="description"
                                value={formValues.description}
                                onChange={handleChange}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="location">
                            <Form.Label>Location</Form.Label>
                            <Form.Control
                                type="text"
                                name="location"
                                value={formValues.location}
                                onChange={handleChange}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="salary">
                            <Form.Label>Salary</Form.Label>
                            <Form.Control
                                type="text"
                                name="salary"
                                value={formValues.salary}
                                onChange={handleChange}
                            />
                        </Form.Group>
                        <Form.Group controlId="job_type">
                            <Form.Label>Job Type</Form.Label>
                            <Form.Select
                                name="job_type"
                                value={formValues.job_type}
                                onChange={handleChange}
                                required
                            >
                                <option value="placement/internship">Placement/Internship</option>
                                <option value="graduate">Graduate</option>
                            </Form.Select>
                        </Form.Group>
                        <Form.Group controlId="hiring_multiple_candidates">
                            <Form.Check
                                type="checkbox"
                                name="hiring_multiple_candidates"
                                checked={formValues.hiring_multiple_candidates}
                                onChange={handleChange}
                            />
                            <Form.Label>Hiring Multiple Candidates</Form.Label>
                        </Form.Group>
                        <Form.Group controlId="degree_required">
                            <Form.Label>Degree Required</Form.Label>
                            <Form.Select
                                name="degree_required"
                                value={formValues.degree_required}
                                onChange={handleChange}
                                required
                            >
                                <option value="All grades">All grades</option>
                                <option value="2.2 and above">2.2 and above</option>
                                <option value="2.1 and above">2.1 and above</option>
                                <option value="First">First</option>
                                <option value="Master's and above">Masters and above</option>
                                <option value="2:2 and above (expected)">2:2 and above (expected)</option>
                                <option value="2:1 and above (expected)">2:1 and above (expected)</option>
                                <option value="First (expected)">First (expected)</option>
                            </Form.Select>
                        </Form.Group>
                        <Form.Group controlId="deadline">
                            <Form.Label>Deadline</Form.Label>
                            <Form.Control
                                type="date" 
                                name="deadline"
                                value={formValues.deadline}
                                onChange={handleChange}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="website_url">
                            <Form.Label>Website URL</Form.Label>
                            <Form.Control
                                type="url"  
                                name="website_url"
                                value={formValues.website_url || ''}
                                onChange={handleChange}
                            />
                        </Form.Group>
                        <Form.Group controlId="status">
                            <Form.Label>Status</Form.Label>
                            <Form.Select
                                name="status"
                                value={formValues.status}
                                onChange={handleChange}
                                required
                            >
                                <option value="ongoing">Ongoing</option>
                                <option value="closed">Closed</option>
                                <option value="removed">Removed</option>
                            </Form.Select>
                        </Form.Group>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={closeModal}>Close</Button>
                        <Button type="submit">Update Job Post</Button>
                    </Modal.Footer>
                </Form>
            </Modal>
        </>
    );
}

export default UpdateJobPostForm;