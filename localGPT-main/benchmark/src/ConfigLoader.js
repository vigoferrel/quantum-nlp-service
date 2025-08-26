const fs = require('fs').promises;
const path = require('path');

class ConfigLoader {
  constructor(configPath) {
    this.configPath = configPath || path.join(__dirname, '../config.json');
  }

  async load() {
    try {
      const data = await fs.readFile(this.configPath, 'utf8');
      const config = JSON.parse(data);
      this.validate(config);
      return config;
    } catch (error) {
      console.error(`Error loading or parsing config file at ${this.configPath}: ${error.message}`);
      throw new Error('Configuration failed to load.');
    }
  }

  validate(config) {
    if (!config.simulatedEnvironment || !config.testSuite) {
      throw new Error('Configuration must include "simulatedEnvironment" and "testSuite" keys.');
    }
    if (!Array.isArray(config.testSuite) || config.testSuite.length === 0) {
      throw new Error('"testSuite" must be a non-empty array.');
    }
    // Add more specific validation as needed
  }
}

module.exports = ConfigLoader;
