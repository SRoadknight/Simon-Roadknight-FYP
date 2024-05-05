from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.groups.models import Group, GroupCreate, GroupUpdate, GroupMember
from src.crud import create_generic, update_generic
from sqlalchemy.orm import selectinload
from src.content.models import ContentGroup
from src.groups.exceptions import GroupNotFound, StudentAlreadyInGroup, StudentNotInGroup



async def get_groups(session: AsyncSession):
    result = await session.exec(select(Group))
    groups = result.all()
    return groups

async def get_group_by_id(session: AsyncSession, group_id: int):
    result = await session.exec(select(Group).where(Group.id == group_id))
    group = result.first()
    return group

async def create_group(session: AsyncSession, group: GroupCreate):
    db_group =  await create_generic(
        model_class=Group,
        create_data=group,
        session=session
    )
    return db_group

async def update_group(session: AsyncSession, group_id: int, group: GroupUpdate):
    return await update_generic(
        model_id=group_id,
        update_data=group,
        model_getter=get_group_by_id,
        session=session
    )

async def get_group_content(session: AsyncSession, group_id: int):
    group = await get_group_by_id(session, group_id)
    if group is None:
        raise GroupNotFound()
    result = await session.exec(
        select(Group)
        .options(selectinload(Group.content).joinedload(ContentGroup.content))
        .where(Group.id == group_id)
    ) 
    group_content = result.all()
    return group_content   

async def get_group_students(session: AsyncSession, group_id: int):
    group = await get_group_by_id(session, group_id)
    if group is None:
        raise GroupNotFound()
    result = await session.exec(
        select(Group)
        .options(selectinload(Group.students).joinedload(GroupMember.student))
        .where(Group.id == group_id)
    )
    group_students = result.all()
    return group_students

async def check_student_in_group(session: AsyncSession, student_id: int, group_id: int):
    result = await session.exec(
        select(GroupMember)
        .where(GroupMember.group_id == group_id, GroupMember.student_id == student_id))
    student_in_group = result.first()
    return student_in_group

async def join_group(session: AsyncSession, student_id: int, group_id: int):
    if await check_student_in_group(session, student_id, group_id):
        raise StudentAlreadyInGroup()   
    group_member_join_data = {"student_id": student_id, "group_id": group_id}
    db_group_member = GroupMember.model_validate(group_member_join_data)
    session.add(db_group_member)
    await session.commit()

async def leave_group(session: AsyncSession, student_id: int, group_id: int):
    group_member = await check_student_in_group(session, student_id, group_id)
    if group_member is None:
        raise StudentNotInGroup()
    await session.delete(group_member)
    await session.commit()                  