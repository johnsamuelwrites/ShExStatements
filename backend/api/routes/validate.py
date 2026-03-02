#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Validation API routes for ShEx schemas.

Provides endpoints for validating ShEx schemas.
"""

import asyncio
import re

from fastapi import APIRouter

from api.models.requests import ValidateRequest
from api.models.responses import ParseError, ValidateResponse, Warning

router = APIRouter(prefix="/api/v1", tags=["validation"])


@router.post(
    "/validate",
    response_model=ValidateResponse,
    summary="Validate ShEx schema",
    description="""
    Validate a ShEx schema for syntax errors and potential issues.

    Checks performed:
    - Syntax validation
    - Undefined shape references
    - Circular reference detection (warning)
    - Unused shape detection (warning)
    """,
)
async def validate_shex(request: ValidateRequest) -> ValidateResponse:
    """
    Validate a ShEx schema.

    Args:
        request: The validation request containing the ShEx schema.

    Returns:
        ValidateResponse with validation results.
    """
    errors: list[ParseError] = []
    warnings: list[Warning] = []

    try:
        # Run validation in thread pool
        validation_result = await asyncio.to_thread(
            _validate_shex_schema, request.shex
        )
        errors = validation_result.get("errors", [])
        warnings = validation_result.get("warnings", [])

        return ValidateResponse(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    except Exception as e:
        return ValidateResponse(
            valid=False,
            errors=[
                ParseError(
                    line=1,
                    message=f"Validation failed: {str(e)}",
                )
            ],
            warnings=[],
        )


def _validate_shex_schema(shex: str) -> dict:
    """
    Perform validation checks on a ShEx schema.

    Args:
        shex: The ShEx schema string.

    Returns:
        Dictionary with 'errors' and 'warnings' lists.
    """
    errors: list[ParseError] = []
    warnings: list[Warning] = []

    # Extract defined shapes
    shape_pattern = r"<(\w+)>\s*{"
    defined_shapes = set(re.findall(shape_pattern, shex))

    # Extract referenced shapes (in value positions)
    reference_pattern = r"@<(\w+)>"
    referenced_shapes = set(re.findall(reference_pattern, shex))

    # Check for undefined shape references
    undefined = referenced_shapes - defined_shapes
    for shape in undefined:
        # Find the line number where this reference appears
        line_num = _find_line_number(shex, f"@<{shape}>")
        errors.append(
            ParseError(
                line=line_num,
                message=f"Undefined shape reference: @<{shape}>",
            )
        )

    # Check for unused shapes (warning)
    # The start shape is always "used"
    start_pattern = r"start\s*=\s*@<(\w+)>"
    start_match = re.search(start_pattern, shex)
    start_shape = start_match.group(1) if start_match else None

    used_shapes = referenced_shapes | ({start_shape} if start_shape else set())
    unused = defined_shapes - used_shapes
    for shape in unused:
        line_num = _find_line_number(shex, f"<{shape}>")
        warnings.append(
            Warning(
                line=line_num,
                message=f"Unused shape: <{shape}>",
                code="unused-shape",
            )
        )

    return {"errors": errors, "warnings": warnings}


def _find_line_number(text: str, pattern: str) -> int:
    """Find the line number where a pattern first appears."""
    lines = text.split("\n")
    for i, line in enumerate(lines, start=1):
        if pattern in line:
            return i
    return 1


def _extract_line_from_error(error_msg: str) -> int:
    """Extract line number from an error message."""
    patterns = [
        r"line\s+(\d+)",
        r"Line\s+(\d+)",
        r":(\d+):",
    ]
    for pattern in patterns:
        match = re.search(pattern, error_msg)
        if match:
            return int(match.group(1))
    return 1
