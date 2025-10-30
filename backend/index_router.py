from fastapi import APIRouter


from app.auth.routers.auth import auth_router
from app.auth.routers.users import users_router
from app.post.routers.posts import posts_router
from app.post.routers.comments import comments_router


index_router = APIRouter()


index_router.include_router(auth_router)
index_router.include_router(users_router)
index_router.include_router(posts_router)
index_router.include_router(comments_router)
