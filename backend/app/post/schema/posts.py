from app.common.schema.response_template import ResponseTemplate


from datetime import datetime
from pydantic import BaseModel
from pydantic import Field
from typing import List
from typing import Optional


class PostResponse(BaseModel):

    id: int = Field(
        ...,
        description="Post id",
    )
    title: str = Field(
        ...,
        description="Post title",
    )
    content: str = Field(
        ...,
        description="Post content",
    )
    updated_at: datetime = Field(
        ...,
        description="Post updated at",
    )
    created_at: datetime = Field(
        ...,
        description="Post created at",
    )


class GetAllPostsResponse(ResponseTemplate):

    posts: List[PostResponse] = Field(
        ...,
        description="Posts",
    )


class GetPostByIdResponse(ResponseTemplate):

    post: PostResponse = Field(
        ...,
        description="Post",
    )


class CreatePostRequest(BaseModel):

    title: str = Field(
        ...,
        description="Post title",
    )
    content: str = Field(
        ...,
        description="Post content",
    )


class CreatePostResponse(ResponseTemplate):

    post: PostResponse = Field(
        ...,
        description="Post",
    )


class UpdatePostRequest(BaseModel):

    title: Optional[str] = Field(
        None,
        description="Post title",
    )
    content: Optional[str] = Field(
        None,
        description="Post content",
    )


class UpdatePostResponse(ResponseTemplate):

    post: PostResponse = Field(
        ...,
        description="Post",
    )


class DeletePostResponse(ResponseTemplate):

    pass
