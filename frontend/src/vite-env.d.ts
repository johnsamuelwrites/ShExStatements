/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_RUNTIME_MODE?: 'api' | 'wasm';
  readonly VITE_API_BASE_URL?: string;
  readonly VITE_API_DOCS_URL?: string;
  readonly VITE_BASE_PATH?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
