from pydantic import BaseModel
from pydantic import Field


class ResponseTemplate(BaseModel):

    success: bool = Field(
        ...,
        description="Success",
    )
    message: str = Field(
        ...,
        description="Message",
    )
