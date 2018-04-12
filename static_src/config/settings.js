module.exports = {
  dev: {
    filename: '[name]-bundle.js',
    publicPath: 'http://localhost:8080/static/dist/', //!!! point to the dev server
    //publicPath: '/static/dist/',
    assetsSubDirectory: 'static',
    sourceMap: false,
    cssFilename: '[name].css'

  },

  prod: {
    filename: '[name]-bundle-[hash].js',
    publicPath: '/static/dist/',
    assetsSubDirectory: '',
    sourceMap: true,
    cssFilename: '[name]-[contenthash].css'

  }
};
