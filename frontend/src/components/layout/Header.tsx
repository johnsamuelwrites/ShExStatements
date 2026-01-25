/**
 * Application header component.
 */

import { ThemeToggle } from '../common/ThemeToggle';

export function Header() {
  return (
    <header className="h-14 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 flex items-center justify-between px-4">
      <div className="flex items-center gap-3">
        <svg
          className="w-8 h-8 text-shex-700 dark:text-shex-400"
          viewBox="0 0 100 100"
          fill="currentColor"
        >
          <path d="M50 5 L95 30 L95 70 L50 95 L5 70 L5 30 Z" fill="none" stroke="currentColor" strokeWidth="4" />
          <text x="50" y="60" textAnchor="middle" fontSize="32" fontWeight="bold">S</text>
        </svg>
        <div>
          <h1 className="text-lg font-semibold text-gray-900 dark:text-white">
            ShExStatements
          </h1>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Shape Expression Generator
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <nav className="hidden md:flex items-center gap-4 text-sm">
          <a
            href="https://shexstatements.readthedocs.io/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-600 dark:text-gray-300 hover:text-shex-700 dark:hover:text-shex-400 transition-colors"
          >
            Documentation
          </a>
          <a
            href="https://github.com/johnsamuelwrites/ShExStatements"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-600 dark:text-gray-300 hover:text-shex-700 dark:hover:text-shex-400 transition-colors"
          >
            GitHub
          </a>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-600 dark:text-gray-300 hover:text-shex-700 dark:hover:text-shex-400 transition-colors"
          >
            API
          </a>
        </nav>
        <ThemeToggle />
      </div>
    </header>
  );
}
