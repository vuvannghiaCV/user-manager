import string
import random
from loguru import logger


async def random_text(
    length: int = 12,
) -> str:
    """
    Generate a random text of characters, numbers and uppercase letters.

    Args:
        length (int, optional): The length of the text to generate. Defaults to 12.

    Returns:
        str: The generated random text.
    """

    logger.info(f'Random text with length={length}')

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits

    text = random.choices(
        lowercase + uppercase + digits,
        k=length,
    )

    random.shuffle(text)
    text = "".join(text)

    return text
