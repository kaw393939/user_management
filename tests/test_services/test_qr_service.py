import pytest
from pathlib import Path
import tempfile
from app.services.qr_service import list_qr_codes, generate_qr_code, delete_qr_code, create_directory

@pytest.fixture
def qr_directory():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)

def test_list_qr_codes_empty(qr_directory):
    qr_files = list_qr_codes(qr_directory)
    assert qr_files == [], "Should return an empty list for an empty directory"

def test_list_qr_codes_non_empty(qr_directory):
    # Create a dummy QR code file
    (qr_directory / "test_qr.png").write_bytes(b"")
    qr_files = list_qr_codes(qr_directory)
    assert qr_files == ["test_qr.png"], "Should list existing QR codes"

def test_generate_qr_code_success(qr_directory):
    qr_path = qr_directory / "qr.png"
    generate_qr_code("https://example.com", qr_path)
    assert qr_path.is_file(), "QR code should be generated and saved"

def test_delete_qr_code_success(qr_directory):
    qr_path = qr_directory / "qr.png"
    qr_path.write_bytes(b"")  # Simulate an existing file
    delete_qr_code(qr_path)
    assert not qr_path.is_file(), "QR code should be deleted"

def test_delete_qr_code_not_found(qr_directory):
    qr_path = qr_directory / "nonexistent.png"
    with pytest.raises(FileNotFoundError):
        delete_qr_code(qr_path)

def test_create_directory_already_exists(qr_directory):
    # Directory already exists because of the fixture
    create_directory(qr_directory)
    assert qr_directory.is_dir(), "Should confirm the directory exists without error"

def test_create_directory_new(qr_directory):
    new_dir = qr_directory / "newdir"
    create_directory(new_dir)
    assert new_dir.is_dir(), "Should create a new directory successfully"
