from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse
from app.database import Database
from app.dependencies import get_settings, get_db
from app.routers import oauth, user_routes
import logging

app = FastAPI(
    title="Event Management",
    description="Manage events and authenticate using OAuth.",
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    Database.initialize(settings.database_url, settings.debug)

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})

app.include_router(oauth.router)
app.include_router(user_routes.router)
