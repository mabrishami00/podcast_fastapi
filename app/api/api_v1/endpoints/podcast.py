from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from core.config import settings

import httpx
import json

router = APIRouter(prefix="/podcast")


@router.get("/get_all_channels")
async def get_all_channels():
    async with httpx.AsyncClient() as client:
        response = await client.get(url=settings.GET_ALL_CHANNELS_URL)
        response_dict = json.loads(response.text)
        if response.status_code == 200:
            return JSONResponse(response_dict)
        else:
            return JSONResponse(response_dict, status_code=status.HTTP_404_NOT_FOUND)


@router.get("/get_podcasts")
async def get_podcasts_of_channel(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.GET_PODCASTS_URL}/?url={url}")
        response_dict = json.loads(response.text)
        if response.status_code == 200:
            return JSONResponse(response_dict)
        else:
            return JSONResponse(response_dict, status_code=status.HTTP_404_NOT_FOUND)

@router.get("/search_podcasts")
async def get_podcasts_of_channel(searched: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.SEARCH_PODCASTS_URL}/?searched={searched}")
        response_dict = json.loads(response.text)
        if response.status_code == 200:
            return JSONResponse(response_dict)
        else:
            return JSONResponse(response_dict, status_code=status.HTTP_404_NOT_FOUND)