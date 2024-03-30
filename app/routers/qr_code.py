from fastapi import APIRouter, HTTPException
from app.models import QRCodeRequest
from app.services.qr_service import generate_qr_code
from app.utils.common import create_directory, QR_DIRECTORY, setup_logging
from datetime import datetime

router = APIRouter()

@router.post("/generate_qr/")
async def generate_qr(request: QRCodeRequest):
    setup_logging()  # Initialize logging
    create_directory()  # Ensure QR directory exists
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f"QRCode_{timestamp}.png"
    qr_code_full_path = QR_DIRECTORY / qr_filename

    try:
        generate_qr_code(request.url, qr_code_full_path, request.fill_color, request.back_color, request.size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    return {"message": "QR code generated successfully", "path": str(qr_code_full_path)}
