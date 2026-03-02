import type {
  ConvertRequest,
  ConvertResponse,
  FileUploadResponse,
  ParseError,
} from '../types/api';

type RuntimePyodide = {
  runPythonAsync: <T = unknown>(code: string) => Promise<T>;
  globals: {
    set: (key: string, value: unknown) => void;
    get: <T = unknown>(key: string) => T;
  };
  loadPackage: (pkg: string) => Promise<void>;
};

declare global {
  interface Window {
    loadPyodide?: (opts: { indexURL: string }) => Promise<RuntimePyodide>;
  }
}

const PYODIDE_VERSION = '0.27.7';
const PYODIDE_INDEX_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;
const PYODIDE_SCRIPT_URL = `${PYODIDE_INDEX_URL}pyodide.js`;

const PYTHON_BOOTSTRAP = `
import micropip
await micropip.install("ply")
await micropip.install("shexstatements", deps=False)

from shexstatements.errors import ParserError, UnrecognizedCharacterError
from shexstatements.shexfromcsv import CSV

def shex_convert(content, delimiter, skip_header):
    import traceback
    try:
        output = CSV.generate_shex_from_csv(
            content,
            delim=delimiter,
            skip_header=skip_header,
            filename=False
        )
        if not output:
            return {
                "success": False,
                "output": None,
                "errors": [{"line": 1, "column": None, "message": "Conversion returned empty output.", "source_line": None}],
                "warnings": [],
                "input_format": "shexstatements",
                "output_format": "shex"
            }
        return {
            "success": True,
            "output": output,
            "errors": [],
            "warnings": [],
            "input_format": "shexstatements",
            "output_format": "shex"
        }
    except (ParserError, UnrecognizedCharacterError) as e:
        return {
            "success": False,
            "output": None,
            "errors": [{"line": 1, "column": None, "message": str(e), "source_line": None}],
            "warnings": [],
            "input_format": "shexstatements",
            "output_format": "shex"
        }
    except Exception as e:
        return {
            "success": False,
            "output": None,
            "errors": [{"line": 1, "column": None, "message": str(e), "source_line": traceback.format_exc()}],
            "warnings": [],
            "input_format": "shexstatements",
            "output_format": "shex"
        }
`;

let pyodidePromise: Promise<RuntimePyodide> | null = null;
let bootstrapPromise: Promise<void> | null = null;

function toError(error: unknown): Error {
  return error instanceof Error ? error : new Error(String(error));
}

async function loadPyodideScript(): Promise<void> {
  if (window.loadPyodide) {
    return;
  }

  await new Promise<void>((resolve, reject) => {
    const existing = document.querySelector<HTMLScriptElement>('script[data-pyodide="true"]');
    if (existing) {
      existing.addEventListener('load', () => resolve(), { once: true });
      existing.addEventListener('error', () => reject(new Error('Failed to load Pyodide script.')), { once: true });
      return;
    }

    const script = document.createElement('script');
    script.src = PYODIDE_SCRIPT_URL;
    script.async = true;
    script.dataset.pyodide = 'true';
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Failed to load Pyodide script.'));
    document.head.appendChild(script);
  });
}

async function getPyodide(): Promise<RuntimePyodide> {
  if (!pyodidePromise) {
    pyodidePromise = (async () => {
      await loadPyodideScript();
      if (!window.loadPyodide) {
        throw new Error('Pyodide loader is not available.');
      }
      return window.loadPyodide({ indexURL: PYODIDE_INDEX_URL });
    })();
  }
  return pyodidePromise;
}

async function ensurePythonRuntime(): Promise<RuntimePyodide> {
  const pyodide = await getPyodide();
  if (!bootstrapPromise) {
    bootstrapPromise = pyodide.runPythonAsync(PYTHON_BOOTSTRAP).then(() => undefined);
  }
  await bootstrapPromise;
  return pyodide;
}

function normalizeErrors(errors: unknown): ParseError[] {
  if (!Array.isArray(errors)) {
    return [];
  }

  return errors.map((error) => {
    const item = (typeof error === 'object' && error) ? error as Record<string, unknown> : {};
    return {
      line: Number(item.line ?? 1),
      column: item.column === null || item.column === undefined ? null : Number(item.column),
      message: String(item.message ?? 'Unknown conversion error'),
      source_line: item.source_line === null || item.source_line === undefined ? null : String(item.source_line),
    };
  });
}

export async function convertShexStatementsWasm(request: ConvertRequest): Promise<ConvertResponse> {
  try {
    const pyodide = await ensurePythonRuntime();
    pyodide.globals.set('input_content', request.content);
    pyodide.globals.set('input_delimiter', request.delimiter);
    pyodide.globals.set('input_skip_header', request.skip_header);

    const raw = await pyodide.runPythonAsync<string>(`
import json
result = shex_convert(input_content, input_delimiter, input_skip_header)
json.dumps(result)
`);

    const response = JSON.parse(raw) as Partial<ConvertResponse>;
    return {
      success: Boolean(response.success),
      output: response.output ?? null,
      errors: normalizeErrors(response.errors),
      warnings: Array.isArray(response.warnings) ? response.warnings : [],
      input_format: response.input_format ?? 'shexstatements',
      output_format: response.output_format ?? request.output_format,
    };
  } catch (error) {
    throw toError(error);
  }
}

export async function convertFileWasm(
  file: File,
  delimiter: ConvertRequest['delimiter'],
  skipHeader: boolean,
  outputFormat: ConvertRequest['output_format']
): Promise<FileUploadResponse> {
  if (!file.name.toLowerCase().endsWith('.csv')) {
    return {
      success: false,
      output: null,
      errors: [{
        line: 1,
        column: null,
        message: 'WASM runtime currently supports CSV input only. Use API runtime for spreadsheet files.',
        source_line: null,
      }],
      warnings: [],
      input_format: 'file',
      output_format: outputFormat,
      filename: file.name,
      file_type: file.type || null,
    };
  }

  const content = await file.text();
  const result = await convertShexStatementsWasm({
    content,
    delimiter,
    skip_header: skipHeader,
    output_format: outputFormat,
  });

  return {
    ...result,
    filename: file.name,
    file_type: file.type || null,
  };
}
