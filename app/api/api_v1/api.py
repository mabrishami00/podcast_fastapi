from fastapi import APIRouter
from .endpoints.podcast import router as podcast_router
from .endpoints.interaction import router as interaction_router

router = APIRouter()
router.include_router(podcast_router)
router.include_router(interaction_router)
