from fastapi import APIRouter
from fastapi import Query
from fastapi import Depends
from fastapi import HTTPException
from loguru import logger


from app.auth.utils.auth_handler import AuthHandler
from app.post.schema.comments import CommentResponse
from app.post.schema.comments import GetAllCommentsResponse
from app.post.schema.comments import GetCommentByIdResponse
from app.post.schema.comments import CreateCommentRequest
from app.post.schema.comments import CreateCommentResponse
from app.post.schema.comments import UpdateCommentRequest
from app.post.schema.comments import UpdateCommentResponse
from app.post.schema.comments import DeleteCommentResponse
from app.post.services.comments import select_all_comments
from app.post.services.comments import select_comment_by_id
from app.post.services.comments import create_new_comment
from app.post.services.comments import update_comment_by_id
from app.post.services.comments import delete_comment_by_id


comments_router = APIRouter(prefix="/{post_id}/comments", tags=["comments"])


@comments_router.post(
    '',
    response_model=CreateCommentResponse,
)
async def create_comment(
    post_id: int,
    request: CreateCommentRequest,
    current_user_id: int = Depends(AuthHandler().get_current_user_id_with_check_otp),
) -> CreateCommentResponse:
    """
    Create a new comment.

    Args:
        request (CreateCommentRequest): The request body must contain the text of the comment.
        current_user_id (int): The id of the current user.

    Returns:
        CreateCommentResponse: The response containing the created comment.

    Raises:
        HTTPException: If the comment could not be created.

    Logs:
        Logs the creation attempt of a comment.
    """

    logger.info(f'Create comment with current_user_id={current_user_id}, post_id={post_id}, request={request}')

    comment = await create_new_comment(current_user_id, post_id, request)

    return CreateCommentResponse(
        success=True,
        message='Create comment successfully',
        comment=CommentResponse(
            id=comment.id,
            text=comment.text,
        )
    )


@comments_router.get(
    '',
    response_model=GetAllCommentsResponse,
)
async def get_all_comments(
    post_id: int,
    limit: int = Query(50, gt=0, le=100),
    offset: int = Query(0, ge=0),
) -> GetAllCommentsResponse:
    """
    Retrieve a list of all comments with pagination.

    Args:
        limit (int): The maximum number of comments to return. Defaults to 50. Must be greater than 0 and less than or equal to 100.
        offset (int): The number of comments to skip before starting to collect the result set. Defaults to 0. Must be greater than or equal to 0.

    Returns:
        GetAllCommentsResponse: The response containing a list of comments, along with a success flag and message.

    Logs:
        Logs the retrieval of all comments with the specified limit and offset.
    """

    logger.info(f'Get all comments with post_id={post_id}, limit={limit}, offset={offset}')

    comments = await select_all_comments(post_id, limit, offset)

    return GetAllCommentsResponse(
        success=True,
        message=f'Get all comments of post_id={post_id} successfully',
        comments=[
            CommentResponse(
                id=comment.id,
                text=comment.text,
            )
            for comment in comments
        ]
    )


@comments_router.get(
    '/{comment_id}',
    response_model=GetCommentByIdResponse,
)
async def get_comment_by_id(
    post_id: int,
    comment_id: int,
) -> GetCommentByIdResponse:
    """
    Retrieve a comment by its ID.

    Args:
        comment_id (int): The ID of the comment to retrieve.

    Returns:
        GetCommentByIdResponse: The response containing the comment if found, or an error message if not found.

    Logs:
        Logs the retrieval attempt of a comment by its ID.
    """

    logger.info(f'Get comment by post_id={post_id}, comment_id={comment_id}')

    comment = await select_comment_by_id(post_id, comment_id)

    if not comment:
        raise HTTPException(
            status_code=404,
            detail=f'Comment with comment_id={comment_id} not found'
        )

    return GetCommentByIdResponse(
        success=True,
        message='Get comment by id successfully',
        comment=CommentResponse(
            id=comment.id,
            text=comment.text,
        )
    )


@comments_router.put(
    '/{comment_id}',
    response_model=UpdateCommentResponse,
)
async def update_comment(
    post_id: int,
    comment_id: int,
    request: UpdateCommentRequest,
    current_user_id: int = Depends(AuthHandler().get_current_user_id_with_check_otp),
) -> UpdateCommentResponse:
    """
    Update a comment with the given comment id.

    Args:
        comment_id (int): The id of the comment to update.
        request (UpdateCommentRequest): The request containing the new text for the comment.
        current_user_id (int): The id of the current user.

    Returns:
        UpdateCommentResponse: The response containing the updated comment.

    Raises:
        HTTPException: If the comment could not be updated.

    Logs:
        Logs the update attempt of a comment.
    """

    logger.info(f'Update comment with current_user_id={current_user_id}, post_id={post_id}, comment_id={comment_id}, request={request}')

    comment = await update_comment_by_id(current_user_id, post_id, comment_id, request)

    return UpdateCommentResponse(
        success=True,
        message='Update comment successfully',
        comment=CommentResponse(
            id=comment.id,
            text=comment.text,
        )
    )


@comments_router.delete(
    '/{comment_id}',
    response_model=DeleteCommentResponse,
)
async def delete_comment(
    post_id: int,
    comment_id: int,
    current_user_id: int = Depends(AuthHandler().get_current_user_id_with_check_otp),
) -> DeleteCommentResponse:
    """
    Delete a comment with the given comment id.

    Args:
        comment_id (int): The id of the comment to delete.

    Returns:
        DeleteCommentResponse: The response containing the result of the deletion.

    Raises:
        HTTPException: If the comment with the given id is not found.

    Logs:
        Logs the deletion attempt of a comment by its id.
    """

    logger.info(f'Delete comment with current_user_id={current_user_id}, post_id={post_id}, comment_id={comment_id}')

    await delete_comment_by_id(current_user_id, post_id, comment_id)

    return DeleteCommentResponse(
        success=True,
        message='Delete comment successfully',
    )
