from .xml_to_obj import xml2obj
from .obj_to_sql import obj2sql


def xml2sql(sql_filename: str, xml_filename: str, parse_source_attributes: bool = False) -> None:
    """Convert a XML datasets ERDDAP configuration to a sql script.

    Args:
        sql_filename (str): sql filename.
        xml_filename (str): xml filename.
        parse_source_Attributes (bool, optional): Flag to enable the parsing of the sourceAttributes nodes. Defaults to False.
    """

    erddap = xml2obj(xml_filename=xml_filename, parse_source_attributes=parse_source_attributes)

    obj2sql(erddap=erddap, sql_filename=sql_filename, parse_source_attributes=parse_source_attributes)
