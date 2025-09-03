export interface LLMResponse {
  text: string;
  tokenCount: number;
  model: string;
  metadata: {
    temperature: number;
    topP: number;
    completionTokens: number;
    promptTokens: number;
    totalTokens: number;
    processingTime: number;
  };
}

export interface QuantumEmbedding {
  vector: number[];
  dimensions: number;
  model: string;
  metadata: {
    processingTime: number;
    quantumCircuitDepth: number;
    quantumGates: number;
  };
}

export interface TrainingMetrics {
  epochMetrics: Array<{
    epoch: number;
    loss: number;
    accuracy: number;
    validationLoss?: number;
    validationAccuracy?: number;
  }>;
  finalMetrics: {
    trainLoss: number;
    trainAccuracy: number;
    validationLoss?: number;
    validationAccuracy?: number;
    trainingTime: number;
    modelParameters: number;
  };
  modelInfo: {
    name: string;
    version: string;
    architecture: string;
    quantumLayers: number;
  };
}
