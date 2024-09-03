# CareerCoach

Project artefact to form part of my individual honours project submission for completion of my undergraduate degree in Computer and Data Science.

## About 

CareerCoach is a data-driven career development platform aimed at Higher Education Institutions (HEI's) to bring alignment between staff and students in the career journey of students and graduates. It focuses on prominent aspects from the literature of what makes students employable and increases their employability. As well as HEI's there is scope and initial implementation to allow third-party companies access the platform, to better integrate employers with HEI's. The application intends to capture data that can later be used for multi-purpose analytics such as understanding student employability within an institution and marketing.

Some features include:
- Track job applications and related activities
- Log career development activities
- Logging and feedback on career services and student interactions
- Meeting and appointment management
- Job recommendation based on the job description and the student's profile

## Running the project

### Running the RESTFul API and associated services 

Running the web server is made simple through containerisation, from the root directory of the project run `docker compose up`, this will start up the database (PostgreSQL) and web server running the applications (Uvicorn and FastAPI)

### Running the front-end React application

Inside the frontend directory run `npm install react-scripts` & `npm start`

### Test credentials 

For ease of development and testing, test credentials are currently set up when the project is run, for both staff and students.

#### Postgres login

- Username: admin
- Password: password
- Database name: career_coach

#### Default application logins

##### Careers staff: 

- Username: test.careers1@bcu.ac.uk
- Password: secret

##### Students:

- Username: joe.blogs@mail.bcu.ac.uk
- Password: secret

## Technology Stack 

Some of the technology used for the creation of the RESTFul API and Frontend include: 

- Docker
- FastAPI
- PostgreSQL
- React
- NLTK and NetworkX


