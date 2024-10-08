from collections import defaultdict
from datetime import datetime
from fastapi import APIRouter
from sqlalchemy import select, or_

from src.models.api_models import ExpenseCreateRequest, \
        EntityCreatedResponse, ResponseMessage, ExpenseResponse, ExpenseBreakDownDetails, \
        ExpenseSummaryUser, PendingAmount, ExpenseDetailsUser
from src.models.schema_models import Expense, ExpenseBreakDown

from src.utils.auth_helper import UserID
from src.utils.db_ops import SessionDep
from src.utils.expense_calculation_helper import get_simplified_map_from_api_expense_list, get_transaction_tuples


router = APIRouter()


@router.post("/")
def create_expense(request: ExpenseCreateRequest, session: SessionDep, user_id: UserID) -> EntityCreatedResponse:
    
    simplified_map = get_simplified_map_from_api_expense_list(request.expense_details)
    transaction_tuples = get_transaction_tuples(simplified_map)
    expense_breakdowns = [ ExpenseBreakDown(payer_id=payer, receiver_id=reciever, amount=amount)  for payer, reciever, amount in transaction_tuples ]
    
    expense = Expense(creator_id=user_id, 
                      description=request.description, 
                      group_id=request.group_id, 
                      date=datetime.now(), 
                      total_amount=request.total_amount,
                      expense_breakdowns=expense_breakdowns)
    session.add(expense)
    session.commit()
    
    return EntityCreatedResponse(id = expense.id)


@router.post("/{expense_id}/settle")
def settleup_expense(session: SessionDep, expense_id: int, user_id: UserID) -> ResponseMessage:
    
    stmt = select(Expense).where(Expense.creator_id == user_id).where(Expense.id == expense_id)
    expense = session.scalars(stmt).one()
    
    for expense_breakdown in expense.expense_breakdowns:
        expense_breakdown.is_settled = True
    
    session.commit()
    return ResponseMessage(message="Expense Settled up successfully")


@router.delete("/{expense_id}")
def delete_expense(session: SessionDep, expense_id: int, user_id: UserID) -> ResponseMessage:
    
    stmt = select(Expense).where(Expense.creator_id == user_id).where(Expense.id == expense_id)
    expense = session.scalars(stmt).one()
    session.delete(expense)
    session.commit()
    
    return ResponseMessage(message="Expense deleted successfully")

@router.get("/summary")
def get_user_expenses_summary(session: SessionDep, user_id: UserID) -> ExpenseSummaryUser:
    payer_query = select(ExpenseBreakDown) \
    .where(ExpenseBreakDown.payer_id == user_id) \
    .where(ExpenseBreakDown.is_settled == False)
    
    summary_map = defaultdict(int)
    for expense_breakdown in session.scalars(payer_query):
        summary_map[expense_breakdown.receiver_id] += expense_breakdown.amount
        
    receiver_query = select(ExpenseBreakDown) \
    .where(ExpenseBreakDown.receiver_id == user_id) \
    .where(ExpenseBreakDown.is_settled == False)
    
    for expense_breakdown in session.scalars(receiver_query):
        summary_map[expense_breakdown.payer_id] -= expense_breakdown.amount
        
    pending_amounts = []
    for user, pending_amount in summary_map.items():
        pending_amounts.append(PendingAmount(to_user=user, amount=pending_amount))
        
    return ExpenseSummaryUser(from_user=user_id, pending_amounts=pending_amounts)

@router.get("/")
def get_user_expenses(session: SessionDep, user_id: UserID) -> list[ExpenseDetailsUser]:
    
    stmt = select(Expense).join(ExpenseBreakDown, Expense.id == ExpenseBreakDown.expense_id) \
            .where(or_(ExpenseBreakDown.payer_id == user_id, ExpenseBreakDown.receiver_id == user_id)) \
            .where(ExpenseBreakDown.is_settled == False)
    
    expense_details = []
    for expense in session.scalars(stmt):
        for expense_breakdown in expense.expense_breakdowns:
            user_amount = 0
            if expense_breakdown.payer_id == user_id:
                user_amount = expense_breakdown.amount
            elif expense_breakdown.receiver_id == user_id:
                user_amount = -1*expense_breakdown.amount
            
            if user_amount != 0:
                expense_details.append(ExpenseDetailsUser(description=expense.description,
                                                        group_id=expense.group_id,
                                                        total_amount=expense.total_amount,
                                                        user_amount=user_amount
                                                        ))
            
    return expense_details


@router.get("/{expense_id}")
def get_expense(session: SessionDep, expense_id: int, user_id: UserID) -> ExpenseResponse:
    
    stmt = select(Expense).where(Expense.creator_id == user_id).where(Expense.id == expense_id)
    expense = session.scalars(stmt).one()
    
    expense_details = [ExpenseBreakDownDetails(payer_id=expense_breakdown.payer_id, receiver_id=expense_breakdown.receiver_id, amount=expense_breakdown.amount) 
        for expense_breakdown in expense.expense_breakdowns]
    
    return ExpenseResponse(id = expense.id, group_id=expense.group_id, description= expense.description, expense_details=expense_details)

    