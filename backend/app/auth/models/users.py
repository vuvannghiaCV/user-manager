from database import Base
from app.common.models.timestamp import TimestampMixin


from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from app.post.models.posts import Post
from app.post.models.comments import Comment


class User(TimestampMixin, Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    is_enable_otp = Column(Boolean, default=False)
    otp_secret = Column(String(255), nullable=True)
    otp_recovery = Column(JSON, nullable=True)
    is_logged_out = Column(Boolean, default=True, nullable=True)

    reset_password = relationship(
        "ResetPassword",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    posts = relationship(
        'Post',
        back_populates='user',
        cascade="all, save-update",
        passive_deletes=True,
    )
    comments = relationship(
        'Comment',
        back_populates='user',
        cascade="all, save-update",
        passive_deletes=True,
    )


class ResetPassword(TimestampMixin, Base):

    __tablename__ = "reset_password"

    id = Column(Integer, primary_key=True, index=True)
    secret = Column(String(255), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="reset_password")
