from app.core.config import settings
import redis


pool = redis.ConnectionPool().from_url('redis://:{}@{}:{}/{}'.format(settings.REDIS_PASSWORD, settings.REDIS_HOST,
                                                                     settings.REDIS_PORT, settings.REDIS_DB))
redis_client = redis.Redis(connection_pool=pool)
