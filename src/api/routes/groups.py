from collections import defaultdict
from fastapi import APIRouter, Depends
from sqlalchemy import select

from src.api.routes.expenses import get_transaction_tuples
from src.utils.db_ops import SessionDep
from src.models.api_models import GroupCreateReuqest, EntityCreatedResponse, \
                        GroupResponse, GroupsResponse, ResponseMessage, \
                        GroupUpdateRequest, ExpenseSummaryGroupEntry
from src.models.schema_models import Group, User, Expense, ExpenseBreakDown
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

def get_simplified_map(expense_breakdown_list: list[ExpenseBreakDown]):
    
    simplified_map = defaultdict(int)
    for expense_breakdown in expense_breakdown_list:
        simplified_map[expense_breakdown.payer_id] += expense_breakdown.amount
        simplified_map[expense_breakdown.receiver_id] -= expense_breakdown.amount
        
    return simplified_map


@router.get("/{group_id}/expenses/summary")
def get_group_expense_summary(session: SessionDep, group_id: int, user_id: UserID) -> list[ExpenseSummaryGroupEntry]:
    
    stmt = select(Expense).where(Expense.group_id == group_id)
    
    expense_breakdown_list = []
    for expense in session.scalars(stmt):
        for expense_breakdown in expense.expense_breakdowns:
            if expense_breakdown.is_settled == False:
                expense_breakdown_list.append(expense_breakdown)
                
    simplified_map = get_simplified_map(expense_breakdown_list)
    print(simplified_map)
    transaction_tuples = get_transaction_tuples(simplified_map)
    
    expense_summary = []
    for payer, reciever, amount in transaction_tuples:
        expense_summary.append(ExpenseSummaryGroupEntry(lender_user_id=payer, borrower_user_id=reciever, amount=amount))
        
    return expense_summary

@router.post("/{group_id}/expenses/settle")
def settleup_group_expense(session: SessionDep, group_id: int, user_id: UserID) -> ResponseMessage:
    
    stmt = select(Expense).where(Expense.group_id == group_id)
    
    for expense in session.scalars(stmt):
        for expense_breakdown in expense.expense_breakdowns:
            expense_breakdown.is_settled = True
                
    session.commit()
    return ResponseMessage(message="Expense Settled up successfully for a group")


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
    