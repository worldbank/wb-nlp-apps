module.exports = {
    devServer: {
        proxy: {
            // '^/nlp': {
            //     target: 'http://10.0.0.25:8991',
            // },
            '^/nlp': {
                target: 'http://localhost:8919',
            },
            '^/redoc': {
                target: 'http://localhost:8919',
                changeOrigin: true
            },
            '^/openapi.json': {
                target: 'http://localhost:8919',
                changeOrigin: true
            },
            '^/api': {
                target: 'http://10.0.0.3:8088',
            },
            '^/dfr': {
                target: 'http://10.0.0.3:8088',
                changeOrigin: true
            }
        }
    }
}