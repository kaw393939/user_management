#!/bin/bash

# Adjust permissions for the qr_codes directory
chmod 777 /app/qr_codes

# Start the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 8000