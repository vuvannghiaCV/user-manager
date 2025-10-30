import settings
from datetime import timedelta
from fastapi import APIRouter
from fastapi import Path
from fastapi import Query
from fastapi import Depends
from fastapi import Security
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from loguru import logger


from app.auth.utils.otp_handler import OtpHandler
from app.auth.utils.auth_handler import AuthHandler
from app.auth.schema.auth import LoginUserResponse
from app.auth.schema.auth import UserResponse
from app.auth.schema.auth import GetCurrentUserResponse
from app.auth.schema.auth import RegisterUserRequest
from app.auth.schema.auth import RegisterUserResponse
from app.auth.schema.auth import ForgotPasswordResponse
from app.auth.schema.auth import ChangePasswordRequest
from app.auth.schema.auth import ChangePasswordResponse
from app.auth.schema.auth import VerifyOtpRequest
from app.auth.schema.auth import VerifyOtpResponse
from app.auth.schema.auth import DownloadRecoveryOtpResponse
from app.auth.schema.auth import VerifyRecoveryOtpResponse
from app.auth.schema.auth import LogoutUserResponse
from app.auth.services.universal import authentication_user
from app.auth.services.universal import update_user
from app.auth.services.universal import get_user_by_id
from app.auth.services.universal import register_user
from app.auth.services.universal import forgot_password_user_by_email
from app.auth.services.universal import reset_password_user_by_secret
from app.auth.services.universal import change_password_user


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    '/register',
    response_model=RegisterUserResponse,
    status_code=201,
    dependencies=[Security(AuthHandler().is_role_admin)],
)
async def register(
    request: RegisterUserRequest
) -> RegisterUserResponse:
    """
    Register a user.

    Args:
        request (RegisterUserRequest): The request of the user to register.

    Returns:
        RegisterUserResponse: The response of the register request.

    Raises:
        HTTPException: If the password and password confirm do not match.
    """

    logger.info(f'Register user with username={request.username}')

    user = await register_user(request)

    return RegisterUserResponse(
        success=True,
        message='Register user successful',
        user=UserResponse(
            id=user.id,
            name=user.name,
            age=user.age,
            username=user.username,
            email=user.email,
            is_admin=user.is_admin,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_enable_otp=user.is_enable_otp,
            is_logged_out=user.is_logged_out,
        ),
    )


@auth_router.post(
    '/login',
    response_model=LoginUserResponse,
)
async def login_user(
    username: str = Query(
        ...,
        description="Username of the user"
    ),
    password: str = Query(
        ...,
        description="Password of the user"
    ),
) -> LoginUserResponse:
    """
    Login a user.

    Args:
        username (str): The username of the user to login.
        password (str): The password of the user to login.

    Returns:
        LoginUserResponse: The response of the login request.

    Raises:
        HTTPException: If the user does not exist or the password is incorrect.
    """

    logger.info(f'Login with username={username}')

    user = await authentication_user(username, password)
    await update_user(user.username, is_logged_out=False)

    otp_qr_code_base64 = None
    if not user.is_enable_otp:
        otp_qr_code_base64 = await OtpHandler().generate_otp_qr_code_base64(user.username)

    access_token = await AuthHandler().encode_token(
        username=user.username,
        access_token_expires=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        otp_expires=timedelta(minutes=0),
    )

    return LoginUserResponse(
        success=True,
        message="Login successful",
        access_token=access_token,
        otp_qr_code_base64=otp_qr_code_base64
    )


@auth_router.get(
    '/convert-otp-qr-code-base64-to-image',
    deprecated=True,
)
async def convert_otp_qr_code_base64_to_image(
    otp_qr_code_base64: str = Query(
        ...,
        description="OTP QR code base64",
    ),
):
    """
    Convert OTP QR code base64 to image

    Args:
        otp_qr_code_base64 (str): OTP QR code base64

    Returns:
        StreamingResponse: The image response

    Note:
        This endpoint is deprecated and will be removed soon.
    """

    logger.info(f'Convert OTP to image with otp_qr_code_base64={otp_qr_code_base64}')

    try:

        import base64
        from io import BytesIO
        from fastapi.responses import StreamingResponse

        img_data = base64.b64decode(otp_qr_code_base64)
        buffered = BytesIO(img_data)

        return StreamingResponse(buffered, media_type="image/png")
    except Exception as e:

        logger.error(f'Error converting OTP to image: {e}')

        raise HTTPException(
            status_code=400,
            detail="Error converting OTP to image"
        )


@auth_router.get(
    '/current-user',
    response_model=GetCurrentUserResponse,
)
async def get_current_user(
    current_user_id: int = Depends(AuthHandler().get_current_user_id_with_check_otp)
) -> GetCurrentUserResponse:
    """
    Get the current user by the given current user id.

    Args:
        current_user_id (int): The id of the current user.

    Returns:
        GetCurrentUserResponse: The response of the get current user request.

    Raises:
        HTTPException: If the user with the given id is not found.
    """

    logger.info(f'Get current user with current_user_id={current_user_id}')

    user = await get_user_by_id(current_user_id)

    if not user:

        logger.error(f'User with id={current_user_id} not found')

        raise HTTPException(
            status_code=404,
            detail=f'User with id={current_user_id} not found'
        )

    return GetCurrentUserResponse(
        success=True,
        message='Get current user successful',
        user=UserResponse(
            id=user.id,
            name=user.name,
            age=user.age,
            username=user.username,
            email=user.email,
            is_admin=user.is_admin,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_enable_otp=user.is_enable_otp,
            is_logged_out=user.is_logged_out,
        ),
    )


@auth_router.post(
    '/mfa/verify-otp',
    response_model=VerifyOtpResponse,
)
async def verify_otp(
    request: VerifyOtpRequest,
    current_user_id: int = Depends(AuthHandler().get_current_user_id),
    jwt_expires_seconds: int = Depends(AuthHandler().get_jwt_expires_seconds),
) -> VerifyOtpResponse:
    """
    Verify the user's OTP.

    Args:
        request (VerifyOtpRequest): The OTP request containing the OTP code to verify.
        current_user_id (int): The ID of the current user.
        jwt_expires_seconds (int): The duration in seconds after which the JWT expires.

    Returns:
        VerifyOtpResponse: The response containing the success status, message, and access token.

    Raises:
        HTTPException: If the OTP is incorrect or the user is not found.
    """

    logger.info(f'Verify OTP with code={request.code}')

    user = await OtpHandler().verify_otp(current_user_id, request.code)

    access_token = await AuthHandler().encode_token(
        username=user.username,
        access_token_expires=timedelta(seconds=jwt_expires_seconds),
        otp_expires=timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
    )

    return VerifyOtpResponse(
        success=True,
        message="Verify OTP successful",
        access_token=access_token,
    )


@auth_router.get(
    '/mfa/download-recovery-otp',
    response_model=DownloadRecoveryOtpResponse,
)
async def download_recovery_otp(
    current_user_id: int = Depends(AuthHandler().get_current_user_id_with_check_otp),
) -> DownloadRecoveryOtpResponse:
    """
    Download recovery OTP.

    This endpoint returns a list of recovery OTPs for the current user.

    Args:
        current_user_id (int): The id of the current user.

    Returns:
        DownloadRecoveryOtpResponse: The response of the download recovery OTP request.

    Raises:
        HTTPException: If the user with the given id is not found.
    """

    logger.info(f'Download recovery OTP with current_user_id={current_user_id}')

    list_otp_recovery = await OtpHandler().generate_otp_recovery(current_user_id)

    return DownloadRecoveryOtpResponse(
        success=True,
        message='Download recovery OTP successful',
        list_otp_recovery=list_otp_recovery,
    )


@auth_router.post(
    '/mfa/verify-recovery-otp',
    response_model=VerifyRecoveryOtpResponse,
)
async def verify_recovery_otp(
    code: str,
    current_user_id: int = Depends(AuthHandler().get_current_user_id_with_check_otp),
) -> VerifyRecoveryOtpResponse:
    """
    Verify the user's recovery OTP.

    This endpoint verifies the recovery OTP code provided by the user.
    If the code is correct, the user's OTP settings will be updated.

    Args:
        code (str): The recovery OTP code to verify.
        current_user_id (int): The ID of the current user.

    Returns:
        VerifyRecoveryOtpResponse: The response containing the success status and message.

    Raises:
        HTTPException: If the recovery OTP is incorrect or the user is not found.
    """

    logger.info(f'Verify recovery OTP with current_user_id={current_user_id} and code={code}')

    await OtpHandler().verify_otp_recovery(current_user_id, code)

    return VerifyRecoveryOtpResponse(
        success=True,
        message='Verify recovery OTP successful',
    )


@auth_router.post(
    '/forgot-password',
    response_model=ForgotPasswordResponse,
)
async def forgot_password(
    request: Request,
    username: str = Query(
        "admin.example",
        description="Username of the user",
    ),
    email: str = Query(
        "admin@admin.admin.example",
        description="Email of the user",
    ),
) -> ForgotPasswordResponse:
    """
    Forgot password.

    Args:
        request (Request): The request object.
        email (str): The email of the user.

    Returns:
        ForgotPasswordResponse: The response of the forgot password request.
    """

    logger.info(f'Forgot password with username={username}, email={email}')

    host = request.base_url
    await forgot_password_user_by_email(host, username, email)

    return ForgotPasswordResponse(
        success=True,
        message='Send email to reset password successful',
    )


@auth_router.get(
    '/reset-password/{username}/{secret}',
    response_class=HTMLResponse,
    deprecated=True,
)
async def reset_password(
    username: str = Path(
        ...,
        description="Username of the user",
    ),
    secret: str = Path(
        ...,
        description="Secret of the user",
    ),
) -> HTMLResponse:
    """
    Reset password.

    Args:
        username (str): The username of the user.
        secret (str): The secret of the user.

    Returns:
        HTMLResponse: The response of the reset password request.

    Raises:
        HTTPException: If the user with the given username is not found.
        HTTPException: If the reset password with the given username is not found.
        HTTPException: If the secret is incorrect.
        HTTPException: If the user reset password with the given username and secret expired.
    """

    logger.info(f'Reset password with username={username}, secret={secret}')

    html_content = await reset_password_user_by_secret(username, secret)

    return HTMLResponse(content=html_content)


@auth_router.put(
    '/change-password',
    response_model=ChangePasswordResponse,
)
async def change_password(
    request: ChangePasswordRequest,
    current_user_id: int = Depends(AuthHandler().get_current_user_id_with_check_otp),
) -> ChangePasswordResponse:
    """
    Change password.

    Args:
        request (ChangePasswordRequest): The request to change password.
        current_user_id (int): The id of the current user.

    Returns:
        ChangePasswordResponse: The response of the change password request.

    Raises:
        HTTPException: If the user with the given id is not found.
    """

    logger.info(f'Change password with current_user_id={current_user_id}')

    await change_password_user(current_user_id, request.password, request.password_confirm)

    return ChangePasswordResponse(
        success=True,
        message='Change password successful',
    )


@auth_router.post(
    '/logout',
    response_model=LogoutUserResponse,
)
async def logout_user(
    current_user_id: int = Depends(AuthHandler().get_current_user_id),
) -> LogoutUserResponse:
    """
    Logout the current user.

    This endpoint logs out the current user by updating their status 
    to logged out in the database.

    Args:
        current_user_id (int): The ID of the current user.

    Returns:
        LogoutUserResponse: The response of the logout request.
    """

    logger.info(f'Logout with current_user_id={current_user_id}')

    await update_user(current_user_id, is_logged_out=True)

    return LogoutUserResponse(
        success=True,
        message='Logout successful',
    )
