"""Implements application business logic."""

# from persistence_wrapper_interface import PersistenceWrapperInterface
from mysql_persistence_wrapper import MySQLPersistenceWrapper
import json


class BusinessLogic:
    """Implements application business logic."""

    def __init__(self):
        """Initialize object."""
        self._persistence_wrapper = MySQLPersistenceWrapper()

    def get_all_inventories(self):
        """Returns a list of inventories."""
        query_results = None
        try:
            query_results = self._persistence_wrapper.get_all_inventories()
        except Exception as e:
            print(f"Exception in business logic: {e}")
        return query_results

    def get_all_inventories_with_format(self, format: str):
        """Returns all inventories in requested format.
        Only supported format is JSON. Add others as required.
        """
        query_results = []
        try:
            query_results = self._persistence_wrapper.get_all_inventories()
        except Exception as e:
            print(f"Exception in business logic: {e}")

        return_results = None
        try:
            match format:
                case "json":
                    res = []
                    for query in query_results:
                        res.append(
                            {"id": query[0], "name": query[1], "description": query[2]}
                        )
                    return res
        except Exception as e:
            print(f"Exception in business logic: {e}")
        return return_results

    def create_new_inventory(self, name: str, description: str, date: str):
        """Adds a new inventory to the datastore."""
        inventory_id = 0
        try:
            inventory_id = self._persistence_wrapper.create_inventory(
                name, description, date
            )
        except Exception as e:
            print(f"Exception in business logic: {e}")
        return inventory_id

    def create_new_inventory_item(self, id, name, count):
        return self._persistence_wrapper.create_item(id, name, count)

    def get_items_for_inventory_id(self, id):
        """Gets all items for given inventory id."""
        query_results = None
        try:
            query_results = self._persistence_wrapper.get_items_for_inventory(id)
        except Exception as e:
            print(f"Exception in business logic: {e}")
        return query_results

    def get_items_for_inventory_id_with_format(self, id, format: str):
        query_results = []
        try:
            query_results = self._persistence_wrapper.get_items_for_inventory(id)
        except Exception as e:
            print(f"Exception in business logic: {e}")

        match format:
            case "json":
                res = []
                for query in query_results:
                    res.append(
                        {
                            "id": query[0],
                            "inventory_id": query[1],
                            "name": query[2],
                            "count": query[3],
                        }
                    )
                return res
