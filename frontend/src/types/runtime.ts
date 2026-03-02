export type RuntimeMode = 'auto' | 'api' | 'wasm';

export function resolveRuntimeMode(mode: RuntimeMode): Exclude<RuntimeMode, 'auto'> {
  if (mode !== 'auto') {
    return mode;
  }

  const envRuntime = import.meta.env.VITE_RUNTIME_MODE as string | undefined;
  if (envRuntime === 'api' || envRuntime === 'wasm') {
    return envRuntime;
  }

  // GitHub Pages is static hosting; default to in-browser WASM runtime.
  if (typeof window !== 'undefined' && window.location.hostname.endsWith('github.io')) {
    return 'wasm';
  }

  return 'api';
}
