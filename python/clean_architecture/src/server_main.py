from inventory_server import HomeInventoryServer


def server_main():
    HomeInventoryServer("127.0.0.1", 5500)


if __name__ == "__main__":
    server_main()
