from app.core.config import settings
from playhouse.pool import PooledMySQLDatabase

database = PooledMySQLDatabase(settings.DATABASE_NAME, port=settings.DATABASE_PORT,
                               host=settings.DATABASE_HOST, user=settings.DATABASE_USER,
                               password=settings.DATABASE_PASSWORD)
