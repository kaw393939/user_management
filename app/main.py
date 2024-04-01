from fastapi import FastAPI
from app.config import QR_DIRECTORY
from app.routers import qr_code, oauth  # Make sure these imports match your project structure.
from app.services.qr_service import create_directory
from app.utils.common import setup_logging

# This function sets up logging based on the configuration specified in your logging configuration file.
# It's important for monitoring and debugging.
setup_logging()

# This ensures that the directory for storing QR codes exists when the application starts.
# If it doesn't exist, it will be created.
create_directory(QR_DIRECTORY)

# This creates an instance of the FastAPI application.
app = FastAPI(
    title="QR Code Manager",
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

# Here, we include the routers for our application. Routers define the paths and operations your API provides.
# We have two routers in this case: one for managing QR codes and another for handling OAuth authentication.
app.include_router(qr_code.router)  # QR code management routes
app.include_router(oauth.router)  # OAuth authentication routes
