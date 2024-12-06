from .db_to_obj import db2obj
from .obj_to_xml import obj2xml


def db2xml(db_filename: str, xml_filename: str, parse_source_attributes: bool = False) -> None:
    """Convert a DB sqlite to a XML datasets ERDDAP configuration.

    Args:
        db_filename (str): database sqlite filename.
        xml_filename (str): xml filename.
        parse_source_Attributes (bool, optional): Flag to enable the parsing of the sourceAttributes nodes. Defaults to False.
    """

    erddap = db2obj(db_filename=db_filename, parse_source_attributes=parse_source_attributes)

    obj2xml(erddap=erddap, xml_filename=xml_filename, parse_source_Attributes=parse_source_attributes)
