import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { Link } from 'react-router-dom';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import Card from 'react-bootstrap/Card';
import ToggleButton from 'react-bootstrap/ToggleButton';
import CreateInteractionForm from '../forms/CreateInteractionForm';
import { cleanData } from '../utils/utils';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import { formatInteractionType } from '../utils/utils';



const StaffInteractions = ({ showUIElements = true, limit = null }) => {
    const [interactions, setInteractions] = useState([]);
    const [error, setError] = useState('');
    const [interactionType, setInteractionType] = useState('');
    const [outstandingInteractions, setOutstandingInteractions] = useState(false);

    useEffect(() => {
        const fetchInteractions = async () => {
            const params = {}; 
            if (interactionType) {
                params.type = interactionType;
            }
            if (outstandingInteractions) {
                params.outstanding = true;
            }
            let endpoint = `/staff/me/interactions`;
         
            try {
                const response = await axiosClient.get(endpoint, { params });
                setInteractions(response.data);
                limit && setInteractions(response.data.slice(0, limit));
            } catch (error) {
                console.error('Error fetching staff interactions:', error);
                setError('Error fetching staff interactions');
            }
        };

        fetchInteractions();
    }, [interactionType, outstandingInteractions, limit]);

    const handleSelect = (eventKey) => {
        setInteractionType(eventKey);
    };

    const handleSubmitNewInteraction = async (newInteraction) => {
        try {
            let endpoint = `/staff/me/interactions`
            const cleanedData = cleanData(newInteraction);
            const response = await axiosClient.post(endpoint, cleanedData);
            const dbInteraction = response.data;
            setInteractions([dbInteraction, ...interactions]);
            return Promise.resolve(dbInteraction);
        } catch (error) {
            console.error('Error creating interaction:', error);
            setError('Error creating interaction');
            return Promise.reject(error);
        }
    };

    return (
        <>
            <Card className="mb-3">
                <Card.Header>
                    <Card.Title>
                        {showUIElements ? 'Interactions' : 'My Recent Interactions'}
                    </Card.Title>
                </Card.Header>
                <Card.Body>
                    {error && <Alert variant="danger">{error}</Alert>}
                    <CreateInteractionForm onFormSubmit={handleSubmitNewInteraction} />
                    {!showUIElements && 
                    <Button as={Link} to="/staff/me/interactions" variant="secondary" className="m-2">
                        View all my interactions
                    </Button>}
                    
                    {showUIElements && 
                    <>
                        <Card.Text className="text-muted m-2">Filter by interaction method</Card.Text>
                        <Nav variant="underline" activeKey={interactionType} onSelect={handleSelect} className="mb-2">
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

            {interactions.length > 0 ? interactions.map((interaction) => (
                <Card key={interaction.id} className="mb-3">
                     <Card.Header>
                                <Card.Title>{interaction.title}</Card.Title>
                                <Card.Text className="text-muted">{interaction.interaction_date}</Card.Text>
                                <Card.Text className="text-muted">{formatInteractionType(interaction.type)}</Card.Text>
                                <Card.Text>With <Link to={`/students/${interaction.student_id}`}>{interaction.student.user.first_name} {interaction.student.user.last_name}</Link></Card.Text>
                            </Card.Header>
                    {interaction.outstanding && 
                    <Card.Body>
                        {interaction.staff_notes && <Card.Text><strong>Staff notes - </strong>{interaction.staff_notes}</Card.Text>}
                        {interaction.helpful && <Card.Text><strong>Found helpful - </strong> {interaction.helpful}</Card.Text>}
                        {interaction.further_support && <Card.Text><strong>Further support - </strong> {interaction.further_support}</Card.Text>}
                        {interaction.emoji_rating && <Card.Text>Feeling {interaction.emoji_rating}</Card.Text>}
                    </Card.Body>}
                </Card>
            )) : <Alert variant="info">No interactions found</Alert>}
        </>
    );
}

export default StaffInteractions;

