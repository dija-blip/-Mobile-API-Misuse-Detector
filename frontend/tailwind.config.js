/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        brand: { 50: '#f0f9ff', 500: '#0ea5e9', 900: '#0c4a6e' },
        threat: { low: '#22c55e', medium: '#f59e0b', high: '#f97316', critical: '#ef4444' },
      },
    },
  },
  plugins: [],
}
