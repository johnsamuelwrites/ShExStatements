/**
 * Hook for ShExStatements conversion with React Query.
 */

import { useMutation } from '@tanstack/react-query';
import { convertShexStatements, convertFile } from '../services/api';
import { convertShexStatementsWasm, convertFileWasm } from '../services/wasm';
import { useEditorStore } from '../stores/editorStore';
import type { ConvertRequest, ConvertResponse, FileUploadResponse } from '../types/api';
import { resolveRuntimeMode } from '../types/runtime';

/**
 * Hook for converting ShExStatements content.
 */
export function useConvert() {
  const {
    setIsConverting,
    setConversionResult,
    setErrors,
    runtimeMode,
  } = useEditorStore();

  const mutation = useMutation<ConvertResponse, Error, ConvertRequest>({
    mutationFn: async (request) => {
      const resolvedRuntime = resolveRuntimeMode(runtimeMode);
      return resolvedRuntime === 'wasm'
        ? convertShexStatementsWasm(request)
        : convertShexStatements(request);
    },
    onMutate: () => {
      setIsConverting(true);
    },
    onSuccess: (data) => {
      setConversionResult({
        output: data.output,
        errors: data.errors,
        warnings: data.warnings,
      });
    },
    onError: (error) => {
      setErrors([{
        line: 1,
        column: null,
        message: error.message,
        source_line: null,
      }]);
    },
    onSettled: () => {
      setIsConverting(false);
    },
  });

  return {
    convert: mutation.mutate,
    convertAsync: mutation.mutateAsync,
    isConverting: mutation.isPending,
    error: mutation.error,
    reset: mutation.reset,
  };
}

/**
 * Hook for converting uploaded files.
 */
export function useFileConvert() {
  const {
    setIsConverting,
    setConversionResult,
    setErrors,
    delimiter,
    skipHeader,
    outputFormat,
    runtimeMode,
  } = useEditorStore();

  const mutation = useMutation<FileUploadResponse, Error, File>({
    mutationFn: (file) => {
      const resolvedRuntime = resolveRuntimeMode(runtimeMode);
      return resolvedRuntime === 'wasm'
        ? convertFileWasm(file, delimiter, skipHeader, outputFormat)
        : convertFile(file, delimiter, skipHeader, outputFormat);
    },
    onMutate: () => {
      setIsConverting(true);
    },
    onSuccess: (data) => {
      setConversionResult({
        output: data.output,
        errors: data.errors,
        warnings: data.warnings,
      });
    },
    onError: (error) => {
      setErrors([{
        line: 1,
        column: null,
        message: error.message,
        source_line: null,
      }]);
    },
    onSettled: () => {
      setIsConverting(false);
    },
  });

  return {
    convertFile: mutation.mutate,
    convertFileAsync: mutation.mutateAsync,
    isConverting: mutation.isPending,
    error: mutation.error,
    reset: mutation.reset,
  };
}
