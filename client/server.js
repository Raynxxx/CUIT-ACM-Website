var webpack = require('webpack');
var WebpackDevServer = require('webpack-dev-server');
var config = require('./webpack.config');

config.entry.index.unshift(
    "webpack-dev-server/client?http://localhost:3000/",
    "webpack/hot/dev-server"
);

new WebpackDevServer(webpack(config), {
    publicPath: config.output.path,
    hot: true,
    historyApiFallback: true,
    stats: { colors: true }
}).listen(3000, 'localhost', function (err, result) {
    if (err) console.log(err);
    console.log('Listening at localhost:3000');
});