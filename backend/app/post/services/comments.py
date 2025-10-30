from database import get_db_session
from sqlalchemy import select
from loguru import logger
from fastapi import HTTPException


from app.auth.services.universal import get_user_by_id
from app.post.services.posts import select_post_by_id
from app.post.models.comments import Comment
from app.post.schema.comments import CreateCommentRequest
from app.post.schema.comments import UpdateCommentRequest


async def select_all_comments(
    post_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[Comment]:
    """
    Retrieve a list of all comments with pagination.

    Args:
        limit (int): The maximum number of comments to return. Defaults to 50.
        offset (int): The number of comments to skip before starting to collect the result set. Defaults to 0.

    Returns:
        list[Comment]: A list of all comment objects.

    Logs:
        Logs the retrieval of all comments with the specified limit and offset.
    """

    logger.info(f'Select all comments with post_id={post_id}, limit={limit}, offset={offset}')

    post = await select_post_by_id(post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f'Post with post_id={post_id} not found'
        )

    async with get_db_session() as session:
        statement = select(Comment).where(Comment.post_id == post_id).offset(offset).limit(limit)
        result = await session.execute(statement)
        comments = result.scalars().all()
        return comments


async def select_comment_by_id(
    post_id: int,
    comment_id: int,
) -> Comment:
    """
    Retrieve a comment by its ID.

    Args:
        comment_id (int): The ID of the comment to retrieve.

    Returns:
        Comment: The comment object if the comment exists, None otherwise.

    Logs:
        Logs the retrieval attempt of a comment by its ID.
    """

    logger.info(f'Select comment by post_id={post_id}, comment_id={comment_id}')

    post = await select_post_by_id(post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f'Post with post_id={post_id} not found'
        )

    async with get_db_session() as session:
        statement = select(Comment).where(Comment.id == comment_id)
        result = await session.execute(statement)
        comment = result.scalars().first()
        return comment


async def create_new_comment(
    user_id: int,
    post_id: int,
    request: CreateCommentRequest,
) -> Comment:
    """
    Create a new comment.

    Args:
        user_id (int): The ID of the user creating the comment.
        request (CreateCommentRequest): The request containing the text of the comment.

    Returns:
        Comment: The newly created comment object after being saved to the database.

    Raises:
        HTTPException: If the user with the given ID is not found.

    Logs:
        Logs the creation attempt of a new comment with its text and user ID.
    """

    logger.info(f'Create new comment with user_id={user_id}, post_id={post_id}, request={request}')

    user = await get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'User with user_id={user_id} not found'
        )

    post = await select_post_by_id(post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f'Post with post_id={post_id} not found'
        )

    async with get_db_session() as session:
        comment = Comment(text=request.text, user_id=user_id, post_id=post_id)
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment


async def update_comment_by_id(
    user_id: int,
    post_id: int,
    comment_id: int,
    request: UpdateCommentRequest,
) -> Comment:
    """
    Update a comment with the given comment id.

    Args:
        user_id (int): The id of the user updating the comment.
        comment_id (int): The id of the comment to update.
        request (UpdateCommentRequest): The request containing the new text for the comment.

    Returns:
        Comment: The updated comment object after being saved to the database.

    Raises:
        HTTPException: If the comment with the given id is not found, or the user with the given id is not the owner of the comment.

    Logs:
        Logs the update attempt of a comment with its text and user ID.
    """

    logger.info(f'Update comment by post_id={post_id}, comment_id={comment_id}, user_id={user_id}, request={request}')

    user = await get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'User with user_id={user_id} not found'
        )

    comment = await select_comment_by_id(post_id, comment_id)

    if comment.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail=f'Current user with user_id={user_id} is not the owner of the comment with comment_id={comment_id}'
        )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail=f'Comment with comment_id={comment_id} not found'
        )

    comment.text = request.text or comment.text

    async with get_db_session() as session:
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment


async def delete_comment_by_id(
    user_id: int,
    post_id: int,
    comment_id: int,
) -> None:
    """
    Delete a comment with the given comment id.

    Args:
        user_id (int): The id of the user deleting the comment.
        comment_id (int): The id of the comment to delete.

    Raises:
        HTTPException: If the user with the given id is not found, or the user with the given id is not the owner of the comment with the given id.

    Logs:
        Logs the deletion attempt of a comment with its id and user id.
    """

    logger.info(f'Delete comment by post_id={post_id}, comment_id={comment_id}, user_id={user_id}')

    user = await get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'User with user_id={user_id} not found'
        )

    comment = await select_comment_by_id(post_id, comment_id)

    if comment.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail=f'Current user with user_id={user_id} is not the owner of the comment with comment_id={comment_id}'
        )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail=f'Comment with comment_id={comment_id} not found'
        )

    async with get_db_session() as session:
        await session.delete(comment)
        await session.commit()
        return
