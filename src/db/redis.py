import aioredis
from src.config import Config

JTI_EXPIRY =3600  # 1 hour in seconds

token_blacklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

async def add_token_to_blacklist(jti: str) -> None:
    await token_blacklist.set(name=jti, value="", ex=JTI_EXPIRY)

async def is_token_blacklisted(jti: str) -> bool:
    jti = await token_blacklist.get(jti)
    return jti is not None