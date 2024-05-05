from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.job_posts.models import JobPostKeyword
from src.students.models import StudentKeyword
from src.models import ConstrainedId
from src.job_posts.models import JobPost, Visibility, DegreeRequired
from src.students.service import get_student_by_id
from src.students.exceptions import StudentNotFound
from src.students.utils import get_highest_level_of_study 



# Use keywords to recommend job posts to students and candidates to companies
# https://www.learndatasci.com/glossary/jaccard-similarity/  

def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

async def get_student_keywords(session: AsyncSession, student_id: ConstrainedId):
    student = await get_student_by_id(student_id, session)
    if student is None:
        raise StudentNotFound()
    result = await session.exec(
        select(StudentKeyword.keyword)
        .where(StudentKeyword.student_id == student_id))
    return set(result.all())

async def get_job_post_keywords(session: AsyncSession, student_id: ConstrainedId):
    highest_level_of_study = await get_highest_level_of_study(student_id=student_id, session=session)

    query = select(JobPostKeyword.job_post_id, JobPostKeyword.keyword).join(JobPost)

    conditions = []

    if highest_level_of_study not in ["PhD", "Postgraduate"]:
        conditions.append(JobPost.degree_required != DegreeRequired.MASTERS)
    
    conditions.append(JobPost.visibility == Visibility.PUBLIC)

    conditions.append(JobPost.status == "ongoing")

    query = query.where(*conditions)

    result = await session.exec(query)

    job_post_keywords = {}
    for job_post_id, keyword in result.all():
        if job_post_id not in job_post_keywords:
            job_post_keywords[job_post_id] = set()
        job_post_keywords[job_post_id].add(keyword)
    return job_post_keywords

async def get_recommended_jobs(session: AsyncSession, student_id: ConstrainedId):
    student_keywords = await get_student_keywords(session, student_id)
    job_post_keywords = await get_job_post_keywords(session=session, student_id=student_id)
    job_post_scores = []
    for job_post_id, keywords in job_post_keywords.items():
        score = jaccard_similarity(student_keywords, keywords)
        if score > 0:
            job_post_scores.append({"job_post_id": job_post_id, "score": score})
    
    
    job_post_scores_sorted = sorted(job_post_scores, key=lambda x: x['score'], reverse=True)
    
    
    top_job_posts = []
    for job_post_score in job_post_scores_sorted[:10]:
        job_post = await session.get(JobPost, job_post_score['job_post_id'])
        top_job_posts.append(job_post)
    return top_job_posts
