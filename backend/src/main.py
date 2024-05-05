from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.init_db import init_db
from src.seed_db import seed_db
from src.auth.router import router as auth_router
from src.skill_tags.router import router as skill_tags_router
from src.job_profiles.router import router as job_profiles_router
from src.events.router import router as events_router
from src.schools_departments.router import router as schools_departments_router
from src.faculties.router import router as faculties_router
from src.content.router import router as content_router
from src.companies.router import router as company_router
from src.job_posts.router import router as job_posts_router
from src.students.router import router as student_router
from src.applications.router import router as applications_router   
from src.appointments.router import router as appointments_router 
from src.staff.router import router as staff_router
from src.degrees.router import router as degrees_router
from src.groups.router import router as groups_router
from src.interactions.router import router as interactions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_db()
    yield


app = FastAPI(lifespan=lifespan)

allowed_origins = [
    "http://localhost:3000"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


router_config = [
    {"router": applications_router, "prefix": "/job-applications", "tags": ["Applications"]},
    {"router": appointments_router, "prefix": "/appointments", "tags": ["Appointments"]},
    {"router": auth_router, "prefix": "/auth", "tags": ["Auth"]},
    {"router": company_router, "prefix": "/companies", "tags": ["Companies"]},
    {"router": content_router, "prefix": "/content", "tags": ["Content"]},
    {"router": degrees_router, "prefix": "/degrees", "tags": ["Degrees"]},
    {"router": events_router, "prefix": "/events", "tags": ["Events"]},
    {"router": faculties_router, "prefix": "/faculties", "tags": ["Faculties"]},
    {"router": groups_router, "prefix": "/groups", "tags": ["Groups"]},
    {"router": interactions_router, "prefix": "/interactions", "tags": ["Interactions"]},
    {"router": job_posts_router, "prefix": "/job-posts", "tags": ["Job Posts"]},
    {"router": job_profiles_router, "prefix": "/job-profiles", "tags": ["Job Profiles"]},
    {"router": schools_departments_router, "prefix": "/schools-departments", "tags": ["Schools and Departments"]},
    {"router": skill_tags_router, "prefix": "/skill-tags", "tags": ["Skills"]},
    {"router": staff_router, "prefix": "/staff", "tags": ["Staff"]},
    {"router": student_router, "prefix": "/students", "tags": ["Students"]}
]

for config in router_config:
    app.include_router(**config)
