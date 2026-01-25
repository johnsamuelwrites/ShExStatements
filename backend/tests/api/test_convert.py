#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Tests for the conversion API endpoints."""

import pytest


@pytest.mark.asyncio
async def test_convert_simple(async_client, sample_shexstatements, expected_shex_output):
    """Test basic ShExStatements to ShEx conversion."""
    response = await async_client.post(
        "/api/v1/convert",
        json={
            "content": sample_shexstatements,
            "delimiter": "|",
            "skip_header": False,
            "output_format": "shex",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert expected_shex_output in data["output"]
    assert len(data["errors"]) == 0


@pytest.mark.asyncio
async def test_convert_csv_delimiter(async_client, sample_csv_content):
    """Test conversion with comma delimiter."""
    response = await async_client.post(
        "/api/v1/convert",
        json={
            "content": sample_csv_content,
            "delimiter": ",",
            "skip_header": False,
            "output_format": "shex",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "person" in data["output"]


@pytest.mark.asyncio
async def test_convert_to_shexj(async_client, sample_shexstatements):
    """Test conversion to ShExJ format."""
    response = await async_client.post(
        "/api/v1/convert",
        json={
            "content": sample_shexstatements,
            "delimiter": "|",
            "skip_header": False,
            "output_format": "shexj",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["output_format"] == "shexj"
    # ShExJ output should be valid JSON
    import json
    try:
        json.loads(data["output"])
    except json.JSONDecodeError:
        pytest.fail("ShExJ output is not valid JSON")


@pytest.mark.asyncio
async def test_convert_empty_content(async_client):
    """Test conversion with empty content fails validation."""
    response = await async_client.post(
        "/api/v1/convert",
        json={
            "content": "",
            "delimiter": "|",
            "skip_header": False,
            "output_format": "shex",
        },
    )

    # Empty content should fail Pydantic validation
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_convert_invalid_delimiter(async_client, sample_shexstatements):
    """Test conversion with invalid delimiter fails validation."""
    response = await async_client.post(
        "/api/v1/convert",
        json={
            "content": sample_shexstatements,
            "delimiter": "X",  # Invalid delimiter
            "skip_header": False,
            "output_format": "shex",
        },
    )

    # Invalid delimiter should fail Pydantic validation
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_convert_skip_header(async_client):
    """Test conversion with skip_header option."""
    content_with_header = """Node,Property,Value,Cardinality,Comment
@person,rdf:type,foaf:Person,,
@person,foaf:name,Literal,+,"""

    response = await async_client.post(
        "/api/v1/convert",
        json={
            "content": content_with_header,
            "delimiter": ",",
            "skip_header": True,
            "output_format": "shex",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # Header should not appear in output
    assert "Node" not in data["output"]


@pytest.mark.asyncio
async def test_convert_with_comments(async_client):
    """Test conversion preserves comments."""
    content = """@person|rdf:type|foaf:Person||#This is a person
@person|foaf:name|Literal|+|#Name field"""

    response = await async_client.post(
        "/api/v1/convert",
        json={
            "content": content,
            "delimiter": "|",
            "skip_header": False,
            "output_format": "shex",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_convert_file_endpoint_csv(async_client, sample_csv_content):
    """Test file upload conversion for CSV."""
    files = {
        "file": ("test.csv", sample_csv_content.encode(), "text/csv"),
    }
    data = {
        "delimiter": ",",
        "skip_header": "false",
        "output_format": "shex",
    }

    response = await async_client.post(
        "/api/v1/convert/file",
        files=files,
        data=data,
    )

    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert result["filename"] == "test.csv"
    assert result["file_type"] == "csv"
