import unittest
from velocity.db.servers import postgres

test_db = "test_foreign_key_db"
engine = postgres.initialize(database=test_db)


@engine.transaction
class TestForeignKeyHandling(unittest.TestCase):
    @classmethod
    @engine.transaction
    def setUpClass(cls, tx):
        # Drop and recreate the test database
        tx.switch_to_database("postgres")
        tx.execute(f"drop database if exists {test_db}", single=True)
        tx.execute(f"create database {test_db}", single=True)
        tx.switch_to_database(test_db)

        # Create parent_table
        parent_table = tx.table("parent_table")
        parent_table.create(
            columns={
                "name": str,
            }
        )

        # Create middle_table with a foreign key to parent_table
        middle_table = tx.table("middle_table")
        middle_table.create(
            columns={
                "parent_id": int,
                "title": str,
            }
        )
        middle_table.create_foreign_key("parent_id", "parent_table", "sys_id")

        # Create child_table with foreign keys to both parent_table and middle_table
        child_table = tx.table("child_table")
        child_table.create(
            columns={
                "parent_id": int,
                "middle_id": int,
            }
        )
        child_table.create_foreign_key("parent_id", "parent_table", "sys_id")
        child_table.create_foreign_key("middle_id", "middle_table", "sys_id")

    @classmethod
    @engine.transaction
    def tearDownClass(cls, tx):
        # Drop the test database
        # tx.switch_to_database("postgres")
        # tx.execute(f"drop database if exists {test_db}", single=True)
        pass

    def test_foreign_key_with_specified_sys_id(self, tx):
        # Insert data into parent_table with specified sys_id
        parent_table = tx.table("parent_table")
        parent_table.insert({"sys_id": 100, "name": "Parent 1"})
        parent_table.insert({"sys_id": 200, "name": "Parent 2"})

        # Insert data into middle_table with specified sys_id
        middle_table = tx.table("middle_table")
        middle_table.insert({"sys_id": 300, "parent_id": 100, "title": "Title 1"})
        middle_table.insert({"sys_id": 400, "parent_id": 200, "title": "Title 2"})

        # Insert data into child_table with specified sys_id
        child_table = tx.table("child_table")
        child_table.insert(
            {
                "sys_id": 500,
                "parent_id": 100,
                "middle_id": 300,
                "description": "Child A",
            }
        )
        child_table.insert(
            {
                "sys_id": 600,
                "parent_id": 200,
                "middle_id": 400,
                "description": "Child B",
            }
        )

        # Query selecting columns with three foreign key references
        result = list(
            child_table.select(
                columns=[
                    "parent_id>name",
                    "middle_id>title",
                    "sys_id",
                    "description",
                ]
            )
        )
        expected_result = [
            {
                "parent_id_name": "Parent 1",
                "middle_id_title": "Title 1",
                "sys_id": 500,
                "description": "Child A",
            },
            {
                "parent_id_name": "Parent 2",
                "middle_id_title": "Title 2",
                "sys_id": 600,
                "description": "Child B",
            },
        ]
        self.assertEqual(result, expected_result)

    def test_foreign_key_conditions_with_specified_sys_id(self, tx):
        # Query with conditions on foreign key references
        child_table = tx.table("child_table")
        result = list(
            child_table.select(
                columns=[
                    "parent_id>name",
                    "middle_id>title",
                    "sys_id",
                    "description",
                ],
                where={"parent_id>name": "Parent 1", "middle_id>title": "Title 1"},
            )
        )
        expected_result = [
            {
                "parent_id_name": "Parent 1",
                "middle_id_title": "Title 1",
                "sys_id": 500,
                "description": "Child A",
            }
        ]
        self.assertEqual(result, expected_result)

    def test_foreign_key_ordering_with_specified_sys_id(self, tx):
        # Query with ordering based on foreign key references
        child_table = tx.table("child_table")
        result = list(
            child_table.select(
                columns=[
                    "parent_id>name",
                    "middle_id>title",
                    "sys_id",
                    "description",
                ],
                orderby="parent_id>name DESC, middle_id>title ASC",
            )
        )
        expected_result = [
            {
                "parent_id_name": "Parent 2",
                "middle_id_title": "Title 2",
                "sys_id": 600,
                "description": "Child B",
            },
            {
                "parent_id_name": "Parent 1",
                "middle_id_title": "Title 1",
                "sys_id": 500,
                "description": "Child A",
            },
        ]
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
