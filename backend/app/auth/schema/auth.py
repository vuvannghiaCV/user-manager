from app.common.schema.response_template import ResponseTemplate


from datetime import datetime
from pydantic import BaseModel
from pydantic import Field
from typing import List
from typing import Optional


class LoginUserResponse(ResponseTemplate):

    access_token: str = Field(
        ...,
        description="Access token",
    )
    otp_qr_code_base64: Optional[str] = Field(
        None,
        description="OTP QR code base64",
    )


class UserResponse(BaseModel):

    id: int = Field(
        ...,
        description="User id",
    )
    name: str = Field(
        ...,
        description="User name",
    )
    age: int = Field(
        ...,
        description="User age",
    )
    username: str = Field(
        ...,
        description="User username",
    )
    email: str = Field(
        ...,
        description="User email",
    )
    is_admin: bool = Field(
        ...,
        description="User is admin",
    )
    created_at: datetime = Field(
        ...,
        description="User created at",
    )
    updated_at: datetime = Field(
        ...,
        description="User updated at",
    )
    is_enable_otp: bool = Field(
        ...,
        description="User is enable OTP",
    )
    is_logged_out: bool = Field(
        ...,
        description="User is logged out",
    )


class GetCurrentUserResponse(ResponseTemplate):

    user: UserResponse = Field(
        ...,
        description="User",
    )


class RegisterUserRequest(BaseModel):

    name: str = Field(
        "Vu Van Nghia",
        description="User name",
        regex=r'^[a-zA-Z\s]+$',
    )
    age: int = Field(
        20,
        gt=0,
        le=100,
        description="Age must be a valid integer.",
    )
    username: str = Field(
        "vu_van_nghia_1",
        min_length=5,
        max_length=50,
        regex=r'^[a-zA-Z0-9_]+$',
        description="Username must be between 5 and 50 characters long and must only contain alphanumeric characters and underscores."
    )
    email: str = Field(
        "vu_van_nghia_1@gmail.com",
        regex=r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$',
        description="Email must be a valid email address."
    )
    password: str = Field(
        ...,
        regex=r'^(?!.*[_;*\'"`])(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$',
        description="Password must be between 8 and 255 characters long."
    )
    password_confirm: str = Field(
        ...,
        regex=r'^(?!.*[_;*\'"`])(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$',
        description="Password confirm must be between 8 and 255 characters long."
    )
    is_admin: bool = Field(
        False,
        description="Is role admin"
    )


class RegisterUserResponse(GetCurrentUserResponse):

    pass


class ForgotPasswordResponse(ResponseTemplate):

    pass


class ChangePasswordRequest(BaseModel):

    password: str = Field(
        ...,
        description="User password",
        regex=r'^(?!.*[_;*\'"`])(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$',
    )
    password_confirm: str = Field(
        ...,
        description="User password confirm",
        regex=r'^(?!.*[_;*\'"`])(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$',
    )


class ChangePasswordResponse(ResponseTemplate):

    pass


class VerifyOtpRequest(BaseModel):

    code: str = Field(
        ...,
        description="OTP code",
        min_length=6,
        max_length=6,
        regex=r'^[0-9]+$',
    )


class VerifyOtpResponse(ResponseTemplate):

    access_token: str = Field(
        ...,
        description="Access token",
    )


class DownloadRecoveryOtpResponse(ResponseTemplate):

    list_otp_recovery: List[str] = Field(
        ...,
        description="List OTP recovery",
    )


class VerifyRecoveryOtpResponse(ResponseTemplate):

    pass


class LogoutUserResponse(ResponseTemplate):

    pass
