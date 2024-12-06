from xml.sax.saxutils import escape
import sqlite3
import logging

import pandas as pd

from .classes import ERDDAP, PARAM, DATASET, ATTRIBUTE, VARIABLE


def db2obj(db_filename: str, parse_source_attributes: bool = False) -> ERDDAP:
    """Convert a DB sqlite to a python object.

    Args:
        db_filename (str): database sqlite filename.
        parse_source_Attributes (bool, optional): Flag to enable the parsing of the sourceAttributes nodes. Defaults to False.
    """

    # Initialize objects for jinja template engine
    erddap = ERDDAP(
        params=[],
        datasets=[],
        parent_child=[],
    )

    # Open database
    connection = sqlite3.connect(db_filename)

    # Loading dataframes from database
    df_params = pd.read_sql_query(
        sql="SELECT * FROM params",
        con=connection,
    )
    df_datasets = pd.read_sql_query(
        sql="SELECT * FROM datasets",
        con=connection,
    )
    df_dataset_params = pd.read_sql_query(
        sql="SELECT * FROM dataset_params",
        con=connection,
    )
    df_dataset_attributes = pd.read_sql_query(
        sql="SELECT * FROM dataset_attributes",
        con=connection,
    )
    df_dataset_source_attributes = pd.read_sql_query(
        sql="SELECT * FROM dataset_source_attributes",
        con=connection,
    )
    df_variables = pd.read_sql_query(
        sql="SELECT * FROM variables",
        con=connection,
    )
    df_variable_attributes = pd.read_sql_query(
        sql="SELECT * FROM variable_attributes JOIN variables USING (variable_id)",
        con=connection,
    )
    df_variable_source_attributes = pd.read_sql_query(
        sql="SELECT * FROM variable_source_attributes JOIN variables USING (variable_id)",
        con=connection,
    )
    df_dataset_children = pd.read_sql_query(
        sql="SELECT dataset_id, child_dataset_id FROM datasets JOIN dataset_children ON datasets.dataset_id==dataset_children.parent_dataset_id",
        con=connection,
    )

    # Load params from db to objects
    for _, row in df_params.iterrows():
        erddap.params.append(
            PARAM(
                name=row["param_name"],
                value=row["param_value"] if row["param_value"] is not None else "",
            )
        )

    # Load datasets from db to objects
    for _, row in df_datasets.iterrows():
        erddap.datasets.append(
            DATASET(
                type=row["dataset_type"],
                datasetID=row["dataset_id"],
                active=row["dataset_active"],
                datasets=[],
                params=[],
                attributes=[],
                source_attributes=[],
                variables=[],
            )
        )

    # Load params, attributes, variables for each dataset from db to objects
    for dataset in erddap.datasets:
        logging.debug(dataset.datasetID)

        # Load dataset params from db to objects
        df = df_dataset_params[df_dataset_params["dataset_id"] == dataset.datasetID]
        for _, row in df.iterrows():
            dataset.params.append(
                PARAM(
                    name=row["param_name"],
                    value=row["param_value"] if row["param_value"] is not None else "",
                )
            )

        # Load dataset attributes from db to objects
        df = df_dataset_attributes[df_dataset_attributes["dataset_id"] == dataset.datasetID]
        for _, row in df.iterrows():
            dataset.attributes.append(
                ATTRIBUTE(
                    name=row["attribute_name"],
                    text=row["attribute_value"] if row["attribute_value"] is not None else "",
                    type=row["attribute_type"],
                )
            )

        # Load dataset source attributes from db to objects
        if parse_source_attributes:
            df = df_dataset_source_attributes[df_dataset_source_attributes["dataset_id"] == dataset.datasetID]
            for _, row in df.iterrows():
                dataset.source_attributes.append(
                    ATTRIBUTE(
                        name=row["attribute_name"],
                        text=row["attribute_value"] if row["attribute_value"] is not None else "",
                        type=row["attribute_type"],
                    )
                )

        # Load variables from db to objects
        df = df_variables[df_variables["dataset_id"] == dataset.datasetID]
        for _, row in df.iterrows():
            dataset.variables.append(
                VARIABLE(
                    tag=row["category"] + "Variable",
                    sourceName=row["source_name"],
                    destinationName=row["destination_name"],
                    dataType=row["data_type"],
                    attributes=None,
                    source_attributes=None,
                )
            )

        # Load attributes and source attributes for each variable from db to objects
        for variable in dataset.variables:
            # Load variable attributes from db to objects
            df = df_variable_attributes[df_variable_attributes["dataset_id"] == dataset.datasetID]
            df = df[df["destination_name"] == variable.destinationName]
            for _, row in df.iterrows():
                if variable.attributes is None:
                    variable.attributes = []

                variable.attributes.append(
                    ATTRIBUTE(
                        name=row["attribute_name"],
                        text=escape(str(row["attribute_value"]).replace('"', ""))
                        if row["attribute_value"] is not None
                        else "",
                        type=row["attribute_type"],
                    )
                )

            # Load variable source attributes from db to objects
            if parse_source_attributes:
                df = df_variable_source_attributes[df_variable_source_attributes["dataset_id"] == dataset.datasetID]
                df = df[df["destination_name"] == variable.destinationName]
                for _, row in df.iterrows():
                    if variable.source_attributes is None:
                        variable.source_attributes = []

                    variable.source_attributes.append(
                        ATTRIBUTE(
                            name=row["attribute_name"],
                            text=escape(str(row["attribute_value"]).replace('"', ""))
                            if row["attribute_value"] is not None
                            else "",
                            type=row["attribute_type"],
                        )
                    )

    # Load the parent - child relations between datasets from db to objects
    for _, row in df_dataset_children.iterrows():
        dataset_parent = [d for d in erddap.datasets if d.datasetID == row["dataset_id"]][0]
        dataset_child = [d for d in erddap.datasets if d.datasetID == row["child_dataset_id"]][0]
        dataset_parent.datasets.append(dataset_child)
        erddap.datasets.remove(dataset_child)

    return erddap
