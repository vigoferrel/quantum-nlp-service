import { ConfigService } from '../config/config.service';
import { LLMResponse, QuantumEmbedding, TrainingMetrics } from '../types/quantum-ai.types';

export class QuantumAIService {
  private readonly apiKey: string;
  private readonly baseUrl: string;
  private readonly config: ConfigService;

  constructor(config: ConfigService) {
    this.config = config;
    this.apiKey = this.config.get('QUANTUM_AI_API_KEY');
    this.baseUrl = this.config.get('QUANTUM_AI_ENDPOINT');
  }

  /**
   * Genera texto usando el modelo LLM cuántico
   * @param prompt El prompt de entrada
   * @param options Opciones de generación como temperatura, tokens max, etc
   */
  async generateText(prompt: string, options?: {
    temperature?: number;
    maxTokens?: number;
    topP?: number;
  }): Promise<LLMResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          prompt,
          ...options
        })
      });

      if (!response.ok) {
        throw new Error(`Error al generar texto: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en generateText:', error);
      throw new Error('Fallo al generar texto con el modelo LLM');
    }
  }

  /**
   * Calcula embeddings cuánticos para el texto dado
   * @param text El texto para procesar
   */
  async computeQuantumEmbeddings(text: string): Promise<QuantumEmbedding> {
    try {
      const response = await fetch(`${this.baseUrl}/embeddings`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({ text })
      });

      if (!response.ok) {
        throw new Error(`Error al computar embeddings: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en computeQuantumEmbeddings:', error);
      throw new Error('Fallo al calcular embeddings cuánticos');
    }
  }

  /**
   * Entrena o fine-tunea el modelo con datos específicos
   * @param trainingData Los datos de entrenamiento
   * @param modelConfig Configuración del modelo y entrenamiento
   */
  async trainModel(
    trainingData: Array<{input: string; output: string}>,
    modelConfig: {
      epochs: number;
      batchSize: number;
      learningRate: number;
    }
  ): Promise<TrainingMetrics> {
    try {
      const response = await fetch(`${this.baseUrl}/train`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          trainingData,
          modelConfig
        })
      });

      if (!response.ok) {
        throw new Error(`Error al entrenar modelo: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en trainModel:', error);
      throw new Error('Fallo al entrenar el modelo');
    }
  }

  /**
   * Verifica el estado de la API y la conectividad
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`
        }
      });

      return response.ok;
    } catch (error) {
      console.error('Error en healthCheck:', error);
      return false;
    }
  }
}
