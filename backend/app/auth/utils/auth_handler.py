import settings
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import jwt
from fastapi.security import HTTPBearer
from fastapi import Depends
from fastapi import HTTPException
from loguru import logger
from app.auth.services.universal import get_user_by_username
from app.auth.services.universal import get_user_by_id


class AuthHandler:

    security = HTTPBearer(
        scheme_name='Authorization'
    )

    async def encode_token(
        self,
        username: str,
        access_token_expires: timedelta = timedelta(hours=24),
        otp_expires: timedelta = timedelta(hours=1),
    ) -> str:
        """
        Encode a JWT token for the given username.

        Args:
            username (str): The username of the user for whom the token is to be encoded.
            access_token_expires (timedelta, optional): The duration after which the access token expires.
            otp_expires (timedelta, optional): The duration after which the OTP expires.

        Returns:
            str: The encoded JWT token.

        Raises:
            HTTPException: If the user with the given username is not found.
        """

        logger.info(f"Encode token with username={username}")

        user = await get_user_by_username(username)

        payload = {
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + access_token_expires,
            "iss": settings.ISSUER_NAME,
            "sub": user.id,
            "is_admin": user.is_admin,
            "otp_expires": int(datetime.now(timezone.utc).timestamp()) + otp_expires.seconds,
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    async def decode_token(
        self,
        token: str
    ) -> dict:
        """
        Decode a JWT token.

        Args:
            token (str): The JWT token to decode.

        Returns:
            dict: The decoded payload.

        Raises:
            HTTPException: If the token is expired or invalid.
        """

        logger.info(f'Decode token with token={token}')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

            if payload.get('exp') < int(datetime.now(timezone.utc).timestamp()):

                logger.error(f'Token expired')

                raise HTTPException(
                    status_code=401,
                    detail='Token expired'
                )

            user_id = payload.get('sub')

            user = await get_user_by_id(user_id)

            if not user:

                logger.error(f'User with user_id={user_id} not found')

                raise HTTPException(
                    status_code=404,
                    detail=f'User with user_id={user_id} not found'
                )

            if user.is_logged_out:

                logger.error(f'User with user_id={user_id} is logged out')

                raise HTTPException(
                    status_code=401,
                    detail=f'User with user_id={user_id} is logged out'
                )

            return payload
        except jwt.InvalidTokenError:

            logger.error(f'Invalid token')

            raise HTTPException(
                status_code=401,
                detail='Invalid token'
            )

    async def get_current_user_id(
        self,
        credentials: str = Depends(security)
    ) -> int:
        """
        Get the current user's id from the given JWT token.

        Args:
            credentials (str): The JWT token to decode.

        Returns:
            int: The id of the current user.

        Raises:
            HTTPException: If the token is expired or invalid.
        """
        token = credentials.credentials

        logger.info(f'Get current user id with token={token}')

        payload = await self.decode_token(token)

        user_id = payload.get('sub')

        return user_id

    async def check_otp(
        self,
        credentials: str = Depends(security)
    ) -> dict:
        """
        Check if the OTP in the JWT token is still valid.

        Args:
            credentials (str): The JWT token to decode.

        Returns:
            dict: The decoded payload if the OTP is valid.

        Raises:
            HTTPException: If the OTP is expired.
        """
        token = credentials.credentials

        logger.info(f'Check otp with token={token}')

        payload = await self.decode_token(token)

        if payload.get('otp_expires') < int(datetime.now(timezone.utc).timestamp()):

            logger.error(f'OTP expired')

            raise HTTPException(
                status_code=401,
                detail='OTP expired'
            )

        return payload

    async def get_current_user_id_with_check_otp(
        self,
        credentials: str = Depends(security)
    ) -> int:
        """
        Get the current user id with check otp.

        This function first checks if the JWT token contains a valid OTP using
        the check_otp function. If the OTP is valid, it then calls the
        get_current_user_id function to retrieve the user id.

        Args:
            credentials (str): The JWT token to decode.

        Returns:
            int: The user id if the OTP is valid.

        Raises:
            HTTPException: If the OTP is expired or invalid.
        """

        token = credentials.credentials

        logger.info(f'Get current user id with check otp token:{token}')

        await self.check_otp(credentials)
        return await self.get_current_user_id(credentials)

    async def is_role_admin(
        self,
        credentials: str = Depends(security)
    ) -> bool:
        """
        Check if the current user has an admin role from the given JWT token.

        Args:
            credentials (str): The JWT token to decode.

        Returns:
            bool: True if the user is an admin, False otherwise.

        Raises:
            HTTPException: If the user is not an admin.
        """
        token = credentials.credentials

        logger.info(f'Check role admin with token={token}')

        payload = await self.check_otp(credentials)

        user_id = payload.get('sub')
        is_admin = payload.get('is_admin')

        if not is_admin:

            logger.error(f'User with user_id={user_id} is not admin')

            raise HTTPException(
                status_code=403,
                detail=f'User with user_id={user_id} is not admin'
            )

    async def get_jwt_expires_seconds(
        self,
        credentials: str = Depends(security)
    ) -> int:
        """
        Get the remaining seconds before the JWT token expires.

        This function decodes the JWT token to retrieve its expiration timestamp
        and calculates the remaining time until it expires.

        Args:
            credentials (str): The JWT token to decode.

        Returns:
            int: The number of seconds remaining before the token expires.

        Raises:
            HTTPException: If the token is expired or invalid.
        """
        token = credentials.credentials

        logger.info(f'Get jwt expires seconds with token={token}')

        payload = await self.decode_token(token)

        return payload.get('exp') - int(datetime.now(timezone.utc).timestamp())
