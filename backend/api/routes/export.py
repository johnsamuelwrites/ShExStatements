#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Export API routes for converting ShEx to other formats.

Provides endpoints for exporting ShEx schemas to JSON Schema,
GraphQL SDL, SHACL, and TypeScript interfaces.
"""

import asyncio
import json
import re
from typing import Literal

from fastapi import APIRouter

from api.models.requests import ExportRequest
from api.models.responses import ExportResponse, ParseError

router = APIRouter(prefix="/api/v1", tags=["export"])


@router.post(
    "/export",
    response_model=ExportResponse,
    summary="Export ShEx to other formats",
    description="""
    Export a ShEx schema to various other schema formats.

    Supported formats:
    - `json-schema` - JSON Schema (draft-07)
    - `graphql` - GraphQL SDL (Schema Definition Language)
    - `shacl` - SHACL (Shapes Constraint Language) in Turtle
    - `typescript` - TypeScript interfaces
    """,
)
async def export_shex(request: ExportRequest) -> ExportResponse:
    """
    Export a ShEx schema to another format.

    Args:
        request: The export request containing the ShEx and target format.

    Returns:
        ExportResponse with the exported content or errors.
    """
    try:
        output = await asyncio.to_thread(
            _export_shex_to_format,
            request.shex,
            request.format,
        )

        return ExportResponse(
            success=True,
            output=output,
            format=request.format,
            errors=[],
        )

    except Exception as e:
        return ExportResponse(
            success=False,
            output=None,
            format=request.format,
            errors=[
                ParseError(
                    line=1,
                    message=f"Export failed: {str(e)}",
                )
            ],
        )


def _export_shex_to_format(
    shex: str,
    target_format: Literal["json-schema", "graphql", "shacl", "typescript"],
) -> str:
    """
    Convert ShEx to the specified format.

    Args:
        shex: The ShEx schema string.
        target_format: The target format.

    Returns:
        The converted schema as a string.
    """
    # Parse the ShEx to extract shapes
    shapes = _parse_shex_shapes(shex)

    if target_format == "json-schema":
        return _to_json_schema(shapes)
    elif target_format == "graphql":
        return _to_graphql(shapes)
    elif target_format == "shacl":
        return _to_shacl(shapes, shex)
    elif target_format == "typescript":
        return _to_typescript(shapes)
    else:
        raise ValueError(f"Unsupported format: {target_format}")


def _parse_shex_shapes(shex: str) -> dict:
    """
    Parse ShEx schema to extract shape definitions.

    Returns a dictionary with shape names as keys and their properties.
    """
    shapes = {}

    # Extract prefixes
    prefix_pattern = r"PREFIX\s+(\w+):\s*<([^>]+)>"
    prefixes = dict(re.findall(prefix_pattern, shex, re.IGNORECASE))

    # Extract shapes
    shape_pattern = r"<(\w+)>\s*(?:CLOSED\s*)?{([^}]*)}"
    for match in re.finditer(shape_pattern, shex, re.DOTALL):
        shape_name = match.group(1)
        shape_body = match.group(2)

        properties = []
        # Parse property constraints
        prop_pattern = r"(\S+)\s+(\S+)(?:\s*\[([^\]]+)\])?\s*([+*?]|\{\d+(?:,\d*)?\})?\s*;?"
        for prop_match in re.finditer(prop_pattern, shape_body):
            prop_name = prop_match.group(1)
            prop_type = prop_match.group(2)
            value_set = prop_match.group(3)
            cardinality = prop_match.group(4) or ""

            properties.append({
                "name": prop_name,
                "type": prop_type,
                "value_set": value_set.split() if value_set else None,
                "cardinality": cardinality,
            })

        shapes[shape_name] = {
            "properties": properties,
            "prefixes": prefixes,
        }

    return shapes


def _to_json_schema(shapes: dict) -> str:
    """Convert parsed shapes to JSON Schema."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "definitions": {},
    }

    for shape_name, shape_data in shapes.items():
        properties = {}
        required = []

        for prop in shape_data["properties"]:
            prop_name = prop["name"].split(":")[-1]  # Remove prefix
            prop_schema = _shex_type_to_json_schema_type(prop["type"], prop["value_set"])

            # Handle cardinality
            card = prop["cardinality"]
            if card in ["+", ""]:
                required.append(prop_name)
            if card in ["*", "+"]:
                prop_schema = {"type": "array", "items": prop_schema}
                if card == "+":
                    prop_schema["minItems"] = 1

            properties[prop_name] = prop_schema

        schema["definitions"][shape_name] = {
            "type": "object",
            "properties": properties,
            "required": required if required else None,
        }

    # Set the first shape as the main schema
    if shapes:
        first_shape = next(iter(shapes.keys()))
        schema["$ref"] = f"#/definitions/{first_shape}"

    return json.dumps(schema, indent=2)


def _shex_type_to_json_schema_type(shex_type: str, value_set: list | None) -> dict:
    """Map ShEx types to JSON Schema types."""
    if value_set:
        return {"enum": value_set}

    type_map = {
        "LITERAL": {"type": "string"},
        "IRI": {"type": "string", "format": "uri"},
        "xsd:string": {"type": "string"},
        "xsd:integer": {"type": "integer"},
        "xsd:decimal": {"type": "number"},
        "xsd:boolean": {"type": "boolean"},
        "xsd:dateTime": {"type": "string", "format": "date-time"},
        "xsd:date": {"type": "string", "format": "date"},
    }

    # Check if it's a shape reference
    if shex_type.startswith("@<"):
        ref_name = shex_type[2:-1]
        return {"$ref": f"#/definitions/{ref_name}"}

    return type_map.get(shex_type, {"type": "string"})


def _to_graphql(shapes: dict) -> str:
    """Convert parsed shapes to GraphQL SDL."""
    lines = []

    for shape_name, shape_data in shapes.items():
        lines.append(f"type {shape_name} {{")

        for prop in shape_data["properties"]:
            prop_name = prop["name"].split(":")[-1]
            graphql_type = _shex_type_to_graphql_type(prop["type"], prop["value_set"])

            # Handle cardinality
            card = prop["cardinality"]
            if card in ["*", "+"]:
                graphql_type = f"[{graphql_type}]"
            if card in ["+", ""] or not card:
                graphql_type = f"{graphql_type}!"

            lines.append(f"  {prop_name}: {graphql_type}")

        lines.append("}")
        lines.append("")

    return "\n".join(lines)


def _shex_type_to_graphql_type(shex_type: str, value_set: list | None) -> str:
    """Map ShEx types to GraphQL types."""
    if value_set:
        # Would need to create an enum type
        return "String"

    type_map = {
        "LITERAL": "String",
        "IRI": "String",
        "xsd:string": "String",
        "xsd:integer": "Int",
        "xsd:decimal": "Float",
        "xsd:boolean": "Boolean",
        "xsd:dateTime": "String",
        "xsd:date": "String",
    }

    # Check if it's a shape reference
    if shex_type.startswith("@<"):
        return shex_type[2:-1]

    return type_map.get(shex_type, "String")


def _to_shacl(shapes: dict, original_shex: str) -> str:
    """Convert parsed shapes to SHACL in Turtle format."""
    lines = [
        "@prefix sh: <http://www.w3.org/ns/shacl#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "@prefix ex: <http://example.org/> .",
        "",
    ]

    # Extract prefixes from original ShEx
    prefix_pattern = r"PREFIX\s+(\w+):\s*<([^>]+)>"
    for prefix, uri in re.findall(prefix_pattern, original_shex, re.IGNORECASE):
        lines.append(f"@prefix {prefix}: <{uri}> .")

    lines.append("")

    for shape_name, shape_data in shapes.items():
        lines.append(f"ex:{shape_name}Shape a sh:NodeShape ;")
        lines.append(f"    sh:targetClass ex:{shape_name} ;")

        props = shape_data["properties"]
        for i, prop in enumerate(props):
            separator = ";" if i < len(props) - 1 else "."
            prop_name = prop["name"]

            lines.append("    sh:property [")
            lines.append(f"        sh:path {prop_name} ;")

            # Add datatype or node constraint
            if prop["type"] == "LITERAL":
                lines.append("        sh:datatype xsd:string ;")
            elif prop["type"].startswith("xsd:"):
                lines.append(f"        sh:datatype {prop['type']} ;")
            elif prop["type"].startswith("@<"):
                ref_name = prop["type"][2:-1]
                lines.append(f"        sh:node ex:{ref_name}Shape ;")

            # Add cardinality
            card = prop["cardinality"]
            if card == "+":
                lines.append("        sh:minCount 1 ;")
            elif card == "?":
                lines.append("        sh:maxCount 1 ;")
            elif card == "":
                lines.append("        sh:minCount 1 ;")
                lines.append("        sh:maxCount 1 ;")

            lines.append(f"    ] {separator}")

        lines.append("")

    return "\n".join(lines)


def _to_typescript(shapes: dict) -> str:
    """Convert parsed shapes to TypeScript interfaces."""
    lines = []

    for shape_name, shape_data in shapes.items():
        lines.append(f"export interface {shape_name} {{")

        for prop in shape_data["properties"]:
            prop_name = prop["name"].split(":")[-1]
            ts_type = _shex_type_to_typescript_type(prop["type"], prop["value_set"])

            # Handle cardinality
            card = prop["cardinality"]
            optional = "?" if card in ["?", "*"] else ""
            if card in ["*", "+"]:
                ts_type = f"{ts_type}[]"

            lines.append(f"  {prop_name}{optional}: {ts_type};")

        lines.append("}")
        lines.append("")

    return "\n".join(lines)


def _shex_type_to_typescript_type(shex_type: str, value_set: list | None) -> str:
    """Map ShEx types to TypeScript types."""
    if value_set:
        return " | ".join(f'"{v}"' for v in value_set)

    type_map = {
        "LITERAL": "string",
        "IRI": "string",
        "xsd:string": "string",
        "xsd:integer": "number",
        "xsd:decimal": "number",
        "xsd:boolean": "boolean",
        "xsd:dateTime": "Date",
        "xsd:date": "Date",
    }

    # Check if it's a shape reference
    if shex_type.startswith("@<"):
        return shex_type[2:-1]

    return type_map.get(shex_type, "string")
