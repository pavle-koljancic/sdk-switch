import logging
from collections.abc import Generator
from contextlib import contextmanager
from functools import lru_cache
from typing import Any

import psycopg
from psycopg import OperationalError

from models.config.database_config import DatabaseConfig


@lru_cache
def _get_database_config() -> DatabaseConfig:
    """
    Retrieves the database configuration.

    Returns:
        DatabaseConfig: The database configuration.
    """
    return DatabaseConfig()


@contextmanager
def create_db_connection(
    database_config: DatabaseConfig | None = None,
) -> Generator[tuple[psycopg.Connection[Any], psycopg.Cursor[Any]], None, None]:
    """
    Context manager for creating and managing a database connection and cursor.

    Args:
        database_config (Optional[DatabaseConfig]): Optional configuration for
            the database. If not provided, the default configuration will be used.

    Yields:
        Tuple[psycopg.Connection[Any], psycopg.Cursor[Any]]: A tuple containing the
            database connection and cursor. These resources should be used within the
            context block.

    Raises:
        Exception: Any exception that occurs during the database connection
            establishment.

    Example:
        ```
        with create_db_connection() as (connection, cursor):
            # Perform database operations using the connection and cursor
        ```
    """
    connection = None
    cursor = None
    try:
        database_config = database_config or _get_database_config()
        logging.debug(
            "Connection to a database: %s",
            database_config.model_dump(exclude={"db_password"}),
        )

        connection = psycopg.connect(database_config.to_uri())
        cursor = connection.cursor()

        yield connection, cursor

    except OperationalError as oe:
        error_message = (
            f"Database connection failed: Possible causes include network issues, incorrect settings, "
            f"or an unreachable database server. Verify your settings and server status. Error: {oe}."
        )
        logging.error(error_message)
        raise RuntimeError(error_message) from oe
    except Exception as e:
        logging.error("Problem with database connection: %s ", e)
        raise
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()
