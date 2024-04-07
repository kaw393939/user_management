from typing import List
from uuid import UUID

from fastapi import Request

from app.schemas.link_schema import Link


def create_user_links(user_id: UUID, request: Request) -> List[Link]:
    """
    Generate navigation links for user actions.

    Parameters:
    - user_id (UUID): The unique identifier of the user.
    - request (Request): The request object.

    Returns:
    - List[Link]: A list of Link objects for navigating user-related actions.
    """
    return [
        Link(rel="self", href=str(request.url_for("get_user", user_id=str(user_id))), method="GET"),
        Link(rel="update", href=str(request.url_for("update_user", user_id=str(user_id))), method="PUT"),
        Link(rel="delete", href=str(request.url_for("delete_user", user_id=str(user_id))), method="DELETE"),
    ]