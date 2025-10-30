from fastapi import APIRouter
from fastapi import Depends
from fastapi import Security
from loguru import logger
from app.auth.schema.auth import UserResponse
from app.auth.schema.users import GetAllUsersResponse
from app.auth.schema.users import GetOneUserResponse
from app.auth.schema.users import UpdateUserRequest
from app.auth.schema.users import UpdateUserResponse
from app.auth.schema.users import RemoveUserResponse
from app.auth.services.universal import select_all_users
from app.auth.services.universal import get_user_by_id
from app.auth.services.universal import update_user_by_id
from app.auth.services.universal import remove_user_by_id
from app.auth.utils.auth_handler import AuthHandler


users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get(
    '',
    response_model=GetAllUsersResponse,
    dependencies=[Security(AuthHandler().is_role_admin)],
)
async def get_all_users(
) -> GetAllUsersResponse:
    """
    Get all users.

    Returns:
        GetAllUsersResponse: The response containing all the users.

    Raises:
        HTTPException: If the user is not an admin.
    """

    logger.info(f'Get all users')

    users = await select_all_users()

    return GetAllUsersResponse(
        success=True,
        message='Get all users successful',
        users=[UserResponse(
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
        ) for user in users
        ],
    )


@users_router.get(
    '/{id}',
    response_model=GetOneUserResponse,
    dependencies=[Security(AuthHandler().is_role_admin)],
)
async def get_one_user(
    id: int,
) -> GetOneUserResponse:
    """
    Get user by id.

    Args:
        id (int): The ID of the user to fetch.

    Returns:
        GetOneUserResponse: The response containing the user object if the user exists, None otherwise.

    Raises:
        HTTPException: If the user with the given ID is not found or if the user is not an admin.
    """

    logger.info(f'Get user by id with id={id}')

    user = await get_user_by_id(id)

    return GetOneUserResponse(
        success=True,
        message='Get user by id successful',
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


@users_router.put(
    '',
    response_model=UpdateUserResponse,
)
async def update_user(
    request: UpdateUserRequest,
    current_user_id: int = Depends(AuthHandler().get_current_user_id_with_check_otp),
) -> UpdateUserResponse:
    """
    Update the user with the given current user id.

    Args:
        request (UpdateUserRequest): The request containing the user info to update.
        current_user_id (int): The id of the current user.

    Returns:
        UpdateUserResponse: The response containing the success status, message, and user object if the user is updated successfully.

    Raises:
        HTTPException: If the user with the given id is not found.
    """

    logger.info(f'Update user with current_user_id={current_user_id}')

    user = await update_user_by_id(current_user_id, request)

    return UpdateUserResponse(
        success=True,
        message='Update user successful',
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


@users_router.delete(
    '/{id}',
    response_model=RemoveUserResponse,
    dependencies=[Security(AuthHandler().is_role_admin)],
)
async def remove_user(
    id: int,
) -> RemoveUserResponse:
    """
    Remove the user with the given user id.

    Args:
        id (int): The id of the user to remove.

    Returns:
        RemoveUserResponse: The response containing the success status and message.

    Raises:
        HTTPException: If the user with the given id is not found or if the user is not an admin.
    """

    logger.info(f'Remove user with id={id}')

    await remove_user_by_id(id)

    return RemoveUserResponse(
        success=True,
        message='Remove user successful',
    )
