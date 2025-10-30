from app.common.schema.response_template import ResponseTemplate


from pydantic import BaseModel
from pydantic import Field
from typing import Optional


from app.auth.schema.auth import UserResponse


class GetAllUsersResponse(ResponseTemplate):

    users: list[UserResponse] = Field(
        ...,
        description="Users",
    )


class GetOneUserResponse(ResponseTemplate):

    user: UserResponse


class UpdateUserRequest(BaseModel):

    name: Optional[str] = Field(
        None,
        description="User name",
        regex=r'^[a-zA-Z\s]+$',
    )
    age: Optional[int] = Field(
        None,
        description="User age",
        gt=0,
        le=100,
    )
    email: Optional[str] = Field(
        None,
        description="User email",
        regex=r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$',
    )


class UpdateUserResponse(GetOneUserResponse):

    pass


class RemoveUserResponse(ResponseTemplate):

    pass
