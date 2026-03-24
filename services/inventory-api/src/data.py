# Static in-memory dictionary acting as our data store
_INVENTORY_DATA = [
    {
        "id": "1",
        "name": "Mechanical Keyboard",
        "stock": 42,
        "price": 150.00
    },
    {
        "id": "2",
        "name": "Wireless Mouse",
        "stock": 8,
        "price": 45.50
    },
    {
        "id": "3",
        "name": "USB-C Hub",
        "stock": 115,
        "price": 29.99
    }
]


def get_inventory() -> dict:
    """
    Fetches the static inventory data.
    Separating this from the router allows future database integrations
    without altering the API controller logic.
    """
    return _INVENTORY_DATA
