import motor.motor_asyncio
from core.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client.rss
likes_collection = db.likes
bookmarks_collection = db.bookmarks
subscribes_collection = db.subscribes
comments_collection = db.comments
