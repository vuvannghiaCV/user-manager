# from sqlalchemy import Column, Integer, String, Table, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# # Bảng trung gian cho quan hệ Many-to-Many giữa Question và Category
# question_category_table = Table('question_category', Base.metadata,
#     Column('question_id', Integer, ForeignKey('questions.id')),
#     Column('category_id', Integer, ForeignKey('categories.id'))
# )

# class Question(Base):
#     __tablename__ = 'questions'

#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     text = Column(String)

#     categories = relationship("Category", secondary=question_category_table, back_populates="questions")

# class Category(Base):
#     __tablename__ = 'categories'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)

#     questions = relationship("Question", secondary=question_category_table, back_populates="categories")
