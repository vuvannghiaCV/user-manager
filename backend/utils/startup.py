from loguru import logger


from app.auth.services.universal import create_admin_default


async def startup():
    """
    Called on application startup.  Currently just creates the admin
    user if it doesn't already exist.
    """

    logger.info("Starting application...")

    await create_admin_default()
