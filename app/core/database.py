import psycopg2
from contextlib import contextmanager
from psycopg2.extras import RealDictCursor

from app.core.config import settings

import logging
logger = logging.getLogger(__name__)

@contextmanager
def get_db_cursor():
    conn = None
    try:
        conn = psycopg2.connect(
            host = settings.DB_HOST,
            port = settings.DB_PORT,
            dbname = settings.DB_NAME,
            user = settings.DB_USER,
            password = settings.DB_PASSWORD
        )
        
        with conn.cursor(cursor_factory = RealDictCursor) as cursor:
            yield cursor
            conn.commit()
            
    except psycopg2.OperationalError as e:
        logger.error(f'Could not connect to database: {e}')
        raise
    except Exception as e:
        logger.error(f'Database error: {e}')
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

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
