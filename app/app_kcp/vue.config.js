module.exports = {
    devServer: {
        proxy: {
            // '^/nlp': {
            //     target: 'http://10.0.0.25:8991',
            // },
            '^/nlp': {
                target: 'http://localhost:8919',
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