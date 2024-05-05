import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';


const UpdateApplicationForm = ({ application, onFormSubmit }) => {
    const [formValues, setFormValues] = useState(application);
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

    return (
        <>
            <Button variant="primary" onClick={openModal}>Update Application</Button>
            <Modal show={isModalOpen} onHide={closeModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Update Application</Modal.Title>
                </Modal.Header>
                    <Form onSubmit={handleSubmit}>
                        <Modal.Body>
                            <Form.Group controlId="stage">
                                <Form.Label>Stage</Form.Label>
                                <Form.Select
                                    name="stage"
                                    value={formValues.stage}
                                    onChange={handleChange}
                                >
                                    <option value="applied">Applied</option>
                                    <option value="interviewing">Interviewing</option>
                                    <option value="offer">Offered</option>
                                    <option value="accepted">Accepted</option>
                                    <option value="rejected">Rejected</option>
                                </Form.Select>
                            </Form.Group>
                            <Form.Group controlId="date_applied">
                                <Form.Label>Date Applied</Form.Label>
                                <Form.Control
                                    type="date"
                                    name="date_applied"
                                    value={formValues.date_applied}
                                    onChange={handleChange}
                                />
                            </Form.Group>
                            <Form.Group controlId="notes">
                                <Form.Label>Notes</Form.Label>
                                <Form.Control
                                    as="textarea"
                                    name="notes"
                                    value={formValues.notes !== null || formValues.notes === "CLEAR" ? formValues.notes : ''}
                                    onChange={handleChange}
                                />
                            </Form.Group>
                            <Form.Group controlId="careers_plus_assisted">
                                <Form.Label>Assisted by Careers+</Form.Label>
                                <Form.Check
                                    type="checkbox"
                                    name="careers_plus_assisted"
                                    checked={formValues.careers_plus_assisted}
                                    onChange={handleChange}
                                />
                            </Form.Group>
                        </Modal.Body>
                        <Modal.Footer>
                            <Button variant="secondary" onClick={closeModal}>Close</Button>
                            <Button type="submit">Update Application</Button>
                        </Modal.Footer>
                    </Form>
            </Modal>
        </>
    );
}

export default UpdateApplicationForm;

