import { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import axiosClient from '../utils/axiosClient';



const CreateInteractionForm = ({ onFormSubmit }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [error, setError] = useState('');
    const [students, setStudents] = useState([]);
    const [validated, setValidated] = useState(false);


    // State variables for form inputs
    const [title, setTitle] = useState('');
    const [interactionDate, setInteractionDate] = useState('');
    const [interactionType, setInteractionType] = useState('');
    const [staffNotes, setStaffNotes] = useState('');
    const [studentId, setStudentId] = useState('');

    useEffect(() => {
        const fetchStudents = async () => {
                try {
                    const response = await axiosClient.get('/students');
                    setStudents(response.data);
                } catch (error) {
                    console.error('Error fetching students:', error);
                    setError('Error fetching students');
                }
            };
            fetchStudents();
    }, []);
        

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const resetForm = () => {
        setTitle('');
        setInteractionDate('');
        setInteractionType('');
        setStaffNotes('');
    };

   

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        const form = event.currentTarget;
        if (!form.checkValidity()) {
            event.stopPropagation();
            setValidated(true);
            return;
        } else {

            const postData = {
                title,
                interaction_date: interactionDate === '' ? null : interactionDate,
                type: interactionType,
                staff_notes: staffNotes,
                student_id: studentId,
            };

            onFormSubmit(postData)
                .then(() => {
                    resetForm();
                    closeModal();
                })
                .catch((error) => {
                    console.error('Error adding interaction:', error);
                    setError(error?.response?.data?.message || 'Error adding interaction');
                });
        };
    }

    return (
        <>
            <Button onClick={openModal} className="m-2">Add Interaction</Button>
            <Modal show={isModalOpen} onHide={closeModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Add Interaction</Modal.Title>
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
                        <Form.Group controlId="interactionDate">
                            <Form.Label>Interaction Date</Form.Label>
                            <Form.Control
                                type="date"
                                value={interactionDate}
                                onChange={(e) => setInteractionDate(e.target.value)}
                            />
                        </Form.Group>
                        <Form.Group controlId="interactionType">
                            <Form.Label>Interaction Type</Form.Label>
                            <Form.Control
                                as="select"
                                value={interactionType}
                                onChange={(e) => setInteractionType(e.target.value)}
                            >
                                <option value="">Select Interaction Type</option>
                                <option value="Email">Email</option>
                                <option value="MS_Teams">MS Teams</option>
                                <option value="Other">Other</option>
                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId="selectStudent">
                            <Form.Label>Select Student</Form.Label>
                            <Form.Control
                                as="select"
                                value={studentId}
                                onChange={(e) => setStudentId(e.target.value)}
                            >
                                <option value="">Select Student</option>
                                {students.map((student) => (
                                    <option key={student.id} value={student.id}>
                                        {student.user.first_name} {student.user.last_name}
                                    </option>
                                ))}
                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId="staffNotes">
                            <Form.Label>Staff Notes</Form.Label>
                            <Form.Control
                                as="textarea"
                                rows={3}
                                value={staffNotes}
                                onChange={(e) => setStaffNotes(e.target.value)}
                            />
                        </Form.Group>
                        </Modal.Body>
                        <Modal.Body>
                                {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
                        </Modal.Body>
                        <Modal.Footer>
                            <Button variant="secondary" onClick={closeModal}>Cancel</Button>
                            <Button type="submit">Add Interaction</Button>
                        </Modal.Footer>
                    </Form>
                
            </Modal>
        </>
    )
}

export default CreateInteractionForm;