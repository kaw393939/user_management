from builtins import dict, int, max, str
from typing import List, Callable
from urllib.parse import urlencode
from uuid import UUID

from fastapi import Request
from app.schemas.link_schema import Link
from app.schemas.pagination_schema import PaginationLink

# Utility function to create a link
def create_link(rel: str, href: str, method: str = "GET", action: str = None) -> Link:
    return Link(rel=rel, href=href, method=method, action=action)

def create_pagination_link(rel: str, base_url: str, params: dict) -> PaginationLink:
    # Ensure parameters are added in a specific order
    query_string = f"skip={params['skip']}&limit={params['limit']}"
    return PaginationLink(rel=rel, href=f"{base_url}?{query_string}")

def create_user_links(user_id: UUID, request: Request) -> List[Link]:
    """
    Generate navigation links for user actions.
    """
    actions = [
        ("self", "get_user", "GET", "view"),
        ("update", "update_user", "PUT", "update"),
        ("delete", "delete_user", "DELETE", "delete")
    ]
    return [
        create_link(rel, str(request.url_for(action, user_id=str(user_id))), method, action_desc)
        for rel, action, method, action_desc in actions
    ]

def generate_pagination_links(request: Request, skip: int, limit: int, total_items: int) -> List[PaginationLink]:
    base_url = str(request.url)
    total_pages = (total_items + limit - 1) // limit
    links = [
        create_pagination_link("self", base_url, {'skip': skip, 'limit': limit}),
        create_pagination_link("first", base_url, {'skip': 0, 'limit': limit}),
        create_pagination_link("last", base_url, {'skip': max(0, (total_pages - 1) * limit), 'limit': limit})
    ]

    if skip + limit < total_items:
        links.append(create_pagination_link("next", base_url, {'skip': skip + limit, 'limit': limit}))

    if skip > 0:
        links.append(create_pagination_link("prev", base_url, {'skip': max(skip - limit, 0), 'limit': limit}))

    return links
