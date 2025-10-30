from loguru import logger


async def shutdown():
    """
    Called on application shutdown.
    """

    logger.info("Shutting down application...")
