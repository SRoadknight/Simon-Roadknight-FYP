from fastapi import APIRouter, Depends
from src.skill_tags.models import SkillTag, SkillTagCreate, SkillTagRead, SkillTagUpdate
from src.auth.models import User
from src.auth.dependencies import get_current_active_user, get_current_active_staff_user
from src.skill_tags.dependencies import valid_skill_tag_create, valid_skill_tag_update
from src.skill_tags import service
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from src.crud import create_generic, update_generic



router = APIRouter(dependencies=[Depends(get_current_active_user)])


# Get all available skills
@router.get("", response_model=list[SkillTagRead])
async def read_skills(session: AsyncSession = Depends(get_session)):
    return await service.get_skills(session)

# Create a new skill
@router.post("", response_model=SkillTagRead)
async def create_skill(
    current_user: User = Depends(get_current_active_staff_user), 
    skill_tag: SkillTagCreate = Depends(valid_skill_tag_create),
    session: AsyncSession = Depends(get_session)
    ):
    skill_tag: SkillTag = await create_generic(
        model_class=SkillTag,
        create_data=skill_tag,
        session=session
        )
    return skill_tag



# Get a single skill by id
@router.get("/{skill_id}", response_model=SkillTagRead)
async def read_skill(skill_id: int, session: AsyncSession = Depends(get_session)):
    skill = await service.get_skill_by_id(skill_id, session)
    
    return skill


# Update a skill
@router.patch("/{skill_id}", response_model=SkillTagRead)
async def update_skill(
    *,
    current_user: User = Depends(get_current_active_staff_user), 
    skill_id: int,
    skill_tag: SkillTagUpdate = Depends(valid_skill_tag_update),
    session: AsyncSession = Depends(get_session)
    ):
    skill = await update_generic(
        model_id=skill_id,
        update_data=skill_tag,
        model_getter=service.get_skill_by_id,
        session=session
        )
    return skill



