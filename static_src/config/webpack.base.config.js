const webpack = require('webpack');
const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

const settings = require('./settings');
const utils = require('./utils');

const isProduction = process.env.NODE_ENV === 'production';
const sourceMapEnabled = isProduction ? settings.prod.sourceMap
  : settings.dev.sourceMap;

function resolve (dir) {
  return path.join(__dirname, '..', dir)
}


module.exports = {
  context: path.resolve(__dirname, '../'),

  entry: {
    main: './src/js/main.js',
    profile: './src/js/profile.js'
  },

  output: {
    filename: isProduction
      ? settings.prod.filename : settings.dev.filename,
    path: path.resolve(__dirname, '../dist'),
    publicPath: isProduction
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
        use:
          ['css-hot-loader'].concat(ExtractTextPlugin.extract({
            fallback: "style-loader",
            use: [
              {
                loader: "css-loader",
                options: {
                  sourceMap: sourceMapEnabled
                }
              },
              {
                loader: "postcss-loader",
                options: {
                  sourceMap: 'inline'
                }
              }
            ]
          }))
      },
      {
        test: /\.less$/,
        use:
          ['css-hot-loader'].concat(ExtractTextPlugin.extract({
            fallback: "style-loader",
            use: [
              {
                loader: "css-loader",
                options: {
                  sourceMap: sourceMapEnabled
                }
              }, {
                loader: "postcss-loader",
                options: {
                  sourceMap: 'inline'
                }
              }, {
                loader: "less-loader",
                options: {
                  sourceMap: sourceMapEnabled,
                  precision: 8,
                  data: "$ENV: " + "PRODUCTION" + ";"
                }
              }
            ]
          }))
      },
      {
        test: /\.(png|svg|gif|jpe?g)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: utils.assetsPath('img/[name].[hash:7].[ext]')
        }
      },
      {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: utils.assetsPath('fonts/[name].[hash:7].[ext]')
        }
      },
      {
        test: /\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: utils.assetsPath('media/[name].[hash:7].[ext]')
        }
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: utils.cssLoaders({
            sourceMap: isProduction,
            extract: isProduction
          }),
          cssSourceMap: sourceMapEnabled,
          transformToRequire: {
            video: 'src',
            source: 'src',
            img: 'src',
            image: 'xlink:href'
          }
        }
      }
    ]
  },

  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      '@': resolve('src'),
      '__STATIC__': resolve('static')
    }
  },

  plugins: [

    new webpack.BannerPlugin('memodir.com Copyright reserves@2018'),

    new BundleTracker({filename: './webpack-stats.json'}) ,

    new ExtractTextPlugin({
      filename: isProduction
        ? settings.prod.cssFilename : settings.dev.cssFilename
    })
  ]
};