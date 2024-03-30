from fastapi import FastAPI
from app.routers import qr_code

app = FastAPI()

app.include_router(qr_code.router)
