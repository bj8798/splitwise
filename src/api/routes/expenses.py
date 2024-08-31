from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import select

from src.models.api_models import ExpenseCreateRequest, ExpenseDetail, EntityCreatedResponse, ResponseMessage
from src.models.schema_models import Expense, ExpenseBreakDown, User

from collections import defaultdict

from src.utils.auth_helper import UserID
from src.utils.db_ops import SessionDep


router = APIRouter()

def get_simplified_map(expense_breakdown_list: list[ExpenseDetail]):
    
    simplified_map = defaultdict(int)
    
    for expense_breakdown in expense_breakdown_list:
        simplified_map[expense_breakdown.user_id] += expense_breakdown.amount
    
    return simplified_map

def get_transaction_tuples(simplified_map: dict):
    
    transaction_tuples = []
    for key1, val1 in simplified_map.items():
        total_positive_money = val1
        
        if total_positive_money > 0:
            for key2, val2 in simplified_map.items():
                if key1 == key2:
                    continue
                if val2 >= 0:
                    continue
                
                if (total_positive_money <= -1*val2) :
                    transaction = (key1, key2, total_positive_money)
                    simplified_map[key2] = total_positive_money + val2
                    transaction_tuples.append(transaction)
                    break
                else:
                    transaction = (key1, key2, -1*val2)
                    simplified_map[key2] = 0
                    total_positive_money += val2
                    transaction_tuples.append(transaction)
    
    return transaction_tuples


@router.post("/")
def create_expense(request: ExpenseCreateRequest, session: SessionDep, user_id: UserID) -> EntityCreatedResponse:
    
    simplified_map = get_simplified_map(request.expense_details)
    transaction_tuples = get_transaction_tuples(simplified_map)
    expense_breakdowns = [ ExpenseBreakDown(payer_id=payer, receiver_id=reciever, amount=amount)  for payer, reciever, amount in transaction_tuples ]
    
    expense = Expense(creator_id=user_id, description=request.description, group_id=request.group_id, date=datetime.now(), expense_breakdowns=expense_breakdowns)
    session.add(expense)
    session.commit()
    
    return EntityCreatedResponse(id = expense.id)


@router.delete("/{expense_id}")
def delete_group(session: SessionDep, expense_id: int, user_id: UserID) -> ResponseMessage:
    
    stmt = select(Expense).where(Expense.creator_id == user_id).where(Expense.id == expense_id)
    expense = session.scalars(stmt).one()
    session.delete(expense)
    session.commit()
    return ResponseMessage(message="Expense deleted successfully")
    

# @router.get("/")
# def get_all_groups(session: SessionDep, user_id: UserID) -> GroupsResponse:
    
#     groups_list = []
    
#     stmt = select(Group).where(Group.creator_id == user_id)
#     for group in session.scalars(stmt):
#         user_ids = [user.id for user in group.users]
#         groups_list.append(
#                             GroupResponse(id=group.id, 
#                                             name=group.name, 
#                                             description=group.description, 
#                                             user_ids=user_ids)
#                         )
        
#     return GroupsResponse(data = groups_list, count = len(groups_list))


# @router.get("/{group_id}")
# def get_group(session: SessionDep, group_id: int, user_id: UserID) -> GroupResponse:
    
#     stmt = select(Group).where(Group.creator_id == user_id).where(Group.id == group_id)
#     group = session.scalars(stmt).one()
    
#     return GroupResponse(id = group.id, name = group.name, description= group.description)


# @router.put("/{group_id}")
# def edit_group(request: GroupUpdateRequest, session: SessionDep, group_id: int, user_id: UserID):

#     stmt = select(Group).where(Group.creator_id == user_id).where(Group.id == group_id)
#     group = session.scalars(stmt).one()
    
#     user_query = select(User).where(User.id.in_(request.user_ids))
    
#     users_list = [user for user in session.scalars(user_query)]
    
#     group.description = request.description
#     group.name = request.name
#     group.users = users_list
    
#     session.commit()
#     return ResponseMessage(message="Group Updated successfully")
    