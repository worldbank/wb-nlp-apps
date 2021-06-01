module.exports = {
    // publicPath: process.env.NODE_ENV === 'production' ? '/jdc/' : '/jdc/',
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
            },
            // 'https://data.worldbank.org/dist/main-7bb673272fb53924a8c2.js': {
            //     target: "http://localhost:8000/static/files/wdi/main-7bb673272fb53924a8c2.js",
            //     changeOrigin: true
            // },
            // 'https://data.worldbank.org/dist/main-daa0e86aeffba93ef358.js': {
            //     target: "http://localhost:8000/static/files/wdi/main-daa0e86aeffba93ef358.js",
            //     changeOrigin: true
            // },
            // 'https://data.worldbank.org/dist/vendor-daa0e86aeffba93ef358.js': {
            //     target: "http://localhost:8000/static/files/wdi/vendor-daa0e86aeffba93ef358.js",
            //     changeOrigin: true
            // }
        }
    }
}