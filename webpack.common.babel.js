import webpack from 'webpack'
import path from 'path'
import git from 'git-rev-sync'

import { VueLoaderPlugin } from 'vue-loader'
import CleanWebpackPlugin from 'clean-webpack-plugin'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'
import FriendlyErrorsWebpackPlugin from 'friendly-errors-webpack-plugin'
import HtmlWebpackPlugin from 'html-webpack-plugin'

export const SOURCE_DIR = path.resolve(__dirname, 'frontend')
export const OUTPUT_DIR = path.resolve('static/dist')
export const DJANGO_SETTINGS_MODULE = process.env.DJANGO_SETTINGS_MODULE
export const IS_DEV_SERVER = process.argv.find(v => v.includes('webpack-dev-server')) !== undefined
export const HOST = process.env.HOST || '127.0.0.1'
export const USE_HTTPS = process.env.WEBPACK_USE_HTTPS === 'true'
export const ENV = process.env.NODE_ENV || 'development'
export const IS_DEV = ENV === 'development'

const miniCssLoader = IS_DEV ? 'vue-style-loader' : MiniCssExtractPlugin.loader

export default {
    entry: {
        main: [ 'app' ]
    },
    output: {
        filename: '[name].[hash].js',
        chunkFilename: '[name].[contenthash].js',
        path: OUTPUT_DIR,
        publicPath: `${ IS_DEV && IS_DEV_SERVER ? `http${ USE_HTTPS ? 's' : '' }://${ HOST }:8080` : '' }/static/dist/`,
        sourceMapFilename: 'js/[name].[hash].js.map'
    },
    resolve: {
        modules: [ SOURCE_DIR, 'node_modules' ],
        extensions: [ '.js', '.vue', '.json' ],
        alias: {
            vue$: 'vue/dist/vue.esm.js',
            '@': SOURCE_DIR
        }
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                exclude: /node_modules/
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                include: [ SOURCE_DIR ],
                exclude: /node_modules/,
                options: {
                    cacheDirectory: true,
                    envName: 'dev'
                }
            },
            {
                test: /\.styl(us)?$/,
                use: [
                    miniCssLoader,
                    'css-loader',
                    {
                        loader: 'postcss-loader',
                        options: { sourceMap: true }
                    },
                    'stylus-loader'
                ]
            },
            {
                test: /\.scss$/,
                use: [
                    miniCssLoader,
                    'css-loader', {
                        loader: 'postcss-loader',
                        options: { sourceMap: true }
                    },
                    'sass-loader' ]
            },
            {
                test: /\.(png|jpg|gif)$/,
                loader: 'file-loader'
            },
            {
                test: /\.css$/,
                use: [ miniCssLoader, 'css-loader' ]
            },
            { test: /\.html$/,
                use: [ {
                    loader: 'html-loader',
                    options: { minimize: true }
                } ]
            }
        ]
    },
    optimization: {
        runtimeChunk: false,
        splitChunks: {
            cacheGroups: {
                default: false,
                common: {
                    chunks: 'initial',
                    name: 'common',
                    priority: 2,
                    minChunks: 2
                }
            }
        }
    },
    plugins: [
        new VueLoaderPlugin(),
        new FriendlyErrorsWebpackPlugin(),
        new CleanWebpackPlugin(),
        new HtmlWebpackPlugin({
            template: `${ SOURCE_DIR }/app/core/index.html`,
            chunksSortMode: 'none',
            chunks: [ 'main', 'common' ]
        }),
        new webpack.DefinePlugin({
            __DEV__: JSON.stringify(ENV === 'development'),
            __TEST__: JSON.stringify(ENV === 'test'),
            __PROD__: JSON.stringify(ENV === 'production'),
            'process.env.NODE_ENV': JSON.stringify(ENV),
            DJANGO_SETTINGS_MODULE: JSON.stringify(DJANGO_SETTINGS_MODULE),
            GITINFO: JSON.stringify({
                short: git.short(),
                long: git.long(),
                branch: git.branch()
            })
        })
    ]
}
