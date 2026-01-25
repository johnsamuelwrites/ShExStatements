#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Tests for the export API endpoint."""

import json

import pytest


SAMPLE_SHEX = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
start = @<person>
<person> {
  foaf:name LITERAL + ;
  foaf:mbox IRI * ;
  foaf:knows @<person> * ;
}
"""


@pytest.mark.asyncio
async def test_export_to_json_schema(async_client):
    """Test export to JSON Schema format."""
    response = await async_client.post(
        "/api/v1/export",
        json={
            "shex": SAMPLE_SHEX,
            "format": "json-schema",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["format"] == "json-schema"

    # Output should be valid JSON
    output = json.loads(data["output"])
    assert "$schema" in output
    assert "definitions" in output


@pytest.mark.asyncio
async def test_export_to_graphql(async_client):
    """Test export to GraphQL SDL format."""
    response = await async_client.post(
        "/api/v1/export",
        json={
            "shex": SAMPLE_SHEX,
            "format": "graphql",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["format"] == "graphql"
    assert "type" in data["output"]


@pytest.mark.asyncio
async def test_export_to_shacl(async_client):
    """Test export to SHACL format."""
    response = await async_client.post(
        "/api/v1/export",
        json={
            "shex": SAMPLE_SHEX,
            "format": "shacl",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["format"] == "shacl"
    assert "sh:NodeShape" in data["output"]


@pytest.mark.asyncio
async def test_export_to_typescript(async_client):
    """Test export to TypeScript interfaces."""
    response = await async_client.post(
        "/api/v1/export",
        json={
            "shex": SAMPLE_SHEX,
            "format": "typescript",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["format"] == "typescript"
    assert "interface" in data["output"] or "export interface" in data["output"]


@pytest.mark.asyncio
async def test_export_invalid_format(async_client):
    """Test export with invalid format fails validation."""
    response = await async_client.post(
        "/api/v1/export",
        json={
            "shex": SAMPLE_SHEX,
            "format": "invalid-format",
        },
    )

    # Invalid format should fail Pydantic validation
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_export_empty_shex(async_client):
    """Test export with empty ShEx fails validation."""
    response = await async_client.post(
        "/api/v1/export",
        json={
            "shex": "",
            "format": "json-schema",
        },
    )

    # Empty content should fail Pydantic validation
    assert response.status_code == 422
