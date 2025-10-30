from database import Base
from app.common.models.timestamp import TimestampMixin


from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Comment(TimestampMixin, Base):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    user = relationship('User', back_populates='comments')

    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    post = relationship('Post', back_populates='comments')
