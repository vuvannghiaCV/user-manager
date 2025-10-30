from passlib.context import CryptContext


class PasswordManager:

    pwd_context = CryptContext(schemes=["bcrypt"])

    def get_password_hash(self, password):
        """
        Hashes a plain-text password.

        Args:
            password (str): The plain-text password to be hashed.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        """
        Verifies a plain-text password against a hashed password.

        Args:
            plain_password (str): The plain-text password to verify.
            hashed_password (str): The hashed password to verify against.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)
