#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Pydantic response models for the ShExStatements API."""

from typing import Literal

from pydantic import BaseModel, Field


class ParseError(BaseModel):
    """Model representing a parsing error with location information."""

    line: int = Field(
        ...,
        description="The line number where the error occurred (1-indexed)",
        ge=1,
    )
    column: int | None = Field(
        default=None,
        description="The column number where the error occurred (1-indexed)",
        ge=1,
    )
    message: str = Field(
        ...,
        description="The error message describing what went wrong",
    )
    source_line: str | None = Field(
        default=None,
        description="The source line where the error occurred",
    )


class Warning(BaseModel):
    """Model representing a warning (non-fatal issue)."""

    line: int | None = Field(
        default=None,
        description="The line number related to the warning (1-indexed)",
        ge=1,
    )
    message: str = Field(
        ...,
        description="The warning message",
    )
    code: str | None = Field(
        default=None,
        description="A code identifying the type of warning",
    )


class ConvertResponse(BaseModel):
    """Response model for conversion results."""

    success: bool = Field(
        ...,
        description="Whether the conversion was successful",
    )
    output: str | None = Field(
        default=None,
        description="The converted ShEx output (if successful)",
    )
    errors: list[ParseError] = Field(
        default_factory=list,
        description="List of parsing errors encountered",
    )
    warnings: list[Warning] = Field(
        default_factory=list,
        description="List of warnings (non-fatal issues)",
    )
    input_format: str | None = Field(
        default=None,
        description="The detected input format",
    )
    output_format: str | None = Field(
        default=None,
        description="The output format used",
    )


class ValidateResponse(BaseModel):
    """Response model for validation results."""

    valid: bool = Field(
        ...,
        description="Whether the ShEx schema is valid",
    )
    errors: list[ParseError] = Field(
        default_factory=list,
        description="List of validation errors",
    )
    warnings: list[Warning] = Field(
        default_factory=list,
        description="List of validation warnings",
    )


class ExportResponse(BaseModel):
    """Response model for export results."""

    success: bool = Field(
        ...,
        description="Whether the export was successful",
    )
    output: str | None = Field(
        default=None,
        description="The exported content in the target format",
    )
    format: str | None = Field(
        default=None,
        description="The format of the exported content",
    )
    errors: list[ParseError] = Field(
        default_factory=list,
        description="List of errors encountered during export",
    )


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: Literal["healthy", "unhealthy"] = Field(
        ...,
        description="The health status of the service",
    )
    version: str = Field(
        ...,
        description="The version of the ShExStatements service",
    )
    python_version: str = Field(
        ...,
        description="The Python version running the service",
    )


class FileUploadResponse(BaseModel):
    """Response model for file upload conversion."""

    success: bool = Field(
        ...,
        description="Whether the file was processed successfully",
    )
    output: str | None = Field(
        default=None,
        description="The converted ShEx output",
    )
    filename: str | None = Field(
        default=None,
        description="The name of the uploaded file",
    )
    file_type: str | None = Field(
        default=None,
        description="The detected file type (csv, xlsx, xls, ods)",
    )
    errors: list[ParseError] = Field(
        default_factory=list,
        description="List of parsing errors",
    )
    warnings: list[Warning] = Field(
        default_factory=list,
        description="List of warnings",
    )
