const webpack = require('webpack');
const path = require('path');
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
      },
      {
        test: /\.css$/,
        use: [
          {
            loader: "style-loader"
          }, {
            loader: "css-loader",
            options: {
              modules: true, 
              localIdentName: '[name]_[local]_[hash:base64:6]' 
            }
          }, {
            loader: "postcss-loader"
          }
        ]
      },
      {
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

    new BundleTracker({filename: './webpack-stats.json'}),
  ],
};

