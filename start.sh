#!/bin/bash

# Adjust permissions for the qr_codes directory
# chmod 777 /app/qr_codes

# Start the FastAPI application for local
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# start for production
# gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b :8000 app.main:app
