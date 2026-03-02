# ShExStatements API

ShExStatements provides a modern FastAPI backend and a legacy compatibility endpoint.

## Base URLs

- Local backend: `http://localhost:8000`
- OpenAPI docs: `http://localhost:8000/docs`

## Modern API (v1)

### `POST /api/v1/convert`

Converts text content in ShExStatements format.

Request body example:

```json
{
  "content": "@shape|prop|value",
  "delimiter": "|",
  "skip_header": false,
  "output_format": "shex"
}
```

Example:

```bash
curl -X POST http://localhost:8000/api/v1/convert \
  -H "Content-Type: application/json" \
  -d '{"content":"@shape|prop|value","delimiter":"|","skip_header":false,"output_format":"shex"}'
```

### `POST /api/v1/convert/file`

Converts uploaded files. Supported formats:

- `.csv`
- `.xlsx`
- `.xls`
- `.ods`

Example:

```bash
curl -X POST http://localhost:8000/api/v1/convert/file \
  -F "file=@examples/language.csv" \
  -F "delimiter=," \
  -F "skip_header=false" \
  -F "output_format=shex"
```

### `GET /api/v1/health`

Returns service status, version, and Python runtime version.

Example:

```bash
curl http://localhost:8000/api/v1/health
```

### Additional API routes

- `POST /api/v1/validate`
- `POST /api/v1/export`

See `http://localhost:8000/docs` for full schemas and response formats.

## Legacy compatibility endpoint

The root endpoint `/` is kept for backward compatibility.

- `GET /` returns API info (or redirects HTML requests to `/docs`).
- `POST /` accepts the old payload style when clients send `Accept: application/json`.

Legacy payload format (from `examples/api/tvseries.json`):

```json
[
  "|",
  "wd|<http://www.wikidata.org/entity/>|||\n@tvseries|wdt:P31|wd:Q5398426|# instance of a tvseries\n"
]
```
