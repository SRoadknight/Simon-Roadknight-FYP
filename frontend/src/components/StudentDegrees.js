import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { useAuth } from '../context/AuthContext';
import { useParams } from 'react-router-dom';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';

const StudentDegrees = ({ showUIElements = true, limit = null }) => {
    const { id: studentId } = useParams();
    const [degrees, setDegrees] = useState([]);
    const [error, setError] = useState('');
    const { userType } = useAuth();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const isStaff = userType === 'staff';
        const endpoint = isStaff
            ? `/students/${studentId}/degrees`
            : `/students/me/degrees`;

        const fetchDegrees = async () => {
            try {
                const response = await axiosClient.get(endpoint)
                setDegrees(response.data);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching student degrees:', error);
                setError('Error fetching student degrees');
            }
        };
        fetchDegrees();
    }, [studentId, userType, showUIElements, limit]);

    if (loading) {
        return <h1>Loading...</h1>
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <>
            <Card className="mb-4">
                <Card.Header>
                    <Card.Title>Degrees with BCU</Card.Title>
                </Card.Header>
                <Card.Body>
                    <ListGroup>
                    {degrees.length > 0 ? degrees.map((degree) => (
                        <ListGroup.Item key={degree.degree_code}>
                            <Card.Text>{degree.degree.degree_code} - {degree.degree.degree_name}</Card.Text>
                            <Card.Text>Degree level: {degree.degree.degree_level}</Card.Text>
                            <Card.Text> Graduated: {degree.graduated ? 'Yes' : 'No'}</Card.Text>
                            <Card.Text> Graduation date: {degree.graduation_date ? degree.graduation_date : 'Not available'}</Card.Text>
                            <Card.Text>Grade awarded: {degree.grade_awarded ? degree.grade_awarded : 'Not available'}</Card.Text>

                        </ListGroup.Item>
                    )) : <Card.Text>No degrees found</Card.Text>}
                    </ListGroup>
                </Card.Body>
            </Card>
            
        </>
    );
}

export default StudentDegrees;