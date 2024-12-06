import os
import sqlite3

from .classes import ERDDAP
from .sql_script import SQL_UNSAFE, SQL_CREATE
from .template_utils import obj2sql_string


def obj2db(erddap: ERDDAP, db_filename: str, parse_source_attributes: bool = False, unsafe: bool = False) -> None:
    """Convert a XML datasets ERDDAP configuration to a DB sqlite.

    Args:
        erddap (ERDDAP): python object to convert.
        db_filename (str): database sqlite filename.
        parse_source_Attributes (bool, optional): Flag to enable the parsing of the sourceAttributes nodes. Defaults to False.
        unsafe (bool, optional): Flag to enable unsafe execution to the database, this will disable journal and synchronous. Defaults to False.
    """

    script = [
        SQL_UNSAFE if unsafe else "",
        SQL_CREATE,
        obj2sql_string(erddap),
    ]

    # Create empty database file
    if os.path.isfile(db_filename):
        os.remove(db_filename)
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    # Execute sql script
    cursor.executescript("".join(script))

    # Save db
    connection.commit()
    connection.close()
