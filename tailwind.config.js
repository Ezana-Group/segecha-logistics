module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
      },
      colors: {
        brand: {
          primary: '#0057A0',
          primaryDark: '#003F73',
          accent: '#FFC107',
          background: '#F7F9FB',
          text: '#222222',
          muted: '#666666',
          success: '#28a745',
          danger: '#dc3545',
          whatsapp: '#25D366'
        }
      }
    }
  },
  plugins: [],
} 