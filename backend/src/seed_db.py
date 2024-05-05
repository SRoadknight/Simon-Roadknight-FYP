from src.database import async_engine
from sqlmodel import Session
from .students.models import *
from .skill_tags.models import *
from .job_posts.models import *
from .events.models import *
from .appointments.models import *
from .staff.models import *
from .schools_departments.models import *
from .degrees.models import *
from .faculties.models import *
from src.interactions.models import *
from .auth.models import *
from .groups.models import *
from .content.models import *
from .companies.models import *
from .job_profiles.models import *
from .applications.models import *
from datetime import datetime, timedelta

      
def insert_dummy_data(conn):
    with Session(conn) as session:

        time_in_30_minutes = datetime.now() + timedelta(minutes=30)
        time_in_120_minutes = datetime.now() + timedelta(minutes=120)
    
        # Faculty
        faculty = Faculty(
            faculty_name="Computing, Engineering and the Built Environment", 
            faculty_description="Computing, Engineering and the Built Environment (CEBE)")
        session.add(faculty)
        session.commit()
        session.refresh(faculty)

        # Schools/Departments for CEBE
        school_computing = SchoolDepartment(
            school_deparment_name="School of Computing and Digital Technology", 
            school_deparment_description="Computing and Digital Technology",
            faculty_id=faculty.id)
        
        session.add(school_computing)
        session.commit()
        session.refresh(school_computing)
        
        # Degree
        degree_computing = Degree(
            degree_code="G401", 
            school_deparment_id=school_computing.id, 
            degree_name="Computer Science", 
            degree_level=LevelTaught.UNDERGRADUATE)
        session.add(degree_computing)
        session.commit()
        session.refresh(degree_computing)

        # Student User 1 
        user ={"email_address": "joe.blogs@mail.bcu.ac.uk", "first_name": "Joe", "last_name": "Blogs", "user_type": UserType.STUDENT}
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        # Student User 2
        user_2 = User(email_address="bob@mail.bcu.ac.uk", first_name="Bob", last_name="Test", user_type=UserType.STUDENT)
        session.add(user_2)
        session.commit()
        session.refresh(user_2)

        # Student
        student = Student(id="12345678", user_id=db_user.id, current_employment_status=CurrentEmploymentStatus.CASUAL_WORK)
        session.add(student)
        session.commit()
        session.refresh(student)

        # Student External Profile
        student_external_profile = ExternalProfile(student_id=student.id, website=ExternalWebsite.linkedin, website_url="https://www.linkedin.com/in/job.blogs/")
        session.add(student_external_profile)
        session.commit()
        session.refresh(student_external_profile)

        # student 2
        student_2 = Student(id="87654321", user_id=user_2.id)
        session.add(student_2)
        session.commit()
        session.refresh(student_2)

        # Careers Staff User
        careers_staff_user = User(email_address="test.careers1@bcu.ac.uk", first_name="Test", last_name="Careers", user_type=UserType.STAFF)
        session.add(careers_staff_user)
        session.commit()
        session.refresh(careers_staff_user)

        # Careers Staff
        careers_staff = CareersStaff(id="87654321", job_title="Careers Advisor", about="Blank for now", user_id=careers_staff_user.id)
        session.add(careers_staff)
        session.commit()
        session.refresh(careers_staff)

        # Careers Staff User 2
        careers_staff_user = User(email_address="test.careers2@bcu.ac.uk", first_name="Test", last_name="Careers2", user_type=UserType.STAFF)
        session.add(careers_staff_user)
        session.commit()
        session.refresh(careers_staff_user)

        # Careers Staff 2
        careers_staff_2 = CareersStaff(id="12345678", job_title="Careers Advisor", about="I am a Careers Advisor.", user_id=careers_staff_user.id)
        session.add(careers_staff_2)
        session.commit()
        session.refresh(careers_staff_2)
        



        # Event
        event = Event(name="Python Workshop", description="A workshop on Python programming", event_start_time=func.now(timezone=True), event_end_time=time_in_120_minutes, event_location="Online", event_type=EventType.workshop)
        session.add(event)
        session.commit()
        session.refresh(event)

        # Event 2
        event_2 = Event(
            name="Java Workshop", 
            description="A workshop on Java programming", 
            event_date=func.now(), 
            event_start_time=func.now(),
            event_end_time=time_in_120_minutes,
            event_location="Online", 
            event_type=EventType.workshop
            )
        session.add(event_2)
        session.commit()
        session.refresh(event_2)

        # Event 3 (Cancelled Event)
        event_3 = Event(
            name="C# Workshop", 
            description="A workshop on C# programming", 
            event_date=func.now(), 
            event_start_time=func.now(),
            event_end_time=time_in_120_minutes,
            event_location="Online", 
            event_type=EventType.workshop,
            status=EventStatus.CANCELLED
            )
        session.add(event_3)
        session.commit()
        session.refresh(event_3)

        # Event 4 (Complete Event)
        event_4 = Event(
            name="F# Workshop",
            description="A workshop on F# programming",
            event_date=func.now(),
            event_start_time=func.now(),
            event_end_time=time_in_120_minutes,
            event_location="Online",
            event_type=EventType.workshop,
            status=EventStatus.COMPLETE
            )
        session.add(event_4)
        session.commit()
        session.refresh(event_4)

        # Student Event
        student_event = EventRegistration(student_id=student.id, event_id=event.id)
        session.add(student_event)
        session.commit()


    
        # Appointment
        appointment = Appointment(name="1-1 Meeting", description="A one to one meeting", staff_id="87654321", app_date=func.now(), app_start_time=func.now(), app_end_time=time_in_120_minutes, location="Online", type=AppointmentType.one_on_one)
        session.add(appointment)
        session.commit()
        session.refresh(appointment)

        # Appointment 2
        appointment_2 = Appointment(name="Group Meeting", description="A group meeting", staff_id="12345678", app_date=func.now(), app_start_time=func.now(), app_end_time=time_in_30_minutes, location="In Person")
        session.add(appointment_2)
        session.commit()
        session.refresh(appointment_2)


        # Student Appointment
        student_appointment = AppointmentBooking(date_booked=func.now(), student_id=student.id, appointment_id=appointment.id)
        session.add(student_appointment)
        session.commit()

        appointment.status = "booked"
        session.commit()
        
    



        # Job Post
        job_post = JobPost(
            title="Software Developer", 
            company_name="Test Company",
            description="A software developer role, looking for an ML Engineer with a background in statistics and experience with Python and R.",
            date_posted="2022-12-01",
            location="Birmingham",
            salary="£25,000 - £30,000",
            degree_required=DegreeRequired.TWO_ONE,
            deadline=func.now(),
            url="https://www.job.com",
            source=JobSource.EXTERNAL,
            status=JobPostStatus.ONGOING,
            visibility=Visibility.PUBLIC
            )
        session.add(job_post)
        session.commit()
        session.refresh(job_post)

        # Job post 2
        job_post_2 = JobPost(
            title="Senior Software Engineer",
            company_name="Test Company 2",
            description="A senior software engineer role, looking for a web developer with experience in React and Node.js.",
            date_posted="2022-12-01",
            location="London",
            salary="£30,000 - £35,000",
            degree_required=DegreeRequired.TWO_ONE,
            deadline=func.now(),
            url="https://www.job.com",
            source=JobSource.EXTERNAL,
            status=JobPostStatus.ONGOING,
            visibility=Visibility.PUBLIC
            )
        session.add(job_post_2)
        session.commit()
        session.refresh(job_post_2)

        # job post 3
        job_post_3 = JobPost(
            title="Junior Software Engineer",
            company_name="Test Company 3",
            description="A junior software engineer role, looking for a backend developer with experience in Java and Spring Boot.",
            date_posted="2022-12-01",
            location="Manchester",
            salary="£20,000 - £25,000",
            degree_required=DegreeRequired.TWO_TWO,
            deadline=func.now(),
            url="https://www.job.com",
            source=JobSource.EXTERNAL,
            status=JobPostStatus.ONGOING,
            visibility=Visibility.PUBLIC
            )
        session.add(job_post_3)
        session.commit()
        session.refresh(job_post_3)

        # Job post 4
        job_post_4 = JobPost(
            title="Software Developer",
            company_name="Test Company",
            description="A software developer role, looking for a OS developer with experience in C and C++.",
            date_posted="2022-12-01",
            location="London",
            salary="£25,000 - £30,000",
            degree_required=DegreeRequired.TWO_ONE,
            deadline=func.now(),
            url="https://www.job.com",
            source=JobSource.EXTERNAL,
            status=JobPostStatus.ONGOING,
            visibility=Visibility.PUBLIC
            )
        session.add(job_post_4)
        session.commit()
        session.refresh(job_post_4)

        # Student Job Application
        student_job_application = JobApplication(
            student_id=student.id, 
            job_post_id=job_post.id, 
            date_applied=func.now(),
            stage=JobApplicationStage.applied)
        session.add(student_job_application)
        session.commit()
        session.refresh(student_job_application)

        # Student Job Application 2
        student_job_application_2 = JobApplication(
            student_id=student.id,
              job_post_id=job_post_2.id, 
              date_applied=func.now(),
              stage=JobApplicationStage.applied)
        session.add(student_job_application_2)
        session.commit()
        session.refresh(student_job_application_2)


        # Student 2 Job Application Job 1
        student_2_job_application = JobApplication(
            student_id=student_2.id,
              job_post_id=job_post.id, 
              date_applied=func.now(),
              stage=JobApplicationStage.applied)
        session.add(student_2_job_application)
        session.commit()
        session.refresh(student_2_job_application)

        # Student 2 Job Application Job 3
        student_2_job_application_2 = JobApplication(
            student_id=student_2.id, 
            job_post_id=job_post_3.id, 
            date_applied=func.now(),
            stage=JobApplicationStage.applied)
        session.add(student_2_job_application_2)
        session.commit()
        session.refresh(student_2_job_application_2)

        # Student Careers Staff Interaction
        student_careers_staff_interaction = Interaction(title="Interaction #1 Email", student_id=student.id, careers_staff_id=careers_staff.id, date="2024-04-20", type=InteractionType.EMAIL, staff_notes="An email interaction")
        session.add(student_careers_staff_interaction)
        session.commit()

        # Student Careers Staff Interaction 2
        student_careers_staff_interaction_2 = Interaction(title="Interaction #2 MS TEAMS", student_id=student.id, careers_staff_id=careers_staff.id, date="2022-12-01", type=InteractionType.MS_TEAMS, staff_notes="An MS Teams interaction")
        session.add(student_careers_staff_interaction_2)
        session.commit()

        # Student Careers Staff Interaction 3
        student_careers_staff_interaction_3 = Interaction(title="Interaction #3 Other", student_id=student.id, careers_staff_id=careers_staff.id, date="2022-12-01", type=InteractionType.OTHER, staff_notes="Met at jobs fair")
        session.add(student_careers_staff_interaction_3)
        session.commit()


        # Add skill tag 
        skill_tag = SkillTag(name="Python", description="Python programming language")
        session.add(skill_tag)
        session.commit()

        # Add skill tag 2
        skill_tag_2 = SkillTag(name="Java", description="Java programming language")
        session.add(skill_tag_2)
        session.commit()

        # Add skill tag 3
        skill_tag_3 = SkillTag(name="C#", description="C# programming language")
        session.add(skill_tag_3)
        session.commit()

        # Add skill tag 4
        skill_tag_4 = SkillTag(name="F#", description="F# programming language", active=False)
        session.add(skill_tag_4)
        session.commit()

        # Add student skill
        student_skill = StudentSkillTag(
            student_id="12345678", 
            skill_id=skill_tag.id,
            date_added="2022-12-01"
            )
        session.add(student_skill)
        session.commit()

        # Add student skill 2
        student_skill_2 = StudentSkillTag(
            student_id="12345678", 
            skill_id=skill_tag_2.id,
            date_added="2022-12-01"
            )
        session.add(student_skill_2)
        session.commit()

        # # Add job post skill
        # job_post_skill = JobPostSkillTag(
        #     job_post_id=1,
        #     skill_id=1,
        #     date_added="2022-12-01"
        # )
        # session.add(job_post_skill)
        # session.commit()

        
        # Add event skill
        event_skill = EventSkillTag(
            event_id=event.id,
            skill_id=skill_tag.id,
        )
        session.add(event_skill)
        session.commit()

        # Add event skill 2
        event_skill_2 = EventSkillTag(
            event_id=event_2.id,
            skill_id=skill_tag_2.id,
        )
        session.add(event_skill_2)
        session.commit()

        # Add event skill 3
        event_skill_3 = EventSkillTag(
            event_id=event.id,
            skill_id=skill_tag_3.id,
        )
        session.add(event_skill_3)
        session.commit()



        # Add appointment skill
        appointment_skill = AppointmentSkillTag(
            appointment_id=appointment.id,
            skill_id=skill_tag.id,
            date_added="2022-12-01"
        )
        session.add(appointment_skill)
        session.commit()


        two_days_ago = datetime.now() - timedelta(days=2)

        # add activity to job application
        job_application_activity = JobApplicationActivity(
            activity_date=func.now(),
            time=func.now(),
            title="Activity 1",
            job_application_id=1,
            student_id="12345678",
            date_created=two_days_ago
        )
        session.add(job_application_activity)
        session.commit()

        # add activity to job application 2
        job_application_activity_2 = JobApplicationActivity(
            title="Activity 2",
            job_application_id=2,
            student_id="12345678"
        )
        session.add(job_application_activity_2)
        session.commit()



       # add new group
        group = Group(name="Python Group", description="A group for Python programming content")
        session.add(group)
        session.commit()
        session.refresh(group)

        # add new group 2 
        group_2 = Group(name="Java Group", description="A group for Java programming content")
        session.add(group_2)
        session.commit()
        session.refresh(group_2)

        # add student to group
        student_group_member = GroupMember(
            student_id="12345678", 
            group_id=group.id, 
            date_joined=func.now())
        session.add(student_group_member)
        session.commit()
        session.refresh(student_group_member)

        # add student to group 2
        student_group_member_2 = GroupMember(
            student_id="12345678", 
            group_id=group_2.id, 
            date_joined=func.now())
        session.add(student_group_member_2)
        session.commit()
        session.refresh(student_group_member_2)


        # add a piece of content
        content = Content(
            title="Python Basics", 
            content={"content": "Python basics content"})
        session.add(content)
        session.commit()
        session.refresh(content)

        # add a piece of content 2
        content_2 = Content(
            title="Advanced Python", 
            content={"content": "Advanced Python Content"})
        session.add(content_2)
        session.commit()
        session.refresh(content_2)

        # add a piece of content 3
        content_3 = Content(
            title="Java Basics", 
            content={"content": "Java basics content"})
        session.add(content_3)
        session.commit()
        session.refresh(content_3)

        
        # add content to group 1
        content_group = ContentGroup(
            content_id=content.id, 
            group_id=group.id, 
            date_assigned=func.now())
        session.add(content_group)
        session.commit()
        session.refresh(content_group)

        # add content to group 1
        content_group_2 = ContentGroup(
            content_id=content_2.id, 
            group_id=group.id, 
            date_assigned=func.now())    
        session.add(content_group_2)
        session.commit()
        session.refresh(content_group_2)

        # add content to group 2
        content_group_3 = ContentGroup(
            content_id=content_3.id, 
            group_id=group_2.id, 
            date_assigned=func.now())
        session.add(content_group_3)
        session.commit()
        session.refresh(content_group_3)

        # add a new student user
        student_user = User(email_address="test3@test.com", first_name="Test3", last_name="User", user_type=UserType.STUDENT)
        session.add(student_user)
        session.commit()
        session.refresh(student_user)

        # add a new student
        student_3 = Student(id="11119999", user_id=student_user.id)
        session.add(student_3)
        session.commit()
        session.refresh(student_3)

        # add a job with student source 
        job_post_student_1 = JobPost(
            title="Junior Software Engineer",
            company_name="Test Company 4",
            description="A junior software engineer role",
            date_posted="2022-12-01",
            location="Manchester",
            salary="£20,000 - £25,000",
            degree_required=DegreeRequired.TWO_TWO,
            deadline=func.now(),
            url="https://www.job.com",
            source=JobSource.STUDENT,
            status=JobPostStatus.ONGOING,
            visibility=Visibility.PRIVATE
            )
        session.add(job_post_student_1)
        session.commit()
        session.refresh(job_post_student_1)

        # Student job post for student 3
        student_job_post = StudentJobPost(
            student_id=student_3.id,
            job_post_id=job_post_student_1.id,
        )
        session.add(student_job_post)
        session.commit()
        session.refresh(student_job_post)


        # add company user
        company_user = User(email_address="testcompany1@test.com", user_type=UserType.COMPANY)
        session.add(company_user)
        session.commit()
        session.refresh(company_user)

        # add company
        company = Company(
            id="11111111",
            name="Test Company", 
            description="A test company", 
            website_url="https://www.testcompany.com", 
            user_id=company_user.id)
        # verify the company / url is validated
        db_comapny = Company.model_validate(company) 
        session.add(company)
        session.commit()
        session.refresh(company)

         # add company user 2
        company_user = User(email_address="testcompany2@test.com", user_type=UserType.COMPANY)
        session.add(company_user)
        session.commit()
        session.refresh(company_user)

        # add company 2
        company = Company(
            id="22222222",
            name="Test Company", 
            description="A test company", 
            website_url="https://www.testcompany.com", 
            user_id=company_user.id)
        # verify the company / url is validated
        db_comapny = Company.model_validate(company) 
        session.add(company)
        session.commit()
        session.refresh(company)

        # add a new job post for a company
        job_post_5 = JobPost(
            title="Software Developer", 
            company_name="Test Company",
            description="A software developer role",
            date_posted="2022-12-01",
            location="Birmingham",
            salary="£25,000 - £30,000",
            degree_required=DegreeRequired.TWO_ONE,
            deadline=func.now(),
            url="https://www.job.com",
            source=JobSource.COMPANY,
            status=JobPostStatus.ONGOING,
            visibility=Visibility.PUBLIC
            )
        session.add(job_post_5)
        session.commit()
        session.refresh(job_post_5)

        # Company Job Post for company 1
        company_job_post = CompanyJobPost(
            company_id=company.id,
            job_post_id=job_post_5.id
        )
        session.add(company_job_post)
        session.commit()
        session.refresh(company_job_post)

        # add a new job profile
        job_profile = JobProfile(
            title="Software Developer", 
            mini_description="A software developer role",
            url="https://www.jobprofile.com"
            )
        session.add(job_profile)
        session.commit()
        session.refresh(job_profile)

    # # add a new job profile skill tag
    #     job_profile_skill_tag = JobProfileSkillTag(
    #         job_profile_id=job_profile.id,
    #         skill_tag_id=skill_tag.id,
    #         date_added="2022-12-01",
    #         skill_tag_weight=1
    #     )
    #     session.add(job_profile_skill_tag)
    #     session.commit()
    #     session.refresh(job_profile_skill_tag) 

        # add a new job profile skill tag 2
        job_profile_skill_tag_2 = JobProfileSkillTag(
            job_profile_id=job_profile.id,
            skill_id=skill_tag_2.id,
            date_added=func.now(),
            skill_tag_weight=1
        )
        session.add(job_profile_skill_tag_2)
        session.commit()
        session.refresh(job_profile_skill_tag_2)

        # add a degree to a student 
        student_degree = StudentDegree(
            student_id=student.id,
            degree_code=degree_computing.degree_code,
            graduated=False,
            grade_awarded=None
        )
        session.add(student_degree)
        session.commit()
        session.refresh(student_degree)

        # add a degree to a job profile
        job_profile_degree = JobProfileDegree(
            job_profile_id=job_profile.id,
            degree_code=degree_computing.degree_code
        )
        session.add(job_profile_degree)
        session.commit()
        session.refresh(job_profile_degree)




async def seed_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(insert_dummy_data)