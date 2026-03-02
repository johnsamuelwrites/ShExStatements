#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Conversion service for ShExStatements to ShEx.

This module provides async wrappers around the core conversion functions,
enabling non-blocking API operations.
"""

import asyncio
import tempfile
from pathlib import Path
from typing import Literal

from api.models.responses import ConvertResponse, ParseError
from shexstatements.errors import UnrecognizedCharacterError
from shexstatements.shexfromcsv import CSV


def _get_spreadsheet_module():
    """Lazy import of Spreadsheet module."""
    from shexstatements.shexfromspreadsheet import Spreadsheet
    return Spreadsheet


class ConverterService:
    """
    Service class for converting ShExStatements to various ShEx formats.

    Provides async methods that wrap the synchronous core conversion
    functions, running them in a thread pool to avoid blocking.
    """

    @staticmethod
    async def convert_string(
        content: str,
        delimiter: Literal[",", "|", ";"] = "|",
        skip_header: bool = False,
        output_format: Literal["shex"] = "shex",
    ) -> ConvertResponse:
        """
        Convert ShExStatements string content to ShEx.

        Args:
            content: The ShExStatements content to convert.
            delimiter: The delimiter used in the content.
            skip_header: Whether to skip the first line.
            output_format: The desired output format.

        Returns:
            ConvertResponse with the conversion result or errors.
        """
        try:
            output = await asyncio.to_thread(
                ConverterService._convert_to_shex,
                content,
                delimiter,
                skip_header,
            )

            return ConvertResponse(
                success=True,
                output=output,
                errors=[],
                warnings=[],
                input_format="shexstatements",
                output_format=output_format,
            )

        except UnrecognizedCharacterError as e:
            error = ParseError(
                line=getattr(e, "line", 1),
                column=getattr(e, "column", None),
                message=str(e),
                source_line=getattr(e, "source_line", None),
            )
            return ConvertResponse(
                success=False,
                output=None,
                errors=[error],
                warnings=[],
                input_format="shexstatements",
                output_format=output_format,
            )

        except Exception as e:
            # Try to extract line number from error message
            line_num = ConverterService._extract_line_number(str(e))
            error = ParseError(
                line=line_num,
                column=None,
                message=str(e),
                source_line=None,
            )
            return ConvertResponse(
                success=False,
                output=None,
                errors=[error],
                warnings=[],
                input_format="shexstatements",
                output_format=output_format,
            )

    @staticmethod
    async def convert_file(
        file_content: bytes,
        filename: str,
        delimiter: Literal[",", "|", ";"] = ",",
        skip_header: bool = False,
        output_format: Literal["shex"] = "shex",
    ) -> ConvertResponse:
        """
        Convert an uploaded file to ShEx.

        Args:
            file_content: The raw file content as bytes.
            filename: The original filename (used to detect format).
            delimiter: The delimiter for CSV files.
            skip_header: Whether to skip the header row.
            output_format: The desired output format.

        Returns:
            ConvertResponse with the conversion result or errors.
        """
        file_extension = Path(filename).suffix.lower()

        try:
            if file_extension == ".csv":
                # Decode CSV content
                content = file_content.decode("utf-8")
                return await ConverterService.convert_string(
                    content, delimiter, skip_header, output_format
                )

            elif file_extension in {".xlsx", ".xls", ".ods"}:
                # Spreadsheet files need to be written to a temp file
                output = await asyncio.to_thread(
                    ConverterService._convert_spreadsheet,
                    file_content,
                    filename,
                    skip_header,
                )

                return ConvertResponse(
                    success=True,
                    output=output,
                    errors=[],
                    warnings=[],
                    input_format=file_extension[1:],
                    output_format=output_format,
                )

            else:
                return ConvertResponse(
                    success=False,
                    output=None,
                    errors=[
                        ParseError(
                            line=1,
                            message=f"Unsupported file format: {file_extension}",
                        )
                    ],
                    warnings=[],
                    input_format=file_extension[1:] if file_extension else "unknown",
                    output_format=output_format,
                )

        except Exception as e:
            line_num = ConverterService._extract_line_number(str(e))
            return ConvertResponse(
                success=False,
                output=None,
                errors=[
                    ParseError(
                        line=line_num,
                        message=str(e),
                    )
                ],
                warnings=[],
                input_format=file_extension[1:] if file_extension else "unknown",
                output_format=output_format,
            )

    @staticmethod
    def _convert_to_shex(
        content: str,
        delimiter: Literal[",", "|", ";"],
        skip_header: bool,
    ) -> str:
        """
        Synchronous conversion to ShEx compact syntax.

        Args:
            content: The ShExStatements content.
            delimiter: The delimiter used.
            skip_header: Whether to skip header.

        Returns:
            The ShEx output string.
        """
        return CSV.generate_shex_from_csv(
            content,
            delim=delimiter,
            skip_header=skip_header,
            filename=False,
        )

    @staticmethod
    def _convert_spreadsheet(
        file_content: bytes,
        filename: str,
        skip_header: bool,
    ) -> str:
        """
        Synchronous conversion of spreadsheet files.

        Args:
            file_content: The raw file bytes.
            filename: The original filename.
            skip_header: Whether to skip header.

        Returns:
            The ShEx output string.
        """
        # Write to a temporary file for processing
        suffix = Path(filename).suffix
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        try:
            Spreadsheet = _get_spreadsheet_module()
            return Spreadsheet.generate_shex_from_spreadsheet(
                filepath=tmp_path,
                skip_header=skip_header,
            )
        finally:
            # Clean up temp file
            Path(tmp_path).unlink(missing_ok=True)

    @staticmethod
    def _extract_line_number(error_message: str) -> int:
        """
        Try to extract a line number from an error message.

        Args:
            error_message: The error message string.

        Returns:
            The extracted line number or 1 if not found.
        """
        import re

        # Common patterns for line numbers in error messages
        patterns = [
            r"line\s+(\d+)",
            r"Line\s+(\d+)",
            r"at line\s+(\d+)",
            r":(\d+):",
        ]

        for pattern in patterns:
            match = re.search(pattern, error_message)
            if match:
                return int(match.group(1))

        return 1
