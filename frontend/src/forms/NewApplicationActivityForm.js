import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert'

const NewApplicationActivityForm = ({ onFormSubmit }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    // State variables for form inputs
    const [title, setTitle] = useState('');
    const [activityDate, setActivityDate] = useState('');
    const [activityTime, setActivityTime] = useState('');
    const [activityType, setActivityType] = useState('other');
    const [notes, setNotes] = useState('');
    const [error, setError] = useState(null)
    const [validated, setValidated] = useState(false)

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);
    
    const resetForm = () => {
        setTitle('');
        setActivityDate('');
        setActivityTime('');
        setActivityType('other');
        setNotes('');
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null)
        const form = event.currentTarget;

        if (!form.checkValidity()) {
            event.stopPropagation();
            setValidated(true);
        } else {
            const postData = {
                title,
                activity_date: activityDate,
                activity_time: activityTime,
                activity_type: activityType,
                notes,
            };
            onFormSubmit(postData)
            .then(() => {
                resetForm();
                closeModal();
                setValidated(false)
            })
            .catch((error) => {
                setError(error?.response?.data?.message || 'An error occurred. Please try again.');
            });
        }
    }

    return (
        <>

        <Button onClick={openModal}>Add New Activity to Application</Button>
        <Modal show={isModalOpen} onHide={closeModal}>
            <Modal.Header closeButton>
                <Modal.Title>Activity details</Modal.Title>
            </Modal.Header>
                <Form noValidate validated={validated} onSubmit={handleSubmit}>
                <Modal.Body>
                    <Form.Group controlId="title">
                        <Form.Label>Title</Form.Label>
                        <Form.Control
                            type="text"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group controlId="activityDate">
                        <Form.Label>Date</Form.Label>
                        <Form.Control
                            type="date"
                            value={activityDate}
                            onChange={(e) => setActivityDate(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group controlId="activityTime">
                        <Form.Label>Time <Form.Text className="text-muted">(Not required)</Form.Text></Form.Label>
                        <Form.Control
                            type="time"
                            value={activityTime}
                            onChange={(e) => setActivityTime(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group controlId="activityType">
                        <Form.Label>Type</Form.Label>
                        <Form.Control
                            as="select"
                            value={activityType}
                            onChange={(e) => setActivityType(e.target.value)}
                        >
                            <option value="interview">Interview</option>
                            <option value="phone_call">Phone Call</option>
                            <option value="test">Test</option>
                            <option value="assessment_center">Assesment Center</option>
                            <option value="take_home_project">Take Home Project</option>
                            <option value="follow_up">Follow up</option>
                            <option value="general_note">General Note</option>
                            <option value="other">Other</option>
                        </Form.Control>
                    </Form.Group>
                    <Form.Group controlId="notes">
                        <Form.Label>Notes</Form.Label>
                        <Form.Control
                            as="textarea"
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                        />
                    </Form.Group>
                    </Modal.Body>
                    <Modal.Body>
                    {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={closeModal}>Close</Button>
                        <Button type="submit" variant="primary">Add Activity</Button>
                    </Modal.Footer>
                </Form>
            
        </Modal>
        </>
    );
}

export default NewApplicationActivityForm;