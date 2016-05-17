var path = require('path');
var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var env = process.env.WEBPACK_ENV;

var plugins = [
    new webpack.optimize.CommonsChunkPlugin("commons", "commons.js"),
    new ExtractTextPlugin('assets/[name].css'),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),
    new HtmlWebpackPlugin({
        title: '后台管理',
        template: path.resolve(__dirname, 'templates/index.html'),
        inject: 'body'
    })
];

if (env === 'build') {
    var UglifyJsPlugin = webpack.optimize.UglifyJsPlugin;
    plugins.push(new UglifyJsPlugin({ minimize: true }));
    outputFile = '[name].min.js';
} else {
    outputFile = '[name].js';
}

var config = {
    entry: {
        commons: ['react', 'react-dom'],
        index: ['./src/index.js']
    },

    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: outputFile
    },

    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                loaders: ['react-hot', 'babel'],
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
        extensions: ['', '.js', '.json', '.jsx']
    },

    plugins: plugins
};

module.exports = config;