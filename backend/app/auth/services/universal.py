import settings
from datetime import datetime
from datetime import timedelta
from database import get_db_session
from sqlalchemy import select
from fastapi import HTTPException
from loguru import logger


from app.auth.models.users import User
from app.auth.models.users import ResetPassword
from app.auth.schema.auth import RegisterUserRequest
from app.auth.schema.users import UpdateUserRequest
from app.auth.utils.password_manager import PasswordManager
from app.auth.utils.random_text import random_text
from app.utils.render_html_template import render_html_template
from app.utils.send_email import send_email


async def create_admin_default():
    """
    Called on application startup.  Currently just creates the admin
    user if it doesn't already exist.
    """

    logger.info("Creating admin default user...")

    is_admin_default_exists = await check_admin_default()

    if not is_admin_default_exists:

        logger.info("Creating admin default user...")

        password = PasswordManager().get_password_hash(settings.ADMIN_DEFAULT_PASSWORD)

        new_user = User(
            name=settings.ADMIN_DEFAULT_NAME,
            age=settings.ADMIN_DEFAULT_AGE,
            username=settings.ADMIN_DEFAULT_USERNAME,
            email=settings.ADMIN_DEFAULT_EMAIL,
            password=password,
            is_admin=True
        )

        await add_user_with_password_hash(new_user)
    else:

        logger.info("Admin default user already exists...")


async def check_admin_default():
    """
    Check if the admin default user exists.

    Returns:
        bool: True if the admin default user exists, False otherwise.
    """

    logger.info("Check admin default user...")

    return await get_user_by_username(settings.ADMIN_DEFAULT_USERNAME)


async def get_user_by_username(username: str) -> User:
    """
    Get user by username.

    Args:
        username (str): The username of the user to fetch.

    Returns:
        User: The user object if the user exists, None otherwise.
    """

    logger.info(f"Get user by username={username}")

    async with get_db_session() as session:
        statement = select(User).where(User.username == username)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user


async def add_user_with_password_hash(
        user: User
) -> User:
    """
    Create a user.

    Args:
        name (str): The name of the user.
        age (int): The age of the user.
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.
        is_admin (bool): Is the user an admin.

    Returns:
        User: The created user object.
    """

    logger.info(f"Creating user with username={user.username}")

    async with get_db_session() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def authentication_user(
    username: str,
    password: str,
) -> User:
    """
    Authentication user.

    Args:
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        User: The authenticated user object.
    """

    logger.info(f'Authentication user with username={username}')

    user = await get_user_by_username(username)

    if not user:

        logger.error(f'Incorrect username or password')

        raise HTTPException(
            status_code=404,
            detail=f'Incorrect username or password'
        )

    if not PasswordManager().verify_password(password, user.password):

        logger.error(f'Incorrect username or password')

        raise HTTPException(
            status_code=401,
            detail=f'Incorrect username or password'
        )

    return user


async def update_user(username: str, **kwargs) -> User:
    """
    Updates a user with the given username.

    Args:
        username (str): The username of the user to update.
        **kwargs: The keyword arguments to update the user with.

    Returns:
        User: The updated user if found, None otherwise.
    """

    logger.info(f"Update user: {username}")

    try:
        user = await get_user_by_username(username)

        if user:
            async with get_db_session() as session:
                for key, value in kwargs.items():
                    setattr(user, key, value)

                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
        else:

            logger.warning(f"User '{username}' not found")

            return None
    except Exception as e:

        logger.error(f"Error: {e}")

        return None


async def get_user_by_id(
    user_id: int,
) -> User:
    """
    Get user by ID.

    Args:
        user_id (int): The ID of the user to fetch.

    Returns:
        User: The user object if the user exists, None otherwise.
    """

    logger.info(f'Get user by id with user_id={user_id}')

    async with get_db_session() as session:
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user


async def get_user_by_email(
    email: str,
) -> User:
    """
    Get user by email.

    Args:
        email (str): The email of the user to fetch.

    Returns:
        User: The user object if the user exists, None otherwise.
    """

    logger.info(f'Get user by email with email={email}')

    async with get_db_session() as session:
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user


async def register_user(
    request: RegisterUserRequest,
) -> User:
    """
    Register a user.

    Args:
        request (RegisterUserRequest): The request of the user to register.

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If the password and password confirm do not match.
    """

    logger.info(f'Register user with username={request.username}')

    user_exists_by_username = await get_user_by_username(request.username)

    if user_exists_by_username:

        logger.error(f'User with username={request.username} already exists')

        raise HTTPException(
            status_code=400,
            detail=f'User with username={request.username} already exists'
        )
    user_exists_by_email = await get_user_by_email(request.email)

    if user_exists_by_email:

        logger.error(f'User with email={request.email} already exists')

        raise HTTPException(
            status_code=400,
            detail=f'User with email={request.email} already exists'
        )

    if request.password != request.password_confirm:

        logger.error(f'Password and password confirm do not match')

        raise HTTPException(
            status_code=400,
            detail=f'Password and password confirm do not match'
        )

    password = PasswordManager().get_password_hash(request.password)

    new_user = User(
        name=request.name,
        age=request.age,
        username=request.username,
        email=request.email,
        password=password,
        is_admin=request.is_admin,
    )

    return await add_user_with_password_hash(new_user)


async def forgot_password_user_by_email(
    host: str,
    username: str,
    email: str,
) -> None:
    """
    Forgot password user by id.

    Args:
        host (str): The host of the system.
        username (str): The username of the user to forgot password.
        email (str): The email of the user to forgot password.

    Raises:
        HTTPException: If the user with the given id is not found.
    """

    logger.info(f'Forgot password user by email with username={username}, email={email}')

    user = await get_user_by_username(username)

    if not user:

        logger.error(f'User with username={username} not found')

        raise HTTPException(
            status_code=404,
            detail=f'User with username={username} not found'
        )

    if user.email != email:

        logger.error(f'User with username={username} and email={email} not found')

        raise HTTPException(
            status_code=404,
            detail=f'User with username={username} and email={email} not found'
        )

    secret = await random_text()
    secret_hash = PasswordManager().get_password_hash(secret)

    async with get_db_session() as session:
        statement = select(ResetPassword).where(ResetPassword.user_id == user.id)
        result = await session.execute(statement)
        user_reset_password = result.scalars().first()

        if user_reset_password:
            user_reset_password.secret = secret_hash
            user_reset_password.updated_at = datetime.now()
            session.add(user_reset_password)
            await session.commit()
            await session.refresh(user_reset_password)
        else:
            new_user_reset_password = ResetPassword(
                user_id=user.id,
                secret=secret_hash,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            session.add(new_user_reset_password)
            await session.commit()
            await session.refresh(new_user_reset_password)

    html_content = render_html_template(
        path_file_template="app/email/forgot_password.html",
        context={
            "name": user.name,
            "url": f"{host}api/auth/reset-password/{username}/{secret}",
        }
    )

    await send_email(
        subject="Forgot password",
        html_content=html_content,
        email_to=user.email
    )


async def reset_password_user_by_secret(
    username: str,
    secret: str,
) -> str:
    """
    Reset password user by secret.

    Args:
        username (str): The username of the user to reset password.
        secret (str): The secret of the user to reset password.

    Returns:
        str: The response of the reset password request.

    Raises:
        HTTPException: If the user with the given username is not found.
        HTTPException: If the reset password with the given username is not found.
        HTTPException: If the secret is incorrect.
        HTTPException: If the user reset password with the given username and secret expired.
    """

    logger.info(f'Reset password user by username={username}, secret={secret}')

    user = await get_user_by_username(username)

    if not user:

        logger.error(f'User with username={username} not found')

        raise HTTPException(
            status_code=404,
            detail=f'User with username={username} not found'
        )

    async with get_db_session() as session:
        statement = select(ResetPassword).where(ResetPassword.user_id == user.id)
        result = await session.execute(statement)
        user_reset_password = result.scalars().first()

    if not user_reset_password:

        logger.error(f'User reset password with username={username} not found')

        raise HTTPException(
            status_code=404,
            detail=f'User reset password with username={username} not found'
        )

    if not PasswordManager().verify_password(secret, user_reset_password.secret):

        logger.error(f'Incorrect secret: {secret}')

        raise HTTPException(
            status_code=404,
            detail=f'Incorrect secret: {secret}'
        )

    if user_reset_password.updated_at < datetime.now() - timedelta(minutes=settings.RESET_PASSWORD_EXPIRED_MINUTES):

        logger.error(f'User reset password with username={username} and secret={secret} expired')

        raise HTTPException(
            status_code=404,
            detail=f'User reset password with username={username} and secret={secret} expired'
        )

    user_reset_password.secret = None
    user_reset_password.updated_at = datetime.now()
    session.add(user_reset_password)
    await session.commit()
    await session.refresh(user_reset_password)

    new_password = await random_text(length=12)
    new_password_hash = PasswordManager().get_password_hash(new_password)
    await update_user(username, password=new_password_hash)

    html_content = render_html_template(
        path_file_template="app/html/reset_password.html",
        context={
            "name": user.name,
            "new_password": new_password,
        }
    )

    return html_content


async def change_password_user(
    current_user_id: int,
    password: str,
    password_confirm: str,
) -> User:
    """
    Change password of the user with the given current user id.

    Args:
        current_user_id (int): The id of the current user.
        password (str): The new password.
        password_confirm (str): The new password confirm.

    Returns:
        User: The user object if the password is changed successfully, None otherwise.

    Raises:
        HTTPException: If the user with the given id is not found.
        HTTPException: If the password and password confirm do not match.
    """

    logger.info(f'Change password with current_user_id={current_user_id}')

    user = await get_user_by_id(current_user_id)

    if not user:

        logger.error(f'User with current_user_id={current_user_id} not found')

        raise HTTPException(
            status_code=404,
            detail=f'User with current_user_id={current_user_id} not found'
        )

    if password != password_confirm:

        logger.error(f'Password and password confirm do not match')

        raise HTTPException(
            status_code=400,
            detail=f'Password and password confirm do not match'
        )

    new_password_hash = PasswordManager().get_password_hash(password)
    await update_user(user.username, password=new_password_hash)

    return user


async def select_all_users() -> list[User]:
    """
    Retrieve all users from the database.

    Returns:
        list[User]: A list of all user objects.

    Logs:
        Logs the selection of all users.
    """

    logger.info(f'Select all users')

    async with get_db_session() as session:
        statement = select(User)
        result = await session.execute(statement)
        users = result.scalars().all()

    return users


async def update_user_by_id(
    current_user_id: int,
    request: UpdateUserRequest,
) -> User:
    """
    Update the user with the given current user id.

    Args:
        current_user_id (int): The id of the current user.
        request (UpdateUserRequest): The request containing the user info to update.

    Returns:
        User: The user object if the user is updated successfully, None otherwise.

    Raises:
        HTTPException: If the user with the given id is not found.
    """

    logger.info(f'Update user by id with current_user_id={current_user_id}')

    user = await get_user_by_id(current_user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'User with current_user_id={current_user_id} not found'
        )

    data_update = {}

    if request.name:
        data_update['name'] = request.name

    if request.age:
        data_update['age'] = request.age

    if request.email:

        user_exists_by_email = await get_user_by_email(request.email)

        if user_exists_by_email:
            raise HTTPException(
                status_code=400,
                detail=f'User with email={request.email} already exists'
            )

        data_update['email'] = request.email

    user = await update_user(
        user.username,
        **data_update
    )

    return user


async def remove_user_by_id(
    user_id: int,
) -> None:
    """
    Remove a user by their ID.

    Args:
        user_id (int): The ID of the user to remove.

    Raises:
        HTTPException: If the user with the given ID is not found.
    """

    logger.info(f'Remove user by id with user_id={user_id}')

    user = await get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'User with user_id={user_id} not found'
        )

    async with get_db_session() as session:
        async with session.begin():
            await session.delete(user)
            await session.commit()
