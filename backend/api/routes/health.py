#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Health check API route.

Provides an endpoint for monitoring the service health.
"""

import sys

from fastapi import APIRouter

from api.models.responses import HealthResponse
from shexstatements.version import __version__

router = APIRouter(tags=["health"])


@router.get(
    "/api/v1/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the service is healthy and get version information.",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse with service status and version information.
    """
    return HealthResponse(
        status="healthy",
        version=__version__,
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    )
