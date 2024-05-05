from src.database import async_engine
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

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)