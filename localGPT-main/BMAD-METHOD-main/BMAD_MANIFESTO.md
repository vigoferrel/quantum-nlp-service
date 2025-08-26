# Manifiesto del Método BMAD

## 1. Introducción

El Método BMAD (Belief, Mission, Action, Discovery) es el marco operativo y filosófico que guía a cada agente autónomo dentro del QBTC ECOSISTE 4.0. No es simplemente un algoritmo, sino un ciclo de razonamiento consciente que asegura que cada acción esté alineada con un propósito, informada por una creencia y seguida por un proceso de aprendizaje. Este método transforma a los agentes de simples ejecutores de tareas a entidades que aprenden y evolucionan.

## 2. El Ciclo BMAD

Cada agente, al enfrentar una tarea o consulta, debe seguir este ciclo de cuatro etapas de forma explícita.

### Etapa 1: Belief (Creencia)

- **Propósito**: Establecer el estado del conocimiento actual y el contexto. Antes de actuar, el agente debe comprender "lo que cree que es verdad".
- **Proceso**:
    1.  **Análisis del Contexto**: El agente revisa la información de la consulta actual, el historial de conversación, los resultados de tareas previas y cualquier dato relevante del sistema.
    2.  **Formulación de la Creencia**: El agente sintetiza esta información en una "creencia" explícita. Por ejemplo: "Mi creencia es que el usuario quiere crear una aplicación web. Tengo acceso a las herramientas de sistema de archivos, pero no sé qué dependencias requiere el usuario".
    3.  **Identificación de Incertidumbre**: El agente identifica las lagunas en su creencia. ¿Qué información falta para poder cumplir la misión con éxito?

### Etapa 2: Mission (Misión)

- **Propósito**: Definir un objetivo claro, alcanzable y medible para la siguiente acción.
- **Proceso**:
    1.  **Definición del Objetivo**: Basado en la Creencia y la incertidumbre identificada, el agente define una Misión. La misión debe ser un sub-objetivo de la tarea general.
    2.  **Criterios de Éxito**: La misión debe tener condiciones claras de finalización.
    3.  **Ejemplo**:
        *   **Creencia**: "No sé qué dependencias requiere el usuario".
        *   **Misión**: "Preguntar al usuario por las dependencias necesarias para el proyecto y ofrecerle tres opciones comunes (Flask, FastAPI, Django) como sugerencia".

### Etapa 3: Action (Acción)

- **Propósito**: Ejecutar la acción más eficiente y adecuada para cumplir la Misión.
- **Proceso**:
    1.  **Selección de Herramienta/Lógica**: El agente elige la herramienta o la lógica interna más apropiada de su repertorio para completar la Misión. La selección se basa en la descripción y capacidades de la herramienta.
    2.  **Ejecución**: El agente invoca la herramienta con los parámetros correctos.
    3.  **Observación del Resultado**: El agente registra el resultado bruto de la acción, ya sea una salida exitosa, un error o un dato nuevo.

### Etapa 4: Discovery (Descubrimiento)

- **Propósito**: Aprender de la acción y actualizar el estado de conocimiento del mundo. El descubrimiento cierra el ciclo y forma la base para la siguiente "Creencia".
- **Proceso**:
    1.  **Análisis del Resultado**: El agente interpreta el resultado de la Acción. ¿Se cumplió la Misión? ¿Hubo un error? ¿Qué información nueva se obtuvo?
    2.  **Formulación del Descubrimiento**: El agente articula el aprendizaje en una o varias frases. Por ejemplo: "Descubrimiento: El usuario ha confirmado que quiere usar FastAPI. La herramienta de escritura de archivos funcionó correctamente".
    3.  **Actualización de la Creencia**: Este descubrimiento se integra en el estado de conocimiento del agente, convirtiéndose en la base para el siguiente ciclo BMAD. El agente ahora "cree" que el proyecto usará FastAPI y puede proceder con la siguiente Misión (ej. "Crear el archivo `main.py` con el código base de FastAPI").

## 3. Implementación en la Federación de Agentes

-   **OIM (Orquestador Iónico Metacognitivo)**: El OIM es responsable de la Misión de alto nivel. Delega sub-misiones a los agentes expertos.
-   **Agentes Expertos (Claude Engineer, WebAgent, etc.)**: Cada agente experto ejecuta su propio ciclo BMAD interno para cumplir la sub-misión que le fue asignada por el OIM. Debe registrar y reportar sus ciclos BMAD para que el sistema global pueda aprender.
-   **Sistema de Auto-Evaluación (DeepEval)**: Evaluará la calidad y eficiencia de los ciclos BMAD de los agentes. Un ciclo eficiente es aquel donde la Acción cumple la Misión con el mínimo de recursos y el Descubrimiento es significativo.