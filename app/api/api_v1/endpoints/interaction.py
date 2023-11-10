from fastapi import APIRouter, Header, Body
from fastapi.responses import JSONResponse

from db.mongo import (
    likes_collection,
    bookmarks_collection,
    comments_collection,
    subscribes_collection,
)
from core.config import settings
from bson import ObjectId

from my_simple_jwt_auth.my_simple_jwt_auth import jwt_authentication
from .utils import action, unaction, action_list
import httpx
import json

router = APIRouter(prefix="/interaction")


@router.post("/like/{channel_id}/{item_id}")
async def like(channel_id: int, item_id: int, authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    result = await action(username, channel_id, item_id, likes_collection, "liked")
    return result


@router.post("/unlike/{channel_id}/{item_id}")
async def unlike(channel_id: int, item_id: int, authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    result = await unaction(username, channel_id, item_id, likes_collection, "liked")
    return result


@router.get("/like_list/")
async def like_list(authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    result = await action_list(username, likes_collection)
    return result
