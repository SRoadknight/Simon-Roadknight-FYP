import { useState } from 'react';
import { cleanData } from '../utils/utils';
import axiosClient from '../utils/axiosClient';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import { useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Alert from 'react-bootstrap/Alert';

const StudentActivityForm = ({ onFormSubmit }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const { id: studentId } = useParams();
    const { userType } = useAuth();
    const [error, setError] = useState('');

    // State variables for form inputs
    const [title, setTitle] = useState('');
    const [activityType, setActivityType] = useState('other');
    const [description, setDescription] = useState('');
    const [activityDate, setActivityDate] = useState('');

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const resetForm = () => {
        setTitle('');
        setActivityType('other');
        setDescription('');
        setActivityDate('');
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const postData = {
            title,
            activity_type: activityType,
            description,
            activity_date: activityDate === '' ? null : activityDate,
        };

        try {
            const isStaff = userType === 'staff';
            const cleanedData = cleanData(postData);
            let endpoint = isStaff ? `/students/${studentId}/activities` : '/students/activities';
            const response = await axiosClient.post(endpoint, cleanedData);
            const dbActivity = response.data;
            onFormSubmit(dbActivity);
            resetForm();
            closeModal();
        } catch (error) {
            console.error('Error adding activity:', error);
            setError('Failed to add activity');
        }
    };

    return (
        <>

        <Button onClick={openModal} className="m-2">Add Activity</Button>
        <Modal show={isModalOpen} onHide={closeModal}>
            <Modal.Header closeButton>
                <Modal.Title>Add Activity</Modal.Title>
            </Modal.Header>
            <Form onSubmit={handleSubmit}>
                <Modal.Body>
                
                    <Form.Group className="mb-3">
                        <Form.Label>Title</Form.Label>
                        <Form.Control
                            type="text"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Activity Type</Form.Label>
                        <Form.Select
                            value={activityType}
                            onChange={(e) => setActivityType(e.target.value)}
                            
                        >
                            <option value="cv_review">CV Review</option>
                            <option value="mock_interview">Mock Interview</option>
                            <option value="networking">Networking</option>
                            <option value="job_search">Job Search</option>
                            <option value="application_support">Application Support</option>
                            <option value="career_development">Career Development</option>
                            <option value="psychometric_test_practice">Psychometric Test Practice</option>
                            <option value="assessment_centre_practice">Assessment Centre Practice</option>
                            <option value="other">Other</option>
                        </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                            as="textarea"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Activity Date</Form.Label>
                        <Form.Control
                            type="date"
                            value={activityDate}
                            onChange={(e) => setActivityDate(e.target.value)}
                        />
                    </Form.Group>
                </Modal.Body>
                <Modal.Body>
                {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
                </Modal.Body>
                <Modal.Footer>
                <Button variant="secondary" onClick={closeModal}>Close</Button>
                <Button variant="primary" type="submit">Add Activity</Button>
            </Modal.Footer>
                </Form>
        </Modal>
        </>
    );
}

export default StudentActivityForm;