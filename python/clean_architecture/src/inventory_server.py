"""Implements inventory application presentation layer (U/I) features in a server with sockets."""

from business_logic import BusinessLogic
import json
import socket
import threading
from datetime import datetime
import os
import sys


class HomeInventoryServer:
    """Implements server functionality of home inventory."""

    def __init__(self, ip, port):
        """Initialize object."""
        self.ip = ip
        self.port = port
        self.business_logic = BusinessLogic()
        self._listen()
        self._accept_connection()

    def _listen(self):
        """Creates a server socket and starts listening on assigned
        IP Address and Port.
        """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if os.name == "nt":
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            else:
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.server.bind((self.ip, self.port))
            print(f"Listening on IP Address: {self.ip} and Port: {self.port} ")
            self.server.listen(4)
        except Exception as e:
            print(f"Problem listening for incoming connection: {e}")
            self.server.close()
            sys.exit(0)

    # Accept incoming connection
    def _accept_connection(self):
        """Accepts incoming client connections and hands off request processing
        to new thread.
        """
        try:
            with self.server:
                while True:
                    print(f"Waiting for incoming client connection...")
                    client, address = self.server.accept()
                    print(
                        f"Accepted client connection from IP Address: {address[0]} and {address[1]}"
                    )
                    client_handler = threading.Thread(
                        target=self._process_client_requests, args=(client, self.server)
                    )
                    client_handler.start()
        except Exception as e:
            print(f"Problem accepting connection: {e}")

    # Process connection in separate thread
    def _process_client_requests(self, client, server):
        """Processes communication between client and server."""
        try:
            with client:
                while True:
                    request = client.recv(1024)
                    if not request:
                        break
                    message = request.decode("utf-8")
                    msg_json = json.loads(message)
                    response = {
                        "requested_func": msg_json["requested_func"],
                        "result": "",
                        "success": False,
                    }
                    options = msg_json["options"]
                    match (msg_json["requested_func"]):
                        case "new_inventory":
                            date = (
                                datetime.isoformat(datetime.now())
                                .replace("T", " ")
                                .split(".")[0]
                            )
                            response["result"] = (
                                self.business_logic.create_new_inventory(
                                    options["inventory_name"],
                                    options["inventory_description"],
                                    date,
                                )
                            )
                            response["success"] = True
                        case "list_inventory":
                            response["result"] = (
                                self.business_logic.get_all_inventories_with_format(
                                    "json"
                                )
                            )
                            response["success"] = True
                        case "list_inventory_items":
                            response["result"] = (
                                self.business_logic.get_items_for_inventory_id_with_format(
                                    options["inventory_id"], "json"
                                )
                            )
                            response["success"] = True
                        case "add_inventory_items":
                            response["result"] = (
                                self.business_logic.create_new_inventory_item(
                                    options["inventory_id"],
                                    options["item_name"],
                                    options["item_count"],
                                )
                            )
                            response["success"] = True

                    client.send(bytearray(json.dumps(response), "utf-8"))

        except Exception as e:
            print(f"Problem processing client requests: {e}")
