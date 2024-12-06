import unittest
import datetime
import decimal
from velocity.db.servers.postgres import (
    make_where,
    quote,
    SQL,
)  # Replace 'your_module' with the actual module name
from velocity.db.core.table import (
    Query,
)  # Adjust the import path according to your project structure


class TestSQLModule(unittest.TestCase):
    # Existing tests (as previously provided)
    # ...

    # New tests for complicated SQL edge cases

    def test_make_where_with_nested_subquery(self):
        sql = []
        vals = []
        subquery = Query("SELECT id FROM other_table WHERE value = %s", ("test",))
        make_where({"id": subquery}, sql, vals)
        self.assertEqual(
            " ".join(sql), "WHERE id in (SELECT id FROM other_table WHERE value = %s)"
        )
        self.assertEqual(vals, ("test",))

    def test_make_where_with_multiple_conditions(self):
        sql = []
        vals = []
        where_conditions = [
            ("column1>", 5),
            ("column2<=", 10),
            ("column3%", "%value%"),
            ("column4!%", "%exclude%"),
        ]
        make_where(where_conditions, sql, vals)
        expected_sql = "WHERE column1 > %s AND column2 <= %s AND column3 ilike %s AND column4 not like %s"
        self.assertEqual(" ".join(sql), expected_sql)
        self.assertEqual(vals, [5, 10, "%value%", "%exclude%"])

    def test_make_where_with_complex_operators(self):
        sql = []
        vals = []
        make_where({"column1~": "^test.*", "column2!~*": ".*exclude$"}, sql, vals)
        self.assertEqual(" ".join(sql), "WHERE column1 ~ %s AND column2 !~* %s")
        self.assertEqual(vals, ["^test.*", ".*exclude$"])

    def test_sql_select_with_complex_join(self):
        sql_query, params = SQL.select(
            columns=["A.id", "B.name", "C.value"],
            table="tableA A",
            inner_join={"tableB B": "A.b_id = B.id", "tableC C": "B.c_id = C.id"},
            where={"A.status": "active", "C.value>": 100},
            orderby="C.value DESC",
        )
        expected_sql = (
            "SELECT A.id,B.name,C.value FROM tableA A "
            "INNER JOIN tableB B ON A.b_id = B.id "
            "INNER JOIN tableC C ON B.c_id = C.id "
            "WHERE A.status = %s AND C.value > %s ORDER BY C.value DESC"
        )
        self.assertEqual(sql_query, expected_sql)
        self.assertEqual(params, ("active", 100))

    def test_sql_select_with_group_by_and_having(self):
        sql_query, params = SQL.select(
            columns="column1, COUNT(*)",
            table="my_table",
            groupby="column1",
            having="COUNT(*) > 1",
            orderby="column1 ASC",
        )
        expected_sql = "SELECT column1, COUNT(*) FROM my_table GROUP BY column1 HAVING COUNT(*) > 1 ORDER BY column1 ASC"
        self.assertEqual(sql_query, expected_sql)
        self.assertEqual(params, ())

    def test_sql_insert_with_special_types(self):
        sql_query, params = SQL.insert(
            table="my_table",
            data={
                "int_column": 123,
                "decimal_column": decimal.Decimal("123.456"),
                "datetime_column": datetime.datetime(2023, 1, 1, 12, 0),
                "bool_column": True,
                "text_column": "Some text",
            },
        )
        self.assertIn("INSERT INTO my_table", sql_query)
        self.assertEqual(len(params), 5)
        self.assertIsInstance(params[1], decimal.Decimal)
        self.assertIsInstance(params[2], datetime.datetime)
        self.assertIsInstance(params[3], bool)

    def test_sql_update_with_excluded(self):
        sql_query, params = SQL.update(
            table="my_table",
            data={"column1": "value1", "column2": "value2"},
            pk={"id": 1},
            excluded=True,
        )
        expected_sql = (
            "UPDATE SET column1 = EXCLUDED.column1,column2 = EXCLUDED.column2"
        )
        self.assertEqual(sql_query, expected_sql)
        self.assertEqual(params, ())

    def test_sql_create_table_with_constraints(self):
        sql_query, params = SQL.create_table(
            name="public.test_table",
            columns={
                "id": "@@SERIAL PRIMARY KEY",
                "name": str,
                "age": int,
                "email": "@@VARCHAR(255) UNIQUE",
                "created_at": "@@TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            },
            drop=True,
        )
        self.assertIn("CREATE TABLE public.test_table", sql_query)
        self.assertIn("id SERIAL PRIMARY KEY", sql_query)
        self.assertIn("email VARCHAR(255) UNIQUE", sql_query)
        self.assertIn("created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP", sql_query)
        self.assertEqual(params, ())

    def test_sql_create_foreign_key_with_schema(self):
        sql_query, params = SQL.create_foreign_key(
            table="schema.child_table",
            columns="parent_id",
            key_to_table="schema.parent_table",
            key_to_columns="id",
            schema="schema",
        )
        self.assertIn("ALTER TABLE schema.child_table ADD CONSTRAINT", sql_query)
        self.assertIn("REFERENCES schema.parent_table (id);", sql_query)
        self.assertEqual(params, ())

    def test_sql_merge_with_complex_conflict_resolution(self):
        sql_query, params = SQL.merge(
            table="my_table",
            data={"column1": "value1", "column2": "value2"},
            pk={"id": 1},
            on_conflict_do_nothing=False,
            on_conflict_update=True,
        )
        self.assertIn("ON CONFLICT (id) DO UPDATE SET", sql_query)
        self.assertIn("column1 = EXCLUDED.column1", sql_query)
        self.assertEqual(params, ("value1", "value2"))

    def test_sql_select_with_subquery_in_columns(self):
        sql_query, params = SQL.select(
            columns="id, (SELECT COUNT(*) FROM orders WHERE user_id = users.id) as order_count",
            table="users",
            where={"status": "active"},
        )
        expected_sql = (
            "SELECT id, (SELECT COUNT(*) FROM orders WHERE user_id = users.id) as order_count "
            "FROM users WHERE status = %s"
        )
        self.assertEqual(sql_query, expected_sql)
        self.assertEqual(params, ("active",))

    def test_make_where_with_special_characters_in_values(self):
        sql = []
        vals = []
        make_where({"text_column": "O'Reilly"}, sql, vals)
        self.assertEqual(" ".join(sql), "WHERE text_column = %s")
        self.assertEqual(vals, ["O'Reilly"])

    def test_sql_update_with_complex_where(self):
        sql_query, params = SQL.update(
            table="my_table",
            data={"status": "inactive"},
            pk={"last_login<": datetime.datetime.now(), "status": "active"},
        )
        expected_sql = (
            "UPDATE my_table SET status = %s WHERE last_login < %s AND status = %s"
        )
        self.assertEqual(sql_query, expected_sql)
        self.assertEqual(len(params), 3)
        self.assertEqual(params[0], "inactive")

    def test_sql_delete_with_subquery(self):
        subquery = Query("SELECT id FROM inactive_users", ())
        sql_query, params = SQL.delete(table="users", where={"id": subquery})
        expected_sql = "DELETE FROM users WHERE id in (SELECT id FROM inactive_users)"
        self.assertEqual(sql_query, expected_sql)
        self.assertEqual(params, ())

    def test_sql_select_with_offset_and_limit(self):
        sql_query, params = SQL.select(columns="*", table="my_table", start=10, qty=20)
        expected_sql = "SELECT * FROM my_table OFFSET 10 ROWS FETCH NEXT 20 ROWS ONLY"
        self.assertEqual(sql_query, expected_sql)
        self.assertEqual(params, ())

    def test_sql_create_index_with_trigram(self):
        sql_query, params = SQL.create_index(
            table="my_table", columns="text_column", trigram="GIN"
        )
        self.assertIn("USING GIN", sql_query)
        self.assertIn("(text_column) gin_trgm_ops", sql_query)
        self.assertEqual(params, ())

    def test_sql_alter_table_add_column(self):
        sql_query, params = SQL.alter_add(
            table="my_table", columns={"new_column": str}, null_allowed=False
        )
        expected_sql = "ALTER TABLE my_table ADD new_column TEXT NOT NULL;"
        self.assertEqual(sql_query.strip(), expected_sql.strip())
        self.assertEqual(params, ())

    def test_sql_alter_table_drop_column(self):
        sql_query, params = SQL.alter_drop(
            table="my_table", columns={"old_column": None}
        )
        expected_sql = "ALTER TABLE my_table DROP COLUMN old_column"
        self.assertIn(expected_sql, sql_query)
        self.assertEqual(params, ())

    def test_sql_alter_column_type(self):
        sql_query, params = SQL.alter_column_by_type(
            table="my_table",
            column="int_column",
            value=decimal.Decimal("0.0"),
            nullable=False,
        )
        expected_sql = (
            "ALTER TABLE my_table ALTER COLUMN int_column TYPE NUMERIC(19, 6) "
            "USING int_column::NUMERIC NOT NULL"
        )
        self.assertEqual(sql_query.strip(), expected_sql.strip())
        self.assertEqual(params, ())

    def test_sql_alter_column_with_sql(self):
        sql_query, params = SQL.alter_column_by_sql(
            table="my_table", column="text_column", value="SET DEFAULT %s"
        )
        expected_sql = "ALTER TABLE my_table ALTER COLUMN text_column SET DEFAULT %s"
        self.assertEqual(sql_query, expected_sql)
        self.assertEqual(params, ())

    def test_sql_duplicate_rows_detection(self):
        sql_query, params = SQL.duplicate_rows(
            table="my_table", columns=["column1", "column2"], where={"status": "active"}
        )
        expected_sql = (
            "SELECT column1,column2 FROM my_table WHERE status = %s "
            "GROUP BY column1,column2 HAVING count(*) > 2"
        )
        self.assertEqual(sql_query, expected_sql)
        self.assertEqual(params, ("active",))

    def test_sql_missing_ids(self):
        sql_query, params = SQL.missing(
            table="my_table",
            list=[1, 2, 3, 4, 5],
            column="id",
            where={"status": "active"},
        )
        expected_sql = (
            "SELECT * FROM UNNEST('{1,2,3,4,5}'::int[]) id EXCEPT ALL "
            "SELECT id FROM my_table WHERE status = %s"
        )
        self.assertEqual(sql_query, expected_sql)
        self.assertEqual(params, ("active",))

    # Additional edge cases can be added here


if __name__ == "__main__":
    unittest.main()
