/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        bg:        '#060e09',
        'bg-card': '#0c1f13',
        'bg-card2':'#0f2a19',
        border:    '#1a4d27',
        teal:      '#00e5b0',
        green:     '#28f07c',
        'green-dim':'#1aaa55',
        'text-dim':'#7aad90',
        danger:    '#ff5f5f',
        warn:      '#ffc857',
      },
      fontFamily: {
        sans: ['Segoe UI', 'system-ui', 'sans-serif'],
        mono: ['Consolas', 'monospace'],
      },
      animation: {
        spin: 'spin .8s linear infinite',
        pulse: 'pulse 1s cubic-bezier(0.4,0,0.6,1) infinite',
      },
    },
  },
  plugins: [],
}
