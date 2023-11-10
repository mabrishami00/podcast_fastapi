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


@router.post("/bookmark/{channel_id}/{item_id}")
async def bookmark(channel_id: int, item_id: int, authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    result = await action(
        username, channel_id, item_id, bookmarks_collection, "bookmarkd"
    )
    return result


@router.post("/unbookmark/{channel_id}/{item_id}")
async def unbookmark(channel_id: int, item_id: int, authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    result = await unaction(
        username, channel_id, item_id, bookmarks_collection, "bookmarkd"
    )
    return result


@router.get("/bookmark_list/")
async def bookmark_list(authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    result = await action_list(username, bookmarks_collection)
    return result

@router.post("/comment/{channel_id}/{item_id}")
async def comment(channel_id: int, item_id: int, body: dict=Body(default=None),authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    if username:
        async with httpx.AsyncClient() as client:
            url = f"{settings.DOES_ITEM_EXIST_URL}/{channel_id}/{item_id}/"
            response = await client.get(url=url)
            if response.status_code == 200:
                value = {
                    "username": username,
                    "body": body.get("body"),
                    "channel_id": channel_id,
                    "item_id": item_id,
                }
                await comments_collection.insert_one(value)
                return JSONResponse(
                    {"detail": f"Your comment has been registered successfully."}
                )
            else:
                return JSONResponse({"detail": "Item has not been found."})

    else:
        return JSONResponse({"detail": "You are not authenticated."})
    
@router.post("/uncomment/{comment_id}/")
async def uncomment(comment_id: str, authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    if username:
        await comments_collection.delete_one({"_id": ObjectId(comment_id), "username": username})
        return JSONResponse(
            {"detail": f"Your comment has been deleted successfully."}
            )
    else:
        return JSONResponse({"detail": "You are not authenticated."})
    
@router.get("/comment_list/{channel_id}/{item_id}")
async def comment_list(channel_id: int, item_id: int, authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    if username:
        comments = comments_collection.find({"channel_id": channel_id, "item_id": item_id}, projection={"_id": False})
        documents = [commnet for commnet in await comments.to_list(length=100)]

        return JSONResponse(documents)
    else:
        return JSONResponse({"detail": "You are not authenticated."})
    

@router.post("/subscribe/{channel_id}/")
async def subscribe(channel_id: int, authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    if username:
        async with httpx.AsyncClient() as client:
            url = f"{settings.DOES_CHANNEL_EXIST_URL}/{channel_id}/"
            response = await client.get(url=url)
            if response.status_code == 200:
                value = {
                    "username": username,
                    "channel_id": channel_id,
                }
                actioned = await subscribes_collection.find_one(value)
                if actioned:
                    return JSONResponse(
                        {"detail": f"You have subscribed this item before."}
                    )
                else:
                    await subscribes_collection.insert_one(value)
                    return JSONResponse(
                        {"detail": f"You subscribed this item successfully."}
                    )
            else:
                return JSONResponse({"detail": "Item has not been found."})

    else:
        return JSONResponse({"detail": "You are not authenticated."})


@router.post("/unsubscribe/{channel_id}/")
async def unsubscribe(channel_id: int, authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    if username:
        async with httpx.AsyncClient() as client:
            url = f"{settings.DOES_CHANNEL_EXIST_URL}/{channel_id}/"
            response = await client.get(url=url)
            if response.status_code == 200:
                value = {
                    "username": username,
                    "channel_id": channel_id,
                }
                liked = await subscribes_collection.find_one(value)
                if not liked:
                    return JSONResponse(
                        {"detail": f"You have not subscribed this item before."}
                    )
                else:
                    subscribes_collection.delete_one(value)
                    return JSONResponse(
                        {"detail": f"You unsubscribed this item successfully."}
                    )
            else:
                return JSONResponse({"detail": "Item has not been found."})
    else:
        return JSONResponse({"detail": "You are not authenticated."})


@router.get("/subscribe_list/")
async def subscribe_list(authorization=Header(default=None)):
    username, jti = jwt_authentication.authenticate(authorization, settings.SECRET_KEY)
    if username:
        results = subscribes_collection.find(
            {"username": username}, projection={"_id": False, "username": False}
        )
        documents = [document for document in await results.to_list(length=100)]
        return JSONResponse(documents)