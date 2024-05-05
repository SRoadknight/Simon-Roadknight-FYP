from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.students.models import Student, StudentDegree
from src.students.exceptions import StudentNotFound
from sqlalchemy.orm import selectinload, joinedload
from src. degrees.models import Degree


async def get_highest_level_of_study(session: AsyncSession, student_id: int):
    result = await session.exec(
        select(Student)
        .options(selectinload(Student.degrees)
                 .joinedload(StudentDegree.degree))
        .where(Student.id == student_id)
    )

    student = result.first()
    if student is None:
        raise StudentNotFound()
    
    degreeLevelsMap = {
        "Foundation": 0,
        "Undergraduate": 1,
        "Postgraduate": 2,
        "PhD": 3
    }
    
    highest_level_of_study = None
    for student_degree in student.degrees:
        if highest_level_of_study is None:
            highest_level_of_study = student_degree.degree.degree_level
        else:
            if degreeLevelsMap[student_degree.degree.degree_level] > degreeLevelsMap[highest_level_of_study]:
                highest_level_of_study = student_degree.degree.degree_level
    return highest_level_of_study
