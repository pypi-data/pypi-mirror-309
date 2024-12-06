"""This module contains the some sql scripts."""

SQL_UNSAFE = """
PRAGMA journal_mode = OFF;
PRAGMA synchronous = 0;
-- The followings has to be manage in some way and tested
-- PRAGMA cache_size = 1000000;
-- PRAGMA locking_mode = EXCLUSIVE;
-- PRAGMA temp_store = MEMORY;
"""

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS params (
    param_name TEXT PRIMARY KEY NOT NULL,
    param_value TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY NOT NULL,
    dataset_type TEXT NOT NULL,
    dataset_active TEXT CHECK(dataset_active='true' or dataset_active='false') NOT NULL DEFAULT 'false'
);

CREATE TABLE IF NOT EXISTS dataset_children (
    parent_dataset_id TEXT NOT NULL,
    child_dataset_id TEXT NOT NULL,
    FOREIGN KEY(parent_dataset_id) REFERENCES datasets(dataset_id),
    FOREIGN KEY(child_dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS dataset_params (
    param_name TEXT NOT NULL,
    param_value TEXT DEFAULT '',
    dataset_id TEXT NOT NULL,
    PRIMARY KEY (param_name, dataset_id),
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS dataset_attributes (
    attribute_name TEXT NOT NULL,
    attribute_type TEXT DEFAULT '',
    attribute_value TEXT DEFAULT '',
    dataset_id TEXT NOT NULL,
    PRIMARY KEY (attribute_name, dataset_id),
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS dataset_source_attributes (
    attribute_name TEXT NOT NULL,
    attribute_type TEXT DEFAULT '',
    attribute_value TEXT DEFAULT '',
    dataset_id TEXT NOT NULL,
    PRIMARY KEY (attribute_name, dataset_id),
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS variables (
    variable_id INTEGER PRIMARY KEY NOT NULL,
    category TEXT CHECK(category='data' or category='axis') DEFAULT 'data',
    source_name TEXT NOT NULL,
    destination_name TEXT NOT NULL,
    data_type TEXT NOT NULL,
    dataset_id TEXT NOT NULL,
    order_number REAL NOT NULL DEFAULT 0,
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS variable_attributes (
    attribute_name TEXT NOT NULL,
    attribute_type TEXT DEFAULT '',
    attribute_value TEXT DEFAULT '',
    variable_id INTEGER NOT NULL,
    PRIMARY KEY (attribute_name, variable_id),
    FOREIGN KEY(variable_id) REFERENCES variables(variable_id)
);

CREATE TABLE IF NOT EXISTS variable_source_attributes (
    attribute_name TEXT NOT NULL,
    attribute_type TEXT DEFAULT '',
    attribute_value TEXT DEFAULT '',
    variable_id INTEGER NOT NULL,
    PRIMARY KEY (attribute_name, variable_id),
    FOREIGN KEY(variable_id) REFERENCES variables(variable_id)
);
"""
