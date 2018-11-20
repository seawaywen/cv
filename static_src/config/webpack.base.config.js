const webpack = require('webpack');
const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin')

const settings = require('./settings');
const utils = require('./utils');

const isProduction = process.env.NODE_ENV === 'production';
const sourceMapEnabled = isProduction ? settings.prod.sourceMap : settings.dev.sourceMap;

//console.log(process.env)
function resolve (dir) {
  return path.join(__dirname, '..', dir)
}


module.exports = {
  context: path.resolve(__dirname, '../'),

  entry: {
    base: './src/js/base.js',
    portfolio: './src/js/portfolio.js',
    profile: './src/js/profile.js',
    blog: './src/js/blog.js'
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
      /*
      {
        enforce: 'pre',
        test: /\.(js|vue)$/,
        loader: 'eslint-loader',
        exclude: /node_modules/
      },
      */
      {
        test: /(\.js)$/,
        loader: "babel-loader",
        exclude: file => (
          /node_modules/.test(file) &&
          !/\.vue\.js/.test(file)
        )
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
      },
      {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            //loader: isProduction ? MiniCssExtractPlugin.loader : 'vue-style-loader',
          },
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
      },
      {
        test: /\.less$/,
        use: [
          {
            //loader: isProduction ? MiniCssExtractPlugin.loader : 'vue-style-loader',
            loader: MiniCssExtractPlugin.loader,
          },
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
        test: require.resolve("blueimp-file-upload"),
        loader: "imports-loader?define=>false"
      },
    ],

  },

  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      '@': resolve('src'),
      'vue$': 'vue/dist/vue.esm.js',
      '__STATIC__': resolve('static')
    }
  },

  plugins: [

    new webpack.BannerPlugin('memodir.com copyright reserves@2018'),

    new VueLoaderPlugin(),

    new BundleTracker({filename: './dist/webpack-stats.json'}) ,

    new MiniCssExtractPlugin({
        filename: isProduction ? '[name].[hash].css' : '[name].css',
        chunkFilename: isProduction ? '[id].[hash].css' : '[id].css',
    }),

    new ExtractTextPlugin({
      filename: isProduction ? settings.prod.cssFilename : settings.dev.cssFilename
    })

  ]
};
