#!/bin/bash

# Ensure the QR_DIRECTORY exists
QR_DIRECTORY=${QR_CODE_DIR:-./qr_codes}
mkdir -p "$QR_DIRECTORY"

# Ensure permissions are correct (if running script as root initially)
# chown myuser:myuser "$QR_DIRECTORY"

# Perform database migrations with alembic
alembic upgrade head

# Choose the command below depending on your environment:
# For local development with hot reload:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Uncomment for production:
# gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b :8000 app.main:app
