# Plan de Fusión Arquitectónica: QBTC Unified System (Revisión 2.0)

## 1. Contexto y Problema

El análisis del sistema actual revela dos proyectos (`localGPT-main` y `qbtc-quantum-supreme`) que operan como sistemas acoplados de forma frágil. Esta arquitectura ha generado deuda técnica, manifestada en:

*   **Infraestructura Confusa**: Múltiples volúmenes de Docker en conflicto y configuraciones duplicadas.
*   **Código Poco Mantenible**: Uso de parches de rutas (`sys.path`) para resolver importaciones entre los proyectos.
*   **Despliegue Complejo**: Scripts de despliegue que no reflejan una arquitectura unificada.

La retroalimentación del equipo ha clarificado que no se trata de dos sistemas redundantes, sino de **dos productos distintos que deben coexistir y compartir un núcleo de IA común**:

1.  **Producto 1: LLM Cuántico**: Un modelo de lenguaje con métricas de rendimiento de élite, consumible a través de una API estándar (ej. por ROO CODE).
2.  **Producto 2: Sistema de Trading Cuántico (HFT)**: Un sistema que se conecta a Binance y utiliza el LLM Cuántico para mejorar la precisión de sus decisiones de trading.

Adicionalmente, se ha identificado una infraestructura de mensajería existente (`RabbitMQ`/`APISIX`) que es ideal para la orquestación.

## 2. Hipótesis de Solución

La refactorización a una **arquitectura de microservicios orquestados por eventos**, desplegados dentro de un monorepo unificado, es la solución óptima para consolidar los dos productos, resolver los problemas de acoplamiento y sentar una base robusta y escalable para el futuro.

## 3. Diagrama de la Arquitectura Propuesta

```mermaid
graph TD;
    subgraph "Cliente Externo (ROO CODE)"
        A[ROO CODE Client]
    end

    subgraph "API Gateway (APISIX)"
        B[APISIX]
    end

    subgraph "Sistema Unificado (Monorepo: qbtc-unified-system)"

        subgraph "Servicios"
            C[API Service for LLM]
            D[Trading Service (HFT)]
            E[Quantum Consciousness Core Service]
        end

        subgraph "Infraestructura de Mensajería"
            F[RabbitMQ Message Broker]
        end

        subgraph "Infraestructura de Datos"
            G[Supabase (PostgreSQL)]
            H[Redis (Cache)]
        end

        C --"Publica 'llm_request' a RabbitMQ"--> F;
        D --"Publica 'trading_analysis_request' a RabbitMQ"--> F;

        F --"Entrega 'llm_request' a Quantum Core"--> E;
        F --"Entrega 'trading_analysis_request' a Quantum Core"--> E;

        E --"Consume eventos de RabbitMQ"--> F;
        E --"Procesa con lógica cuántica"--> G;
        E --"Usa cache"--> H;
        E --"Publica 'llm_response' a RabbitMQ"--> F;
        E --"Publica 'trading_signal' a RabbitMQ"--> F;

        F --"Entrega 'llm_response' a API Service"--> C;
        F --"Entrega 'trading_signal' a Trading Service"--> D;

    end

    A --> B;
    B --> C;
```

## 4. Plan de Implementación por Fases

### Fase 1: Consolidar y Configurar la Infraestructura
*   **Objetivo**: Establecer una base de infraestructura única y centralizada.
*   **Acciones**:
    1.  Crear un directorio `qbtc-unified-system` que funcionará como el nuevo monorepo.
    2.  Dentro de `qbtc-unified-system`, crear una carpeta `infrastructure/`.
    3.  Mover y consolidar las configuraciones existentes de `RabbitMQ`, `APISIX`, `Supabase` y `Redis` a la carpeta `infrastructure/`.
    4.  Crear un único `docker-compose.yml` maestro en `infrastructure/` que orqueste el despliegue de toda la infraestructura base (RabbitMQ, APISIX, Supabase, Redis).
    5.  Definir y configurar los `exchanges` y `queues` necesarios en RabbitMQ a través de un archivo de definiciones o script de inicialización.

### Fase 2: Contenerizar los Servicios Principales
*   **Objetivo**: Aislar cada componente de la lógica de negocio en su propio microservicio contenerizado.
*   **Acciones**:
    1.  Crear una carpeta `services/` en la raíz del monorepo.
    2.  **`quantum-consciousness-service`**: Crear un subdirectorio `services/quantum_core/`. Mover la lógica del `QuantumConsciousnessCore26D` a este servicio. Su única responsabilidad será procesar eventos. Crear su `Dockerfile`.
    3.  **`llm-api-service`**: Crear `services/llm_api/`. Este servicio contendrá el servidor FastAPI que expone la API compatible con OpenAI. No contendrá lógica de IA. Crear su `Dockerfile`.
    4.  **`trading-hft-service`**: Crear `services/trading_hft/`. Este servicio contendrá la lógica de conexión con Binance y la gestión de órdenes. Crear su `Dockerfile`.

### Fase 3: Definir y Documentar el Contrato de Eventos
*   **Objetivo**: Establecer un "lenguaje" común y estricto para la comunicación entre servicios.
*   **Acciones**:
    1.  Crear una carpeta `event-schemas/` en la raíz del monorepo.
    2.  Definir, usando `JSON Schema`, la estructura de cada tipo de evento que fluirá por RabbitMQ (e.g., `llm_request.json`, `llm_response.json`, `trading_request.json`, `trading_signal.json`).
    3.  Documentar cada campo del esquema para asegurar claridad.

### Fase 4: Implementar la Lógica de Productores y Consumidores
*   **Objetivo**: "Cablear" los servicios al bus de eventos.
*   **Acciones**:
    1.  En el `llm-api-service`, implementar la lógica para recibir una solicitud HTTP, validarla, construir un evento `llm_request`, publicarlo en RabbitMQ y esperar una respuesta en una cola de respuesta temporal.
    2.  En el `quantum-consciousness-service`, implementar un consumidor que escuche las colas `q_llm_requests` y `q_trading_requests`. Al recibir un evento, procesa la lógica y publica el resultado en el `responses_exchange`.
    3.  En el `trading-hft-service`, implementar la lógica para consumir las señales de trading (`trading_signal`) y actuar en consecuencia.

### Fase 5: Configurar las Rutas y la Seguridad en el API Gateway (APISIX)
*   **Objetivo**: Exponer los servicios de forma segura y controlada al mundo exterior.
*   **Acciones**:
    1.  Configurar las rutas en `APISIX` para dirigir el tráfico entrante a los servicios correspondientes (ej. `/v1/chat/completions` -> `llm-api-service`).
    2.  Implementar plugins de APISIX para la gestión de autenticación (API Keys), rate limiting y logging centralizado de solicitudes.

### Fase 6: Realizar Pruebas Completas del Flujo de Eventos End-to-End
*   **Objetivo**: Validar que la nueva arquitectura funciona como un todo integrado.
*   **Acciones**:
    1.  Actualizar el script `test-quantum-system.py` para que actúe como un cliente HTTP que se comunica con el sistema a través de `APISIX`.
    2.  Diseñar pruebas que verifiquen el flujo completo: `Cliente -> APISIX -> LLM API Service -> RabbitMQ -> Quantum Core Service -> RabbitMQ -> LLM API Service -> Cliente`.
    3.  Añadir pruebas para el flujo del servicio de trading.
    4.  Verificar en la base de datos Supabase que las interacciones se registran correctamente.

## 5. Estado Final Deseado

Un único repositorio `qbtc-unified-system` que es fácil de clonar, instalar (`docker-compose up`) y ejecutar. Contiene:
*   **Servicios desacoplados y autónomos**.
*   **Infraestructura consolidada y centralizada**.
*   **Comunicación asíncrona y resiliente** a través de un bus de eventos.
*   **Dos productos claramente definidos y mantenibles** que comparten un núcleo de IA común.
*   **Eliminación completa de la deuda técnica** relacionada con el acoplamiento y las rutas.
