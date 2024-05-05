import { useEffect, useState } from 'react';
import { useParams, NavLink, Link, Outlet} from 'react-router-dom';
import axiosClient from '../utils/axiosClient';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';


const StaffProfileRoutes = ({ isCurrentUser = false }) => {
    const { id: staffId } = useParams();
    const [staffName, setStaffName] = useState('');
    const effectiveId = isCurrentUser ? 'me' : staffId;

    useEffect(() => {

        const fetchProfile = async () => {
            try {
                const response = await axiosClient.get(`/staff/${effectiveId}`);
                setStaffName(response.data.user.first_name + ' ' + response.data.user.last_name);
            } catch (error) {
                console.error(error);
            }
        };

        fetchProfile();
    }, [effectiveId]);

    return (
        <>
            <Navbar expand="lg">
            <Navbar.Brand as={Link} to={`about`}>{staffName}</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="mr-auto">
                        <Nav.Link as={NavLink} to={`about`}>About</Nav.Link>
                        <Nav.Link as ={NavLink} to={`appointments`}>
                            {isCurrentUser ? 'Appointments' : 'Availability'}
                        </Nav.Link>
                        {isCurrentUser && <Nav.Link as={Link} to={`interactions`}>Interactions</Nav.Link>}
                    </Nav>
                </Navbar.Collapse>
            </Navbar>

            <Outlet />
        </>
    )
}

export default StaffProfileRoutes;