import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { useParams, NavLink, Link, Outlet} from 'react-router-dom';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Alert from 'react-bootstrap/Alert';


const StudentProfileRoutes = ({ isCurrentUser }) => {
    const { id: studentId } = useParams();
    const [error, setError] = useState('');
    const [studentName, setStudentName] = useState('');
    const effectiveId = isCurrentUser ? 'me' : studentId;

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await axiosClient.get(`/students/${effectiveId}`);
                setStudentName(response.data.user.first_name + ' ' + response.data.user.last_name);
            } catch (error) {
                setError(error.message);
            }
        };
        fetchProfile();
    }, [effectiveId]);


    return (
        <>
            {error && <Alert variant='danger'>{error}</Alert>}
            <Navbar expand="lg">
                <Navbar.Brand as={Link} to={`about`}>{studentName}</Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto" variant='underline'>
                        <Nav.Link as ={NavLink} to={`about`}>Student Home</Nav.Link>
                        <Nav.Link as ={NavLink} to={`applications`}>Applications</Nav.Link>
                        <Nav.Link as ={NavLink} to={`activities`}>Activities</Nav.Link>
                        <Nav.Link as ={NavLink} to={`interactions`}>Interactions</Nav.Link>
                        <Nav.Link as ={NavLink} to={`appointments`}>Appointments</Nav.Link>
                        <Nav.Link as ={NavLink} to={`events`}>Events</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
            <div>
                <Outlet />
            </div>
            
        </>
    )
}

export default StudentProfileRoutes;
