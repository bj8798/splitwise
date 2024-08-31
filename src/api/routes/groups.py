from fastapi import APIRouter, Depends
from sqlalchemy import select

from src.utils.db_ops import SessionDep
from src.models.api_models import GroupCreateReuqest, EntityCreatedResponse, \
                        GroupResponse, GroupsResponse, ResponseMessage, \
                        GroupUpdateRequest
from src.models.schema_models import Group, User
from src.utils.auth_helper import UserID

router = APIRouter()

@router.post("/")
def create_group(request: GroupCreateReuqest, session: SessionDep, user_id: UserID) -> EntityCreatedResponse:
    group = Group(name = request.name, description = request.description, creator_id = user_id)
    session.add(group)
    session.commit()
    return EntityCreatedResponse(id = group.id)


@router.delete("/{group_id}")
def delete_group(session: SessionDep, group_id: int, user_id: UserID) -> ResponseMessage:
    
    stmt = select(Group).where(Group.creator_id == user_id).where(Group.id == group_id)
    group = session.scalars(stmt).one()
    session.delete(group)
    session.commit()
    return ResponseMessage(message="Group deleted successfully")
    

@router.get("/")
def get_all_groups(session: SessionDep, user_id: UserID) -> GroupsResponse:
    
    groups_list = []
    
    stmt = select(Group).where(Group.creator_id == user_id)
    for group in session.scalars(stmt):
        user_ids = [user.id for user in group.users]
        groups_list.append(
                            GroupResponse(id=group.id, 
                                            name=group.name, 
                                            description=group.description, 
                                            user_ids=user_ids)
                        )
        
    return GroupsResponse(data = groups_list, count = len(groups_list))


@router.get("/{group_id}")
def get_group(session: SessionDep, group_id: int, user_id: UserID) -> GroupResponse:
    
    stmt = select(Group).where(Group.creator_id == user_id).where(Group.id == group_id)
    group = session.scalars(stmt).one()
    
    return GroupResponse(id = group.id, name = group.name, description= group.description)


@router.put("/{group_id}")
def edit_group(request: GroupUpdateRequest, session: SessionDep, group_id: int, user_id: UserID):

    stmt = select(Group).where(Group.creator_id == user_id).where(Group.id == group_id)
    group = session.scalars(stmt).one()
    
    user_query = select(User).where(User.id.in_(request.user_ids))
    
    users_list = [user for user in session.scalars(user_query)]
    
    group.description = request.description
    group.name = request.name
    group.users = users_list
    
    session.commit()
    return ResponseMessage(message="Group Updated successfully")
    