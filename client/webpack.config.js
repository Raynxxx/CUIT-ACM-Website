var path = require('path');
var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var env = process.env.WEBPACK_ENV;

var commons = [
    'babel-polyfill', 'isomorphic-fetch', 'jwt-decode',
    'react', 'react-dom', 'redux', 'react-router',
    'react-redux', 'react-router-redux', 'redux-thunk'
];

var plugins = [
    new webpack.optimize.CommonsChunkPlugin("commons", "commons.js"),
    new ExtractTextPlugin('[name].css'),
    new webpack.NoErrorsPlugin()
    /*new HtmlWebpackPlugin({
        title: '后台管理',
        template: path.resolve(__dirname, 'templates/index.html'),
        inject: 'body'
    })*/
];

if (env === 'build') {
    var UglifyJsPlugin = webpack.optimize.UglifyJsPlugin;
    var OccurrenceOrderPlugin = webpack.optimize.OccurrenceOrderPlugin;
    plugins.push(new UglifyJsPlugin({ minimize: true }));
    plugins.push(new OccurrenceOrderPlugin());
}

var config = {
    entry: {
        commons: commons,
        index: ['./src/index.js']
    },

    output: {
        path: path.resolve(__dirname, '../app/static'),
        publicPath: 'static',
        filename: '[name].js'
    },

    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                loader: 'babel',
                exclude: /node_modules/
            },
            {
                test: /\.css/,
                loader: ExtractTextPlugin.extract('style-loader', 'css-loader')
            },
            {
                test: /\.less$/,
                loader: ExtractTextPlugin.extract('style-loader', 'css-loader!less-loader')
            }
        ]
    },

    resolve: {
        extensions: ['', '.js', '.json', '.jsx', '.less', '.css']
    },

    plugins: plugins
};

module.exports = config;