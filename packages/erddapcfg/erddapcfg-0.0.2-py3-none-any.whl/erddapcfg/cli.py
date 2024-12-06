import argparse
import logging

from .db_to_xml import db2xml
from .xml_to_db import xml2db
from .xml_to_sql import xml2sql


def cli_entry_point():
    """Entry point of the cli application"""

    # Initialize parser for the command line
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="What the cli should do", required=True)

    # Initialize parser for the command to convert db to xml
    parser_db2xml = subparsers.add_parser("db2xml", help="From the db to the xml")
    parser_db2xml.add_argument("db", help="db filename")
    parser_db2xml.add_argument("xml", help="xml filename")
    parser_db2xml.add_argument("-d", "--debug", help="enable debug", action="store_true", required=False)
    parser_db2xml.add_argument(
        "-p",
        "--parse-source-attributes",
        help="enable parsing of source attributes",
        action="store_true",
        required=False,
    )

    # Initialize parser for the command to convert xml to db
    parser_xml2db = subparsers.add_parser("xml2db", help="From the xml to the db.")
    parser_xml2db.add_argument("xml", help="xml filename")
    parser_xml2db.add_argument("db", help="db filename")
    parser_xml2db.add_argument("-d", "--debug", help="enable debug", action="store_true", required=False)
    parser_xml2db.add_argument(
        "-p",
        "--parse-source-attributes",
        help="enable parsing of source attributes",
        action="store_true",
        required=False,
    )
    parser_xml2db.add_argument(
        "-u",
        "--unsafe",
        help="enable the unsafe database insertions, use it carefully to gain speed",
        action="store_true",
        required=False,
    )

    # Initialize parser for the command to convert xml to sql
    parser_xml2sql = subparsers.add_parser("xml2sql", help="From the xml to the sql.")
    parser_xml2sql.add_argument("xml", help="xml filename")
    parser_xml2sql.add_argument("sql", help="sql filename")
    parser_xml2sql.add_argument("-d", "--debug", help="enable debug", action="store_true", required=False)
    parser_xml2sql.add_argument(
        "-p",
        "--parse-source-attributes",
        help="enable parsing of source attributes",
        action="store_true",
        required=False,
    )

    # Initialize parser for the command to test the application
    parser_test = subparsers.add_parser("test", help="Test if the console program is installed.")
    parser_test.add_argument("-d", "--debug", help="enable debug", action="store_true", required=False)

    # Parse arguments
    args = parser.parse_args()

    if args.debug:
        # Start the logging via terminal
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    # Execute the command given in the arguments
    if args.command == "db2xml":
        cli_db2xml(db=args.db, xml=args.xml, p=args.parse_source_attributes, debug=args.debug)

    elif args.command == "xml2db":
        cli_xml2db(db=args.db, xml=args.xml, p=args.parse_source_attributes, unsafe=args.unsafe, debug=args.debug)

    elif args.command == "xml2sql":
        cli_xml2sql(sql=args.sql, xml=args.xml, p=args.parse_source_attributes, debug=args.debug)

    elif args.command == "test":
        print("sqlerddap installed correctly.")


def check_xml_extension(xml: str) -> bool:
    """Check if the given xml filename has the right extension and print some debug info.

    Args:
        xml (str): xml filename to check.

    Returns:
        bool: the given xml filename is valid
    """

    valid = xml.endswith(".xml")
    if not valid:
        logging.debug("ATTENTION: the given xml file doesn't match the xml extension.")
    return valid


def check_db_extension(db: str) -> bool:
    """Check if the given db filename has the right extension and print some debug info.

    Args:
        db (str): db filename to check.

    Returns:
        bool: the given db filename is valid
    """

    valid = db.endswith(".db") or db.endswith(".sqlite") or db.endswith(".db3")
    if not (valid):
        logging.debug("ATTENTION: the given db file doesn't match the db extension: [.sqlite, .db, .db3]")
    return valid


def check_sql_extension(sql: str) -> bool:
    """Check if the given sql filename has the right extension and print some debug info.

    Args:
        sql (str): sql filename to check.

    Returns:
        bool: the given sql filename is valid
    """

    valid = sql.endswith(".sql")
    if not (valid):
        logging.debug("ATTENTION: the given sql filename doesn't match the sql extension: .sql")
    return valid


def cli_db2xml(db: str, xml: str, p: bool, debug: bool) -> None:
    """Execute the db to xml command with additional cli procedures.

    Args:
        db (str): database filename.
        xml (str): xml filename.
        p (bool): parse_source_attributes argument.
        debug (bool): debug argument.
    """

    if debug:
        check_xml_extension(xml)
        check_db_extension(db)

    db2xml(db_filename=db, xml_filename=xml, parse_source_attributes=p)


def cli_xml2db(db: str, xml: str, p: bool, unsafe: bool, debug: bool) -> None:
    """Execute the xml to db command with additional cli procedures.

    Args:
        db (str): database filename.
        xml (str): xml filename.
        p (bool): parse_source_attributes argument.
        debug (bool): debug argument.
    """

    if debug:
        check_xml_extension(xml)
        check_db_extension(db)

    xml2db(db_filename=db, xml_filename=xml, parse_source_attributes=p, unsafe=unsafe)


def cli_xml2sql(sql: str, xml: str, p: bool, debug: bool) -> None:
    """Execute the xml to sql command with additional cli procedures.

    Args:
        db (str): database filename.
        xml (str): xml filename.
        p (bool): parse_source_attributes argument.
        debug (bool): debug argument.
    """

    if debug:
        check_xml_extension(xml)
        check_sql_extension(sql)

    xml2sql(sql_filename=sql, xml_filename=xml, parse_source_attributes=p)
