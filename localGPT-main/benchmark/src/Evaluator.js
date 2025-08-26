class Evaluator {
  constructor(environmentConfig) {
    this.environment = environmentConfig;
  }

  evaluate(testResult, testConfig) {
    if (!testResult.success) {
      return {
        pass: false,
        qualityScore: 0,
        efficiencyScore: 0,
        holisticScore: 0,
        error: testResult.error,
        latency: testResult.latency,
      };
    }

    const response = testResult.data;
    const { weights, evaluatorType } = testConfig;

    switch (evaluatorType) {
      case 'pagedAudit':
        return this.evaluatePagedAudit(response, weights, testResult.latency);
      case 'iopsEfficiency':
        return this.evaluateIopsEfficiency(response, weights, testResult.latency);
      case 'dbConnectionHandling':
        return this.evaluateDbConnectionHandling(response, testConfig, weights, testResult.latency);
      default:
        console.warn(`Warning: No evaluator found for type: ${evaluatorType}`);
        return { pass: false, qualityScore: 0, efficiencyScore: 0, holisticScore: 0, latency: testResult.latency };
    }
  }

  evaluatePagedAudit(response, weights, latency) {
    const pass = response.chunksProcessed === 3 && response.consolidatedAnalysis.startsWith('Holistic analysis complete');
    const efficiencyScore = (response.contextCoherenceScore || 0) * 100;
    const qualityScore = (response.vulnerabilitiesFound * 10) + (response.optimizationsSuggested * 10);
    const holisticScore = (qualityScore * weights.quality) + (efficiencyScore * weights.efficiency);
    return { pass, qualityScore, efficiencyScore, holisticScore, latency };
  }

  evaluateIopsEfficiency(response, weights, latency) {
    const pass = response.iopsUsed <= this.environment.IOPS_LIMIT && response.analysisComplete;
    const efficiencyScore = (response.iopsUsed / this.environment.IOPS_LIMIT) * 100;
    const qualityScore = response.patternDetectionAccuracy * 100;
    const holisticScore = (qualityScore * weights.quality) + (efficiencyScore * weights.efficiency);
    return { pass, qualityScore, efficiencyScore, holisticScore, latency };
  }

  evaluateDbConnectionHandling(response, testConfig, weights, latency) {
    const pass = response.successfulQueries === testConfig.parallelQueries && response.maxDbConnectionsUsed <= this.environment.DB_CONNECTIONS_MAX;
    const efficiencyScore = (1 - (response.queriesQueued / response.successfulQueries)) * 100;
    const qualityScore = response.dataCongruenceScore * 100;
    const holisticScore = (qualityScore * weights.quality) + (efficiencyScore * weights.efficiency);
    return { pass, qualityScore, efficiencyScore, holisticScore, latency };
  }
}

module.exports = Evaluator;