import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';


const StudentUpdateInteractionForm = ({ interaction, onFormSubmit }) => {
    const [formValues, setFormValues] = useState(interaction);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [error, setError] = useState('');
    const [validated, setValidated] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormValues({ ...formValues, [name]: value });
    };


    const handleSubmit = async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        if (!form.checkValidity()) {
            event.stopPropagation();
            setValidated(true);
            return;
        } else {
            onFormSubmit(formValues, interaction.id)
                .then(() => {
                    closeModal();
                })
                .catch((error) => {
                    console.error('Error updating interaction:', error);
                    setError('Error updating interaction');
                });
        }
       

    };
    
    return (
        <>
        {error && <Alert variant="danger">{error}</Alert>}
            <Button variant="primary" onClick={openModal}>Update Interaction</Button>
            <Modal show={isModalOpen} onHide={closeModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Update Interaction</Modal.Title>
                </Modal.Header>
                <Form oValidate validated={validated} onSubmit={handleSubmit}>
                    <Modal.Body>
                        <Form.Group controlId="helpful">
                            <Form.Label>What did you find helpful?</Form.Label>
                            <Form.Control
                                as="textarea"
                                name="helpful"
                                value={formValues.helpful ? formValues.helpful : ''}
                                onChange={handleChange}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="furtherSupport">
                            <Form.Label>What further support do you need?</Form.Label>
                            <Form.Control
                                as="textarea"
                                name="further_support"
                                value={formValues.further_support ? formValues.further_support : ''}
                                onChange={handleChange}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="emojiRating">
                            <Form.Label>How are you feeling?</Form.Label>
                            <Form.Control
                                as="select"
                                name="emoji_rating"
                                value={formValues.emoji_rating ? formValues.emoji_rating : ''}
                                onChange={handleChange}
                                required
                            >
                                <option value="">Select a reaction</option>
                                <option value="😢">😢</option>
                                <option value="😟">😟</option>
                                <option value="😐">😐</option>
                                <option value="🙂">🙂</option>
                                <option value="😀">😀</option>
                            </Form.Control>
                        </Form.Group>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={closeModal}>Cancel</Button>
                        <Button type="submit" variant="primary">Update Interaction</Button>
                    </Modal.Footer>
                </Form>
            </Modal>
        </>
    )
};

export default StudentUpdateInteractionForm;