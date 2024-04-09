from typing import List
from urllib.parse import urlencode
from uuid import UUID

from fastapi import Request

from app.schemas.link_schema import Link
from app.schemas.pagination_schema import PaginationLink


def create_user_links(user_id: UUID, request: Request) -> List[Link]:
    """
    Generate navigation links for user actions, ensuring each link includes the 'action' field.

    Parameters:
    - user_id (UUID): The unique identifier of the user.
    - request (Request): The request object.

    Returns:
    - List[Link]: A list of Link objects for navigating user-related actions.
    """
    # Each Link now includes an 'action' field indicating the intended action (view, update, delete)
    return [
        Link(rel="self", href=str(request.url_for("get_user", user_id=str(user_id))), method="GET", action="view"),
        Link(rel="update", href=str(request.url_for("update_user", user_id=str(user_id))), method="PUT", action="update"),
        Link(rel="delete", href=str(request.url_for("delete_user", user_id=str(user_id))), method="DELETE", action="delete"),
    ]



def generate_pagination_links(request: Request, skip: int, limit: int, total_items: int) -> List[PaginationLink]:
    links = []
    total_pages = (total_items + limit - 1) // limit
    base_url = str(request.url)

    # Self link
    links.append(PaginationLink(rel="self", href=f"{base_url}?{urlencode({'skip': skip, 'limit': limit})}"))

    # First page link
    links.append(PaginationLink(rel="first", href=f"{base_url}?{urlencode({'skip': 0, 'limit': limit})}"))

    # Last page link
    last_skip = max(0, (total_pages - 1) * limit)
    links.append(PaginationLink(rel="last", href=f"{base_url}?{urlencode({'skip': last_skip, 'limit': limit})}"))

    # Next page link
    if skip + limit < total_items:
        links.append(PaginationLink(rel="next", href=f"{base_url}?{urlencode({'skip': skip + limit, 'limit': limit})}"))

    # Previous page link
    if skip > 0:
        prev_skip = max(skip - limit, 0)
        links.append(PaginationLink(rel="prev", href=f"{base_url}?{urlencode({'skip': prev_skip, 'limit': limit})}"))

    return links
