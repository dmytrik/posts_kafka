from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import PostRequestSchema, PostResponseSchema
from models import PostModel
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[PostResponseSchema], status_code=status.HTTP_200_OK)
async def get_posts(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(PostModel))
    posts = res.scalars().all()
    return posts


@router.post("/", response_model=PostResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostRequestSchema, db: AsyncSession = Depends(get_db)):
    post = PostModel(
        content=post.content,
        author=post.author
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post