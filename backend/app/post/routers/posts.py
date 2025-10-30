from fastapi import APIRouter
from fastapi import Query
from fastapi import Depends
from fastapi import HTTPException
from loguru import logger


from app.auth.utils.auth_handler import AuthHandler
from app.post.schema.posts import PostResponse
from app.post.schema.posts import GetAllPostsResponse
from app.post.schema.posts import GetPostByIdResponse
from app.post.schema.posts import CreatePostRequest
from app.post.schema.posts import CreatePostResponse
from app.post.schema.posts import UpdatePostRequest
from app.post.schema.posts import UpdatePostResponse
from app.post.schema.posts import DeletePostResponse
from app.post.services.posts import select_all_posts
from app.post.services.posts import select_post_by_id
from app.post.services.posts import create_new_post
from app.post.services.posts import update_post_by_id
from app.post.services.posts import delete_post_by_id


posts_router = APIRouter(prefix="/posts", tags=["posts"])


@posts_router.post(
    '',
    response_model=CreatePostResponse,
)
async def create_post(
    request: CreatePostRequest,
    current_user_id: int = Depends(AuthHandler().get_current_user_id_with_check_otp),
) -> CreatePostResponse:
    """
    Create a new post.

    Args:
        request (CreatePostRequest): The request body must contain the title and content of the post.

    Returns:
        CreatePostResponse: The response containing the created post.

    Raises:
        HTTPException: If the post could not be created.

    Logs:
        Logs the creation attempt of a post.
    """

    logger.info(f'Create post with current_user_id={current_user_id}, title={request.title}, content={request.content}')

    post = await create_new_post(current_user_id, request)

    return CreatePostResponse(
        success=True,
        message='Create post successfully',
        post=PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            updated_at=post.updated_at,
            created_at=post.created_at,
        )
    )


@posts_router.get(
    '',
    response_model=GetAllPostsResponse,
)
async def get_all_posts(
    limit: int = Query(50, gt=0, le=100),
    offset: int = Query(0, ge=0),
) -> GetAllPostsResponse:
    """
    Retrieve a list of all posts with pagination.

    Args:
        limit (int): The maximum number of posts to return. Defaults to 50. Must be greater than 0 and less than or equal to 100.
        offset (int): The number of posts to skip before starting to collect the result set. Defaults to 0. Must be greater than or equal to 0.

    Returns:
        GetAllPostsResponse: The response containing a list of posts, along with a success flag and message.

    Logs:
        Logs the retrieval of all posts with the specified limit and offset.
    """

    logger.info(f'Get all posts with limit={limit}, offset={offset}')

    posts = await select_all_posts(limit, offset)

    return GetAllPostsResponse(
        success=True,
        message='Get all posts successfully',
        posts=[
            PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                updated_at=post.updated_at,
                created_at=post.created_at,
            )
            for post in posts
        ]
    )


@posts_router.get(
    '/{post_id}',
    response_model=GetPostByIdResponse,
)
async def get_post_by_id(
    post_id: int,
) -> GetPostByIdResponse:
    """
    Retrieve a post by its ID.

    Args:
        post_id (int): The ID of the post to retrieve.

    Returns:
        GetPostByIdResponse: The response containing the post if found, or an error message if not found.

    Logs:
        Logs the retrieval attempt of a post by its ID.
    """

    logger.info(f'Get post by post_id={post_id}')

    post = await select_post_by_id(post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f'Post with post_id={post_id} not found'
        )

    return GetPostByIdResponse(
        success=True,
        message='Get post by id successfully',
        post=PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            updated_at=post.updated_at,
            created_at=post.created_at,
        )
    )


@posts_router.put(
    '/{post_id}',
    response_model=UpdatePostResponse,
)
async def update_post(
    post_id: int,
    request: UpdatePostRequest,
    current_user_id: int = Depends(AuthHandler().get_current_user_id_with_check_otp),
) -> UpdatePostResponse:
    """
    Update a post with the given post id.

    Args:
        post_id (int): The id of the post to update.
        request (UpdatePostRequest): The request body must contain the title and content of the post.

    Returns:
        UpdatePostResponse: The response containing the updated post.

    Raises:
        HTTPException: If the post could not be updated.

    Logs:
        Logs the update attempt of a post.
    """

    logger.info(f'Update post with current_user_id={current_user_id}, post_id={post_id}, title={request.title}, content={request.content}')

    post = await update_post_by_id(current_user_id, post_id, request)

    return UpdatePostResponse(
        success=True,
        message='Update post successfully',
        post=PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            updated_at=post.updated_at,
            created_at=post.created_at,
        )
    )


@posts_router.delete(
    '/{post_id}',
    response_model=DeletePostResponse,
)
async def delete_post(
    post_id: int,
    current_user_id: int = Depends(AuthHandler().get_current_user_id_with_check_otp),
) -> DeletePostResponse:
    """
    Delete a post with the given post id.

    Args:
        post_id (int): The id of the post to delete.

    Returns:
        DeletePostResponse: The response containing the result of the deletion.

    Raises:
        HTTPException: If the post could not be deleted.

    Logs:
        Logs the deletion attempt of a post.
    """

    logger.info(f'Delete post with current_user_id={current_user_id}, post_id={post_id}')

    await delete_post_by_id(current_user_id, post_id)

    return DeletePostResponse(
        success=True,
        message='Delete post successfully',
    )
