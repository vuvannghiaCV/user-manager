import settings
import pyotp
import qrcode
import base64
from io import BytesIO
from fastapi import HTTPException
from loguru import logger
from app.auth.models.users import User
from app.auth.services.universal import get_user_by_username
from app.auth.services.universal import get_user_by_id
from app.auth.services.universal import update_user
from app.auth.utils.random_text import random_text


class OtpHandler:

    async def generate_otp_qr_code_base64(self, username: str) -> str:
        """
        Generate OTP QR Code Base64 for the given username.

        Args:
            username (str): The username of the user to generate OTP QR Code Base64.

        Returns:
            str: The OTP QR Code Base64 string.
        """

        logger.info(f'Generate OTP QR Code Base64 with username: {username}')

        otp_secret = await self.generate_secret_if_not_exits(username)
        uri = await self.create_uri_from_secret(username, otp_secret)
        otp_qr_code_base64 = await self.create_qr_from_uri(uri)
        return otp_qr_code_base64

    async def generate_secret_if_not_exits(self, username: str) -> str:
        """
        Generate a secret for the user if it does not exist.

        This function checks if the provided username exists in the database.
        If the user is found and does not have an existing OTP secret, a new
        secret is generated and updated in the user's record.

        Args:
            username (str): The username of the user for whom the secret is to be generated.

        Returns:
            str: The OTP secret for the user.

        Raises:
            HTTPException: If the user with the given username is not found.
        """

        logger.info(f'Generate secret if not exits with username: {username}')

        user = await get_user_by_username(username)

        if not user:

            logger.error(f"User with username '{username}' not found")

            raise HTTPException(
                status_code=404,
                detail=f"User with username '{username}' not found"
            )

        otp_secret = user.otp_secret
        if not otp_secret:
            otp_secret = pyotp.random_base32()
        await update_user(username, otp_secret=otp_secret)

        return otp_secret

    async def create_uri_from_secret(self, username: str, otp_secret: str) -> str:
        """
        Create a URI from the given OTP secret for the user.

        Args:
            username (str): The username of the user.
            otp_secret (str): The OTP secret for the user.

        Returns:
            str: The URI for the user's OTP.
        """

        logger.info(f'Create URI from secret with username: {username}')

        totp = pyotp.TOTP(otp_secret)

        return totp.provisioning_uri(
            issuer_name=settings.ISSUER_NAME,
            name=username
        )

    async def create_qr_from_uri(self, uri: str) -> str:
        """
        Create a QR code from the given URI and return it as a base64-encoded string.

        Args:
            uri (str): The URI to create a QR code from.

        Returns:
            str: The base64-encoded QR code string.
        """

        logger.info(f'Create QR from URI with uri: {uri}')

        qr_img = qrcode.make(uri)
        buffered = BytesIO()
        qr_img.save(buffered, "PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return qr_base64

    async def verify_otp(
        self,
        user_id: int,
        code: str,
    ) -> User:
        """
        Verify the user's OTP.

        Args:
            user_id (int): The ID of the user to verify the OTP for.
            code (str): The OTP code to verify.

        Returns:
            User: The user object if the OTP is correct.

        Raises:
            HTTPException: If the user with the given ID is not found or if the OTP is incorrect.
        """

        logger.info(f'Verify OTP with code={code}')

        user = await get_user_by_id(user_id)

        if not user:

            logger.error(f"User with id '{user_id}' not found")

            raise HTTPException(
                status_code=404,
                detail=f"User with id '{user_id}' not found"
            )

        totp = pyotp.TOTP(user.otp_secret)
        if not totp.verify(code):
            raise HTTPException(
                status_code=400,
                detail="Incorrect OTP."
            )

        await update_user(
            user.username,
            is_enable_otp=True,
            is_logged_out=False,
        )

        return user

    async def generate_otp_recovery(
        self,
        user_id: int,
    ) -> list[str]:
        """
        Generate a list of OTP recovery codes for the specified user.

        Args:
            user_id (int): The ID of the user to generate OTP recovery codes for.

        Returns:
            List[str]: A list of OTP recovery codes for the user.

        Raises:
            HTTPException: If the user with the given ID is not found.
        """

        logger.info(f'Generate OTP Recovery with user_id={user_id}')

        user = await get_user_by_id(user_id)

        if not user:

            logger.error(f"User with id '{user_id}' not found")

            raise HTTPException(
                status_code=404,
                detail=f"User with id '{user_id}' not found"
            )

        if not user.otp_recovery:
            list_otp_recovery = []
            for _ in range(8):
                temp = ""
                temp += await random_text(4)
                temp += "-"
                temp += await random_text(4)
                list_otp_recovery.append(temp)

            await update_user(
                user.username,
                otp_recovery=list_otp_recovery,
            )

        return user.otp_recovery

    async def verify_otp_recovery(self, user_id: int, code: str) -> None:
        """
        Verify the OTP recovery code.

        Args:
            user_id (int): The ID of the user to verify the OTP recovery code for.
            code (str): The OTP recovery code to verify.

        Raises:
            HTTPException: If the user with the given ID is not found or if the OTP recovery code is incorrect.
        """

        logger.info(f'Verify OTP Recovery with user_id={user_id} and code={code}')

        user = await get_user_by_id(user_id)

        if not user:

            logger.error(f"User with id '{user_id}' not found")

            raise HTTPException(
                status_code=404,
                detail=f"User with id '{user_id}' not found"
            )

        if code not in user.otp_recovery:

            logger.error(f"Incorrect OTP recovery with code={code}.")

            raise HTTPException(
                status_code=400,
                detail=f"Incorrect OTP recovery with code={code}."
            )

        await update_user(
            user.username,
            otp_secret=None,
            is_enable_otp=False,
            is_logged_out=True,
        )
