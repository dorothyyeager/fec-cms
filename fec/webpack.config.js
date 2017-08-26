/* global __dirname */

var path = require('path');
var webpack = require('webpack');
var ManifestPlugin = require('webpack-manifest-plugin');

var fs = require('fs');

var entries = {
  'init': './fec/static/js/init.js',
  'data-init': './fec/static/js/data-init.js'
};


fs.readdirSync('./fec/static/js/pages').forEach(function(f) {
  if (f.search('.js') < 0 ) { return; } // Skip non-js files
  var name = f.split('.js')[0];
  var p = path.join('./fec/static/js/pages', f);
  entries[name] = './' + p;
});

module.exports = {
  entry: entries,
  plugins: [
    new webpack.SourceMapDevToolPlugin(),
    new ManifestPlugin({
      fileName: 'rev-manifest.json',
      basePath: '/static/js/'
    }),
  ],
  output: {
    filename: '[name]-[hash].js',
    path: path.resolve(__dirname, './dist/fec/static/js')
  },
  module: {
      loaders: [
          {
            test: /\.hbs/,
            loader: 'handlebars-template-loader'
          }
      ]
  },
  resolve: {
    alias: {
      'jquery': path.join(__dirname, '../node_modules/jquery/dist/jquery.js'),
      'inputmask.dependencyLib': path.join(__dirname, '../node_modules/jquery.inputmask/dist/inputmask/inputmask.dependencyLib.js'),
      'inputmask/inputmask.date.extensions': path.join(__dirname, '../node_modules/jquery.inputmask/dist/inputmask/inputmask.date.extensions.js'),
      'inputmask': path.join(__dirname, '../node_modules/jquery.inputmask/dist/inputmask/inputmask.js'),
      'jquery.inputmask': path.join(__dirname, '../node_modules/jquery.inputmask/dist/inputmask/jquery.inputmask.js')
    }
  },
  node: {
    fs: 'empty'
  }
};