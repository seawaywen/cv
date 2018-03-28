const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require("clean-webpack-plugin");
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  entry: {
    main: __dirname + '/src/js/main.js',
    profile: __dirname + '/src/js/profile.js',
  },
  output: {
    //filename: 'bundle.js',
    filename: "[name]-bundle-[hash].js",
    path: path.resolve(__dirname, 'dist'),
    publicPath: '/static/dist/',
  },
  
  devtool: 'eval-source-map',
  
  devServer: {
      contentBase: "./dist",
      historyApiFallback: true,
      inline: true,
      hot: true
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
      }

    ]
  },
  
  plugins: [
    new webpack.BannerPlugin('memodir.com copyright reserverd@2018'),
    
    
    new webpack.HotModuleReplacementPlugin(),
    
    new CleanWebpackPlugin('dist/*.*', {
      root: __dirname,
      verbose: true,
      dry: false
    }),
    
    new BundleTracker({filename: './webpack-stats.json'}),

  ],
};

