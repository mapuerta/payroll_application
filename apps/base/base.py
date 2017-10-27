
base_tables = {
    "ir_fields": """
    CREATE TABLE ir_fields
    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    NAME TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    MODEL TEXT NOT NULL,
    ATTRS TEXT NOT NULL);
    """,
    "ir_model_change": """
    CREATE TABLE ir_model_change
    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    NAME TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    MODEL TEXT NOT NULL,
    ATTR TEXT NOT NULL,
    CHANGE TEXT NOT NULL);
    """,
    "ir_users": """
    CREATE TABLE ir_users
    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    NAME TEXT NOT NULL,
    LOGIN TEXT NOT NULL,
    LAST_CONNECT TEXT NOT NULL);
    """
}

property_table = {
    "required": "NOT NULL",
    "unique": "UNIQUE",
    "default": "DEFAULT {0}",
    "check": "CHECK({0})"
}

create_index = lambda field, table: "CREATE INDEX {field}_index ON {table}({field});".format(field=field, table=table)
