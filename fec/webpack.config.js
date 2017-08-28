/* global __dirname */
/* jslint maxlen: false */

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

module.exports = [
  {
    entry: entries,
    plugins: [
      new webpack.SourceMapDevToolPlugin(),
      new ManifestPlugin({
        fileName: 'rev-manifest.json',
        basePath: '/static/js/'
      }),
      // new webpack.optimize.CommonsChunkPlugin({
      //   name: 'common',
      //   filename: 'common.js'
      // })
      // new webpack.optimize.UglifyJsPlugin()
    ],
    output: {
      filename: '[name]-[hash].js',
      path: path.resolve(__dirname, './dist/fec/static/js')
    },
    module: {
        loaders: [
            {
              test: /\.hbs/,
              use: ['handlebars-template-loader', 'cache-loader']
            }
        ]
    },
    resolve: {
      alias: {
        // There's a known issue with jquery.inputmask and webpack.
        // These aliases resolve the issues
        'jquery': path.join(__dirname, '../node_modules/jquery/dist/jquery.js'),
        'inputmask.dependencyLib': path.join(__dirname, '../node_modules/jquery.inputmask/dist/inputmask/inputmask.dependencyLib.js'),
        'inputmask/inputmask.date.extensions': path.join(__dirname, '../node_modules/jquery.inputmask/dist/inputmask/inputmask.date.extensions.js'),
        'inputmask': path.join(__dirname, '../node_modules/jquery.inputmask/dist/inputmask/inputmask.js'),
        'jquery.inputmask': path.join(__dirname, '../node_modules/jquery.inputmask/dist/inputmask/jquery.inputmask.js')
      }
    },
    node: {
      fs: 'empty'
    },
    watchOptions: {
      ignored: /node_modules/
    },
    stats: {
      assetSort: 'field',
      modules: false,
      warnings: false
    }
  },
  {
    name: 'legal',
    entry: {'legalApp': './fec/static/js/legal/LegalApp.js'},
    output: {
      filename: 'legalApp-[hash].js',
      path: path.resolve(__dirname, './dist/fec/static/js')
    },
    plugins: [
      new webpack.SourceMapDevToolPlugin(),
      new ManifestPlugin({
        fileName: 'rev-legal-manifest.json',
        basePath: '/static/js/'
      }),
    ],
    module: {
      loaders: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          loader: 'babel-loader',
          options: {
            presets: ['latest', 'react']
          }
        }
      ]
    },
    stats: {
      assetSort: 'field',
      modules: false,
      warnings: false
    }
  }
];
