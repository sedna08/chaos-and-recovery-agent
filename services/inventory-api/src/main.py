import logging
from fastapi import FastAPI, APIRouter, HTTPException

from src.data import get_inventory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s - %(extra_info)s",
)
logger = logging.getLogger("inventory-api")


def log_info(context: dict, msg: str):
    logger.info(msg, extra={"extra_info": context})


def log_error(context: dict, msg: str):
    logger.error(msg, extra={"extra_info": context})


app = FastAPI(title="Inventory API", version="1.0.0")
router = APIRouter()


@router.get("/health")
async def health_check():
    """Kubernetes liveness/readiness probe target."""
    log_info({"endpoint": "/health"}, "Health check requested")
    return {"status": "healthy"}


@router.get("/api/stock")
async def get_stock():
    """Retrieves current inventory levels."""
    log_info({"endpoint": "/api/stock"}, "Stock inventory requested")
    try:
        data = get_inventory()
        # Updated: Log the count of items rather than dictionary keys
        log_info(
            {"items_count": len(data)},
            "Successfully fetched inventory",
        )
        return data
    except Exception as e:
        log_error({"error": str(e)}, "Failed to fetch inventory")
        raise HTTPException(
            status_code=500, detail="Internal server error fetching inventory"
        )


app.include_router(router)