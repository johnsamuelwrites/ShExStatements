# ShExStatements Documentation

ShExStatements converts CSV-like statements and spreadsheet files into Shape Expressions (ShEx).

## Supported usage modes

1. `WASM` (in-browser conversion via Pyodide)
2. `Docker` (frontend + backend services)
3. `Python` (CLI and legacy Flask web app)

## 1) Python mode

Clone and install:

```bash
git clone https://github.com/johnsamuelwrites/ShExStatements.git
cd ShExStatements
python3 -m venv .venv
source .venv/bin/activate
pip3 install .
```

Run CLI conversion:

```bash
./shexstatements.sh examples/language.csv
```

Use a different delimiter:

```bash
./shexstatements.sh examples/languagedelimsemicolon.csv --delim ";"
```

Skip CSV header:

```bash
./shexstatements.sh --skipheader examples/header/languageheader.csv
```

Convert spreadsheet files:

```bash
./shexstatements.sh examples/language.ods
./shexstatements.sh examples/language.xls
./shexstatements.sh examples/language.xlsx
```

Run legacy Flask UI:

```bash
./shexstatements.sh -r
```

Legacy UI URL: `http://127.0.0.1:5000/`

## 2) Docker mode

From repository root:

```bash
cd docker
docker compose up
```

Services:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

Development mode:

```bash
cd docker
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## 3) WASM mode

The frontend can convert in the browser with runtime mode set to `wasm` (for example in GitHub Pages builds).

In WASM mode:

- Text conversion is done fully in-browser.
- File conversion supports `.csv`, `.xlsx`, `.xls`, and `.ods`.
- Python packages are installed in Pyodide at runtime.

## ShExStatements input format

Typical row structure:

```text
@node|property|value|cardinality|comment
```

Column expectations:

- 1: node name
- 2: property
- 3: allowed value(s)
- 4: cardinality (optional)
- 5: comment (optional, starts with `#`)

Cardinality values:

- `*`: zero or more
- `+`: one or more
- `m`: exactly `m`
- `m,n`: between `m` and `n`, inclusive

Application profile CSV format:

```text
Entity_name,Property,Property_label,Mand,Repeat,Value,Value_type,Annotation
```

Command:

```bash
./shexstatements.sh -ap --skipheader examples/languageap.csv
```

Examples are available in the [examples directory](https://github.com/johnsamuelwrites/ShExStatements/tree/master/examples).
