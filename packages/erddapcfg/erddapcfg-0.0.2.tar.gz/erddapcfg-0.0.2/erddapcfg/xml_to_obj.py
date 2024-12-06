import xml.etree.ElementTree as ET
import logging

from .classes import ERDDAP, PARAM, DATASET, ATTRIBUTE, VARIABLE


def xml2obj(xml_filename: str, parse_source_attributes: bool = False) -> ERDDAP:
    """Convert a XML datasets ERDDAP configuration to python objects.

    Args:
        xml_filename (str): xml filename.
        parse_source_Attributes (bool, optional): Flag to enable the parsing of the sourceAttributes nodes. Defaults to False.
    """

    # Initialize erddap object
    erddap = ERDDAP(
        params=[],
        datasets=[],
        parent_child=[],
    )

    # Load XML file
    with open(xml_filename, "r") as file:
        xml_string = "".join(file.readlines())

        # Custom escape CDATA blocks
        xml_string = xml_string.replace("<![CDATA[", "<![CDATA[::CDATA_START").replace("]]>", "::CDATA_STOP]]>")

        # Uncomment sourceAttributes blocks to make it readable from the parser
        if parse_source_attributes:
            xml_string = xml_string.replace("<!-- sourceAttributes>", "<sourceAttributes>").replace(
                "</sourceAttributes -->", "</sourceAttributes>"
            )

    datasets_root: ET.Element = ET.XML(xml_string)

    # Load params from xml to objects
    for child in datasets_root:
        if child.tag == "dataset":
            continue

        erddap.params.append(
            PARAM(
                name=child.tag,
                value=child.text if child.text is not None else "",
            )
        )

    # Load datasets from xml to objects
    children = datasets_root.findall(".//dataset")
    for child in children:
        erddap.datasets.append(
            DATASET(
                type=child.attrib["type"],
                datasetID=child.attrib["datasetID"],
                active=child.attrib["active"] if "active" in child.attrib else "true",
                datasets=[],
                params=[],
                attributes=[],
                source_attributes=[],
                variables=[],
            )
        )

    # Load params, attributes, variables for each dataset from xml to objects
    for dataset in erddap.datasets:
        logging.debug(dataset.datasetID)
        dataset_node = datasets_root.find(f".//dataset[@datasetID='{dataset.datasetID}']")

        # Load dataset params from xml to objects
        params_nodes = [
            child
            for child in dataset_node
            if child.tag not in ("dataset", "addAttributes", "sourceAttributes", "dataVariable", "axisVariable")
        ]
        for node in params_nodes:
            dataset.params.append(
                PARAM(
                    name=node.tag,
                    value=node.text if node.text is not None else "",
                )
            )

        # Load dataset attributes from xml to objects
        attribute_node = dataset_node.find("addAttributes")
        if attribute_node is not None:
            for node in attribute_node:
                dataset.attributes.append(
                    ATTRIBUTE(
                        name=node.attrib["name"],
                        text=node.text if node.text is not None else "",
                        type=node.attrib["type"] if "type" in node.attrib else "",
                    )
                )

        # Load dataset source attributes from xml to objects
        if parse_source_attributes:
            source_attribute_node = dataset_node.find("sourceAttributes")
            if source_attribute_node is not None:
                for node in source_attribute_node:
                    dataset.source_attributes.append(
                        ATTRIBUTE(
                            name=node.attrib["name"],
                            text=node.text if node.text is not None else "",
                            type=node.attrib["type"] if "type" in node.attrib else "",
                        )
                    )

        # Load dataset variables from xml to objects
        variable_nodes = dataset_node.findall("dataVariable") + dataset_node.findall("axisVariable")
        if variable_nodes is not None:
            for node in variable_nodes:
                source_name_node = node.find("sourceName")
                destination_name_node = node.find("destinationName")
                data_type_node = node.find("dataType")
                dataset.variables.append(
                    VARIABLE(
                        tag=node.tag,
                        sourceName=source_name_node.text if source_name_node is not None else "",
                        destinationName=destination_name_node.text if destination_name_node is not None else "",
                        dataType=data_type_node.text if data_type_node is not None else "",
                        attributes=[],
                        source_attributes=[],
                    )
                )

                # Load variable attributes from xml to objects
                attributes_node = node.find("addAttributes")
                if attributes_node is not None:
                    for child in attributes_node:
                        dataset.variables[-1].attributes.append(
                            ATTRIBUTE(
                                name=child.attrib["name"],
                                text=child.text if child.text is not None else "",
                                type=child.attrib["type"] if "type" in child.attrib else "",
                            )
                        )

                # Load variable source attributes from xml to objects
                if parse_source_attributes:
                    source_attribute_node = node.find("sourceAttributes")
                    if source_attribute_node is not None:
                        for node in source_attribute_node:
                            dataset.source_attributes.append(
                                ATTRIBUTE(
                                    name=node.attrib["name"],
                                    text=node.text if node.text is not None else "",
                                    type=node.attrib["type"] if "type" in node.attrib else "",
                                )
                            )

        # Load the parent - child relations between datasets from xml to objects
        dataset_children = dataset_node.findall("dataset")
        if dataset_children is not None:
            for dataset_child in dataset_children:
                erddap.parent_child.append((dataset.datasetID, dataset_child.attrib["datasetID"]))

    return erddap
