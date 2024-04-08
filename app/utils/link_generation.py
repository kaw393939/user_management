from typing import List
from uuid import UUID

from fastapi import Request

from app.schemas.link_schema import Link


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