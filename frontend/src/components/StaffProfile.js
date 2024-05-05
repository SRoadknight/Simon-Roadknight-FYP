import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axiosClient from '../utils/axiosClient';
import { cleanData } from '../utils/utils';
import StaffAppointments from './StaffAppointments';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import StaffInteractions from '../components/StaffInteractions';
import Form from 'react-bootstrap/Form';

const StaffProfile = () => {
    const { id: staffId } = useParams();
    const [profileData, setProfileData] = useState(null); 
    const [originalProfileData, setOriginalProfileData] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const { token, userType } = useAuth();

    useEffect(() => {
        const isStaff = userType === 'staff';
        const endpoint = isStaff 
            ? `/staff/me`
            : `/staff/${staffId}`;

        const fetchProfile = async () => {
            try {
                const response = await axiosClient.get(endpoint);
                setProfileData(response.data);
                setOriginalProfileData(response.data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchProfile();
    }, [staffId, token, userType]);

    const openModal = () => setShowModal(true);
    const closeModal = () => setShowModal(false);

    const handleSubmitUpdateStaffProfile = async (e) => {
        e.preventDefault();
        const isStaff = userType === 'staff';
        const endpoint = isStaff 
            ? `/staff/me`
            : `/staff/${staffId}`;
        try {
            const cleanedData = cleanData(profileData);
            const response = await axiosClient.patch(endpoint, cleanedData);
            setProfileData(response.data);
            setOriginalProfileData(response.data);
            closeModal();
        } catch (error) {
            console.error(error);
        }
    };

    const handleResetProfile = () => {
        setProfileData(originalProfileData);
        closeModal();
    }

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setProfileData({ ...profileData, [name]: value });
    };

    if (!profileData) {
        return <h1>Loading...</h1>
    }

    return (
        <>
            <Card className="mb-4">
                <Card.Header>
                    <Card.Title>Staff Profile</Card.Title>
                </Card.Header>  
                <Card.Body>
                    <Card.Text> {profileData.user.first_name} {profileData.user.last_name} </Card.Text>
                    <Card.Text> <strong> Job Title - </strong>{profileData.job_title} </Card.Text>
                    <Card.Text> <strong> Email - </strong>{profileData.user.email_address} </Card.Text>
                </Card.Body>
                <Card.Body>
                    <Card.Title> About </Card.Title>
                    <Card.Text> {profileData.about} </Card.Text>
                    {userType === 'staff' &&
                        <Button variant="primary" onClick={openModal}>Edit About</Button>
                    }
                </Card.Body>
            </Card>
            <Modal show={showModal} onHide={closeModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Edit about</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleSubmitUpdateStaffProfile}>
                        <Form.Group className="mb-3" controlId="about">
                            <Form.Label>About</Form.Label>
                            <Form.Control
                                as="textarea"
                                rows={3}
                                name="about"
                                value={profileData.about}
                                onChange={handleInputChange}
                            />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleResetProfile}>Cancel</Button>
                    <Button variant="primary" onClick={handleSubmitUpdateStaffProfile}>Save Changes</Button>
                </Modal.Footer>
            </Modal>

            <Row>
                <Col lg={6}>
                {userType === 'staff' && 
                <><StaffAppointments staffId={staffId} showUIElements={false} limit={5}/></>
                }
                </Col>
                <Col lg={6}>
                {userType === 'staff' && <><StaffInteractions showUIElements={false} limit={5}/></>}
                </Col>
            </Row>

            {userType === 'student' &&
                <>
                    <h2>Available Appointments</h2>
                    <StaffAppointments staffId={staffId} showUIElements={false} limit={5}/>
                </>
            }
        </>
    )
}

export default StaffProfile;