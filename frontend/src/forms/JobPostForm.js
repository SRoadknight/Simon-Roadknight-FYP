import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

const JobPostForm = () => {
    const { token, userType } = useAuth();
    const [title, setTitle] = useState('');
    const [companyName, setCompanyName] = useState('');
    const [description, setDescription] = useState('');
    const [location, setLocation] = useState('');
    const [salary, setSalary] = useState('');
    const [jobType, setJobType] = useState('graduate job');
    const [hiringMultipleCandidates, setHiringMultipleCandidates] = useState(false);
    const [degreeRequired, setDegreeRequired] = useState('');
    const [deadline, setDeadline] = useState('');
    const [websiteUrl, setWebsiteUrl] = useState('');
    const [jobStatus, setJobStatus] = useState('ongoing');

    const handleSubmit = async (event) => {
        event.preventDefault();

        const postData = {
            title,
            company_name: companyName,
            description,
            location,
            salary,
            job_type: jobType,
            hiring_multiple_candidates: hiringMultipleCandidates,
            degree_required: degreeRequired,
            deadline,
            website_url: websiteUrl === 'Website URL' ? '' : websiteUrl,
            status: jobStatus
        };

        const staffApiUrl = 'http://localhost:8007/job-posts';
        const companyApiUrl = 'http://localhost:8007/companies/job-posts';

        const headers = { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };

        try {
            await axios.post(userType === 'staff' ? staffApiUrl : companyApiUrl, postData, { headers });
        } catch (error) {
            console.error('Error posting job:', error);
        }
    }; 

    return (
        <form onSubmit={handleSubmit}>
            <h2>Create Job Post</h2>
            <input 
                type="text"
                placeholder="Title"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
            />  

            <input 
                type="text"
                placeholder="Company Name"
                value={companyName}
                onChange={(event) => setCompanyName(event.target.value)}
            />

            <textarea 
                placeholder="Description"
                value={description}
                onChange={(event) => setDescription(event.target.value)}
            />

            <input 
                type="text"
                placeholder="Location"
                value={location}
                onChange={(event) => setLocation(event.target.value)}
            />

            <input 
                type="text"
                placeholder="Salary"
                value={salary}
                onChange={(event) => setSalary(event.target.value)}
            />

            <select 
                value={jobType}
                onChange={(event) => setJobType(event.target.value)}
            >

                <option value="graduate job">Graduate Job</option>
                <option value="placement/internship">Placement / Internship</option>
            </select>

            <label>
                Hiring multiple candidates:
                <input 
                    type="checkbox"
                    checked={hiringMultipleCandidates}
                    onChange={(event) => setHiringMultipleCandidates(event.target.checked)}
                />
            </label>

            <select 
                value={degreeRequired}
                onChange={(event) => setDegreeRequired(event.target.value)}
            >
                <option value="">Degree Required</option>
                <option value="All grades">All grades</option>
                <option value="2:2 and above">2:2 and above</option>
                <option value="2:1 and above">2:1 and above</option>
                <option value="First">First class</option>
                <option value="Master's and above">Master's and above</option>
                <option value="2:2 and above (expected)">2:2 and above (expected)</option>
                <option value="2:1 and above (expected)">2:1 and above (expected)</option>
                <option value="First (expected)">First class (expected)</option>
            </select>

            <input 
                type="date"
                value={deadline}
                onChange={(event) => setDeadline(event.target.value)}
            />

            <input 
                type="url"
                placeholder="Website URL"
                value={websiteUrl}
                onChange={(event) => setWebsiteUrl(event.target.value)}
            />

            <select 
                value={jobStatus}
                onChange={(event) => setJobStatus(event.target.value)}
            >
                <option value="ongoing">Ongoing</option>
                <option value="closed">Closed</option>
            </select>
            
            <button type="submit">Post Job</button>

        </form>
    )
};

export default JobPostForm;
