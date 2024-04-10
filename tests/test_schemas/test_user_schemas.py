import pytest
from pydantic import ValidationError
from datetime import datetime, timedelta
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest
from app.schemas.link_schema import Link
from app.schemas.pagination_schema import EnhancedPagination, PaginationLink

# Test valid base user creation
def test_user_base_valid():
    valid_data = {"username": "testuser", "email": "test@example.com"}
    user = UserBase(**valid_data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"

# Test username validation
@pytest.mark.parametrize("username", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_username_valid(username):
    user = UserBase(username=username, email="test@example.com")
    assert user.username == username

@pytest.mark.parametrize("username", ["test user", "test?user", "", "us"])
def test_user_base_username_invalid(username):
    with pytest.raises(ValidationError):
        UserBase(username=username, email="test@example.com")

# Test email validation
@pytest.mark.parametrize("email", ["email@example.com", "firstname.lastname@example.com"])
def test_user_base_email_valid(email):
    user = UserBase(username="testuser", email=email)
    assert user.email == email

@pytest.mark.parametrize("email", ["testuser", "testuser@example", "@example.com"])
def test_user_base_email_invalid(email):
    with pytest.raises(ValidationError):
        UserBase(username="testuser", email=email)

# Test password validation for UserCreate
@pytest.mark.parametrize("password", ["ValidPassword123!", "Another$Password1"])
def test_user_create_password_valid(password):
    user = UserCreate(username="testuser", email="test@example.com", password=password)
    assert user.password == password

@pytest.mark.parametrize("password", ["short", "alllowercase", "ALLUPPERCASE", "12345678", "noSpecialChar123"])
def test_user_create_password_invalid(password):
    with pytest.raises(ValidationError):
        UserCreate(username="testuser", email="test@example.com", password=password)

# Test UserUpdate allows partial updates
def test_user_update_partial():
    update_data = {"email": "newemail@example.com"}
    user_update = UserUpdate(**update_data)
    assert user_update.email == "newemail@example.com"

# Test UserResponse datetime fields
def test_user_response_datetime():
    datetime_now = datetime.now()
    user_data = {
        "id": "unique-id-string",
        "username": "testuser",
        "email": "test@example.com",
        "last_login_at": datetime_now,
        "created_at": datetime_now,
        "updated_at": datetime_now,
        "links": []
    }
    user = UserResponse(**user_data)
    assert user.last_login_at == datetime_now
    assert user.created_at == datetime_now
    assert user.updated_at == datetime_now

# Test UserListResponse pagination and items
def test_user_list_response():
    users = [UserResponse(id="id1", username="user1", email="user1@example.com", created_at=datetime.now(), updated_at=datetime.now(), last_login_at=datetime.now(), links=[])]
    pagination = EnhancedPagination(page=1, per_page=1, total_items=1, total_pages=1, links=[])
    user_list_response = UserListResponse(items=users, pagination=pagination)
    assert len(user_list_response.items) == 1
    assert user_list_response.pagination.page == 1

# Test LoginRequest schema
def test_login_request():
    login_data = {"username": "user", "password": "password"}
    login_request = LoginRequest(**login_data)
    assert login_request.username == "user"
    assert login_request.password == "password"

# Add more tests as necessary for comprehensive coverage
