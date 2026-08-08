from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    done: Mapped[bool] = mapped_column(default=False)