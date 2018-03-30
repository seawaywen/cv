const path = require('path');
const webpack = require('webpack');
const merge = require('webpack-merge');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin');
const baseWebpackConfig = require('./webpack.base.config');
const utils = require('./utils');
const settings = require('./settings');


const prodWebpackConfig = merge(baseWebpackConfig, {
  devtool: false,

  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production')
    }),

    // UglifyJs do not support ES6+, you can also use babel-minify for better treeshaking: https://github.com/babel/minify
    new UglifyJsPlugin({
      /*compress: {
        warnings: false
      },*/
      sourceMap: settings.prod.sourceMap,
      parallel: true
    }),


    // Compress extracted CSS. We are using this plugin so that possible
    // duplicated CSS from different components can be deduped.
    new OptimizeCSSPlugin({
      cssProcessorOptions: settings.prod.sourceMap
        ? { safe: true, map: { inline: false } }
        : { safe: true }
    }),
    // keep module.id stable when vender modules does not change
    new webpack.HashedModuleIdsPlugin(),

    // copy custom static assets
    /*
    new CopyWebpackPlugin([
      {
        from: path.resolve(__dirname, '../../static'),
        to: settings.prod.assetsSubDirectory,
        ignore: ['.*']
      }
    ])
    */
  ],
});


module.exports = prodWebpackConfig;
