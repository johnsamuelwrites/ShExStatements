#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Pydantic request models for the ShExStatements API."""

from typing import Literal

from pydantic import BaseModel, Field


class ConvertRequest(BaseModel):
    """Request model for converting ShExStatements to ShEx."""

    content: str = Field(
        ...,
        description="The ShExStatements content to convert (CSV or pipe-delimited format)",
        min_length=1,
        examples=["@person|rdf:type|foaf:Person\n@person|foaf:name|Literal"],
    )
    delimiter: Literal[",", "|", ";"] = Field(
        default="|",
        description="The delimiter used in the input content",
    )
    skip_header: bool = Field(
        default=False,
        description="Whether to skip the first row (header) of the input",
    )
    output_format: Literal["shex"] = Field(
        default="shex",
        description="The desired output format",
    )


class ValidateRequest(BaseModel):
    """Request model for validating ShEx schemas."""

    shex: str = Field(
        ...,
        description="The ShEx schema to validate",
        min_length=1,
    )


class ExportRequest(BaseModel):
    """Request model for exporting ShEx to other formats."""

    shex: str = Field(
        ...,
        description="The ShEx schema to export",
        min_length=1,
    )
    format: Literal["json-schema", "graphql", "shacl", "typescript"] = Field(
        ...,
        description="The target export format",
    )
