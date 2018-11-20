
const os = require('os');
const ifaces = os.networkInterfaces();
var interface_name = 'wlp2s0';
var get_ip_address = function(interface_name) {
    var ip = '0.0.0.0';
    if (interface_name != null) {
        Object.keys(ifaces).forEach(function(ifname) {
            ifaces[ifname].forEach(function(iface) {
                if ('IPv4' !== iface.family || iface.internal !== false) {
                    // skip over internal (i.e. 127.0.0.1) and non-ipv4 addresses
                    return;
                }

                // this interface has only one ipv4 adress
                if (ifname == interface_name) {
                    ip = iface.address;
                }
            });
        });
    };

    return ip
}

var interface_name = 'wlp2s0';
var ip_address = get_ip_address(interface_name);

module.exports = {

  dev: {
    filename: '[name]-bundle.js',
    //publicPath: 'http://localhost:8080/static/dist/', //!!! point to the dev server
    publicPath: 'http://'+ip_address+':8080/static/dist/', //!!! point to the dev server
    //publicPath: '/static/dist/',
    assetsSubDirectory: 'static',
    sourceMap: true,
    cssFilename: '[name].css'

  },

  prod: {
    filename: '[name]-bundle-[hash].js',
    publicPath: '/static/dist/',
    assetsSubDirectory: '',
    sourceMap: false,
    cssFilename: '[name]-bundle-[hash].css',
  }
};
