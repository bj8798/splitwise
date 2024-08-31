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
    date: datetime
    group_id: int
    expense_details: list[ExpenseDetail]
    
class ExpenseCreateRequest(Expense):
    pass

class ExpenseUpdateRequest(Expense):
    pass
    
class ExpenseResponse(Expense):
    id: int
    
class ResponseMessage(BaseModel):
    message: str
    
class EntityCreatedResponse(BaseModel):
    id: int