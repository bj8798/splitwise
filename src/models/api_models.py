import uuid
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

    
class Group(BaseModel):
    name: str
    description: Optional[str] = None
    user_ids: Optional[list[int]] = []

        
class GroupCreateReuqest(Group):
    pass


class GroupUpdateRequest(Group):
    pass


class GroupResponse(Group):
    id: int

    
class GroupsResponse(BaseModel):
    data: list[GroupResponse]
    count: int
    

class ExpenseDetail(BaseModel):
    user_id: int
    amount: int

   
class ExpenseBreakDownDetails(BaseModel):
    payer_id: int
    receiver_id: int
    amount: int


class Expense(BaseModel):
    description: str
    group_id: int
    total_amount: int
    expense_details: list[ExpenseDetail]

    
class ExpenseCreateRequest(Expense):
    pass


class ExpenseUpdateRequest(Expense):
    pass


class PendingAmount(BaseModel):
    to_user: int
    amount: int


class ExpenseSummaryUser(BaseModel):
    from_user: int
    pending_amounts: list[PendingAmount]
    
    
class ExpenseSummaryGroupEntry(BaseModel):
    lender_user_id: int
    borrower_user_id: int
    amount: int
    
 
class ExpenseDetailsUser(BaseModel):
    description: str
    group_id: int
    total_amount: int
    user_amount: int
    
class ExpenseResponse(BaseModel):
    id: int
    description: str
    group_id: int
    expense_details: list[ExpenseBreakDownDetails]

        
class ResponseMessage(BaseModel):
    message: str

    
class EntityCreatedResponse(BaseModel):
    id: int