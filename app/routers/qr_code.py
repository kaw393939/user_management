from fastapi import APIRouter, HTTPException
from app.models import QRCodeRequest
from app.services.qr_service import generate_qr_code
from app.utils.common import create_directory, QR_DIRECTORY, SERVER_BASE_URL
from datetime import datetime
import os

router = APIRouter()

# Assuming logging is set up at application startup level
# No need to call setup_logging() here

@router.post("/generate_qr/")
async def generate_qr(request: QRCodeRequest):
    create_directory(QR_DIRECTORY)  # Ensure QR directory exists
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f"QRCode_{timestamp}.png"
    qr_code_full_path = QR_DIRECTORY / qr_filename

    try:
        # Generate the QR code and save it to the specified path
        generate_qr_code(request.url, qr_code_full_path, request.fill_color, request.back_color, request.size)
        # Construct the URL to access the QR code via the web server
        qr_code_url = os.path.join(SERVER_BASE_URL, 'qr_codes', qr_filename)
        return {"message": "QR code generated successfully", "qr_code_url": qr_code_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
