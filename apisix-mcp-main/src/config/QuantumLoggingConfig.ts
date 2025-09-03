import { QUANTUM_MAINFRAME } from '@quantum/config/QuantumMainframeConstants';

export const QUANTUM_LOGGING_CONFIG = {
    BUFFER: {
        SIZE: 100,
        FLUSH_INTERVAL: 5000, // ms
    },
    PERSISTENCE: {
        ENABLED: true,
        TYPE: 'file' as const,
        PATH: './logs/quantum',
        RETENTION_DAYS: 30,
        MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
        COMPRESSION: true
    },
    LEVELS: {
        DEBUG: {
            value: 0,
            color: '\x1b[34m' // blue
        },
        INFO: {
            value: 1,
            color: '\x1b[32m' // green
        },
        WARN: {
            value: 2,
            color: '\x1b[33m' // yellow
        },
        ERROR: {
            value: 3,
            color: '\x1b[31m' // red
        },
        QUANTUM: {
            value: 4,
            color: '\x1b[35m' // magenta
        }
    },
    FORMAT: {
        TIMESTAMP: 'ISO', // 'ISO' | 'UNIX' | 'RELATIVE'
        INCLUDE_SOURCE: true,
        INCLUDE_COHERENCE: true,
        MAX_CONTEXT_DEPTH: 3
    },
    COHERENCE: {
        MIN_LEVEL: QUANTUM_MAINFRAME.CONFIG.COHERENCE_THRESHOLD * 0.95,
        ALERT_ON_LOW: true
    }
} as const;

export type LogLevel = keyof typeof QUANTUM_LOGGING_CONFIG.LEVELS;
export type PersistenceType = typeof QUANTUM_LOGGING_CONFIG.PERSISTENCE.TYPE;
export type TimestampFormat = typeof QUANTUM_LOGGING_CONFIG.FORMAT.TIMESTAMP;

export interface LoggingOptions {
    bufferSize?: number;
    flushInterval?: number;
    persistence?: {
        enabled: boolean;
        type: PersistenceType;
        path?: string;
    };
    format?: {
        timestamp: TimestampFormat;
        includeSource: boolean;
        includeCoherence: boolean;
    };
}