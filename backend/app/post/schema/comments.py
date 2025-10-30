from app.common.schema.response_template import ResponseTemplate


from pydantic import BaseModel
from pydantic import Field
from typing import List


class CommentResponse(BaseModel):

    id: int = Field(
        ...,
        description="Comment id",
    )
    text: str = Field(
        ...,
        description="Comment text",
    )


class GetAllCommentsResponse(ResponseTemplate):

    comments: List[CommentResponse] = Field(
        ...,
        description="Comments",
    )


class GetCommentByIdResponse(ResponseTemplate):

    comment: CommentResponse = Field(
        ...,
        description="Comment",
    )


class CreateCommentRequest(BaseModel):

    text: str = Field(
        ...,
        description="Comment text",
    )


class CreateCommentResponse(ResponseTemplate):

    comment: CommentResponse = Field(
        ...,
        description="Comment",
    )


class UpdateCommentRequest(BaseModel):

    text: str = Field(
        ...,
        description="Comment text",
    )


class UpdateCommentResponse(ResponseTemplate):

    comment: CommentResponse = Field(
        ...,
        description="Comment",
    )


class DeleteCommentResponse(ResponseTemplate):

    pass
