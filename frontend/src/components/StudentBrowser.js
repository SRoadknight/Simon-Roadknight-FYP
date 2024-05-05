import { useEffect, useState } from 'react';
import axiosClient from '../utils/axiosClient';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

const StudentBrowser = () => {
    const { token } = useAuth();
    const [students, setStudents] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
    

    useEffect(() => {
        const fetchStudents = async () => {
            const endpoint = `/students`;
            try {
                const response = await axiosClient.get(endpoint);
                setStudents(response.data);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching students:', error);
                setError(error);
            }
        };
        fetchStudents();
    }
    , [token]);

    if (loading) {
        return <h1>Loading...</h1>
    }

    if (error) {
        return <div>Error fetching students: {error.message}</div>;
    }

    if (students.length === 0) {
        return <div>No students found</div>;
    } else {
        return (
            <div>
                <h1>Students</h1>
                <ul>
                    {students.map((student) => {
                        return (
                            <li key={student.id}>
                                <Link to={`/students/${student.id}`}> {student.user.first_name} {student.user.last_name} </Link>
                                <div> Student ID: {student.id}</div>
                                <div>Email: {student.user.email_address}</div>
                            </li>
                        );
                    })}
                </ul>
            </div>
        )
    }
}

export default StudentBrowser;