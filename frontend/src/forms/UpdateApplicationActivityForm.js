import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

const activityTypes = [
    'interview', 
    'phone_call', 
    'test', 
    'assessment_center',
    'take_home_project', 
    'follow_up', 
    'general_note',
    'other'];

    function formatActivityType(tag) {
        const tagMap = {
            'interview': 'Interview',
            'phone_call': 'Phone Call',
            'test': 'Test',
            'assessment_center': 'Assessment Center',
            'take_home_project': 'Take Home Project',
            'follow_up': 'Follow Up',
            'general_note': 'General Note',
            'other': 'Other'
        };
        return tagMap[tag];
    }

const UpdateApplicationActivityForm = ({ activity, onFormSubmit }) => {
    const [formValues, setFormValues] = useState(activity);
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
    }

    return (
        <>
            <Button variant="primary" onClick={openModal} className="m-2">Update Activity</Button>
            <Modal show={isModalOpen} onHide={closeModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Update Activity</Modal.Title>
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
                                />
                            </Form.Group>
                            <Form.Group controlId="activity_date">
                                <Form.Label>Date</Form.Label>
                                <Form.Control
                                    type="date"
                                    name="activity_date"
                                    value={formValues.activity_date ? formValues.activity_date : ''}
                                    onChange={handleChange}
                                />
                            </Form.Group>
                            <Form.Group controlId="activity_time">
                                <Form.Label>Time</Form.Label>
                                <Form.Control
                                    type="time"
                                    name="activity_time"
                                    value={formValues.activity_time ? formValues.activity_time : ''}
                                    onChange={handleChange}
                                />
                            </Form.Group>
                            <Form.Group controlId="activity_type">
                                <Form.Label>Type</Form.Label>
                                <Form.Select
                                    name="activity_type"
                                    value={formValues.activity_type}
                                    onChange={handleChange}
                                >
                                    {activityTypes.map(type => (
                                        <option key={type} value={type}>{formatActivityType(type)}</option>
                                    ))}
                                </Form.Select>
                            </Form.Group>
                            <Form.Group controlId="notes">
                                <Form.Label>Notes</Form.Label>
                                <Form.Control
                                    as="textarea"
                                    name="notes"
                                    value={formValues.notes ? formValues.notes : ''}
                                    onChange={handleChange}
                                />
                            </Form.Group>
                        </Modal.Body>
                        <Modal.Footer>
                            <Button variant="secondary" onClick={closeModal}>Cancel</Button>
                            <Button variant="primary" type="submit">Update Activity</Button>
                        </Modal.Footer>
                    </Form>
            </Modal>
        </>
    );
}

export default UpdateApplicationActivityForm;