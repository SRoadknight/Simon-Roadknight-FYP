import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

const ApplicationForm = ({ onFormSubmit }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const [stage, setStage] = useState('applied');
    const [dateApplied, setDateApplied] = useState('');
    const [notes, setNotes] = useState('');
    const [assistedByCareers, setAssistedByCareers] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);


    const handleSubmit = (event) => {
        event.preventDefault();
        const formValues = {
            stage,
            date_applied: dateApplied,
            notes,
            assisted_by_careers: assistedByCareers,
        };
        onFormSubmit(formValues);
        closeModal();
    };

    return ( 
        <>
        <Button variant="primary" onClick={openModal} className="m-2">Track Application</Button>
            <Modal show={isModalOpen} onHide={closeModal}>
            <Form onSubmit={handleSubmit}>
                <Modal.Header closeButton>
                    <Modal.Title>Update Application</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form.Group controlId="stage">
                        <Form.Label>Stage</Form.Label>
                        <Form.Select
                            name="stage"
                            value={stage}
                            onChange={(event) => setStage(event.target.value)}
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
                            value={dateApplied}
                            onChange={(event) => setDateApplied(event.target.value)}
                        />
                    </Form.Group>
                    <Form.Group controlId="notes" className="mb-2">
                        <Form.Label>Notes</Form.Label>
                        <Form.Control
                            as="textarea"
                            name="notes"
                            value={notes}
                            onChange={(event) => setNotes(event.target.value)}
                        />
                    </Form.Group>
                    <Form.Group controlId="assisted_by_careers">
                        <Form.Check
                            type="checkbox"
                            label="Assisted by Careers+"
                            name="assisted_by_careers"
                            checked={assistedByCareers}
                            onChange={(event) => setAssistedByCareers(event.target.checked)}
                        /> 
                    </Form.Group>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={closeModal}>Cancel</Button>
                    <Button variant="primary" type="submit">Save Application</Button>
                </Modal.Footer>
                </Form>
            </Modal>
        </>
    );
};

export default ApplicationForm;