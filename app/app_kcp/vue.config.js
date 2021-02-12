module.exports = {
    devServer: {
        proxy: {
            '^/nlp': {
                target: 'http://10.0.0.25:8991',
            },
            '^/api': {
                target: 'http://10.0.0.25:8088',
            },
            '^/dfr': {
                target: 'http://10.0.0.25:8088',
                changeOrigin: true
            }
        }
    }
}