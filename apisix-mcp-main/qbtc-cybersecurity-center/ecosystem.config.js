module.exports = {
  apps: [
    {
      name: 'quantum-core',
      script: './index.js',
      instances: 1,
      exec_mode: 'fork',
      watch: true,
      env: {
        NODE_ENV: 'development',
        PORT: 7000
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 7000
      }
    },
    {
      name: 'quantum-security',
      script: './core/quantum-security.js',
      instances: 1,
      exec_mode: 'fork',
      watch: true,
      env: {
        NODE_ENV: 'development',
        PORT: 7100
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 7100
      }
    },
    {
      name: 'api-gateway',
      script: './core/api-gateway.js',
      instances: 1,
      exec_mode: 'fork',
      watch: true,
      env: {
        NODE_ENV: 'development',
        PORT: 7200
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 7200
      }
    },
    {
      name: 'quantum-monitor',
      script: './core/quantum-monitor.js',
      instances: 1,
      exec_mode: 'fork',
      watch: true,
      env: {
        NODE_ENV: 'development',
        PORT: 7300
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 7300
      }
    },
    {
      name: 'web-dashboard',
      script: './core/web-interface.js',
      instances: 1,
      exec_mode: 'fork',
      watch: true,
      env: {
        NODE_ENV: 'development',
        PORT: 7400
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 7400
      }
    }
  ]
};
