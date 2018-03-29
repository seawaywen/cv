const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require("clean-webpack-plugin");
const BundleTracker = require('webpack-bundle-tracker');


var buildEntryPoint = function(entryPoint){
  return [
    'webpack-dev-server/client?http://localhost:8080/',
    entryPoint
  ]
};

module.exports = {
  entry: {
    main: buildEntryPoint(__dirname + '/src/js/main.js'),
    profile: buildEntryPoint(__dirname + '/src/js/profile.js'),
  },
  output: {
    filename: '[name]-bundle.js',
    //filename: "[name]-bundle-[hash].js",
    path: path.resolve(__dirname, 'dist'),
    //hotUpdateChunkFilename: 'hot-update.js',
    //hotUpdateMainFilename: 'hot-update.json',
    //publicPath: '/static/dist/',
    publicPath: 'http://localhost:8080/static/dist/' //!!! point to the dev server
  },
  
  devtool: 'eval-source-map',
  
  devServer: {
      contentBase: "./dist",
      historyApiFallback: true,
      inline: true,
      hot: true,
      clientLogLevel: 'warning',
      //host: process.env.HOST || 'localhost', 
      //port: process.env.PORT || 8080, 
      open: false, 
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
    /*
    new CleanWebpackPlugin('dist/*.*', {
      root: __dirname,
      verbose: true,
      dry: false
    }),
    */
    
    new webpack.BannerPlugin('memodir.com copyright reserverd@2018'),
    /* 
    new HtmlWebpackPlugin({
      template: __dirname + "/index.html",
      chunks: ['main'],
    }),
    */
    
    new BundleTracker({filename: './webpack-stats.json'}),
    
    new webpack.NamedModulesPlugin(),
    
    new webpack.HotModuleReplacementPlugin(),
    

  ],
};

