import psycopg2
import re
import os
import hashlib
import decimal
import datetime
from ..core import exceptions
from ..core import engine
from ..core.table import Query
from .postgres_reserved import reserved_words

system_fields = [
    "sys_id",
    "sys_created",
    "sys_modified",
    "sys_modified_by",
    "sys_dirty",
    "sys_table",
    "description",
]

default_config = {
    "database": os.environ["DBDatabase"],
    "host": os.environ["DBHost"],
    "port": os.environ["DBPort"],
    "user": os.environ["DBUser"],
    "password": os.environ["DBPassword"],
}

def initialize(config=None, **kwargs):
    if not config:
        config = default_config.copy()
    config.update(kwargs)
    return engine.Engine(psycopg2, config, SQL)

def make_where(where, sql, vals, is_join=False):
    if not where:
        return
    sql.append("WHERE")
    if isinstance(where, str):
        sql.append(where)
        return
    if isinstance(where, dict):
        where = list(where.items())
    if not isinstance(where, list):
        raise Exception("Parameter `where` is not a valid datatype.")
    alias = "A"
    if is_join and isinstance(is_join, str):
        alias = is_join
    connect = ""
    for key, val in where:
        if connect:
            sql.append(connect)
        if is_join:
            if "." not in key:
                key = f"{alias}.{quote(key.lower())}"
        if val is None:
            if "!" in key:
                key = key.replace("!", "")
                sql.append(f"{key} is not NULL")
            else:
                sql.append(f"{key} is NULL")
        elif isinstance(val, (list, tuple)) and "><" not in key:
            if "!" in key:
                key = key.replace("!", "")
                sql.append(f"{key} not in %s")
                vals.append(tuple(val))
            else:
                sql.append(f"{key} in %s")
                vals.append(tuple(val))
        elif isinstance(val, Query):
            sql.append(f"{key} in ({val})")
        else:
            case = None
            if "<>" in key:
                key = key.replace("<>", "")
                op = "<>"
            elif "!=" in key:
                key = key.replace("!=", "")
                op = "<>"
            elif "!><" in key:
                key = key.replace("!><", "")
                op = "not between"
            elif "><" in key:
                key = key.replace("><", "")
                op = "between"
            elif "!%" in key:
                key = key.replace("!%", "")
                op = "not like"
            elif "%%" in key:
                key = key.replace("%%", "")
                op = "%"
            elif "%>" in key:
                key = key.replace("%>", "")
                op = "%>"
            elif "<%" in key:
                key = key.replace("<%", "")
                op = "<%"
            elif "==" in key:
                key = key.replace("==", "")
                op = "="
            elif "<=" in key:
                key = key.replace("<=", "")
                op = "<="
            elif ">=" in key:
                key = key.replace(">=", "")
                op = ">="
            elif "<" in key:
                key = key.replace("<", "")
                op = "<"
            elif ">" in key:
                key = key.replace(">", "")
                op = ">"
            elif "%" in key:
                key = key.replace("%", "")
                op = "ilike"
            elif "!~*" in key:
                key = key.replace("!~*", "")
                op = "!~*"
            elif "~*" in key:
                key = key.replace("~*", "")
                op = "~*"
            elif "!~" in key:
                key = key.replace("!~", "")
                op = "!~"
            elif "~" in key:
                key = key.replace("~", "")
                op = "~"
            elif "!" in key:
                key = key.replace("!", "")
                op = "<>"
            elif "=" in key:
                key = key.replace("=", "")
                op = "="
            else:
                op = "="
            if "#" in key:
                key = key.replace("#", "")
                op = "="
                case = "lower"
            if isinstance(val, str) and val[:2] == "@@" and val[2:]:
                sql.append(f"{key} {op} {val[2:]}")
            elif op in ["between", "not between"]:
                sql.append(f"{key} {op} %s and %s")
                vals.extend(val)
            else:
                if case:
                    sql.append(f"{case}({key}) {op} {case}(%s)")
                else:
                    sql.append(f"{key} {op} %s")
                vals.append(val)
        connect = "AND"

def quote(data):
    if isinstance(data, list):
        new = []
        for item in data:
            if "@@" in item:
                new.append(item[2:])
            else:
                new.append(quote(item))
        return new
    else:
        parts = data.split(".")
        new = []
        for part in parts:
            if '"' in part:
                new.append(part)
            elif part.upper() in reserved_words:
                new.append(f'"{part}"')
            elif re.findall("[/]", part):
                new.append(f'"{part}"')
            else:
                new.append(part)
        return ".".join(new)

class SQL(object):
    server = "PostGreSQL"
    type_column_identifier = "data_type"
    is_nullable = "is_nullable"

    default_schema = "public"

    ApplicationErrorCodes = ["22P02", "42883"]

    DatabaseMissingErrorCodes = []
    TableMissingErrorCodes = ["42P01"]
    ColumnMissingErrorCodes = ["42703"]
    ForeignKeyMissingErrorCodes = ["42704"]

    ConnectionErrorCodes = ["08001", "08S01","57P03", "08006", "53300"]
    DuplicateKeyErrorCodes = []  # Handled in regex check.
    RetryTransactionCodes = []
    TruncationErrorCodes = ["22001"]
    LockTimeoutErrorCodes = ["55P03"]
    DatabaseObjectExistsErrorCodes = ["42710", "42P07", "42P04"]
    DataIntegrityErrorCodes = ["23503"]

    @classmethod
    def version(cls):
        return "select version()", tuple()

    @classmethod
    def timestamp(cls):
        return "select current_timestamp", tuple()

    @classmethod
    def user(cls):
        return "select current_user", tuple()

    @classmethod
    def databases(cls):
        return "select datname from pg_database where datistemplate = false", tuple()

    @classmethod
    def schemas(cls):
        return "select schema_name from information_schema.schemata", tuple()

    @classmethod
    def current_schema(cls):
        return "select current_schema", tuple()

    @classmethod
    def current_database(cls):
        return "select current_database()", tuple()

    @classmethod
    def tables(cls, system=False):
        if system:
            return (
                "select table_schema,table_name from information_schema.tables where table_type = 'BASE TABLE' order by table_schema,table_name",
                tuple(),
            )
        else:
            return (
                "select table_schema, table_name from information_schema.tables where table_type = 'BASE TABLE' and table_schema NOT IN ('pg_catalog', 'information_schema')",
                tuple(),
            )

    @classmethod
    def views(cls, system=False):
        if system:
            return (
                "select table_schema, table_name from information_schema.views order by table_schema,table_name",
                tuple(),
            )
        else:
            return (
                "select table_schema, table_name from information_schema.views where table_schema = any (current_schemas(false)) order by table_schema,table_name",
                tuple(),
            )

    @classmethod
    def __has_pointer(cls, columns):
        if isinstance(columns, str):
            columns = columns.split(",")
        if isinstance(columns, list):
            for column in columns:
                if "@@" in column:
                    continue
                if ">" in column:
                    return True
        return False

    @classmethod
    def select(
        cls,
        columns=None,
        table=None,
        where=None,
        orderby=None,
        groupby=None,
        having=None,
        start=None,
        qty=None,
        tbl=None,
        lock=None,
        skip_locked=None,
    ):
        if not table:
            raise Exception("Table name required")
        is_join = False

        if isinstance(columns, str) and "distinct" in columns.lower():
            sql = [
                "SELECT",
                columns,
                "FROM",
                quote(table),
            ]
        elif cls.__has_pointer(columns):
            is_join = True
            if isinstance(columns, str):
                columns = columns.split(",")
            letter = 65
            tables = {table: chr(letter)}
            letter += 1
            __select = []
            __from = [f"{quote(table)} AS {tables.get(table)}"]
            __left_join = []

            for column in columns:
                if "@@" in column:
                    __select.append(column[2:])
                elif ">" in column:
                    parts = column.split(">")
                    foreign = tbl.foreign_key_info(parts[0])
                    if not foreign:
                        raise exceptions.DbApplicationError("Foreign key not defined")
                    ref_table = foreign["referenced_table_name"]
                    ref_schema = foreign["referenced_table_schema"]
                    ref_column = foreign["referenced_column_name"]
                    lookup = f"{ref_table}:{parts[0]}"
                    if lookup in tables:
                        __select.append(
                            f'{tables.get(lookup)}."{parts[1]}" as "{'_'.join(parts)}"'
                        )
                    else:
                        tables[lookup] = chr(letter)
                        letter += 1
                        __select.append(
                            f'{tables.get(lookup)}."{parts[1]}" as "{'_'.join(parts)}"'
                        )
                        __left_join.append(
                            f'LEFT OUTER JOIN "{ref_schema}"."{ref_table}" AS {tables.get(lookup)}'
                        )
                        __left_join.append(
                            f'ON {tables.get(table)}."{parts[0]}" = {tables.get(lookup)}."{ref_column}"'
                        )
                    if orderby and column in orderby:
                        orderby = orderby.replace(
                            column, f"{tables.get(lookup)}.{parts[1]}"
                        )

                else:
                    if "(" in column:
                        __select.append(column)
                    else:
                        __select.append(f"{tables.get(table)}.{column}")
            sql = ["SELECT"]
            sql.append(",".join(__select))
            sql.append("FROM")
            sql.extend(__from)
            sql.extend(__left_join)
        else:
            if columns:
                if isinstance(columns, str):
                    columns = columns.split(",")
                if isinstance(columns, list):
                    columns = quote(columns)
                    columns = ",".join(columns)
            else:
                columns = "*"
            sql = [
                "SELECT",
                columns,
                "FROM",
                quote(table),
            ]
        vals = []
        make_where(where, sql, vals, is_join)
        if groupby:
            sql.append("GROUP BY")
            if isinstance(groupby, (list, tuple)):
                groupby = ",".join(groupby)
            sql.append(groupby)
        if having:
            sql.append("HAVING")
            if isinstance(having, (list, tuple)):
                having = ",".join(having)
            sql.append(having)
        if orderby:
            sql.append("ORDER BY")
            if isinstance(orderby, (list, tuple)):
                orderby = ",".join(orderby)
            sql.append(orderby)
        if start and qty:
            sql.append(f"OFFSET {start} ROWS FETCH NEXT {qty} ROWS ONLY")
        elif start:
            sql.append(f"OFFSET {start} ROWS")
        elif qty:
            sql.append(f"FETCH NEXT {qty} ROWS ONLY")
        if lock or skip_locked:
            sql.append("FOR UPDATE")
        if skip_locked:
            sql.append("SKIP LOCKED")
        sql = " ".join(sql)
        return sql, tuple(vals)

    @classmethod
    def create_database(cls, name):
        return f"create database {name}", tuple()

    @classmethod
    def last_id(cls, table):
        return "SELECT CURRVAL(PG_GET_SERIAL_SEQUENCE(%s, 'sys_id'))", tuple([table])

    @classmethod
    def current_id(cls, table):
        return (
            "SELECT pg_sequence_last_value(PG_GET_SERIAL_SEQUENCE(%s, 'sys_id'))",
            tuple([table]),
        )

    @classmethod
    def set_id(cls, table, start):
        return "SELECT SETVAL(PG_GET_SERIAL_SEQUENCE(%s, 'sys_id'), %s)", tuple(
            [table, start]
        )

    @classmethod
    def drop_database(cls, name):
        return f"drop database if exists {name}", tuple()

    @classmethod
    def create_table(cls, name, columns={}, drop=False):
        if "." in name:
            fqtn = name
        else:
            fqtn = f"public.{name}"
        schema, table = fqtn.split(".")
        name = fqtn.replace(".", "_")
        sql = []
        if drop:
            sql.append(cls.drop_table(fqtn)[0])
        sql.append(
            f"""
            CREATE TABLE {fqtn} (
              sys_id BIGSERIAL PRIMARY KEY,
              sys_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              sys_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              sys_modified_by TEXT,
              sys_dirty BOOLEAN NOT NULL DEFAULT FALSE,
              sys_table TEXT,
              description TEXT
            );

            SELECT SETVAL(PG_GET_SERIAL_SEQUENCE('{fqtn}', 'sys_id'),1000,TRUE);

            CREATE OR REPLACE FUNCTION {schema}.on_sys_modified()
              RETURNS TRIGGER AS
            $BODY$
                        BEGIN
                        -- update sys_modified on each insert/update.
                        NEW.sys_modified := now();
                        if (TG_OP = 'INSERT') THEN
                            NEW.sys_created :=now();
                        ELSEIF (TG_OP = 'UDPATE') THEN
                         -- Do not allow sys_created to be modified.
                            NEW.sys_created := OLD.sys_created;
                        END IF;
                        -- Insert table name to row
                        NEW.sys_table := TG_TABLE_NAME;
                        RETURN NEW;
                        END;
            $BODY$
              LANGUAGE plpgsql VOLATILE
              COST 100;

            CREATE TRIGGER on_update_row_{fqtn.replace('.', '_')}
            BEFORE INSERT OR UPDATE ON {fqtn}
            FOR EACH ROW EXECUTE PROCEDURE {schema}.on_sys_modified();

        """
        )

        for key, val in columns.items():
            key = re.sub("<>!=%", "", key.lower())
            if key in system_fields:
                continue
            sql.append(
                f"ALTER TABLE {quote(fqtn)} ADD COLUMN {quote(key)} {cls.get_type(val)};"
            )
        return "\n\t".join(sql), tuple()

    @classmethod
    def drop_table(cls, name):
        return f"drop table if exists {quote(name)} cascade;", tuple()

    @classmethod
    def drop_column(cls, table, name, cascade=True):
        if cascade:
            return (
                f"ALTER TABLE {quote(table)} DROP COLUMN {quote(name)} CASCADE",
                tuple(),
            )
        else:
            return (
                f"ALTER TABLE {quote(table)} DROP COLUMN {quote(name)}",
                tuple(),
            )

    @classmethod
    def columns(cls, name):
        if "." in name:
            return """
            select column_name
            from information_schema.columns
            where UPPER(table_schema) = UPPER(%s)
            and UPPER(table_name) = UPPER(%s)
            """, tuple(
                name.split(".")
            )
        else:
            return """
            select column_name
            from information_schema.columns
            where UPPER(table_name) = UPPER(%s)
            """, tuple(
                [
                    name,
                ]
            )

    @classmethod
    def column_info(cls, table, name):
        params = table.split(".")
        params.append(name)
        if "." in table:
            return """
            select *
            from information_schema.columns
            where UPPER(table_schema ) = UPPER(%s)
            and UPPER(table_name) = UPPER(%s)
            and UPPER(column_name) = UPPER(%s)
            """, tuple(
                params
            )
        else:
            return """
            select *
            from information_schema.columns
            where UPPER(table_name) = UPPER(%s)
            and UPPER(column_name) = UPPER(%s)
            """, tuple(
                params
            )

    @classmethod
    def primary_keys(cls, table):
        params = table.split(".")
        params.reverse()
        if "." in table:
            return """
            SELECT
              pg_attribute.attname
            FROM pg_index, pg_class, pg_attribute, pg_namespace
            WHERE
              pg_class.oid = %s::regclass AND
              indrelid = pg_class.oid AND
              nspname = %s AND
              pg_class.relnamespace = pg_namespace.oid AND
              pg_attribute.attrelid = pg_class.oid AND
              pg_attribute.attnum = any(pg_index.indkey)
             AND indisprimary
            """, tuple(
                params
            )
        else:
            return """
            SELECT
              pg_attribute.attname
            FROM pg_index, pg_class, pg_attribute, pg_namespace
            WHERE
              pg_class.oid = %s::regclass AND
              indrelid = pg_class.oid AND
              pg_class.relnamespace = pg_namespace.oid AND
              pg_attribute.attrelid = pg_class.oid AND
              pg_attribute.attnum = any(pg_index.indkey)
             AND indisprimary
            """, tuple(
                params
            )

    @classmethod
    def foreign_key_info(cls, table=None, column=None, schema=None):
        if "." in table:
            schema, table = table.split(".")

        sql = [
            """
        SELECT
             KCU1.CONSTRAINT_NAME AS "FK_CONSTRAINT_NAME"
           , KCU1.CONSTRAINT_SCHEMA AS "FK_CONSTRAINT_SCHEMA"
           , KCU1.CONSTRAINT_CATALOG AS "FK_CONSTRAINT_CATALOG"
           , KCU1.TABLE_NAME AS "FK_TABLE_NAME"
           , KCU1.COLUMN_NAME AS "FK_COLUMN_NAME"
           , KCU1.ORDINAL_POSITION AS "FK_ORDINAL_POSITION"
           , KCU2.CONSTRAINT_NAME AS "UQ_CONSTRAINT_NAME"
           , KCU2.CONSTRAINT_SCHEMA AS "UQ_CONSTRAINT_SCHEMA"
           , KCU2.CONSTRAINT_CATALOG AS "UQ_CONSTRAINT_CATALOG"
           , KCU2.TABLE_NAME AS "UQ_TABLE_NAME"
           , KCU2.COLUMN_NAME AS "UQ_COLUMN_NAME"
           , KCU2.ORDINAL_POSITION AS "UQ_ORDINAL_POSITION"
           , KCU1.CONSTRAINT_NAME AS "CONSTRAINT_NAME"
           , KCU2.CONSTRAINT_SCHEMA AS "REFERENCED_TABLE_SCHEMA"
           , KCU2.TABLE_NAME AS "REFERENCED_TABLE_NAME"
           , KCU2.COLUMN_NAME AS "REFERENCED_COLUMN_NAME"
        FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS RC
        JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU1
        ON KCU1.CONSTRAINT_CATALOG = RC.CONSTRAINT_CATALOG
           AND KCU1.CONSTRAINT_SCHEMA = RC.CONSTRAINT_SCHEMA
           AND KCU1.CONSTRAINT_NAME = RC.CONSTRAINT_NAME
        JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU2
        ON KCU2.CONSTRAINT_CATALOG = RC.UNIQUE_CONSTRAINT_CATALOG
           AND KCU2.CONSTRAINT_SCHEMA = RC.UNIQUE_CONSTRAINT_SCHEMA
           AND KCU2.CONSTRAINT_NAME = RC.UNIQUE_CONSTRAINT_NAME
           AND KCU2.ORDINAL_POSITION = KCU1.ORDINAL_POSITION
        """
        ]
        vals = []
        where = {}
        if schema:
            where["LOWER(KCU1.CONSTRAINT_SCHEMA)"] = schema.lower()
        if table:
            where["LOWER(KCU1.TABLE_NAME)"] = table.lower()
        if column:
            where["LOWER(KCU1.COLUMN_NAME)"] = column.lower()
        make_where(where, sql, vals)
        return " ".join(sql), tuple(vals)

    @classmethod
    def create_foreign_key(
        cls, table, columns, key_to_table, key_to_columns, name=None, schema=None
    ):
        if "." not in table and schema:
            table = f"{schema}.{table}"
        if isinstance(key_to_columns, str):
            key_to_columns = [key_to_columns]
        if isinstance(columns, str):
            columns = [columns]
        if not name:
            m = hashlib.md5()
            m.update(table.encode("utf-8"))
            m.update(" ".join(columns).encode("utf-8"))
            m.update(key_to_table.encode("utf-8"))
            m.update(" ".join(key_to_columns).encode("utf-8"))
            name = f"FK_{m.hexdigest()}"
        sql = f"ALTER TABLE {table} ADD CONSTRAINT {name} FOREIGN KEY ({','.join(columns)}) REFERENCES {key_to_table} ({','.join(key_to_columns)});"

        return sql, tuple()

    @classmethod
    def drop_foreign_key(
        cls,
        table,
        columns,
        key_to_table=None,
        key_to_columns=None,
        name=None,
        schema=None,
    ):
        if "." not in table and schema:
            table = f"{schema}.{table}"
        if isinstance(key_to_columns, str):
            key_to_columns = [key_to_columns]
        if isinstance(columns, str):
            columns = [columns]
        if not name:
            m = hashlib.md5()
            m.update(table.encode("utf-8"))
            m.update(" ".join(columns).encode("utf-8"))
            m.update(key_to_table.encode("utf-8"))
            m.update(" ".join(key_to_columns).encode("utf-8"))
            name = f"FK_{m.hexdigest()}"
        sql = f"ALTER TABLE {table} DROP CONSTRAINT {name};"
        return sql, tuple()

    @classmethod
    def create_index(
        cls,
        table=None,
        columns=None,
        unique=False,
        direction=None,
        where=None,
        name=None,
        schema=None,
        trigram=None,
        tbl=None,
        lower=None,
    ):
        """
        The following statements must be executed on the database instance once to enable respective trigram features.
        CREATE EXTENSION pg_trgm; is required to use  gin.
        CREATE EXTENSION btree_gist; is required to use gist
        """
        if "." not in table and schema:
            table = f"{schema}.{table}"
        if isinstance(columns, (list, set)):
            columns = ",".join([quote(c.lower()) for c in columns])
        else:
            columns = quote(columns)
        sql = ["CREATE"]
        if unique:
            sql.append("UNIQUE")
        sql.append("INDEX")
        tablename = quote(table)
        if not name:
            name = re.sub(
                r"\([^)]*\)",
                "",
                columns.replace(" ", "").replace(",", "_").replace('"', ""),
            )
        if trigram:
            sql.append(
                f"IDX__TRGM_{table.replace('.', '_')}_{trigram.upper()}__{name}"
            )
        else:
            sql.append(f"IDX__{table.replace('.', '_')}__{name}")
        sql.append("ON")
        sql.append(quote(tablename))

        if trigram:
            sql.append("USING")
            sql.append(trigram)
        sql.append("(")
        if tbl:
            join = ""
            for column_name in columns.split(","):
                column_name = column_name.replace('"', "")
                if join:
                    sql.append(join)
                column = tbl.column(column_name)
                if column.py_type == str:
                    if lower:
                        sql.append(f"lower({quote(column_name)})")
                    else:
                        sql.append(quote(column_name))
                else:
                    sql.append(quote(column_name))
                join = ","
        else:
            sql.append(columns)
        if trigram:
            sql.append(f"{trigram.lower()}_trgm_ops")
        sql.append(")")
        vals = []

        make_where(where, sql, vals)
        return " ".join(sql), tuple(vals)

    @classmethod
    def drop_index(cls, table=None, columns=None, name=None, schema=None, trigram=None):
        if "." not in table and schema:
            table = f"{schema}.{table}"
        if isinstance(columns, (list, set)):
            columns = ",".join([quote(c.lower()) for c in columns])
        else:
            columns = quote(columns)
        sql = ["DROP"]
        sql.append("INDEX IF EXISTS")
        tablename = quote(table)
        if not name:
            name = re.sub(
                r"\([^)]*\)",
                "",
                columns.replace(" ", "").replace(",", "_").replace('"', ""),
            )
        if trigram:
            sql.append(
                f"IDX__TRGM_{table.replace('.', '_')}_{trigram.upper()}__{name}"
            )
        else:
            sql.append(f"IDX__{table.replace('.', '_')}__{name}")
        return " ".join(sql), tuple()

    @classmethod
    def merge(cls, table, data, pk, on_conflict_do_nothing, on_conflict_update):
        d = {}
        d.update(data)
        d.update(pk)
        sql, vals = cls.insert(table, d)
        sql = [sql]
        vals = list(vals)
        if on_conflict_do_nothing != on_conflict_update:
            sql.append("ON CONFLICT")
            sql.append("(")
            sql.append(",".join(pk.keys()))
            sql.append(")")
            sql.append("DO")
            if on_conflict_do_nothing:
                sql.append("NOTHING")
            elif on_conflict_update:
                sql2, vals2 = cls.update(table, data, pk, excluded=True)
                sql.append(sql2)
                vals.extend(vals2)
        else:
            raise Exception(
                "Update on conflict must have one and only one option to complete on conflict."
            )
        return " ".join(sql), tuple(vals)

    @classmethod
    def insert(cls, table, data):
        keys = []
        vals = []
        args = []
        for key, val in data.items():
            keys.append(quote(key.lower()))
            if isinstance(val, str) and len(val) > 2 and val[:2] == "@@" and val[2:]:
                vals.append(val[2:])
            else:
                vals.append("%s")
                args.append(val)

        sql = ["INSERT INTO"]
        sql.append(quote(table))
        sql.append("(")
        sql.append(",".join(keys))
        sql.append(")")
        sql.append("VALUES")
        sql.append("(")
        sql.append(",".join(vals))
        sql.append(")")
        sql = " ".join(sql)
        return sql, tuple(args)

    @classmethod
    def update(
        cls,
        table,
        data,
        pk,
        left_join=None,
        inner_join=None,
        outer_join=None,
        excluded=False,
    ):
        alias = "A"
        if " " in table:
            alias, table = table.split(" ")
        is_join = bool(left_join or inner_join or outer_join)
        sql = ["UPDATE"]
        if not excluded:
            sql.append(quote(table))
        sql.append("SET")
        vals = []
        connect = ""
        for key, val in data.items():
            if connect:
                sql.append(connect)
            if isinstance(val, str) and val[:2] == "@@" and val[2:]:
                sql.append(f"{key} = {val[2:]}")
            else:
                if excluded:
                    sql.append(f"{key} = EXCLUDED.{key}")
                else:
                    sql.append(f"{key} = %s")
                    vals.append(val)
            connect = ","
        if is_join:
            sql.append("FROM")
            sql.append(table)
            sql.append("AS")
            sql.append(alias)
        if left_join:
            for k, v in left_join.items():
                sql.append("LEFT JOIN")
                sql.append(k)
                sql.append("ON")
                sql.append(v)
        if outer_join:
            for k, v in outer_join.items():
                sql.append("OUTER JOIN")
                sql.append(k)
                sql.append("ON")
                sql.append(v)
        if inner_join:
            for k, v in inner_join.items():
                sql.append("INNER JOIN")
                sql.append(k)
                sql.append("ON")
                sql.append(v)
        if not excluded:
            make_where(pk, sql, vals, is_join)
        return " ".join(sql), tuple(vals)

    @classmethod
    def get_type(cls, v):
        if isinstance(v, str):
            if v[:2] == "@@":
                return v[2:] or cls.TYPES.TEXT
        elif isinstance(v, str) or v is str:
            return cls.TYPES.TEXT
        elif isinstance(v, bool) or v is bool:
            return cls.TYPES.BOOLEAN
        elif isinstance(v, int) or v is int:
            return cls.TYPES.BIGINT
        elif isinstance(v, float) or v is float:
            return f"{cls.TYPES.NUMERIC}(19, 6)"
        elif isinstance(v, decimal.Decimal) or v is decimal.Decimal:
            return f"{cls.TYPES.NUMERIC}(19, 6)"
        elif isinstance(v, datetime.datetime) or v is datetime.datetime:
            return cls.TYPES.DATETIME
        elif isinstance(v, datetime.date) or v is datetime.date:
            return cls.TYPES.DATE
        elif isinstance(v, datetime.time) or v is datetime.time:
            return cls.TYPES.TIME
        elif isinstance(v, datetime.timedelta) or v is datetime.timedelta:
            return cls.TYPES.INTERVAL
        elif isinstance(v, bytes) or v is bytes:
            return cls.TYPES.BINARY
        return cls.TYPES.TEXT

    @classmethod
    def get_conv(cls, v):
        if isinstance(v, str):
            if v[:2] == "@@":
                return v[2:] or cls.TYPES.TEXT
        elif isinstance(v, str) or v is str:
            return cls.TYPES.TEXT
        elif isinstance(v, bool) or v is bool:
            return cls.TYPES.BOOLEAN
        elif isinstance(v, int) or v is int:
            return cls.TYPES.BIGINT
        elif isinstance(v, float) or v is float:
            return cls.TYPES.NUMERIC
        elif isinstance(v, decimal.Decimal) or v is decimal.Decimal:
            return cls.TYPES.NUMERIC
        elif isinstance(v, datetime.datetime) or v is datetime.datetime:
            return cls.TYPES.DATETIME
        elif isinstance(v, datetime.date) or v is datetime.date:
            return cls.TYPES.DATE
        elif isinstance(v, datetime.time) or v is datetime.time:
            return cls.TYPES.TIME
        elif isinstance(v, datetime.timedelta) or v is datetime.timedelta:
            return cls.TYPES.INTERVAL
        elif isinstance(v, bytes) or v is bytes:
            return cls.TYPES.BINARY
        return cls.TYPES.TEXT

    @classmethod
    def py_type(cls, v):
        v = str(v).upper()
        if v == cls.TYPES.INTEGER:
            return int
        elif v == cls.TYPES.SMALLINT:
            return int
        elif v == cls.TYPES.BIGINT:
            return int
        elif v == cls.TYPES.NUMERIC:
            return decimal.Decimal
        elif v == cls.TYPES.TEXT:
            return str
        elif v == cls.TYPES.BOOLEAN:
            return bool
        elif v == cls.TYPES.DATE:
            return datetime.date
        elif v == cls.TYPES.TIME:
            return datetime.time
        elif v == cls.TYPES.TIME_TZ:
            return datetime.time
        elif v == cls.TYPES.DATETIME:
            return datetime.datetime
        elif v == cls.TYPES.INTERVAL:
            return datetime.timedelta
        elif v == cls.TYPES.DATETIME_TZ:
            return datetime.datetime
        elif v == cls.TYPES.INTERVAL_TZ:
            return datetime.timedelta
        else:
            raise Exception(f"unmapped type {v}")

    @classmethod
    def massage_data(cls, data):
        data = {key.lower(): val for key, val in data.items()}
        primaryKey = set(cls.GetPrimaryKeyColumnNames())
        if not primaryKey:
            if not cls.Exists():
                raise exceptions.DbTableMissingError
        dataKeys = set(data.keys()).intersection(primaryKey)
        dataColumns = set(data.keys()).difference(primaryKey)
        pk = {}
        pk.update([(k, data[k]) for k in dataKeys])
        d = {}
        d.update([(k, data[k]) for k in dataColumns])
        return d, pk

    @classmethod
    def alter_add(cls, table, columns, null_allowed=True):
        sql = []
        null = "NOT NULL" if not null_allowed else ""
        if isinstance(columns, dict):
            for key, val in columns.items():
                key = re.sub("<>!=%", "", key.lower())
                sql.append(
                    f"ALTER TABLE {quote(table)} ADD {quote(key)} {cls.get_type(val)} {null};"
                )
        return "\n\t".join(sql), tuple()

    @classmethod
    def alter_drop(cls, table, columns):
        sql = [f"ALTER TABLE {quote(table)} DROP COLUMN"]
        if isinstance(columns, dict):
            for key, val in columns.items():
                key = re.sub("<>!=%", "", key.lower())
                sql.append(f"{key},")
        if sql[-1][-1] == ",":
            sql[-1] = sql[-1][:-1]
        return "\n\t".join(sql), tuple()

    @classmethod
    def alter_column_by_type(cls, table, column, value, nullable=True):
        sql = [f"ALTER TABLE {quote(table)} ALTER COLUMN"]
        sql.append(f"{quote(column)} TYPE {cls.get_type(value)}")
        sql.append(f"USING {quote(column)}::{cls.get_conv(value)}")
        if not nullable:
            sql.append("NOT NULL")
        return "\n\t".join(sql), tuple()

    @classmethod
    def alter_column_by_sql(cls, table, column, value):
        sql = [f"ALTER TABLE {quote(table)} ALTER COLUMN"]
        sql.append(f"{quote(column)} {value}")
        return " ".join(sql), tuple()

    @classmethod
    def rename_column(cls, table, orig, new):
        return (
            f"ALTER TABLE {quote(table)} RENAME COLUMN {quote(orig)} TO {quote(new)};",
            tuple(),
        )

    @classmethod
    def rename_table(cls, table, new):
        return f"ALTER TABLE {quote(table)} RENAME TO {quote(new)};", tuple()

    @classmethod
    def create_savepoint(cls, sp):
        return f'SAVEPOINT "{sp}"', tuple()

    @classmethod
    def release_savepoint(cls, sp):
        return f'RELEASE SAVEPOINT "{sp}"', tuple()

    @classmethod
    def rollback_savepoint(cls, sp):
        return f'ROLLBACK TO SAVEPOINT "{sp}"', tuple()

    @classmethod
    def duplicate_rows(cls, table, columns, where={}):
        return cls.select(
            columns,
            table,
            where,
            orderby=columns,
            groupby=columns,
            having="count(*) > 2",
        )

    @classmethod
    def delete(cls, table, where):
        sql = [f"DELETE FROM {table}"]
        vals = []
        make_where(where, sql, vals)
        return " ".join(sql), tuple(vals)

    @classmethod
    def truncate(cls, table):
        return f"truncate table {quote(table)}", tuple()

    @classmethod
    def create_view(cls, name, query, temp=False, silent=True):
        sql = ["CREATE"]
        if silent:
            sql.append("OR REPLACE")
        if temp:
            sql.append("TEMPORARY")
        sql.append("VIEW")
        sql.append(name)
        sql.append("AS")
        sql.append(query)
        return " ".join(sql), tuple()

    @classmethod
    def drop_view(cls, name, silent=True):
        sql = ["DROP VIEW"]
        if silent:
            sql.append("IF EXISTS")
        sql.append(name)
        return " ".join(sql), tuple()

    @classmethod
    def alter_trigger(cls, table, state="ENABLE", name="USER"):
        return f"ALTER TABLE {table} {state} TRIGGER {name}", tuple()

    @classmethod
    def set_sequence(cls, table, next_value):
        return (
            f"SELECT SETVAL(PG_GET_SERIAL_SEQUENCE('{table}', 'sys_id'),{next_value},FALSE)",
            tuple(),
        )

    @classmethod
    def missing(cls, table, list, column="SYS_ID", where=None):
        sql = [
            f"SELECT * FROM",
            f"UNNEST('{{{','.join([str(x) for x in list])}}}'::int[]) id",
            f"EXCEPT ALL",
            f"SELECT {column} FROM {table}",
        ]
        vals = []
        make_where(where, sql, vals)
        return " ".join(sql), tuple(vals)

    class TYPES(object):
        TEXT = "TEXT"
        INTEGER = "INTEGER"
        NUMERIC = "NUMERIC"
        DATETIME_TZ = "TIMESTAMP WITH TIME ZONE"
        TIMESTAMP_TZ = "TIMESTAMP WITH TIME ZONE"
        DATETIME = "TIMESTAMP WITHOUT TIME ZONE"
        TIMESTAMP = "TIMESTAMP WITHOUT TIME ZONE"
        DATE = "DATE"
        TIME_TZ = "TIME WITH TIME ZONE"
        TIME = "TIME WITHOUT TIME ZONE"
        BIGINT = "BIGINT"
        SMALLINT = "SMALLINT"
        BOOLEAN = "BOOLEAN"
        BINARY = "BYTEA"
        INTERVAL = "INTERVAL"
