import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';


const confidenceLevelsMap = {
    very_low: 'Very Low',
    low: 'Low',
    medium: 'Medium',
    high: 'High',
    very_high: 'Very High',
};

function getConfidenceLevelOptions() {
    return Object.entries(confidenceLevelsMap).map(([key, value]) => (
        <option key={key} value={key}>{value}</option>
    ));
}


const StudentInfoUpdateForm = ({ student, onFormSubmit }) => {
    const [formValues, setFormValues] = useState(student);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const handleChange = (event) => {
        const { name, type, checked, value } = event.target 
        const inputValue = type === 'checkbox' ? checked : value;
        setFormValues({...formValues, [name]: inputValue})
    };


    const handleSubmit = (event) => {
        event.preventDefault();
        onFormSubmit(formValues);
        closeModal();
    };


// To update: About, career and options confidence, employment status, checkboxes: Casual work experience, inernship and related work
    return (
        <>
            <Button variant="primary" onClick={openModal}>Update Profile</Button>
            <Modal show={isModalOpen} onHide={closeModal}>
                <Modal.Header>
                    <Modal.Title>Update Profile</Modal.Title>
                </Modal.Header>
                <Form onSubmit={handleSubmit}>
                    <Modal.Body>
                        <Form.Group controlId="about">
                            <Form.Label>About</Form.Label>
                            <Form.Control
                                as="textarea"
                                name="about"
                                value={formValues.about}
                                onChange={handleChange}
                            />
                        </Form.Group>
                        <Form.Group controlId="career_confidence_level">
                            <Form.Label>Career Confidence Level</Form.Label>
                            <Form.Select
                                name="career_confidence_level"
                                value={formValues.career_confidence_level || ''}
                                onChange={handleChange}
                            >
                                {getConfidenceLevelOptions()}
                            </Form.Select>
                        </Form.Group>
                        <Form.Group controlId="career_options_confidence_level">
                            <Form.Label>Career Options Confidence</Form.Label>
                            <Form.Select
                                name="career_options_confidence_level"
                                value={formValues.career_options_confidence_level || ''}
                                onChange={handleChange}
                            >
                                {getConfidenceLevelOptions()}
                            </Form.Select>
                        </Form.Group>
                        <Form.Group controlId="employment_status">
                            <Form.Label>Employment Status</Form.Label>
                            <Form.Select
                                name="employment_status"
                                value={formValues.employment_status}
                                onChange={handleChange}
                            >
                                <option value="employed">Employed</option>
                                <option value="unemployed">Unemployed</option>
                            </Form.Select>
                        </Form.Group>
                        <Form.Group controlId="casual_work_experience">
                            <Form.Check
                                type="checkbox"
                                label="Casual Work Experience"
                                name="casual_work_experience"
                                checked={formValues.casual_work_experience}
                                onChange={handleChange}
                            />
                        </Form.Group>
                        <Form.Group controlId="internship_experience">
                            <Form.Check
                                type="checkbox"
                                label="Internship Experience"
                                name="internship_experience"
                                checked={formValues.internship_experience}
                                onChange={handleChange}
                            />
                        </Form.Group>
                        <Form.Group controlId="related_work_experience">
                            <Form.Check
                                type="checkbox"
                                label="Related Work"
                                name="related_work_experience"
                                checked={formValues.related_work_experience}
                                onChange={handleChange}
                            />
                        </Form.Group>    
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={closeModal}>Close</Button>
                        <Button type="submit">Update Profile</Button>
                    </Modal.Footer>
                </Form>
            </Modal>
        </>
    );
}

export default StudentInfoUpdateForm;

