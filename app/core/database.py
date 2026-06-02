import psycopg2
from contextlib import contextmanager
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

from app.core.config import settings

import logging
logger = logging.getLogger(__name__)

# A single process-wide connection pool. FastAPI's sync endpoints run in a
# threadpool, so a ThreadedConnectionPool lets concurrent requests reuse
# connections instead of paying the TCP/TLS/auth handshake on every query.
_pool = None


def _get_pool():
    global _pool
    if _pool is None:
        _pool = ThreadedConnectionPool(
            minconn = 1,
            maxconn = 20,
            host = settings.DB_HOST,
            port = settings.DB_PORT,
            dbname = settings.DB_NAME,
            user = settings.DB_USER,
            password = settings.DB_PASSWORD,
        )
    return _pool


@contextmanager
def get_db_cursor():
    pool = _get_pool()
    conn = None
    try:
        conn = pool.getconn()

        with conn.cursor(cursor_factory = RealDictCursor) as cursor:
            yield cursor
            conn.commit()

    except psycopg2.OperationalError as e:
        logger.error(f'Could not connect to database: {e}')
        if conn:
            pool.putconn(conn, close = True)
            conn = None
        raise
    except Exception as e:
        logger.error(f'Database error: {e}')
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            pool.putconn(conn)


def test_connection():
    try:
        with get_db_cursor() as cursor:
            cursor.execute('SELECT 1')
            return True
    except Exception as e:
        logger.error(f'Connection test failed: {e}')
        return False

if __name__ == '__main__':
    print(test_connection())
