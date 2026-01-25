/**
 * API service for ShExStatements backend communication.
 */

import type {
  ConvertRequest,
  ConvertResponse,
  ExportRequest,
  ExportResponse,
  FileUploadResponse,
  HealthResponse,
  ValidateRequest,
  ValidateResponse,
  Delimiter,
  OutputFormat,
} from '../types/api';

const API_BASE_URL = '/api/v1';

/**
 * Generic fetch wrapper with error handling.
 */
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP error ${response.status}`);
  }

  return response.json();
}

/**
 * Convert ShExStatements content to ShEx.
 */
export async function convertShexStatements(
  request: ConvertRequest
): Promise<ConvertResponse> {
  return fetchApi<ConvertResponse>('/convert', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

/**
 * Convert an uploaded file to ShEx.
 */
export async function convertFile(
  file: File,
  delimiter: Delimiter = ',',
  skipHeader: boolean = false,
  outputFormat: OutputFormat = 'shex'
): Promise<FileUploadResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('delimiter', delimiter);
  formData.append('skip_header', String(skipHeader));
  formData.append('output_format', outputFormat);

  const response = await fetch(`${API_BASE_URL}/convert/file`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP error ${response.status}`);
  }

  return response.json();
}

/**
 * Validate a ShEx schema.
 */
export async function validateShex(
  request: ValidateRequest
): Promise<ValidateResponse> {
  return fetchApi<ValidateResponse>('/validate', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

/**
 * Export ShEx to another format.
 */
export async function exportShex(
  request: ExportRequest
): Promise<ExportResponse> {
  return fetchApi<ExportResponse>('/export', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

/**
 * Check API health status.
 */
export async function checkHealth(): Promise<HealthResponse> {
  return fetchApi<HealthResponse>('/health');
}
