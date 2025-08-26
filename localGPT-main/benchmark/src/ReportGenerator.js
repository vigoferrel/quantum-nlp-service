const fs = require('fs').promises;
const path = require('path');

function classifyConstrainedSupremacy(score) {
  if (score >= 90) return 'SUPREMACÍA EFICIENTE TRASCENDENTAL - Inteligencia Adaptativa Cuántica';
  if (score >= 75) return 'ALTO RENDIMIENTO EN RESTRICCIONES - Optimización Holística';
  if (score >= 50) return 'OPERACIONAL BAJO PRESIÓN';
  return 'REQUIERE OPTIMIZACIÓN';
}

class ReportGenerator {
  constructor(environmentConfig) {
    this.environment = environmentConfig;
    this.logsDir = path.join(__dirname, '../../logs');
  }

  async save(finalScore, results) {
    await this.ensureLogsDirExists();

    const report = {
      benchmarkVersion: 'v6.0-Modular',
      timestamp: new Date().toISOString(),
      simulatedEnvironment: this.environment,
      constrainedSupremacyIndex: finalScore,
      classification: classifyConstrainedSupremacy(finalScore),
      detailedResults: results,
    };

    const filename = `vigoleonrocks-constrained-supremacy-report-${Date.now()}.json`;
    const fullPath = path.join(this.logsDir, filename);

    try {
      await fs.writeFile(fullPath, JSON.stringify(report, null, 2));
      return fullPath;
    } catch (error) {
      console.error(`Failed to save report to ${fullPath}: ${error.message}`);
      throw error;
    }
  }

  async ensureLogsDirExists() {
    try {
      await fs.mkdir(this.logsDir, { recursive: true });
    } catch (error) {
      console.error(`Could not create logs directory at ${this.logsDir}: ${error.message}`);
      throw error;
    }
  }
}

module.exports = ReportGenerator;
