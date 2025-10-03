from sqlalchemy import TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts_2"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    published: Mapped[bool] = mapped_column(server_default="TRUE", nullable=False)
    created_at = mapped_column(TIMESTAMP, nullable=False, server_default=text("now()"))
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users_2.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User")


class User(Base):
    __tablename__ = "users_2"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Vote(Base):
    __tablename__ = "votes_2"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users_2.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts_2.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
