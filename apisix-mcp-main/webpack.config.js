import { dirname } from 'path';
import { fileURLToPath } from 'url';
import TsconfigPathsPlugin from 'tsconfig-paths-webpack-plugin';

const __dirname = dirname(fileURLToPath(import.meta.url));

export default {
  mode: 'development',
  entry: './src/quantum-apisix-tiger-types-ultimate.ts',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
    plugins: [
      new TsconfigPathsPlugin({
        configFile: './tsconfig.json',
        extensions: ['.ts', '.tsx', '.js']
      })
    ],
    alias: {
      '@': `${__dirname}/src`,
      '@tools': `${__dirname}/src/tools`,
      '@utils': `${__dirname}/src/utils`
    }
  },
  output: {
    filename: 'quantum-apisix-vigoleonrocks-ultimate.js',
    path: `${__dirname}/dist`,
  },
  devtool: 'source-map'
};