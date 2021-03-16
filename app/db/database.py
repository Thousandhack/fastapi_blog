# from app.core.config import settings
# from playhouse.pool import PooledMySQLDatabase

# database = PooledMySQLDatabase(settings.DATABASE_NAME, port=settings.DATABASE_PORT,
#                                host=settings.DATABASE_HOST, user=settings.DATABASE_USER,
#                                password=settings.DATABASE_PASSWORD)

from app.core.config import settings
from playhouse.pool import PooledMySQLDatabase

from peewee import _ConnectionState

from contextvars import ContextVar

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(_ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


database = PooledMySQLDatabase(settings.DATABASE_NAME,
                               port=settings.DATABASE_PORT,
                               host=settings.DATABASE_HOST,
                               user=settings.DATABASE_USER,
                               password=settings.DATABASE_PASSWORD,
                               # timeout=10,  # 当池满时阻塞的秒数。默认情况下，当池满时，peewee不会阻塞，而只是抛出一个异常。若要无限期阻塞，请将此值设置为0。
                               # stale_timeout=300,  # 允许使用连接的秒数。
                               max_connections=settings.DATABASE_POOL_SIZE)

database._state = PeeweeConnectionState()

