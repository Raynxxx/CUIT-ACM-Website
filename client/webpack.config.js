var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var pagesPath = './src/pages';

module.exports = {
  entry: {
    admin: [
      'webpack-dev-server/client?http://localhost:3000',
      'webpack/hot/only-dev-server',
      pagesPath + '/admin'],
    common: ['react', 'react-dom', 'antd']
  },

  output: {
    path: path.resolve(__dirname, "build"),
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
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),
    new ExtractTextPlugin('[name].css'),
    new webpack.optimize.CommonsChunkPlugin("common", "common.js")
  ]
};
