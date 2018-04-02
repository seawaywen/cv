const webpack = require('webpack');
const path = require('path');
//const ExtractTextPlugin = require('extract-text-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleTracker = require('webpack-bundle-tracker');

const settings = require('./settings');

module.exports = {
  context: path.resolve(__dirname, '../'),

  entry: {
    main: './src/js/main.js',
    profile: './src/js/profile.js',
  },

  output: {
    filename: process.env.NODE_ENV === 'production'
      ? settings.prod.filename : settings.dev.filename,
    path: path.resolve(__dirname, '../dist'),
    publicPath: process.env.NODE_ENV === 'production'
      ? settings.prod.publicPath : settings.dev.publicPath
  },

  module: {
    rules: [
      {
        test: /(\.jsx|\.js)$/,
        use: {
          loader: "babel-loader"
        },
        exclude: /node_modules/
      }, {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          }, {
            loader: "css-loader",
            options: {
              modules: true,
              localIdentName: '[name]_[local]_[hash:base64:6]'
            }
          }]
      }, {
        test: /\.less$/,
        use: [
            MiniCssExtractPlugin.loader,
            {
              loader: "css-loader"
            }, {
              loader: "less-loader",
              options: {
                sourceMap: true,
                precision: 8,
                data: "$ENV: " + "PRODUCTION" + ";"
              }
          }
        ]
      }, {
        test: /\.(png|svg|jpg|gif)$/,
        use: [
          'file-loader'
        ]
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        use: [
          'file-loader'
        ]
      }
    ]
  },
  
  plugins: [

    new webpack.BannerPlugin('memodir.com copyright reserves@2018'),

    new BundleTracker({filename: './webpack-stats.json'}) ,

    /*new ExtractTextPlugin({
        allChunks: true
    }) */

    new MiniCssExtractPlugin({
      // Options similar to the same options in webpackOptions.output
      // both options are optional
      //filename: '[name]-[hash:6].css',
      filename: '[name].css',
      chunkFilename: "[id].css"
    })
  ],
};

