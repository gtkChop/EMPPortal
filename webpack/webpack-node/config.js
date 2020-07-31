const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const webpack = require("webpack");

module.exports = {
    watch: true,
    optimization: {
        minimize: true,
        minimizer: [
            new UglifyJsPlugin({
                include: /\.min\.js$/})
        ]
    },
    entry: './src/main.js',
    mode: 'development',
    output: {
        filename: 'index.min.js',
        path: '/home/static/js'
    },
    module: {
        rules: [
            {
                test: /\.s(a|c)ss$/,
                use: [
                    'style-loader',
                     MiniCssExtractPlugin.loader,
                     'css-loader',
                     'sass-loader'
                ]
            },
             {
                test: /\.css$/i,
                use: [
                    'to-string-loader',
                    'css-loader'
                ],
            },
        ],
    },
     resolve: {
        extensions: ['.js', '.jsx', '.scss']
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery"
        }),
        new MiniCssExtractPlugin({
            filename: '../css/index.min.css',
        }),
    ]
};
