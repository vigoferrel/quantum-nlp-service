import { EventEmitter } from 'events';

/**
 * Un bus de eventos singleton para desacoplar la comunicación
 * entre los diferentes componentes del sistema cuántico de trading.
 */
class EventBus extends EventEmitter {
    private static instance: EventBus;

    private constructor() {
        super();
        // Aumentar el límite de listeners para evitar warnings en caso de
        // que múltiples componentes escuchen el mismo evento.
        this.setMaxListeners(20);
    }

    /**
     * Obtiene la instancia única (singleton) del EventBus.
     * @returns La instancia de EventBus.
     */
    public static getInstance(): EventBus {
        if (!EventBus.instance) {
            EventBus.instance = new EventBus();
        }
        return EventBus.instance;
    }
}

// Exportar una única instancia para ser usada en todo el proyecto.
export const tradingEventBus = EventBus.getInstance();