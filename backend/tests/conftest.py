#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Pytest configuration and fixtures for ShExStatements API tests."""

import pytest
from httpx import AsyncClient, ASGITransport

from api.main import app


@pytest.fixture
def sample_shexstatements():
    """Sample ShExStatements input for testing."""
    return """foaf|<http://xmlns.com/foaf/0.1/>|||
xsd|<http://www.w3.org/2001/XMLSchema#>|||
@person|rdf:type|foaf:Person||
@person|foaf:name|xsd:string|+|Name is required
@person|foaf:mbox|IRI|*|Email addresses"""


@pytest.fixture
def sample_csv_content():
    """Sample CSV content with comma delimiter."""
    return """foaf,<http://xmlns.com/foaf/0.1/>,,,
@person,rdf:type,foaf:Person,,
@person,foaf:name,Literal,+,name is required"""


@pytest.fixture
def expected_shex_output():
    """Expected ShEx output pattern."""
    return "start = @<person>"


@pytest.fixture
async def async_client():
    """Async HTTP client for API testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def invalid_shexstatements():
    """Invalid ShExStatements for error testing."""
    return "@invalid|||missing|fields|too|many"
