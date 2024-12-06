# erddapcfg

- [erddapcfg](#erddapcfg)
  - [Description](#description)
    - [Features](#features)
    - [Who should use it?](#who-should-use-it)
    - [Why?](#why)
  - [Install](#install)
  - [Uninstall](#uninstall)
  - [Usage](#usage)
    - [CLI](#cli)
      - [db2xml](#db2xml)
      - [xml2db](#xml2db)
      - [xml2sql](#xml2sql)
      - [xml2sql](#xml2sql-1)
    - [Python library](#python-library)
  - [Database structure](#database-structure)
    - [params](#params)
    - [datasets](#datasets)
    - [dataset\_params](#dataset_params)
    - [dataset\_children](#dataset_children)
    - [dataset\_attributes](#dataset_attributes)
    - [dataset\_source\_attributes](#dataset_source_attributes)
    - [variables](#variables)
    - [variable\_attributes](#variable_attributes)
    - [variable\_source\_attributes](#variable_source_attributes)
  - [Development](#development)
    - [Background on project](#background-on-project)
    - [System](#system)
    - [License](#license)
    - [Dependency](#dependency)
      - [pandas](#pandas)
      - [jinja2](#jinja2)
    - [Known bugs](#known-bugs)
    - [Known issues](#known-issues)
      - [StrEnum (python \< 3.11)](#strenum-python--311)
    - [Wish todo / ideas](#wish-todo--ideas)


## Description
Python package and CLI that can help in the configuration of ERDDAP.

### Features
1) Convert datasets.xml configuration to SQLite database.
2) Convert SQLite database back to datasets.xml configuration.
3) Convert datasets.xml configuration to sql script.
4) Python library to work with the datasets.xml configuration from code.

### Who should use it?
1) People that manage and maintain ERDDAP instances, particularly those handling large numbers of datasets.
2) Those who may find xml erddap configuration daunting.

### Why?
1) Managing a huge xml can be stressful and time consuming.
2) Using SQL for quick, simultaneous view and edit of multiple configurations is much simpler.


## Install
```
pip install erddapcfg
```

## Uninstall
```
pip uninstall erddapcfg
```

## Usage

### CLI

#### db2xml
Convert from database to datasets.xml ERDDAP configuration.
```
erddapcfg db2xml database.db datasets.xml
```
Additional arguments:
- -p --parse-source-attributes : enable the parsing of the source attributes as comments.
- -d --debug : enable some debug logging information.

#### xml2db
Convert from datasets.xml ERDDAP configuration to database.
```
erddapcfg xml2db datasets.xml database.db
```
Additional arguments:
- -p --parse-source-attributes : enable the parsing of the source attributes as comments.
- -d --debug : enable some debug logging information.

#### xml2sql
Convert from datasets.xml ERDDAP configuration to sql script.
```
erddapcfg xml2db datasets.xml database.sql
```
Additional arguments:
- -p --parse-source-attributes : enable the parsing of the source attributes as comments.
- -d --debug : enable some debug logging information.


#### xml2sql
Test the installation.
```
erddapcfg test
```
- -d --debug : enable some debug logging information.


### Python library
```python
# Convert from datasets.xml ERDDAP configuration to python object
from erddapcfg import xml2obj, ERDDAP
erddap:ERDDAP = xml2obj(xml_filename="datasets.xml")


# Convert from database to python object
from erddapcfg import db2obj, ERDDAP
erddap:ERDDAP = db2xml(db_filename="database.db")


# Convert from python object to datasets.xml ERDDAP configuration
from erddapcfg import obj2xml
obj2xml(erddap=erddap, xml_filename="datasets.xml")


# Convert from python object to database
from erddapcfg import obj2db
obj2db(erddap=erddap, db_filename="database.db")


# Convert from python object to sql
from erddapcfg import obj2sql
obj2sql(erddap=erddap, sql_filename="database.sql")


# Convert from database to datasets.xml ERDDAP configuration
from erddapcfg import db2xml
db2xml(db_filename="database.db", xml_filename="datasets.xml")


# Convert from database to python object
from erddapcfg import db2obj
db2obj(db_filename="database.db")


# Convert from datasets.xml ERDDAP configuration to database
from erddapcfg import xml2db
xml2db(db_filename="database.db", xml_filename="datasets.xml")


# Convert from datasets.xml ERDDAP configuration to sql script
from erddapcfg import xml2sql
xml2sql(sql_filename="database.sql", xml_filename="datasets.xml")


# Convert from datasets.xml ERDDAP configuration to python object
from erddapcfg import xml2obj
xml2obj(xml_filename="datasets.xml")
```


## Database structure
The database converted from a datasets.xml ERDDAP configuration has the following structure:
![alt text](./images/database_structure.png)


### params
Contains the global parameters of the ERDDAP configuration, so every tag which is not "dataset".
<br>
Columns:
- <strong>param_name</strong> the name of the parameter, it's a primary key;
- <strong>param_value</strong> the value of the parameter.

Note: if your goal is to edit only datasets metadata ignore this table.


### datasets
Contains the list of all the dataset inside the configuration.
<br>
Columns:
- <strong>dataset_id</strong> string name index of the dataset, it's a primary key;
- <strong>dataset_type</strong> ERDDAP type of dataset, for example "EDDTableFromDatabase";
- <strong>dataset_active</strong> true or false value, tells ERDDAP to enable the dataset.


### dataset_params
Contains the ERDDAP parameters by dataset.
<br>
Columns:
- <strong>param_name</strong> the name of the parameter;
- <strong>param_value</strong> the value of the parameter;
- <strong>dataset_id</strong> the dataset which the parameter refers to.

The pair param_name and dataset_id form the Primary Key, there cannot be duplicate params in the same dataset.
<br>
Note: this parameters are used by ERDDAP to make the dataset work properly, these are not metadata.


### dataset_children
Contains the relation between two datasets as parent - child.
<br>
Columns:
- <strong>parent_dataset_id</strong> dataset_id of the parent;
- <strong>child_dataset_id</strong> dataset_id of the child.

The union of parent and child makes a Primary Key, there cannot be duplicate pairs.
<br>
This table usage is mainly for the datasets of type "...Aggregate..." which must have one or more dataset as children.
<br>
Note: if the configuration doesn't have Aggregated dataset ignore this table.


### dataset_attributes
Contains the metadata values of the given dataset.
<br>
Columns:
- <strong>attribute_name</strong> the name of the metadata;
- <strong>attribute_type</strong> the type of the metadata, if the value is a string this is often not used;
- <strong>attribute_value</strong> the value of the metadata;
- <strong>dataset_id</strong> the dataset which the metadata refers to.

The pair attribute_name and dataset_id makes the Primary Key, there cannot be duplicate metadata in the same dataset.
<br>
Note: if you have to edit metadata of a given dataset work with this table.


### dataset_source_attributes
Contains the source metadata of the given dataset.
<br>
Columns:
- <strong>attribute_name</strong> the name of the metadata;
- <strong>attribute_type</strong> the type of the metadata, if the value is a string this is often not used;
- <strong>attribute_value</strong> the value of the metadata;
- <strong>dataset_id</strong> the dataset which the metadata refers to.

The pair attribute_name and dataset_id makes the Primary Key, there cannot be duplicate metadata in the same dataset.
<br>
Note: the structure of this table is exactly the same as dataset_attributes, but this table is not meant to be edited: it contains default values for specific metadata extracted from the data source.
<br>
If in the dataset_attributes table you don't specific a metadata which is in this table then the metadata in this table will be display on ERDDAP. The only way to not display a source metadata is to overwrite the attribute in the dataset_attributes table.


### variables
Contains the variables of a given dataset.
<br>
Columns:
- <strong>variable_id</strong> identifier used in the database to refer to variables, it's the Primary Key;
- <strong>category</strong> the ERDDAP type of variable, the two allowed values are "data" and "axis", which will be translated to "dataVariable" and "axisVariable" respectively;
- <strong>source_name</strong> the name of the variable in the source data;
- <strong>destination_name</strong> the name of the variable that ERDDAP will display;
- <strong>data_type</strong> the data type of the variable, for example "string" of "float";
- <strong>dataset_id</strong> the dataset which the metadata refers to;
- <strong>order_number</strong> this is a number used to get the variables in a given order, this is useful because you have to tell ERDDAP the exact order of the source data.

Note: if you edit the source_name column then also the data source will have to be edited with the same name.


### variable_attributes
Contains the metadata of a given variable.
<br>
Columns:
- <strong>attribute_name</strong> the name of the metadata;
- <strong>attribute_type</strong> the type of the metadata, if the value is a string this is often not used.
- <strong>attribute_value</strong> the value of the metadata;
- <strong>variable_id</strong> the variable which the metadata refers to.

The pair attribute_name and variable_id makes the Primary Key, there cannot be duplicate metadata in the same variable.
<br>
Note: if you have to edit metadata of a given variable work with this table.


### variable_source_attributes
Contains the source metadata of a given variable.
<br>
Columns:
- <strong>attribute_name</strong> the name of the metadata;
- <strong>attribute_type</strong> the type of the metadata, if the value is a string this is often not used.
- <strong>attribute_value</strong> the value of the metadata;
- <strong>variable_id</strong> the variable which the metadata refers to.

The pair attribute_name and variable_id makes the Primary Key, there cannot be duplicate metadata in the same variable.
<br>
Note: the structure of this table is exactly the same as variable_attributes, but this table is not meant to be edited: it contains default values for specific metadata extracted from the data source.
<br>
If in the variable_attributes table you don't specific a metadata which is in this table then the metadata in this table will be display on ERDDAP. The only way to not display a source metadata is to overwrite the attribute in the variable_attributes table.


## Development

### Background on project
The main purpose of this project is to simplify the configuration process, particularly for handling metadata (ERDDAP attributes).
<br>
Further enhancements and features will be incorporated as time allows and will tailored with my personal preferences.

### System
The project was developed using Python 3.11, on Windows 11.
<br>
If you encounter any issues in other environment, consider opening an issue.

### License
This project is licensed under the open source MIT License.

### Dependency

#### pandas
The pandas library is used to elaborate the database responses when converting database to datasets.xml.

#### jinja2
The jinja2 library is used to generate the datasets.xml and the sql insert scripts with a template engine.

### Known bugs
<strong>For now none</strong>, the lack of tests can be partially the cause of that.

### Known issues

#### StrEnum (python < 3.11)

In version of python older than 3.11 there will be an error regarding the using of StrEnum from the [utils module](./erddapcfg/utils.py).
<br>
A workaround can be replacing:
```python
from enum import StrEnum


class Mode(StrEnum):
```
with the following:
```python
from enum import Enum


class Mode(str, Enum):
```

### Wish todo / ideas
(In no particular order)
- Make the process faster.
- Make an automatic sync system, without recreating each time the output file.
- Make better debug and error handling.
- Make the process compatible with other database systems, this will make it easier to work in group on the same configuration at the cost of installing a server somewhere. (In code maybe using SQLAlchemy library)
- Make more tests.
- Handle datasets recursion more in depth.
- Handle the setup.xml ERDDAP configuration.
- Write better documentation.
- Enhance python library.
