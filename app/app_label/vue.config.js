module.exports = {
    devServer: {
        proxy: {
            '^/api': {
                target: 'http://10.0.0.25:8088',
            },
            '^/dfr': {
                target: 'http://10.0.0.25:8088',
                changeOrigin: true
            },
            '^/nlp_api': {
                target: 'http://10.0.0.25:8088',
            }
        }
    }
}
