const path = require('path');
const config = require('./settings');

exports.assetsPath = function (_path) {
  const assetsSubDirectory = process.env.NODE_ENV === 'production'
    ? config.prod.assetsSubDirectory
    : config.dev.assetsSubDirectory;
  return path.posix.join(assetsSubDirectory, _path)
};
