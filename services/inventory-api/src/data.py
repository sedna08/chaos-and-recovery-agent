# Static in-memory dictionary acting as our data store
_INVENTORY_DATA = {"item": "shoes", "qty": 42}


def get_inventory() -> dict:
    """
    Fetches the static inventory data.
    Separating this from the router allows future database integrations
    without altering the API controller logic.
    """
    return _INVENTORY_DATA
