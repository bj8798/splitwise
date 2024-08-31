from typing import Annotated
from fastapi import Depends, Request

def get_user_id(request: Request) -> int:
    user_id = request.headers.get('user_id')
    return user_id
    
UserID = Annotated[int, Depends(get_user_id)]
