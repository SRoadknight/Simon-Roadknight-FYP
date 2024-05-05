import { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import Container from 'react-bootstrap/Row';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

const LoginForm = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { handleLogin } = useAuth();

    const handleSubmit = async (event) => {
        event.preventDefault();

        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await axios.post('http://localhost:8007/auth/token', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
            handleLogin(response.data.access_token);
        } catch (error) {
            setError('Error logging in');
        }
    };
    return (
        <Container>   
            <Row className="justify-content-center align-items-center">
                <Col md={6} className="mt-4">
                    <Card className="p-4">
                    <Card.Title>
                        Login
                    </Card.Title>
                    {error && <Alert variant="danger" dismissible>{error}</Alert>}
                    <Form onSubmit={handleSubmit}>

                        <Form.Group controlId="formBasicEmail">
                            <Form.Label>Username:</Form.Label>
                            <Form.Control
                                type="email"
                                value={username}
                                onChange={(event) => setUsername(event.target.value)}
                            />
                        </Form.Group>

                        <Form.Group controlId="formBasicPassword">
                            <Form.Label>Password:</Form.Label>
                            <Form.Control
                                type="password"
                                value={password}
                                onChange={(event) => setPassword(event.target.value)}
                            />
                        </Form.Group>

                        <Button variant="primary" type="submit" className="mt-4">Login</Button>
                    </Form>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};

export default LoginForm;