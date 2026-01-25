#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Tests for the health check API endpoint."""

import pytest


@pytest.mark.asyncio
async def test_health_check(async_client):
    """Test health check endpoint returns healthy status."""
    response = await async_client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "python_version" in data


@pytest.mark.asyncio
async def test_health_check_version_format(async_client):
    """Test health check returns valid version format."""
    response = await async_client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()

    # Version should be a non-empty string
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0

    # Python version should match X.Y.Z format
    assert isinstance(data["python_version"], str)
    parts = data["python_version"].split(".")
    assert len(parts) >= 2
