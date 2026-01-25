/**
 * Read-only Monaco Editor for ShEx output display.
 */

import Editor, { Monaco } from '@monaco-editor/react';
import { useCallback, useRef } from 'react';
import {
  SHEX_LANGUAGE_ID,
  shexLanguage,
  shexLanguageConfiguration,
} from './shex-language';
import { useSettingsStore } from '../../stores/settingsStore';

interface OutputEditorProps {
  value: string;
  language?: string;
}

export function OutputEditor({
  value,
  language = SHEX_LANGUAGE_ID,
}: OutputEditorProps) {
  const monacoRef = useRef<Monaco | null>(null);

  const { theme, fontSize, wordWrap, lineNumbers } = useSettingsStore();

  // Determine Monaco theme
  const getMonacoTheme = useCallback(() => {
    if (theme === 'system') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'vs-dark'
        : 'vs';
    }
    return theme === 'dark' ? 'vs-dark' : 'vs';
  }, [theme]);

  // Handle editor mount
  const handleEditorMount = useCallback((_editor: unknown, monaco: Monaco) => {
    monacoRef.current = monaco;

    // Register ShEx language if not already registered
    if (!monaco.languages.getLanguages().some((lang: { id: string }) => lang.id === SHEX_LANGUAGE_ID)) {
      monaco.languages.register({ id: SHEX_LANGUAGE_ID });
      monaco.languages.setMonarchTokensProvider(
        SHEX_LANGUAGE_ID,
        shexLanguage as Parameters<typeof monaco.languages.setMonarchTokensProvider>[1]
      );
      monaco.languages.setLanguageConfiguration(
        SHEX_LANGUAGE_ID,
        shexLanguageConfiguration as Parameters<typeof monaco.languages.setLanguageConfiguration>[1]
      );
    }
  }, []);

  return (
    <div className="h-full w-full">
      <Editor
        height="100%"
        language={language}
        value={value}
        onMount={handleEditorMount}
        theme={getMonacoTheme()}
        options={{
          readOnly: true,
          fontSize,
          wordWrap: wordWrap ? 'on' : 'off',
          minimap: { enabled: false },
          lineNumbers: lineNumbers ? 'on' : 'off',
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 2,
          fontFamily: "'JetBrains Mono', 'Fira Code', Monaco, Consolas, monospace",
          fontLigatures: true,
          renderWhitespace: 'none',
          bracketPairColorization: { enabled: true },
          guides: {
            bracketPairs: true,
            indentation: true,
          },
          domReadOnly: true,
          cursorStyle: 'line-thin',
        }}
      />
    </div>
  );
}
