/**
 * Editor toolbar with controls for conversion options.
 */

import { useCallback, useRef } from 'react';
import { useEditorStore } from '../../stores/editorStore';
import { useConvert, useFileConvert } from '../../hooks/useConvert';
import type { Delimiter } from '../../types/api';
import type { RuntimeMode } from '../../types/runtime';
import { resolveRuntimeMode } from '../../types/runtime';

export function Toolbar() {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const {
    inputContent,
    delimiter,
    skipHeader,
    runtimeMode,
    isConverting,
    setDelimiter,
    setSkipHeader,
    setRuntimeMode,
    setInputContent,
    clearOutput,
    reset,
  } = useEditorStore();

  const { convert } = useConvert();
  const { convertFile } = useFileConvert();
  const resolvedRuntime = resolveRuntimeMode(runtimeMode);

  const handleConvert = useCallback(() => {
    convert({
      content: inputContent,
      delimiter,
      skip_header: skipHeader,
      output_format: 'shex',
    });
  }, [convert, inputContent, delimiter, skipHeader]);

  const handleFileUpload = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (file) {
        // For CSV files, read and display content
        if (file.name.toLowerCase().endsWith('.csv')) {
          const reader = new FileReader();
          reader.onload = (e) => {
            const content = e.target?.result as string;
            setInputContent(content);
          };
          reader.readAsText(file);
        } else {
          // For spreadsheets, delegate to selected runtime.
          convertFile(file);
        }
      }
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    },
    [setInputContent, convertFile]
  );

  const handleClear = useCallback(() => {
    clearOutput();
  }, [clearOutput]);

  const handleReset = useCallback(() => {
    reset();
  }, [reset]);

  return (
    <div className="h-12 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 flex items-center justify-between px-4 gap-4">
      <div className="flex items-center gap-3">
        {/* Delimiter selector */}
        <label className="flex items-center gap-2 text-sm">
          <span className="text-gray-600 dark:text-gray-400">Delimiter:</span>
          <select
            value={delimiter}
            onChange={(e) => setDelimiter(e.target.value as Delimiter)}
            className="select py-1 px-2 text-sm w-20"
          >
            <option value="|">Pipe (|)</option>
            <option value=",">Comma (,)</option>
            <option value=";">Semicolon (;)</option>
          </select>
        </label>

        {/* Skip header checkbox */}
        <label className="flex items-center gap-2 text-sm cursor-pointer">
          <input
            type="checkbox"
            checked={skipHeader}
            onChange={(e) => setSkipHeader(e.target.checked)}
            className="rounded border-gray-300 dark:border-gray-600 text-shex-600 focus:ring-shex-500"
          />
          <span className="text-gray-600 dark:text-gray-400">Skip header</span>
        </label>

        {/* Runtime selector */}
        <label className="flex items-center gap-2 text-sm">
          <span className="text-gray-600 dark:text-gray-400">Runtime:</span>
          <select
            value={runtimeMode}
            onChange={(e) => setRuntimeMode(e.target.value as RuntimeMode)}
            className="select py-1 px-2 text-sm w-28"
          >
            <option value="auto">Auto</option>
            <option value="api">API</option>
            <option value="wasm">WASM</option>
          </select>
        </label>
      </div>

      <div className="flex items-center gap-2">
        {/* File upload */}
        <input
          ref={fileInputRef}
          type="file"
          accept={resolvedRuntime === 'wasm' ? '.csv' : '.csv,.xlsx,.xls,.ods'}
          onChange={handleFileUpload}
          className="hidden"
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className="btn btn-secondary py-1 px-3 text-sm cursor-pointer"
        >
          Upload File
        </label>

        {/* Clear button */}
        <button
          onClick={handleClear}
          className="btn btn-secondary py-1 px-3 text-sm"
        >
          Clear
        </button>

        {/* Reset button */}
        <button
          onClick={handleReset}
          className="btn btn-secondary py-1 px-3 text-sm"
        >
          Reset
        </button>

        {/* Convert button */}
        <button
          onClick={handleConvert}
          disabled={isConverting || !inputContent.trim()}
          className="btn btn-primary py-1 px-4 text-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {isConverting ? (
            <>
              <LoadingSpinner />
              Converting...
            </>
          ) : (
            'Convert'
          )}
        </button>
      </div>
    </div>
  );
}

function LoadingSpinner() {
  return (
    <svg
      className="animate-spin h-4 w-4"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  );
}
