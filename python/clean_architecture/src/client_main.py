"""Explicit main execution module."""

from inventory_client import HomeInventoryClient

# from datetime import date


def main():
    """Execute main program."""
    app = HomeInventoryClient("127.0.0.1", 5500)
    app.start_application()


# Call main() if this is the main execution module
if __name__ == "__main__":
    main()
