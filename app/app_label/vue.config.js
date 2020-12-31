module.exports = {
    devServer: {
        proxy: {
            '^/api': {
                target: 'http://10.0.0.25:8088',
            }
        }
    }
}
