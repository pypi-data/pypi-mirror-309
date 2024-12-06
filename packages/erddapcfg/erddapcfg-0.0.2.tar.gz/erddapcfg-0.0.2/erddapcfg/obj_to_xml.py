from .classes import ERDDAP
from .utils import change_line_ending
from .template_utils import obj2xml_string


def obj2xml(erddap: ERDDAP, xml_filename: str, parse_source_Attributes: bool = False) -> None:
    """Convert a python object to a XML datasets ERDDAP configuration.

    Args:
        erddap (ERDDAP): python object to convert.
        xml_filename (str): xml filename.
        parse_source_Attributes (bool, optional): Flag to enable the parsing of the sourceAttributes nodes. Defaults to False.
    """

    # Render the template
    output = obj2xml_string(erddap=erddap)

    # Custom unescape the CDATA blocks
    output = output.replace("::CDATA_START", "<![CDATA[")
    output = output.replace("::CDATA_STOP", "]]>")

    # Save xml
    with open(xml_filename, "w", encoding="utf-8") as f:
        f.write(output)
    change_line_ending(xml_filename)
