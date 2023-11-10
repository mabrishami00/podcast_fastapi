import httpx
from core.config import settings
from fastapi.responses import JSONResponse


async def action(username: str, channel_id: int, item_id: int, collection, word):
    if username:
        async with httpx.AsyncClient() as client:
            url = f"{settings.DOES_ITEM_EXIST_URL}/{channel_id}/{item_id}/"
            response = await client.get(url=url)
            if response.status_code == 200:
                value = {
                    "username": username,
                    "channel_id": channel_id,
                    "item_id": item_id,
                }
                actioned = await collection.find_one(value)
                if actioned:
                    return JSONResponse(
                        {"detail": f"You have {word} this item before."}
                    )
                else:
                    await collection.insert_one(value)
                    return JSONResponse(
                        {"detail": f"You {word} this item successfully."}
                    )
            else:
                return JSONResponse({"detail": "Item has not been found."})

    else:
        return JSONResponse({"detail": "You are not authenticated."})


async def unaction(username: str, channel_id: int, item_id: int, collection, word):
    if username:
        async with httpx.AsyncClient() as client:
            url = f"{settings.DOES_ITEM_EXIST_URL}/{channel_id}/{item_id}/"
            response = await client.get(url=url)
            if response.status_code == 200:
                value = {
                    "username": username,
                    "channel_id": channel_id,
                    "item_id": item_id,
                }
                liked = await collection.find_one(value)
                if not liked:
                    return JSONResponse(
                        {"detail": f"You have not {word} this item before."}
                    )
                else:
                    collection.delete_one(value)
                    return JSONResponse(
                        {"detail": f"You un{word} this item successfully."}
                    )
            else:
                return JSONResponse({"detail": "Item has not been found."})
    else:
        return JSONResponse({"detail": "You are not authenticated."})


async def action_list(username: str, collection):
    if username:
        results = collection.find(
            {"username": username}, projection={"_id": False, "username": False}
        )
        documents = [document for document in await results.to_list(length=100)]
        return JSONResponse(documents)
