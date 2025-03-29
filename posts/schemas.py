from pydantic import BaseModel


class PostRequestSchema(BaseModel):
    content: str
    author: str


class PostResponseSchema(PostRequestSchema):
    id: int

    class Config:
        from_attributes=True
