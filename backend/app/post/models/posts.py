from database import Base
from app.common.models.timestamp import TimestampMixin


from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Post(TimestampMixin, Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    content = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    user = relationship('User', back_populates='posts')

    comments = relationship(
        'Comment',
        back_populates='post',
        cascade="all, delete-orphan",
        passive_deletes=True
    )


# class Category(Base):
    # __tablename__ = "categories"

    # id
    # name
    # description
