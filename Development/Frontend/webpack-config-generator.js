const path = require('path');

class WebpackConfigGenerator {
  constructor(options = {}) {
    this.mode = options.mode || 'production';
    this.entry = options.entry || './src/index.js';
    this.output = options.output || './dist';
    this.devServer = options.devServer || false;
  }

  generateConfig() {
    const config = {
      mode: this.mode,
      entry: this.entry,
      output: {
        path: path.resolve(__dirname, this.output),
        filename: '[name].[contenthash].js',
        clean: true,
      },
      module: {
        rules: this.getLoaders(),
      },
      plugins: this.getPlugins(),
      optimization: this.getOptimization(),
      resolve: {
        extensions: ['.js', '.jsx', '.ts', '.tsx', '.json'],
        alias: {
          '@': path.resolve(__dirname, 'src'),
          '@components': path.resolve(__dirname, 'src/components'),
          '@utils': path.resolve(__dirname, 'src/utils'),
        },
      },
    };

    if (this.devServer) {
      config.devServer = {
        port: 3000,
        hot: true,
        open: true,
        historyApiFallback: true,
      };
    }

    return config;
  }

  getLoaders() {
    return [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react',
              '@babel/preset-typescript',
            ],
          },
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        type: 'asset/resource',
      },
    ];
  }

  getPlugins() {
    const plugins = [];
    
    // HTML Plugin
    plugins.push({
      plugin: 'HtmlWebpackPlugin',
      options: {
        template: './public/index.html',
        minify: this.mode === 'production',
      },
    });

    // Bundle Analyzer (production only)
    if (this.mode === 'production') {
      plugins.push({
        plugin: 'BundleAnalyzerPlugin',
        options: {
          analyzerMode: 'static',
          openAnalyzer: false,
        },
      });
    }

    return plugins;
  }

  getOptimization() {
    if (this.mode === 'production') {
      return {
        minimize: true,
        splitChunks: {
          chunks: 'all',
          cacheGroups: {
            vendor: {
              test: /[\\/]node_modules[\\/]/,
              name: 'vendors',
              priority: 10,
            },
            common: {
              minChunks: 2,
              priority: 5,
              reuseExistingChunk: true,
            },
          },
        },
        runtimeChunk: 'single',
      };
    }
    return {};
  }

  printConfig() {
    const config = this.generateConfig();
    console.log('📦 Webpack Configuration Generated:');
    console.log(JSON.stringify(config, null, 2));
    return config;
  }
}

// Example usage
const generator = new WebpackConfigGenerator({
  mode: 'production',
  entry: './src/index.tsx',
  output: './dist',
  devServer: false,
});

const config = generator.printConfig();

console.log('\n✅ Webpack config ready for use!');
console.log('💡 Features included:');
console.log('  - TypeScript/React support');
console.log('  - CSS processing with PostCSS');
console.log('  - Code splitting');
console.log('  - Bundle optimization');
console.log('  - Asset handling');

module.exports = WebpackConfigGenerator;
