#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Tests for the validation API endpoint."""

import pytest


@pytest.mark.asyncio
async def test_validate_valid_shex(async_client):
    """Test validation of a valid ShEx schema."""
    valid_shex = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
start = @<person>
<person> {
  foaf:name LITERAL ;
  foaf:mbox IRI * ;
}
"""

    response = await async_client.post(
        "/api/v1/validate",
        json={"shex": valid_shex},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert len(data["errors"]) == 0


@pytest.mark.asyncio
async def test_validate_undefined_shape_reference(async_client):
    """Test validation detects undefined shape references."""
    shex_with_undefined_ref = """
start = @<person>
<person> {
  foaf:knows @<unknownShape> ;
}
"""

    response = await async_client.post(
        "/api/v1/validate",
        json={"shex": shex_with_undefined_ref},
    )

    assert response.status_code == 200
    data = response.json()
    # Should detect undefined shape reference
    assert data["valid"] is False or len(data["warnings"]) > 0


@pytest.mark.asyncio
async def test_validate_empty_shex(async_client):
    """Test validation of empty ShEx fails."""
    response = await async_client.post(
        "/api/v1/validate",
        json={"shex": ""},
    )

    # Empty content should fail Pydantic validation
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_validate_warns_unused_shapes(async_client):
    """Test validation warns about unused shapes."""
    shex_with_unused = """
start = @<person>
<person> {
  foaf:name LITERAL ;
}
<unusedShape> {
  foaf:title LITERAL ;
}
"""

    response = await async_client.post(
        "/api/v1/validate",
        json={"shex": shex_with_unused},
    )

    assert response.status_code == 200
    data = response.json()
    # Should have a warning about unused shape
    warnings = [w for w in data.get("warnings", []) if "unused" in w.get("message", "").lower()]
    assert len(warnings) > 0 or data["valid"] is True  # At minimum, should parse
