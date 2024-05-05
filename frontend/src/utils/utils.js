// Clean data -- remove empty strings and null values

export function cleanData(data) {
    const cleanedData = {};
    for (const key in data) {
        if (data[key] !== '' && data[key] !== null) {
            cleanedData[key] = data[key];
        }
    }
    return cleanedData;
}



export function getDate(dateString) {
    const date = new Date(dateString);
    return date.toDateString();
}

export function getTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString();
}

export function getDuration(start, end) {
    const startDate = new Date(start);
    const endDate = new Date(end);
    const duration = (endDate - startDate) / 1000 / 60;
    return duration.toFixed(0).toString() + ' minutes';
}


export function staffOrStudentRoute(userType, studentId, endpoint) {
    return userType === 'staff' 
    ? `/students/${studentId}/${endpoint}`
    : `/students/me/${endpoint}`;
}

export function formatInteractionType(interactionType) {
    const typeMap = {
        'Email': (
        <>
            <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="25" height="25" viewBox="0 0 48 48">
            <path fill="#673AB7" d="M40,10H8c-2.209,0-4,1.791-4,4v20c0,2.209,1.791,4,4,4h32c2.209,0,4-1.791,4-4V14C44,11.791,42.209,10,40,10z"></path>
            <path fill="#B39DDB" d="M44,14.025c0-0.465-0.095-0.904-0.24-1.32L24,27.025L4.241,12.705C4.095,13.121,4,13.561,4,14.025V15l20,14.495L44,15V14.025z"></path>
            </svg><span> Email</span>
        </>
        ),
        'MS_Teams': (
        <>
        <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="25" height="25" viewBox="0 0 48 48">
        <path fill="#5c6bc0" d="M41.5 13A3.5 3.5 0 1 0 41.5 20 3.5 3.5 0 1 0 41.5 13zM4 40l23 4V4L4 8V40z"></path>
        <path fill="#fff" d="M21 16.27L21 19 17.01 19.18 16.99 31.04 14.01 30.95 14.01 19.29 10 19.45 10 16.94z"></path>
        <path fill="#5c6bc0" d="M36 14c0 2.21-1.79 4-4 4-1.2 0-2.27-.53-3-1.36v-5.28c.73-.83 1.8-1.36 3-1.36C34.21 10 36 11.79 36 14zM38 23v11c0 0 1.567 0 3.5 0 1.762 0 3.205-1.306 3.45-3H45v-8H38zM29 20v17c0 0 1.567 0 3.5 0 1.762 0 3.205-1.306 3.45-3H36V20H29z"></path>
        </svg><span> Teams</span>
        </>
        ),
        'Other': (
        <>
        <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="25" height="25" viewBox="0 0 48 48">
        <path fill="#64B5F6" d="M8 20A4 4 0 1 0 8 28 4 4 0 1 0 8 20zM40 20A4 4 0 1 0 40 28 4 4 0 1 0 40 20zM24 20A4 4 0 1 0 24 28 4 4 0 1 0 24 20z"></path>
        </svg><span> Other</span>
        </>
        )
    };
    return typeMap[interactionType];
}