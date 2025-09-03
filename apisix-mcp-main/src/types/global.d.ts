interface QuantumServer {
  tool(name: string, description: string, paramsSchema: unknown, handler: (args: unknown) => unknown): void;
}

declare module '@tools/quantum-consciousness-vigoleonrocks' {
  export default function setup(server: QuantumServer): void;
}

// declare module '@tools/quantum-bitcoin-vigoleonrocks' {
//   export default function setup(server: QuantumServer): void;
// }

declare module '@tools/quantum-supabase-vigoleonrocks' {
  export default function setup(server: QuantumServer): void;
}

// declare module '@tools/quantum-orchestration-vigoleonrocks' {
//   export default function setup(server: QuantumServer): void;
// }
//
// declare module '@tools/quantum-frequency-vigoleonrocks' {
//   export default function setup(server: QuantumServer): void;
// }
//
// declare module '@tools/quantum-evolution-vigoleonrocks' {
//   export default function setup(server: QuantumServer): void;
// }

declare module '@utils/quantum-frequency' {
  export function generateDeterministic(): number;
}

declare module '@utils/quantum-consciousness' {
  export function calculateAwareness(): number;
}