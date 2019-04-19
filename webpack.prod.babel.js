import webpack from 'webpack'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'

import merge from 'webpack-merge'
import common from './webpack.common.babel'

export default merge(common, {
    optimization: {
        minimize: true
    },
    stats: {
        children: false,
        chunks: true,
        assets: true,
        modules: true,
        hash: true
    },
    plugins: [
        new webpack.optimize.AggressiveMergingPlugin(),
        new webpack.LoaderOptionsPlugin({
            minimize: true,
            debug: false
        }),
        new MiniCssExtractPlugin({
            filename: '[name].[hash].css',
            chunkFilename: '[id].[hash].css'
        })
    ]
})
