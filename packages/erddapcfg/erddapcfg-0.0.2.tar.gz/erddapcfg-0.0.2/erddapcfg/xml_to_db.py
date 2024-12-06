from .xml_to_obj import xml2obj
from .obj_to_db import obj2db


def xml2db(db_filename: str, xml_filename: str, parse_source_attributes: bool = False, unsafe: bool = False) -> None:
    """Convert a XML datasets ERDDAP configuration to a DB sqlite.

    Args:
        db_filename (str): database sqlite filename.
        xml_filename (str): xml filename.
        parse_source_Attributes (bool, optional): Flag to enable the parsing of the sourceAttributes nodes. Defaults to False.
        unsafe (bool, optional): Flag to enable unsafe execution to the database, this will disable journal and synchronous. Defaults to False.
    """

    erddap = xml2obj(
        xml_filename=xml_filename,
        parse_source_attributes=parse_source_attributes,
    )

    obj2db(
        erddap=erddap,
        db_filename=db_filename,
        parse_source_attributes=parse_source_attributes,
        unsafe=unsafe,
    )
