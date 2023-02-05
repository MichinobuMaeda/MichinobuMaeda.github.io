const defaultTheme = require('tailwindcss/defaultTheme')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    fontFamily: {
      ...defaultTheme.fontFamily,
      sans: [
        '"Hiragino Kaku Gothic Pro"',
        '"Hiragino Sans"',
        '"Meiryo"',
        '"メイリオ"',
        '"MS Pgothic"',
        '"ＭＳ Ｐゴシック"',
        '"Osaka"',
        'sans-serif',
        'Helvetica',
        'Helvetica Neue',
        'Arial',
        'Verdana'
      ],
    },
    extend: {},
  },
  plugins: [],
}
