/**
 * Declaración de tipos mínima para satisfacer a TypeScript
 * para el módulo @binance/connector.
 */
declare module '@binance/connector' {
  export class Spot {
    constructor(apiKey: string, apiSecret: string, options?: any);
    
    // Declara los metodos que se usan en el codigo para que TS los conozca
    time(): Promise<any>;
    tickerPrice(symbol: string): Promise<{ symbol: string; price: string; }>;

    // Permite cualquier otro metodo o propiedad para evitar errores de tipo
    [key: string]: any;
  }
}