from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    code: int = 2000
    msg: str = 'Success'
    access_token: str
    token_type: str = 'bearer'
    is_superuser: Optional[bool] = None
    # userinfo: UserInfo
