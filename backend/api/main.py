#
# SPDX-FileCopyrightText: 2024 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
FastAPI application for ShExStatements.

This module provides a modern REST API for converting ShExStatements
to ShEx and other formats.
"""

import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from api.routes import convert, export, health, validate
from shexstatements.parser_cache import ParserCache
from shexstatements.shexfromcsv import CSV
from shexstatements.version import __version__


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Initializes resources on startup and cleans up on shutdown.
    """
    # Startup: Pre-initialize the parser cache for better first-request performance
    ParserCache.get_parser()
    yield
    # Shutdown: Clean up resources
    ParserCache.reset()


app = FastAPI(
    title="ShExStatements API",
    description="""
    A modern API for generating Shape Expressions (ShEx) from CSV files and spreadsheets.

    ## Features

    - **Convert** ShExStatements CSV format to ShEx compact syntax or ShEx JSON
    - **Upload** CSV, XLSX, XLS, or ODS files for conversion
    - **Validate** ShEx schemas for syntax errors and issues
    - **Export** ShEx to JSON Schema, GraphQL SDL, SHACL, or TypeScript

    ## ShExStatements Format

    The ShExStatements format uses pipe-delimited fields:

    ```
    @nodename|property|value|cardinality|comment
    ```

    Example:
    ```
    foaf|<http://xmlns.com/foaf/0.1/>|||
    @person|rdf:type|foaf:Person||
    @person|foaf:name|Literal|+|name is required
    @person|foaf:knows|@person|*|friends
    ```

    ## Links

    - [GitHub Repository](https://github.com/johnsamuelwrites/ShExStatements)
    - [Documentation](https://shexstatements.readthedocs.io/)
    """,
    version=__version__,
    license_info={
        "name": "GPL-3.0-or-later",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html",
    },
    contact={
        "name": "John Samuel",
        "url": "https://github.com/johnsamuelwrites",
    },
    lifespan=lifespan,
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(convert.router)
app.include_router(validate.router)
app.include_router(export.router)
app.include_router(health.router)


# Backward compatibility: Legacy endpoint for existing users
@app.api_route("/", methods=["GET", "POST"])
async def legacy_endpoint(request: Request):
    """
    Legacy endpoint for backward compatibility.

    - GET: Redirects to the frontend or returns API info
    - POST with Accept: text/html: Processes form and redirects to frontend
    - POST with Accept: application/json: Returns JSON (legacy format)
    """
    accept_header = request.headers.get("accept", "")

    if request.method == "GET":
        # For GET requests, redirect to frontend or show API info
        if "text/html" in accept_header:
            # Redirect to frontend (when available)
            return RedirectResponse(url="/docs", status_code=302)
        else:
            return JSONResponse({
                "name": "ShExStatements API",
                "version": __version__,
                "docs": "/docs",
                "openapi": "/openapi.json",
            })

    # POST request handling
    if "application/json" in accept_header:
        # Legacy JSON API format: [delimiter, content]
        try:
            form_data = await request.form()
            # The old API sent JSON as a form key
            json_key = next(iter(form_data.keys()), None)
            if json_key:
                json_val = json.loads(json_key)
                delimiter = json_val[0]
                content = json_val[1]
                shex = CSV.generate_shex_from_csv(
                    content, delim=delimiter, filename=False
                )
                return JSONResponse(json.dumps(shex))
        except Exception as e:
            return JSONResponse(
                {"error": str(e)},
                status_code=400,
            )

    elif "text/html" in accept_header:
        # Form submission - redirect to new API
        return RedirectResponse(url="/docs", status_code=302)

    # Default: return API info
    return JSONResponse({
        "name": "ShExStatements API",
        "version": __version__,
        "message": "Use /api/v1/convert for conversions",
        "docs": "/docs",
    })


def run_server(
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = False,
) -> None:
    """
    Run the FastAPI server using uvicorn.

    Args:
        host: The host to bind to.
        port: The port to bind to.
        reload: Enable auto-reload for development.
    """
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    run_server(reload=True)
