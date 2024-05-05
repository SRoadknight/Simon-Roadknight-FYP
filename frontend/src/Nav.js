import { useAuth } from './context/AuthContext';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/NavBar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Container from 'react-bootstrap/Container';

const AppNav = () => {
    const { userType } = useAuth();


    if (userType === 'student') {
        return (
            <Navbar expand="lg">
                <Container>
                    <Navbar.Brand href="/">Careers+</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="me-auto">
                            <NavDropdown title="My Profile" id="basic-nav-dropdown">
                                <NavDropdown.Item href="/students/me">Profile</NavDropdown.Item>
                                <NavDropdown.Item href="/students/me/applications">Applications</NavDropdown.Item>
                                <NavDropdown.Item href="/students/me/interactions">Interactions</NavDropdown.Item>
                                <NavDropdown.Item href="/students/me/activities">Activities</NavDropdown.Item>
                                <NavDropdown.Item href="/students/me/appointments">Appointments</NavDropdown.Item>
                                <NavDropdown.Item href="/students/me/events">Events</NavDropdown.Item>
                                <NavDropdown.Item href="/students/me/degrees">Degrees</NavDropdown.Item>
                            </NavDropdown>
                            <NavDropdown title="Browse" id="basic-nav-dropdown">
                                <NavDropdown.Item href="/job-posts">Job Posts</NavDropdown.Item>
                                <NavDropdown.Item href="/staff">Careers Staff</NavDropdown.Item>
                                <NavDropdown.Item href="/appointments">Appointments</NavDropdown.Item>
                                <NavDropdown.Item href="/events">Events</NavDropdown.Item>
                            </NavDropdown>
                        </Nav>
                        <Nav>
                            <Nav.Link href="/logout">Logout</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        );
    } else

    if (userType === 'staff') {
        return (
            <Navbar expand="lg">
                <Container>
                    <Navbar.Brand href="/">Careers+</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="me-auto">
                            <NavDropdown title="My Profile" id="basic-nav-dropdown">
                                <NavDropdown.Item href="/staff/me">Profile</NavDropdown.Item>
                                <NavDropdown.Item href="/staff/me/interactions">Interactions</NavDropdown.Item>
                                <NavDropdown.Item href="/staff/me/appointments">Appointments</NavDropdown.Item>
                            </NavDropdown>
                            <NavDropdown title="Browse" id="basic-nav-dropdown">
                                <NavDropdown.Item href="/students">Students</NavDropdown.Item>
                                <NavDropdown.Item href="/job-posts">Job Posts</NavDropdown.Item>
                            </NavDropdown>
                            <Nav.Link href="/applications/activities">Upcoming Activities</Nav.Link>
                        </Nav>
                        <Nav>
                            <Nav.Link href="/logout">Logout</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        );
    };
};

export default AppNav;