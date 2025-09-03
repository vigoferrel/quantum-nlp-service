/**
 * Declaración de tipos mínima para simular el SDK de MCP
 * y permitir que el resto del proyecto compile.
 */
declare module '@modelcontextprotocol/sdk/server/mcp.js' {
  export class McpServer {
    constructor(options: { name: string; version: string });
    tool(name: string, description: string, schema: any, handler: any): void;
    connect(transport: any): Promise<void>;
    // Permitir cualquier otra propiedad para evitar errores
    [key: string]: any;
  }
}

declare module '@modelcontextprotocol/sdk/server/stdio.js' {
  export class StdioServerTransport {
    constructor();
  }
}