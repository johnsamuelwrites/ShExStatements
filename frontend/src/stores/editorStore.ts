/**
 * Editor state management using Zustand.
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Delimiter, OutputFormat, ParseError, Warning } from '../types/api';
import type { RuntimeMode } from '../types/runtime';

interface EditorState {
  // Input state
  inputContent: string;
  delimiter: Delimiter;
  skipHeader: boolean;
  outputFormat: OutputFormat;
  runtimeMode: RuntimeMode;

  // Output state
  outputContent: string;
  errors: ParseError[];
  warnings: Warning[];

  // UI state
  isConverting: boolean;
  lastConvertedAt: number | null;

  // Actions
  setInputContent: (content: string) => void;
  setDelimiter: (delimiter: Delimiter) => void;
  setSkipHeader: (skip: boolean) => void;
  setOutputFormat: (format: OutputFormat) => void;
  setRuntimeMode: (runtime: RuntimeMode) => void;
  setOutputContent: (content: string) => void;
  setErrors: (errors: ParseError[]) => void;
  setWarnings: (warnings: Warning[]) => void;
  setIsConverting: (converting: boolean) => void;
  setConversionResult: (result: {
    output: string | null;
    errors: ParseError[];
    warnings: Warning[];
  }) => void;
  clearOutput: () => void;
  reset: () => void;
}

const DEFAULT_INPUT = `wd,<http://www.wikidata.org/entity/>,,,
wdt,<http://www.wikidata.org/prop/direct/>,,,
xsd,<http://www.w3.org/2001/XMLSchema#>,,,

@language,wdt:P31,wd:Q34770,,# instance of a language
@language,wdt:P1705,LITERAL,,# native name
@language,wdt:P17,.,+,# spoken in country
@language,wdt:P2989,.,+,# grammatical cases
@language,wdt:P282,.,+,# writing system
@language,wdt:P1098,.,+,# speakers
@language,wdt:P1999,.,*,# UNESCO language status
@language,wdt:P2341,.,+,# indigenous to`;

const initialState = {
  inputContent: DEFAULT_INPUT,
  delimiter: ',' as Delimiter,
  skipHeader: false,
  outputFormat: 'shex' as OutputFormat,
  runtimeMode: 'auto' as RuntimeMode,
  outputContent: '',
  errors: [] as ParseError[],
  warnings: [] as Warning[],
  isConverting: false,
  lastConvertedAt: null as number | null,
};

// Storage version - increment when default example format changes
const STORAGE_VERSION = 4;

export const useEditorStore = create<EditorState>()(
  persist(
    (set) => ({
      ...initialState,

      setInputContent: (content) => set({ inputContent: content }),

      setDelimiter: (delimiter) => set({ delimiter }),

      setSkipHeader: (skip) => set({ skipHeader: skip }),

      setOutputFormat: (format) => set({ outputFormat: format }),

      setRuntimeMode: (runtimeMode) => set({ runtimeMode }),

      setOutputContent: (content) => set({ outputContent: content }),

      setErrors: (errors) => set({ errors }),

      setWarnings: (warnings) => set({ warnings }),

      setIsConverting: (converting) => set({ isConverting: converting }),

      setConversionResult: (result) => set({
        outputContent: result.output || '',
        errors: result.errors,
        warnings: result.warnings,
        lastConvertedAt: Date.now(),
      }),

      clearOutput: () => set({
        outputContent: '',
        errors: [],
        warnings: [],
      }),

      reset: () => set(initialState),
    }),
    {
      name: 'shexstatements-editor',
      version: STORAGE_VERSION,
      partialize: (state) => ({
        inputContent: state.inputContent,
        delimiter: state.delimiter,
        skipHeader: state.skipHeader,
        outputFormat: state.outputFormat,
        runtimeMode: state.runtimeMode,
      }),
      // Migration: reset inputContent when version changes
      migrate: (persistedState, version) => {
        // Type the persisted state shape (only data, not actions)
        type PersistedData = {
          inputContent: string;
          delimiter: Delimiter;
          skipHeader: boolean;
          outputFormat: OutputFormat;
          runtimeMode?: RuntimeMode;
        };
        const state = persistedState as PersistedData | null;
        if (version < STORAGE_VERSION || !state) {
          // Reset to default input when migrating from old version
          return {
            inputContent: DEFAULT_INPUT,
            delimiter: state?.delimiter ?? (',' as Delimiter),
            skipHeader: state?.skipHeader ?? false,
            outputFormat: state?.outputFormat ?? ('shex' as OutputFormat),
            runtimeMode: state?.runtimeMode ?? ('auto' as RuntimeMode),
          };
        }
        return state;
      },
    }
  )
);
