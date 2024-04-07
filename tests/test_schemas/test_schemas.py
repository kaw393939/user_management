import pytest
from pydantic import ValidationError
from app.schemas.schemas import QRCodeRequest

def test_qr_code_request_valid():
    """Test that a valid QRCodeRequest is accepted."""
    data = {
        "url": "https://example.com",
        "fill_color": "black",
        "back_color": "yellow",
        "size": 20
    }
    request = QRCodeRequest(**data)
    assert str(request.url) == data["url"] + "/"  # Adjusting for automatic normalization
    assert request.fill_color == data["fill_color"]
    assert request.back_color == data["back_color"]
    assert request.size == data["size"]
    
def test_qr_code_request_invalid_url():
    """Test that an invalid URL is rejected."""
    data = {
        "url": "not_a_valid_url",
        "fill_color": "black",
        "back_color": "yellow",
        "size": 20
    }
    with pytest.raises(ValidationError):
        QRCodeRequest(**data)

def test_qr_code_request_invalid_size():
    """Test that an invalid size is rejected."""
    data = {
        "url": "https://example.com",
        "fill_color": "black",
        "back_color": "yellow",
        "size": 0  # Invalid size, should be >= 1
    }
    with pytest.raises(ValidationError):
        QRCodeRequest(**data)

def test_qr_code_request_defaults():
    """Test that default values are correctly applied."""
    data = {"url": "https://example.com"}
    request = QRCodeRequest(**data)
    assert request.fill_color == "red"  # Default fill_color
    assert request.back_color == "white"  # Default back_color
    assert request.size == 10  # Default size
