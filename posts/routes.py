import json
import logging

from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import PostRequestSchema, PostResponseSchema
from models import PostModel
from database import get_db
from producer import get_kafka_producer


router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[PostResponseSchema], status_code=status.HTTP_200_OK)
async def get_posts(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(PostModel))
    posts = res.scalars().all()
    return posts


@router.post("/", response_model=PostResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_post(
        post: PostRequestSchema,
        db: AsyncSession = Depends(get_db),
        producer: AIOKafkaProducer = Depends(get_kafka_producer)
):
    new_post = PostModel(
        content=post.content,
        author=post.author
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    await producer.send_and_wait(
        topic="post_created",
        value=json.dumps({
            "id": new_post.id,
            "content": new_post.content,
            "author": new_post.author
        }).encode("utf-8")
    )
    logger.info(f"Message sent to Kafka topic 'post_created'")

    return new_post
