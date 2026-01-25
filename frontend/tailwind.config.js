/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // ShExStatements brand colors
        shex: {
          50: '#e6f7f5',
          100: '#b3e8e3',
          200: '#80d9d1',
          300: '#4dcabf',
          400: '#1abbad',
          500: '#00a396',
          600: '#008a7f',
          700: '#006d64',
          800: '#005049',
          900: '#003d33',
          950: '#002821',
        },
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'Monaco', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
};
