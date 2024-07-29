from fastapi import APIRouter

from apps.chat.http.routers.chat import chat_router

from apps.chat.http.routers.health import health_router


router = APIRouter()
prefix = "/api/v1"

router.include_router(health_router, prefix=prefix, tags=["Health"])
router.include_router(chat_router, prefix=prefix, tags=["Chat-Inference"])

__all__ = ["router"]
