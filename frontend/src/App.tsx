/**
 * Main application component.
 */

import { useCallback } from 'react';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { Header } from './components/layout/Header';
import { Toolbar } from './components/layout/Toolbar';
import { ShExEditor } from './components/editor/ShExEditor';
import { OutputEditor } from './components/editor/OutputEditor';
import { useEditorStore } from './stores/editorStore';
import { SHEX_LANGUAGE_ID } from './components/editor/shex-language';
import { resolveRuntimeMode } from './types/runtime';

function App() {
  const {
    inputContent,
    outputContent,
    delimiter,
    runtimeMode,
    errors,
    warnings,
    isConverting,
    setInputContent,
  } = useEditorStore();
  const resolvedRuntime = resolveRuntimeMode(runtimeMode);

  // Handle input content change
  const handleInputChange = useCallback(
    (value: string) => {
      setInputContent(value);
    },
    [setInputContent]
  );

  return (
    <div className="h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Header />
      <Toolbar />

      <main className="flex-1 min-h-0">
        <PanelGroup direction="horizontal" className="h-full">
          {/* Input Panel */}
          <Panel defaultSize={50} minSize={30}>
            <div className="h-full flex flex-col border-r border-gray-200 dark:border-gray-700">
              <div className="h-8 px-4 flex items-center justify-between bg-gray-100 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  ShExStatements Input
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  {inputContent.split('\n').length} lines
                </span>
              </div>
              <div className="flex-1 min-h-0">
                <ShExEditor
                  value={inputContent}
                  onChange={handleInputChange}
                  errors={errors}
                />
              </div>
            </div>
          </Panel>

          {/* Resize Handle */}
          <PanelResizeHandle className="w-1 bg-gray-200 dark:bg-gray-700 hover:bg-shex-500 dark:hover:bg-shex-600 transition-colors cursor-col-resize" />

          {/* Output Panel */}
          <Panel defaultSize={50} minSize={30}>
            <div className="h-full flex flex-col">
              <div className="h-8 px-4 flex items-center justify-between bg-gray-100 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Generated ShEx
                </span>
                <div className="flex items-center gap-2">
                  {isConverting && (
                    <span className="text-xs text-shex-600 dark:text-shex-400 flex items-center gap-1">
                      <span className="animate-pulse">Converting...</span>
                    </span>
                  )}
                  {warnings.length > 0 && (
                    <span className="text-xs text-yellow-600 dark:text-yellow-400">
                      {warnings.length} warning{warnings.length > 1 ? 's' : ''}
                    </span>
                  )}
                  {errors.length > 0 && (
                    <span className="text-xs text-red-600 dark:text-red-400">
                      {errors.length} error{errors.length > 1 ? 's' : ''}
                    </span>
                  )}
                  {outputContent && (
                    <button
                      onClick={() => navigator.clipboard.writeText(outputContent)}
                      className="text-xs text-gray-500 dark:text-gray-400 hover:text-shex-600 dark:hover:text-shex-400 transition-colors"
                      title="Copy to clipboard"
                    >
                      Copy
                    </button>
                  )}
                </div>
              </div>
              <div className="flex-1 min-h-0">
                {errors.length > 0 && !outputContent ? (
                  <ErrorDisplay errors={errors} />
                ) : (
                  <OutputEditor
                    value={outputContent}
                    language={SHEX_LANGUAGE_ID}
                  />
                )}
              </div>
            </div>
          </Panel>
        </PanelGroup>
      </main>

      {/* Status Bar */}
      <footer className="h-6 bg-shex-800 dark:bg-shex-900 text-white text-xs flex items-center justify-between px-4">
        <div className="flex items-center gap-4">
          <span>ShExStatements v1.0.0</span>
          <span className="text-shex-300">|</span>
          <span>Delimiter: {delimiter === '|' ? 'Pipe' : delimiter === ',' ? 'Comma' : 'Semicolon'}</span>
          <span className="text-shex-300">|</span>
          <span>Runtime: {resolvedRuntime.toUpperCase()}</span>
        </div>
        <div className="flex items-center gap-4">
          <a
            href="https://github.com/johnsamuelwrites/ShExStatements"
            target="_blank"
            rel="noopener noreferrer"
            className="text-shex-300 hover:text-white transition-colors"
          >
            GPL-3.0
          </a>
        </div>
      </footer>
    </div>
  );
}

function ErrorDisplay({ errors }: { errors: Array<{ line: number; message: string }> }) {
  return (
    <div className="h-full p-4 bg-red-50 dark:bg-red-900/20 overflow-auto">
      <h3 className="text-sm font-medium text-red-800 dark:text-red-300 mb-2">
        Conversion Errors
      </h3>
      <ul className="space-y-2">
        {errors.map((error, index) => (
          <li
            key={index}
            className="text-sm text-red-700 dark:text-red-400 bg-white dark:bg-gray-800 rounded p-2 border border-red-200 dark:border-red-800"
          >
            <span className="font-mono text-red-500 dark:text-red-500">
              Line {error.line}:
            </span>{' '}
            {error.message}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
