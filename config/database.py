import os
from dotenv import load_dotenv
load_dotenv()
"""
config/database.py — Async MongoDB connection via Motor
"""
from motor.motor_asyncio import AsyncIOMotorClient
_client = None
_db = None
async def connect_db():
    global _client, _db
    _client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
    _db = _client[os.getenv("MONGODB_DB_NAME")]
    await _client.admin.command("ping")
async def disconnect_db():
    global _client
    if _client:
        _client.close()
def get_db():
    if _db is None:
        raise RuntimeError("DB not initialized — call connect_db() first.")
    return _db
