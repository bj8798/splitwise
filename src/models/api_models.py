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
    
class GroupCreateResponse(BaseModel):
    id: int
    
class GroupsResponse(BaseModel):
    data: list[GroupResponse]
    count: int
    
class ResponseMessage(BaseModel):
    message: str