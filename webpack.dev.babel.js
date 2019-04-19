import webpack from 'webpack'

import merge from 'webpack-merge'

import SimpleProgressWebpackPlugin from 'simple-progress-webpack-plugin'

import common, { HOST, IS_DEV_SERVER, OUTPUT_DIR, USE_HTTPS } from './webpack.common.babel'

const config = merge(common, {
    devtool: 'eval-source-map',
    output: { publicPath: '/' },
    devServer: {
        host: HOST,
        port: 8080,
        disableHostCheck: true,
        historyApiFallback: true,
        overlay: {
            warnings: true,
            errors: true
        },
        hot: true,
        contentBase: OUTPUT_DIR,
        headers: { 'Access-Control-Allow-Origin': '*' },
        proxy: [ {
            context: [
                '/admin',
                '/static',
                '/media',
                '/api'
            ],
            target: 'http://127.0.0.1:8000'
        } ]
    },
    performance: {
        hints: false
    },
    plugins: [
        new SimpleProgressWebpackPlugin(),
        new webpack.NamedModulesPlugin(),
        new webpack.HotModuleReplacementPlugin()
    ]
})

if (IS_DEV_SERVER && USE_HTTPS) {
    const fs = require('fs')
    if (process.env.HTTPS_CRT_PATH && process.env.HTTPS_KEY_PATH && process.env.HTTPS_CA_PEM) {
        config.devServer.https = {
            cert: fs.readFileSync(process.env.HTTPS_CRT_PATH),
            key: fs.readFileSync(process.env.HTTPS_KEY_PATH),
            ca: fs.readFileSync(process.env.HTTPS_CA_PEM)
        }
    }
}

export default config
