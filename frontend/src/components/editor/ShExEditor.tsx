/**
 * Monaco Editor wrapper for ShExStatements input.
 */

import { useEffect, useRef, useCallback } from 'react';
import Editor, { OnMount, OnChange, Monaco } from '@monaco-editor/react';
import type { editor } from 'monaco-editor';
import {
  SHEXSTATEMENTS_LANGUAGE_ID,
  shexstatementsLanguage,
  shexstatementsLanguageConfiguration,
  COMMON_PREFIXES,
  NODE_KINDS,
  CARDINALITIES,
} from './shex-language';
import { useSettingsStore } from '../../stores/settingsStore';
import type { ParseError } from '../../types/api';

interface ShExEditorProps {
  value: string;
  onChange: (value: string) => void;
  errors?: ParseError[];
  readOnly?: boolean;
  language?: string;
}

export function ShExEditor({
  value,
  onChange,
  errors = [],
  readOnly = false,
  language = SHEXSTATEMENTS_LANGUAGE_ID,
}: ShExEditorProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);
  const monacoRef = useRef<Monaco | null>(null);

  const { theme, fontSize, wordWrap, minimap, lineNumbers } = useSettingsStore();

  // Determine Monaco theme based on app theme
  const getMonacoTheme = useCallback(() => {
    if (theme === 'system') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'vs-dark'
        : 'vs';
    }
    return theme === 'dark' ? 'vs-dark' : 'vs';
  }, [theme]);

  // Handle editor mount
  const handleEditorMount: OnMount = useCallback((editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;

    // Register ShExStatements language if not already registered
    if (!monaco.languages.getLanguages().some((lang: { id: string }) => lang.id === SHEXSTATEMENTS_LANGUAGE_ID)) {
      monaco.languages.register({ id: SHEXSTATEMENTS_LANGUAGE_ID });
      monaco.languages.setMonarchTokensProvider(
        SHEXSTATEMENTS_LANGUAGE_ID,
        shexstatementsLanguage as Parameters<typeof monaco.languages.setMonarchTokensProvider>[1]
      );
      monaco.languages.setLanguageConfiguration(
        SHEXSTATEMENTS_LANGUAGE_ID,
        shexstatementsLanguageConfiguration as Parameters<typeof monaco.languages.setLanguageConfiguration>[1]
      );

      // Register completion provider
      monaco.languages.registerCompletionItemProvider(SHEXSTATEMENTS_LANGUAGE_ID, {
        provideCompletionItems: (model: editor.ITextModel, position: { lineNumber: number; column: number }) => {
          const word = model.getWordUntilPosition(position);
          const range = {
            startLineNumber: position.lineNumber,
            endLineNumber: position.lineNumber,
            startColumn: word.startColumn,
            endColumn: word.endColumn,
          };

          const lineContent = model.getLineContent(position.lineNumber);
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          const suggestions: any[] = [];

          // Suggest prefixes at line start
          if (position.column <= 2 || lineContent.trim() === '') {
            COMMON_PREFIXES.forEach((p) => {
              suggestions.push({
                label: p.prefix,
                kind: monaco.languages.CompletionItemKind.Module,
                insertText: `${p.prefix}|<${p.uri}>|||`,
                detail: p.uri,
                documentation: `Define prefix ${p.prefix}`,
                range,
              });
            });

            // Suggest node definition
            suggestions.push({
              label: '@shape',
              kind: monaco.languages.CompletionItemKind.Class,
              insertText: '@${1:shapeName}|${2:property}|${3:value}|${4:}|${5:#comment}',
              insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
              detail: 'Define a new shape',
              range,
            });
          }

          // Suggest node kinds after pipe
          if (lineContent.includes('|')) {
            NODE_KINDS.forEach((kind) => {
              suggestions.push({
                label: kind,
                kind: monaco.languages.CompletionItemKind.Keyword,
                insertText: kind,
                detail: `Node kind: ${kind}`,
                range,
              });
            });

            // Suggest cardinalities
            CARDINALITIES.forEach((card) => {
              suggestions.push({
                label: card.label,
                kind: monaco.languages.CompletionItemKind.Operator,
                insertText: card.label,
                detail: card.description,
                range,
              });
            });

            // Suggest prefixed properties
            COMMON_PREFIXES.forEach((p) => {
              suggestions.push({
                label: `${p.prefix}:`,
                kind: monaco.languages.CompletionItemKind.Property,
                insertText: `${p.prefix}:$0`,
                insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                detail: `Property from ${p.prefix}`,
                range,
              });
            });
          }

          return { suggestions };
        },
      });
    }
  }, []);

  // Handle content change
  const handleChange: OnChange = useCallback(
    (newValue) => {
      if (newValue !== undefined) {
        onChange(newValue);
      }
    },
    [onChange]
  );

  // Update error markers when errors change
  useEffect(() => {
    if (!editorRef.current || !monacoRef.current) return;

    const monaco = monacoRef.current;
    const model = editorRef.current.getModel();
    if (!model) return;

    const markers: editor.IMarkerData[] = errors.map((error) => ({
      severity: monaco.MarkerSeverity.Error,
      startLineNumber: error.line,
      startColumn: error.column || 1,
      endLineNumber: error.line,
      endColumn: error.column ? error.column + 10 : model.getLineMaxColumn(error.line),
      message: error.message,
      source: 'shexstatements',
    }));

    monaco.editor.setModelMarkers(model, 'shexstatements', markers);
  }, [errors]);

  return (
    <div className="h-full w-full">
      <Editor
        height="100%"
        language={language}
        value={value}
        onChange={handleChange}
        onMount={handleEditorMount}
        theme={getMonacoTheme()}
        options={{
          readOnly,
          fontSize,
          wordWrap: wordWrap ? 'on' : 'off',
          minimap: { enabled: minimap },
          lineNumbers: lineNumbers ? 'on' : 'off',
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 2,
          fontFamily: "'JetBrains Mono', 'Fira Code', Monaco, Consolas, monospace",
          fontLigatures: true,
          renderWhitespace: 'selection',
          bracketPairColorization: { enabled: true },
          guides: {
            bracketPairs: true,
            indentation: true,
          },
        }}
      />
    </div>
  );
}
