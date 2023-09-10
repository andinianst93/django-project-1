/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./encyclopedia/templates/encyclopedia/**/*.html'],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

