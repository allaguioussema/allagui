/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './face_analyzer/templates/**/*.html',
    './templates/**/*.html',
    './static/src/**/*.js',
  ],
  theme: {
    extend: {
        colors: {
            ai: {
                50: '#e6f2ff',
                100: '#b3dcff',
                200: '#80c7ff',
                300: '#4db2ff',
                400: '#1a9dff',
                500: '#007bff', // Primary AI blue
                600: '#0059bf',
                700: '#00378a',
                800: '#001a4d',
                900: '#000c26'
            },
            neural: {
                100: '#f0f9ff',
                200: '#e0f2fe',
                300: '#bae6fd',
                400: '#7dd3fc',
                500: '#38bdf8',
                600: '#0284c7',
                700: '#0369a1',
                800: '#075985',
                900: '#0c4a6e'
            }
        },
        backgroundImage: {
            'ai-gradient': 'linear-gradient(135deg, #007bff 0%, #0059bf 100%)',
            'neural-grid': 'radial-gradient(rgba(56, 189, 248, 0.1) 1px, transparent 1px)',
        },
        boxShadow: {
            'ai-glow': '0 0 15px rgba(0, 123, 255, 0.3), 0 4px 6px rgba(0, 123, 255, 0.1)',
            'neural-shadow': '0 10px 25px rgba(56, 189, 248, 0.15)'
        },
        animation: {
            'pulse-glow': 'pulse-glow 2s infinite',
            'neural-pulse': 'neural-pulse 3s infinite'
        },
        keyframes: {
            'pulse-glow': {
                '0%, 100%': { 'box-shadow': '0 0 10px rgba(0, 123, 255, 0.3)' },
                '50%': { 'box-shadow': '0 0 20px rgba(0, 123, 255, 0.5)' }
            },
            'neural-pulse': {
                '0%, 100%': { transform: 'scale(1)' },
                '50%': { transform: 'scale(1.02)' }
            }
        },
        fontFamily: {
            'ai': ['Inter', 'system-ui', 'sans-serif']
        }
    },
  },
    plugins: [],
}
