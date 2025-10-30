from database import get_db_session
from sqlalchemy import select
from loguru import logger
from fastapi import HTTPException


from app.auth.services.universal import get_user_by_id
from app.post.models.posts import Post
from app.post.schema.posts import CreatePostRequest
from app.post.schema.posts import UpdatePostRequest


async def select_all_posts(
    limit: int = 50,
    offset: int = 0,
) -> list[Post]:
    """
    Retrieve a list of all posts with pagination.

    Args:
        limit (int): The maximum number of posts to return. Defaults to 50.
        offset (int): The number of posts to skip before starting to collect the result set. Defaults to 0.

    Returns:
        list[Post]: A list of all post objects.

    Logs:
        Logs the retrieval of all posts with the specified limit and offset.
    """

    logger.info(f'Select all posts with limit={limit}, offset={offset}')

    async with get_db_session() as session:
        statement = select(Post).offset(offset).limit(limit)
        result = await session.execute(statement)
        posts = result.scalars().all()
        return posts


async def select_post_by_id(
    post_id: int,
) -> Post:
    """
    Retrieve a post by its ID.

    Args:
        post_id (int): The ID of the post to retrieve.

    Returns:
        Post: The post object if the post exists, None otherwise.

    Logs:
        Logs the retrieval attempt of a post by its ID.
    """

    logger.info(f'Select post by post_id={post_id}')

    async with get_db_session() as session:
        statement = select(Post).where(Post.id == post_id)
        result = await session.execute(statement)
        post = result.scalars().first()
        return post


async def create_new_post(
    user_id: int,
    request: CreatePostRequest,
) -> Post:
    """
    Create a new post in the database.

    Args:
        request (CreatePostRequest): The request object containing the title and content of the post to be created.

    Returns:
        Post: The newly created post object after being saved to the database.

    Logs:
        Logs the creation attempt of a new post with its title and content.
    """

    logger.info(f'Create new post with user_id={user_id}, title={request.title}, content={request.content}')

    user = await get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'User with user_id={user_id} not found'
        )

    async with get_db_session() as session:
        post = Post(title=request.title, content=request.content, user_id=user_id)
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post


async def update_post_by_id(
    user_id: int,
    post_id: int,
    request: UpdatePostRequest,
) -> Post:
    """
    Update a post with the given post id.

    Args:
        post_id (int): The id of the post to update.
        request (UpdatePostRequest): The request containing the title and content to update.

    Returns:
        Post: The updated post object after being saved to the database.

    Raises:
        HTTPException: If the post with the given id is not found.

    Logs:
        Logs the update attempt of a post with its title and content.
    """

    logger.info(f'Update post by post_id={post_id}, user_id={user_id}, title={request.title}, content={request.content}')

    user = await get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'User with user_id={user_id} not found'
        )

    post = await select_post_by_id(post_id)

    if post.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail=f'Current user with user_id={user_id} is not the owner of the post with post_id={post_id}'
        )

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f'Post with post_id={post_id} not found'
        )

    post.title = request.title or post.title
    post.content = request.content or post.content

    async with get_db_session() as session:
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post


async def delete_post_by_id(
    user_id: int,
    post_id: int,
) -> None:
    """
    Delete a post with the given post id.

    Args:
        post_id (int): The id of the post to delete.

    Raises:
        HTTPException: If the post with the given id is not found.

    Logs:
        Logs the deletion attempt of a post by its id.
    """

    logger.info(f'Delete post by post_id={post_id}, user_id={user_id}')

    user = await get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'User with user_id={user_id} not found'
        )

    post = await select_post_by_id(post_id)

    if post.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail=f'Current user with user_id={user_id} is not the owner of the post with post_id={post_id}'
        )

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f'Post with post_id={post_id} not found'
        )

    async with get_db_session() as session:
        await session.delete(post)
        await session.commit()
        return
