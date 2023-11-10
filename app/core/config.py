from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL :str 
    REDIS_URL: str 
    SECRET_KEY: str 

    DOES_ITEM_EXIST_URL: str = "http://django:8000/interactions/does_item_exist"
    DOES_CHANNEL_EXIST_URL: str = "http://django:8000/interactions/does_channel_exist"
    GET_ALL_CHANNELS_URL: str = "http://django:8000/get_all_channels/"
    GET_PODCASTS_URL: str = "http://django:8000/get_channel_podcasts"
    SEARCH_PODCASTS_URL: str = "http://django:8000/get_podcasts"

    class Config:
        env_file = "/home/mahdi/Documents/rss_project/podcast_fastapi/.env"

settings = Settings()