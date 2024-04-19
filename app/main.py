from builtins import Exception
from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse
from app.database import Database
from app.dependencies import get_settings
from app.routers import oauth, user_routes
from app.utils.common import setup_logging
import logging

# This function sets up logging based on the configuration specified in your logging configuration file.
setup_logging()

# Create an instance of the FastAPI application.
app = FastAPI(
    title="Event Management",
    description="A FastAPI application for creating, listing available codes, and deleting QR codes. "
                "It also supports OAuth for secure access.",
    version="0.0.1",
    redoc_url=None,
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()  # This could also be injected if settings are used elsewhere
    try:
        await Database.initialize_async_db(settings.database_url, settings.debug)
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")
        raise e  # Optionally, raise an exception to fail the startup if critical

# Exception handlers can be defined globally if needed
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred during processing."},
    )

# Include the routers for your application.
app.include_router(oauth.router)  # OAuth authentication routes
app.include_router(user_routes.router)  # User management routes

# Future enhancements or extensions can be commented here or noted in documentation
# Example: app.include_router(events.router)  # Event management routes
