from builtins import len, max, sorted, str
from unittest.mock import MagicMock
from urllib.parse import parse_qs, urlparse, parse_qsl, urlunparse, urlencode
from uuid import uuid4

import pytest
from fastapi import Request

from app.utils.link_generation import create_link, create_pagination_link, create_user_links, generate_pagination_links

from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

def normalize_url(url):
    """Normalize the URL for consistent comparison by sorting query parameters."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query, keep_blank_values=True)
    # Sort the query parameters by key, and sort their values if there are multiple for a single key
    sorted_query_items = sorted((k, sorted(v)) for k, v in query_params.items())
    # Convert the sorted query parameters back to a query string
    encoded_query = urlencode(sorted_query_items, doseq=True)
    normalized_url = urlunparse(parsed_url._replace(query=encoded_query))
    return normalized_url.rstrip('/')


@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.url_for = MagicMock(side_effect=lambda action, user_id: f"http://testserver/{action}/{user_id}")
    request.url = "http://testserver/users"
    return request

def test_create_link():
    link = create_link("self", "http://example.com", "GET", "view")
    assert normalize_url(str(link.href)) == "http://example.com"

def test_create_user_links(mock_request):
    user_id = uuid4()
    links = create_user_links(user_id, mock_request)
    assert len(links) == 3
    assert normalize_url(str(links[0].href)) == f"http://testserver/get_user/{user_id}"
    assert normalize_url(str(links[1].href)) == f"http://testserver/update_user/{user_id}"
    assert normalize_url(str(links[2].href)) == f"http://testserver/delete_user/{user_id}"

def test_generate_pagination_links(mock_request):
    skip = 10
    limit = 5
    total_items = 50
    links = generate_pagination_links(mock_request, skip, limit, total_items)
    assert len(links) >= 4
    expected_self_url = "http://testserver/users?limit=5&skip=10"
    assert normalize_url(str(links[0].href)) == normalize_url(expected_self_url), "Self link should match expected URL"
