from datetime import datetime
from zoneinfo import ZoneInfo
import pytest
from pydantic import ValidationError
from app.schemas.pagination_schema import EnhancedPagination, PaginationLink
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, Link

def test_user_base():
    user_data = {
        "username": "johndoe",
        "email": "johndoe@example.com"
    }
    user = UserBase(**user_data)
    assert user.username == "johndoe"
    assert user.email == "johndoe@example.com"

def test_user_create():
    user_data = {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "Password123!",

    }
    user = UserCreate(**user_data)
    assert user.username == "johndoe"
    assert user.email == "johndoe@example.com"
    assert user.password == "Password123!"

def test_user_create_invalid_username():
    user_data = {
        "username": "john doe",
        "email": "johndoe@example.com",
        "password": "Password123!"
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)

def test_user_create_invalid_password():
    user_data = {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "password"
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)

def test_user_update():
    user_data = {
        "email": "johndoe_updated@example.com",
        "full_name": "John Doe Updated"
    }
    user = UserUpdate(**user_data)
    assert user.email == "johndoe_updated@example.com"
    assert user.full_name == "John Doe Updated"

def test_user_response():
    user_data = {
        "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "last_login_at": "2023-06-10T12:00:00Z",
        "created_at": "2023-06-10T12:00:00Z",
        "updated_at": "2023-06-10T12:00:00Z",
        "links": [
            {
                "rel": "self",
                "href": "https://api.example.com/users/a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "method": "GET",
                "action": "view"  # Correctly added the 'action' field
            }
        ]
    }

    user = UserResponse(**user_data)
    # Other assertions remain unchanged

    # Correct the Link creation in the assertion to include the 'action' field
    expected_link = Link(rel="self", href="https://api.example.com/users/a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", method="GET", action="view")
    
    assert str(user.id) == "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    assert user.username == "johndoe"
    assert user.email == "johndoe@example.com"
    assert user.last_login_at == datetime(2023, 6, 10, 12, 0, tzinfo=ZoneInfo("UTC"))
    assert user.created_at == datetime(2023, 6, 10, 12, 0, tzinfo=ZoneInfo("UTC"))
    assert user.updated_at == datetime(2023, 6, 10, 12, 0, tzinfo=ZoneInfo("UTC"))
    assert user.links == [expected_link]

def test_user_list_response():
    user_list_data = {
        "items": [
            {
                "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "last_login_at": "2023-06-10T12:00:00Z",
                "created_at": "2023-06-10T12:00:00Z",
                "updated_at": "2023-06-10T12:00:00Z",
                "links": [
                    {
                        "rel": "self",
                        "href": "https://api.example.com/users/a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                        "method": "GET",
                        "action": "view"
                    }
                ]
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 10,
            "total_items": 50,
            "total_pages": 5,
            "links": [
                {
                    "rel": "next",
                    "href": "https://api.example.com/users?page=2",
                    "method": "GET"
                }
            ]
        }
    }

    # Conversion of dict to objects for the 'pagination' field
    user_list_data["pagination"]["links"] = [PaginationLink(**link) for link in user_list_data["pagination"]["links"]]
    user_list_data["pagination"] = EnhancedPagination(**user_list_data["pagination"])

    user_list = UserListResponse(**user_list_data)

    # Assertions for pagination
    assert user_list.pagination.page == 1
    assert user_list.pagination.per_page == 10
    assert user_list.pagination.total_items == 50
    assert user_list.pagination.total_pages == 5
    assert len(user_list.pagination.links) == 1
    assert user_list.pagination.links[0].rel == "next"
    assert str(user_list.pagination.links[0].href) == "https://api.example.com/users?page=2"
    assert user_list.pagination.links[0].method == "GET"

    # Assertions for items
    assert len(user_list.items) == 1
    assert user_list.items[0].username == "johndoe"
    assert user_list.items[0].email == "johndoe@example.com"
