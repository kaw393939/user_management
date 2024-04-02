# Import necessary modules and functions from FastAPI and other standard libraries
from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import List

# Import classes and functions from our application's modules
from app.schema import QRCodeRequest, QRCodeResponse
from app.services.qr_service import generate_qr_code, list_qr_codes, delete_qr_code
from app.utils.common import decode_filename_to_url, encode_url_to_filename, generate_links
from app.config import QR_DIRECTORY, SERVER_BASE_URL, FILL_COLOR, BACK_COLOR, SERVER_DOWNLOAD_FOLDER

import logging

# Create an APIRouter instance to register our endpoints
router = APIRouter()

# Setup OAuth2 with Password (and hashing), using a simple OAuth2PasswordBearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define an endpoint to create QR codes
# It responds to POST requests at "/qr-codes/" and returns data matching the QRCodeResponse model
# This endpoint is tagged as "QR Codes" in the API docs and returns HTTP 201 when a QR code is created successfully
@router.post("/qr-codes/", response_model=QRCodeResponse, status_code=status.HTTP_201_CREATED, tags=["QR Codes"])
async def create_qr_code(request: QRCodeRequest, token: str = Depends(oauth2_scheme)):
    # Log the creation request
    logging.info(f"Creating QR code for URL: {request.url}")
    
    # Encode the URL to a safe filename format
    encoded_url = encode_url_to_filename(request.url)
    qr_filename = f"{encoded_url}.png"
    qr_code_full_path = QR_DIRECTORY / qr_filename

    # Construct the download URL for the QR code
    qr_code_download_url = f"{SERVER_BASE_URL}/{SERVER_DOWNLOAD_FOLDER}/{qr_filename}"
    
    # Generate HATEOAS (Hypermedia As The Engine Of Application State) links for this resource
    links = generate_links("create", qr_filename, SERVER_BASE_URL, qr_code_download_url)

    # Check if the QR code already exists to prevent duplicates
    if qr_code_full_path.exists():
        logging.info("QR code already exists.")
        # If it exists, return a conflict response
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "QR code already exists.", "links": links}
        )

    # Generate the QR code if it does not exist
    generate_qr_code(request.url, qr_code_full_path, FILL_COLOR, BACK_COLOR, request.size)
    # Return a response indicating successful creation
    return QRCodeResponse(message="QR code created successfully.", qr_code_url=qr_code_download_url, links=links)

# Define an endpoint to list all QR codes
# It responds to GET requests at "/qr-codes/" and returns a list of QRCodeResponse objects
@router.get("/qr-codes/", response_model=List[QRCodeResponse], tags=["QR Codes"])
async def list_qr_codes_endpoint(token: str = Depends(oauth2_scheme)):
    logging.info("Listing all QR codes.")
    # Retrieve all QR code files
    qr_files = list_qr_codes(QR_DIRECTORY)
    # Create a response object for each QR code
    responses = [QRCodeResponse(
        message="QR code available",
        qr_code_url=decode_filename_to_url(qr_file[:-4]),  # Decode the filename to the original URL
        links=generate_links("list", qr_file, SERVER_BASE_URL, f"{SERVER_BASE_URL}/{SERVER_DOWNLOAD_FOLDER}/{qr_file}")
    ) for qr_file in qr_files]
    return responses

@router.delete("/qr-codes/{qr_filename}", status_code=status.HTTP_204_NO_CONTENT, tags=["QR Codes"])
async def delete_qr_code_endpoint(qr_filename: str, token: str = Depends(oauth2_scheme)):
    logging.info(f"Deleting QR code: {qr_filename}.")
    qr_code_path = QR_DIRECTORY / qr_filename
    if not qr_code_path.is_file():
        logging.warning(f"QR code not found: {qr_filename}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="QR code not found")

    delete_qr_code(qr_code_path)
    # No need to generate or return any links since the 204 response should not contain a body
    return Response(status_code=status.HTTP_204_NO_CONTENT)