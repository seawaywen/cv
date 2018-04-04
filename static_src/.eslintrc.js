module.exports = {
  env: {
    "browser": true,
  },
  root: true,
  parser: 'babel-eslint',
  parserOptions: {
    sourceType: 'module'
  },

  extends: "eslint:recommended",
  plugins: [
    'html'
  ],
  parserOptions: {
    "sourceType": "module"
  },
  rules: {
    // keep 2 spaces for indentation
    "indent": [
      "error", 2
    ],
    "linebreak-style": [
      "error", "unix"
    ],
    // use the double quotes for JS files
    "quotes": [
      "error", "double"
    ],
    // must contain the semicolon
    "semi": [
      "error", "always"
    ],
    // allow paren-less arrow functions
    'arrow-parens': 0,
    // allow async-await
    'generator-star-spacing': 0,
    // allow debugger during development
    'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0

  }
};