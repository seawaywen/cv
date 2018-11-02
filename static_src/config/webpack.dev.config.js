const webpack = require('webpack');
const merge = require('webpack-merge');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require("clean-webpack-plugin");
const baseWebpackConfig = require('./webpack.base.config');


const devWebpackConfig = merge(baseWebpackConfig, {
  mode: 'development',

  devtool: 'eval-source-map',

  devServer: {
      contentBase: "./dist",
      historyApiFallback: true,
      inline: true,
      hot: true,
      host: process.env.HOST || 'localhost',
      port: process.env.PORT || '8080' ,
      open: false,
      clientLogLevel: 'warning',
      overlay: {
        warnings: false,
        errors: true,
      },
      publicPath: '/static/dist/',
      proxy: {},
      //quiet: true, // necessary for FriendlyErrorsPlugin
      watchOptions: {
        poll: false
      },
      headers: {
        "Access-Control-Allow-Origin": "\*",
      }
  },

  plugins: [

    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('development')
    }),

    /*
    new CleanWebpackPlugin('dist/*.*', {
      root: __dirname,
      verbose: true,
      dry: false
    }),
    */

    /*
    new HtmlWebpackPlugin({
      template: __dirname + "/index.html",
      chunks: ['main'],
    }),
    */

    new webpack.NamedModulesPlugin(),

    new webpack.HotModuleReplacementPlugin(),

    new webpack.NoEmitOnErrorsPlugin()

  ],
});


let buildEntryPoint = (entryPoint) =>{
  return [
    'webpack-dev-server/client?http://localhost:8080/',
    entryPoint
  ]
};

devWebpackConfig.entry.portfolio = buildEntryPoint(baseWebpackConfig.entry.portfolio);
devWebpackConfig.entry.profile= buildEntryPoint(baseWebpackConfig.entry.profile);
devWebpackConfig.entry.blog= buildEntryPoint(baseWebpackConfig.entry.blog);
//console.log(devWebpackConfig);

module.exports = devWebpackConfig;
