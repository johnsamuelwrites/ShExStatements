/**
 * Settings state management using Zustand.
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

type Theme = 'light' | 'dark' | 'system';
type PanelLayout = 'horizontal' | 'vertical';

interface SettingsState {
  // Theme settings
  theme: Theme;

  // Editor settings
  fontSize: number;
  wordWrap: boolean;
  minimap: boolean;
  lineNumbers: boolean;

  // Layout settings
  panelLayout: PanelLayout;
  showVisualization: boolean;

  // Auto-convert settings
  autoConvert: boolean;
  autoConvertDelay: number;

  // Actions
  setTheme: (theme: Theme) => void;
  setFontSize: (size: number) => void;
  setWordWrap: (wrap: boolean) => void;
  setMinimap: (show: boolean) => void;
  setLineNumbers: (show: boolean) => void;
  setPanelLayout: (layout: PanelLayout) => void;
  setShowVisualization: (show: boolean) => void;
  setAutoConvert: (auto: boolean) => void;
  setAutoConvertDelay: (delay: number) => void;
  reset: () => void;
}

const initialState = {
  theme: 'system' as Theme,
  fontSize: 14,
  wordWrap: true,
  minimap: false,
  lineNumbers: true,
  panelLayout: 'horizontal' as PanelLayout,
  showVisualization: false,
  autoConvert: true,
  autoConvertDelay: 500,
};

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      ...initialState,

      setTheme: (theme) => {
        set({ theme });
        applyTheme(theme);
      },

      setFontSize: (fontSize) => set({ fontSize }),

      setWordWrap: (wordWrap) => set({ wordWrap }),

      setMinimap: (minimap) => set({ minimap }),

      setLineNumbers: (lineNumbers) => set({ lineNumbers }),

      setPanelLayout: (panelLayout) => set({ panelLayout }),

      setShowVisualization: (showVisualization) => set({ showVisualization }),

      setAutoConvert: (autoConvert) => set({ autoConvert }),

      setAutoConvertDelay: (autoConvertDelay) => set({ autoConvertDelay }),

      reset: () => {
        set(initialState);
        applyTheme(initialState.theme);
      },
    }),
    {
      name: 'shexstatements-settings',
      onRehydrateStorage: () => (state) => {
        if (state) {
          applyTheme(state.theme);
        }
      },
    }
  )
);

/**
 * Apply the theme to the document.
 */
function applyTheme(theme: Theme): void {
  const root = document.documentElement;

  if (theme === 'system') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.classList.toggle('dark', prefersDark);
  } else {
    root.classList.toggle('dark', theme === 'dark');
  }
}

// Listen for system theme changes
if (typeof window !== 'undefined') {
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    const state = useSettingsStore.getState();
    if (state.theme === 'system') {
      document.documentElement.classList.toggle('dark', e.matches);
    }
  });
}
