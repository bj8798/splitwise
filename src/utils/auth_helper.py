from typing import Annotated
from fastapi import Depends, Request

def get_user_id(request: Request) -> int:
    user_id = request.headers.get('user_id')
    user_id = int(user_id)
    
    # Here, I have taken user_id from header directly. 
    # for performing actual authorization, we can get access jwt token from header and derive user_id from it.
    
    return user_id
    
UserID = Annotated[int, Depends(get_user_id)]
