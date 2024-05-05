import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { useAuth } from '../context/AuthContext';
import { Link, useParams } from 'react-router-dom';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import Card from 'react-bootstrap/Card';
import ToggleButton from 'react-bootstrap/ToggleButton';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import StudentUpdateInteractionForm from '../forms/StudentUpdateInteractionForm';
import { cleanData } from '../utils/utils';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { formatInteractionType } from '../utils/utils';




const StudentInteractions = ({ showUIElements = true, limit = null }) => {
    const { id:studentId } = useParams();
    const [interactions, setInteractions] = useState([]);
    const [error, setError] = useState('');
    const [interactionType, setInteractionType] = useState('');
    const [outstandingInteractions, setOutstandingInteractions] = useState(false);
    const { userType } = useAuth();

    useEffect(() => {
        const fetchInteractions = async () => {
            const params = {};
            if (interactionType) {
                params.type = interactionType;
            }
            if (outstandingInteractions) {
                params.outstanding = true;
            }

            const interactionsEndpoint = userType === 'staff' ? `/students/${studentId}/interactions` : `/students/me/interactions`;

            try {
                
                const response = await axiosClient.get(interactionsEndpoint, { params });
                setInteractions(response.data);
                limit && setInteractions(response.data.slice(0, limit));
            } catch (error) {
                console.error('Error fetching student interactions:', error);
                setError('Error fetching student interactions');
            }
        };

        fetchInteractions();
    }, [interactionType, outstandingInteractions, userType, studentId, limit]);

    const handleSelect = (eventKey) => {
        setInteractionType(eventKey);
    }

    const handleSubmitUpdateInteraction = async (updatedInteraction, interactionId) => {
        try {
            let endpoint = `/students/interactions/${interactionId}`
            const cleanedData = cleanData(updatedInteraction);
            const response = await axiosClient.patch(endpoint, cleanedData);
            const dbInteraction = response.data;
            setInteractions(interactions.map(interaction => interaction.id === interactionId ? dbInteraction : interaction));
            
            return Promise.resolve(dbInteraction);
        } catch (error) {
            console.error('Error updating interaction:', error);
            setError('Error updating interaction');
            return Promise.reject(error);
        }
    }


    return (
        <>
            <Card className="mb-3">
                <Card.Header>
                    <Card.Title>
                        {showUIElements ? 'Interactions' : 'Recent Interactions'}
                    </Card.Title>
                </Card.Header>
                <Card.Body>
                    {error && <Alert variant="danger">{error}</Alert>}
                    {!showUIElements && userType === 'student' &&
                        <Button as={Link} to="/students/me/interactions" className="m-2" variant="secondary">
                            View All Interactions
                        </Button>
                    }
                    {!showUIElements && userType === 'staff' &&
                        <Button as={Link} to={`/students/${studentId}/interactions`} className="m-2" variant="secondary">
                            View All Interactions
                        </Button>
                    }
                    {showUIElements && 
                    <>
                        <Card.Text className="text-muted m-2">Filter by interaction method</Card.Text>
                        <Nav variant="underline" activeKey={interactionType} onSelect={handleSelect}>
                            <Nav.Item>
                                <Nav.Link eventKey="">All</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="Email">Email</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="MS_Teams">MS Teams</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="Other">Other</Nav.Link>
                            </Nav.Item>
                        </Nav>
                    </>}
                    <ButtonGroup className="m-2">
                        <ToggleButton
                            id="outstanding-toggle"
                            type="checkbox"
                            variant="outline-primary"
                            checked={outstandingInteractions}
                            value="1"
                            onChange={() => setOutstandingInteractions(!outstandingInteractions)}
                        >
                            {outstandingInteractions ? 'Show all interactions' : 'Only show outstanding interactions'}
                        </ToggleButton>
                    </ButtonGroup>
                </Card.Body>
            </Card>
            <Row xs={1} md={3} lg={4} className="g-4 mb-4">
                {interactions.length > 0 && interactions.map((interaction) => (
                    <Col key={interaction.id}>
                        <Card>
                            <Card.Header>
                                <Card.Title>{interaction.title}</Card.Title>
                                <Card.Text className="text-muted">{interaction.interaction_date}</Card.Text>
                                <Card.Text className="text-muted">{formatInteractionType(interaction.type)}</Card.Text>
                                <Card.Text>With @ <Link to={`/staff/${interaction.careers_staff_id}`}>{interaction.careers_staff.user.first_name} {interaction.careers_staff.user.last_name}</Link></Card.Text>
                                
                            </Card.Header>
                            <Card.Body>
                                {interaction.staff_notes && <Card.Text><strong>Staff notes - </strong>{interaction.staff_notes}</Card.Text>}
                                {interaction.helpful && <Card.Text><strong>Found helpful - </strong> {interaction.helpful}</Card.Text>}
                                {interaction.further_support && <Card.Text><strong>Further support - </strong> {interaction.further_support}</Card.Text>}
                                {interaction.emoji_rating && <Card.Text>Feeling {interaction.emoji_rating}</Card.Text>}
                                {!interaction.staff_notes && !interaction.helpful && !interaction.further_support && !interaction.emoji_rating && <Card.Text>No information to display</Card.Text>}
                                {userType === 'student' && 
                                <StudentUpdateInteractionForm
                                    onFormSubmit={handleSubmitUpdateInteraction}
                                    interaction={interaction}
                                />}
                            </Card.Body>
                            </Card>
                    </Col>
                    ))}
            </Row>
            {interactions.length === 0 && <Alert variant="info">No interactions found</Alert>}

        </>
    );
}


export default StudentInteractions;