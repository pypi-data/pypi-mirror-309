import sqlite3
from collections.abc import Callable, Iterator
from contextlib import closing, contextmanager
from typing import TypeVar

R = TypeVar("R")


@contextmanager
def _open_db(db_name: str, pragmas: list[str]) -> Iterator[sqlite3.Cursor]:
    with closing(sqlite3.connect(db_name, uri=True)) as connection:
        if pragmas:
            for pragma in pragmas:
                connection.execute(pragma)
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            try:
                yield cursor
                connection.commit()
            except Exception:
                connection.rollback()
                raise


def query(
    schema: str, db_name: str, pragmas: list[str], executor: Callable[..., R]
) -> R:
    with _open_db(db_name, pragmas) as cursor:
        try:
            return executor(cursor)
        except sqlite3.OperationalError as err:
            match err.args:
                case (msg,) if msg.startswith("no such table:"):
                    cursor.executescript(schema)
                    return executor(cursor)
                case _:
                    raise
