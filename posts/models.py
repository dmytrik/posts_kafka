from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import BaseModel


class PostModel(BaseModel):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f"{self.content} - {self.author}"
