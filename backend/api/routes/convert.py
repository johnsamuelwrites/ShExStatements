#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Conversion API routes for ShExStatements.

Provides endpoints for converting ShExStatements CSV content
to ShEx format.
"""

from typing import Literal

from fastapi import APIRouter, File, Form, UploadFile

from api.models.requests import ConvertRequest
from api.models.responses import ConvertResponse, FileUploadResponse
from api.services.converter import ConverterService

router = APIRouter(prefix="/api/v1", tags=["conversion"])


@router.post(
    "/convert",
    response_model=ConvertResponse,
    summary="Convert ShExStatements to ShEx",
    description="""
    Convert ShExStatements content (CSV or pipe-delimited format) to ShEx.

    The input should be in the ShExStatements format:
    - Pipe-delimited: `@nodename|property|value|cardinality|comment`
    - CSV format with configurable delimiter

    Example input:
    ```
    @person|rdf:type|foaf:Person
    @person|foaf:name|Literal|+|name is required
    ```
    """,
)
async def convert_shexstatements(request: ConvertRequest) -> ConvertResponse:
    """
    Convert ShExStatements string content to ShEx format.

    Args:
        request: The conversion request containing the content and options.

    Returns:
        ConvertResponse with the generated ShEx or error information.
    """
    return await ConverterService.convert_string(
        content=request.content,
        delimiter=request.delimiter,
        skip_header=request.skip_header,
        output_format=request.output_format,
    )


@router.post(
    "/convert/file",
    response_model=FileUploadResponse,
    summary="Convert uploaded file to ShEx",
    description="""
    Upload a file (CSV, XLSX, XLS, or ODS) and convert it to ShEx.

    Supported file formats:
    - `.csv` - Comma-separated values (or other delimiter)
    - `.xlsx` - Excel 2007+ format
    - `.xls` - Legacy Excel format
    - `.ods` - OpenDocument Spreadsheet
    """,
)
async def convert_file(
    file: UploadFile = File(..., description="The file to convert"),
    delimiter: Literal[",", "|", ";"] = Form(
        default=",",
        description="Delimiter for CSV files",
    ),
    skip_header: bool = Form(
        default=False,
        description="Skip the first row (header)",
    ),
    output_format: Literal["shex"] = Form(
        default="shex",
        description="Output format",
    ),
) -> FileUploadResponse:
    """
    Convert an uploaded file to ShEx format.

    Args:
        file: The uploaded file.
        delimiter: The delimiter for CSV files.
        skip_header: Whether to skip the header row.
        output_format: The desired output format.

    Returns:
        FileUploadResponse with the generated ShEx or error information.
    """
    # Read file content
    file_content = await file.read()
    filename = file.filename or "unknown.csv"

    # Get file extension for response
    file_extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else "csv"

    # Convert using the service
    result = await ConverterService.convert_file(
        file_content=file_content,
        filename=filename,
        delimiter=delimiter,
        skip_header=skip_header,
        output_format=output_format,
    )

    return FileUploadResponse(
        success=result.success,
        output=result.output,
        filename=filename,
        file_type=file_extension,
        errors=result.errors,
        warnings=result.warnings,
    )
