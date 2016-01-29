var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');


module.exports = {
  entry: {
    admin: './src/admin/index.jsx',
    common: ['react', 'react-dom', 'antd']
  },

  output: {
    path: path.resolve(__dirname, "../app/static/bundle"),
    filename: '[name].js'
  },

  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        loader: 'babel',
        exclude: /node_modules/,
        query: { presets: ['react', 'es2015'] }
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract('style-loader',
            'css-loader?modules&localIdentName=[name]__[local]___[hash:base64:5]!postcss-loader')
      }
    ]
  },

  postcss: [
    require('autoprefixer')({ browsers: ['last 2 versions'] })
  ],

  resolve: {
    extensions: ['', '.js', '.json', '.jsx']
  },

  plugins: [
    new ExtractTextPlugin('[name].css'),
    new webpack.optimize.CommonsChunkPlugin("common", "common.js")
  ]
};
