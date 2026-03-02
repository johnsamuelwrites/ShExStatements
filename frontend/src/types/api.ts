/**
 * API types for ShExStatements frontend.
 */

export type Delimiter = ',' | '|' | ';';
export type OutputFormat = 'shex';
export type ExportFormat = 'json-schema' | 'graphql' | 'shacl' | 'typescript';

export interface ParseError {
  line: number;
  column: number | null;
  message: string;
  source_line: string | null;
}

export interface Warning {
  line: number | null;
  message: string;
  code: string | null;
}

export interface ConvertRequest {
  content: string;
  delimiter: Delimiter;
  skip_header: boolean;
  output_format: OutputFormat;
}

export interface ConvertResponse {
  success: boolean;
  output: string | null;
  errors: ParseError[];
  warnings: Warning[];
  input_format: string | null;
  output_format: string | null;
}

export interface FileUploadResponse extends ConvertResponse {
  filename: string | null;
  file_type: string | null;
}

export interface ValidateRequest {
  shex: string;
}

export interface ValidateResponse {
  valid: boolean;
  errors: ParseError[];
  warnings: Warning[];
}

export interface ExportRequest {
  shex: string;
  format: ExportFormat;
}

export interface ExportResponse {
  success: boolean;
  output: string | null;
  format: string | null;
  errors: ParseError[];
}

export interface HealthResponse {
  status: 'healthy' | 'unhealthy';
  version: string;
  python_version: string;
}
