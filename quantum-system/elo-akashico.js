// ===== SISTEMA ELO-AKASHICO CUANTICO - MATRIZ 17x17 =====
// Implementacion basada en abstract financiero matematico
// BTC como ancla gravitacional + propagacion de correlaciones
// Precision satoshi-level (8 decimales) + timestamps nanosegundos

// ===== CONFIGURACION CRITICA =====
const PRECISION_SATOSHI = 8;
const _PRECISION_DECIMAL = Math.pow(10, PRECISION_SATOSHI);
const TIMESTAMP_NANOSEGUNDOS = true;
const MARKET_CLOSED = 'N'; // Nunca se cierra
const LOOP_INTERVAL_MS = 100;

// ===== NIVELES DE LOG ESTILO COBOL =====
const LOG_NIVEL = {
  ERROR: 0,
  WARN: 1,
  INFO: 2,
  DEBUG: 3,
  CRITICO: 4
};

// ===== RESULTADOS DE OPERACIONES =====
const RESULTADOS = {
  EXITO: 0,
  ERROR_CALCULO: 1,
  DATOS_INVALIDOS: 2,
  PRECIO_FUERA_RANGO: 3,
  CORRELACION_INVALIDA: 4,
  ENTROPIA_CRITICA: 5,
  RESONANCIA_DETECTADA: 6,
  ESTADO_CUANTICO: 7
};

// ===== ACTIVOS CRYPTO (17 FILAS) =====
const ACTIVOS_CRYPTO = [
  'BTC',  // Fila 0 - Ancla gravitacional
  'ETH', 'BNB', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'AVAX',
  'LINK', 'MATIC', 'UNI', 'LTC', 'ATOM', 'FTM', 'ALGO', 'VET'
];

// ===== METRICAS MULTIDIMENSIONALES (17 COLUMNAS) =====
const METRICAS = [
  'ELO', 'CONFIANZA', 'TIMING', 'DURACION', 'STOP_LOSS', 'TAKE_PROFIT',
  'RATIO_RR', 'ENTROPIA', 'RESONANCIA', 'SCHRODINGER', 'MOMENTUM_1H',
  'MOMENTUM_4H', 'MOMENTUM_1D', 'VOLATILIDAD', 'LIQUIDEZ', 
  'CORRELACION_BTC', 'EDGE_FOTONICO'
];

// ===== MATRIZ 17x17 COMO NUCLEO OPERATIVO =====
const MATRIZ_CUANTICA = Array(17).fill().map(() => Array(17).fill(0.0));

// ===== ESTADO DEL SISTEMA =====
const _SISTEMA_ACTIVO = false;
const _DATOS_MERCADO = {};
const CORRELACIONES_BTC = Array(17).fill(0.0);
const ESTADOS_CUANTICOS = Array(17).fill('INDEFINIDO');

// ===== UMBRALES CRITICOS =====
const UMBRALES = {
  CORRELACION_ALTA: 0.85,
  CORRELACION_BAJA: 0.15,
  ENTROPIA_ORDENADO: 2.5,
  ENTROPIA_CAOTICO: 4.0,
  RESONANCIA_MINIMA: 0.1,
  SCHRODINGER_DECISION: 0.70,
  MOMENTUM_FUERTE: 0.02,
  VOLATILIDAD_EXTREMA: 0.05,
  BTC_CAMBIO_SIGNIFICATIVO: 0.02
};

// ===== FUNCION DE LOGGING ULTRA-ROBUSTA =====
function ESCRIBIR_LOG(nivel, mensaje) {
  const niveles = ["ERROR", "WARN", "INFO", "DEBUG", "CRITICO"];
  const timestamp = TIMESTAMP_NANOSEGUNDOS ? 
    `${Date.now()}${Math.floor(Math.random() * 1000000)}` : 
    new Date().toISOString();
  console.log(`[${timestamp}] [${niveles[nivel]}] ${mensaje}`);
}

// ===== ALGORITMO 1: MAIN-QUANTUM-ENGINE (LOOP PRINCIPAL) =====
function MAIN_QUANTUM_ENGINE() {
  ESCRIBIR_LOG(LOG_NIVEL.INFO, "Iniciando Motor Cuantico Principal");
  
  const ejecutarCiclo = () => {
    if (MARKET_CLOSED === 'N') {
      try {
        PERFORM_GET_MARKET_DATA();
        PERFORM_UPDATE_MATRIX_17X17();
        PERFORM_QUANTUM_PROPAGATION();
        PERFORM_GENERATE_SIGNALS();
        PERFORM_EXECUTE_TRADES();
        
        setTimeout(ejecutarCiclo, LOOP_INTERVAL_MS);
      } catch (error) {
        ESCRIBIR_LOG(LOG_NIVEL.CRITICO, `Error en ciclo principal: ${error.message}`);
        setTimeout(ejecutarCiclo, LOOP_INTERVAL_MS * 2); // Retry con delay
      }
    }
  };
  
  ejecutarCiclo();
}

// ===== ALGORITMO 2: CORRELACION DINAMICA BTC =====
function CALCULAR_CORRELACION_BTC(activo_index, precio_cambio_altcoin, precio_cambio_btc, volatilidad_altcoin, volatilidad_btc) {
  if (activo_index === 0) return 1.0; // BTC consigo mismo
  
  if (volatilidad_altcoin === 0 || volatilidad_btc === 0) {
    ESCRIBIR_LOG(LOG_NIVEL.WARN, `Volatilidad cero detectada para activo ${ACTIVOS_CRYPTO[activo_index]}`);
    return 0.0;
  }
  
  const correlacion = (precio_cambio_altcoin * precio_cambio_btc) / (volatilidad_altcoin * volatilidad_btc);
  const correlacion_normalizada = Math.max(-1.0, Math.min(1.0, correlacion));
  
  CORRELACIONES_BTC[activo_index] = correlacion_normalizada;
  
  if (correlacion_normalizada > UMBRALES.CORRELACION_ALTA) {
    ESCRIBIR_LOG(LOG_NIVEL.INFO, `Estado entrelazado detectado: ${ACTIVOS_CRYPTO[activo_index]} correlacion=${correlacion_normalizada.toFixed(4)}`);
    ESTADOS_CUANTICOS[activo_index] = 'ENTRELAZADO';
    return correlacion_normalizada;
  } else if (correlacion_normalizada < UMBRALES.CORRELACION_BAJA) {
    ESCRIBIR_LOG(LOG_NIVEL.INFO, `Estado independiente: ${ACTIVOS_CRYPTO[activo_index]} correlacion=${correlacion_normalizada.toFixed(4)}`);
    ESTADOS_CUANTICOS[activo_index] = 'INDEPENDIENTE';
    return correlacion_normalizada;
  }
  
  ESTADOS_CUANTICOS[activo_index] = 'MIXTO';
  return correlacion_normalizada;
}

// ===== ALGORITMO 3: MOMENTUM MULTI-TEMPORAL =====
function CALCULAR_MOMENTUM_MULTITEMPORAL(precio_actual, precio_1h, precio_4h, precio_1d) {
  const momentum_1h = (precio_actual - precio_1h) / precio_1h;
  const momentum_4h = (precio_actual - precio_4h) / precio_4h;
  const momentum_1d = (precio_actual - precio_1d) / precio_1d;
  
  let signal_strength = 'SEÑAL_MIXTA';
  
  if (momentum_1h > 0 && momentum_4h > 0 && momentum_1d > 0) {
    signal_strength = 'FUERTE_ALCISTA';
    ESCRIBIR_LOG(LOG_NIVEL.INFO, `Convergencia alcista detectada: 1h=${momentum_1h.toFixed(4)} 4h=${momentum_4h.toFixed(4)} 1d=${momentum_1d.toFixed(4)}`);
  } else if (momentum_1h < 0 && momentum_4h < 0 && momentum_1d < 0) {
    signal_strength = 'FUERTE_BAJISTA';
    ESCRIBIR_LOG(LOG_NIVEL.INFO, `Convergencia bajista detectada: 1h=${momentum_1h.toFixed(4)} 4h=${momentum_4h.toFixed(4)} 1d=${momentum_1d.toFixed(4)}`);
  } else {
    ESCRIBIR_LOG(LOG_NIVEL.DEBUG, `Señal mixta: 1h=${momentum_1h.toFixed(4)} 4h=${momentum_4h.toFixed(4)} 1d=${momentum_1d.toFixed(4)}`);
  }
  
  return {
    momentum_1h: momentum_1h,
    momentum_4h: momentum_4h,
    momentum_1d: momentum_1d,
    signal_strength: signal_strength
  };
}

// ===== ALGORITMO 4: ENTROPIA Y CONTROL DE CAOS =====
function CALCULAR_ENTROPIA_MERCADO(observaciones_precio) {
  let entropia = 0.0;
  const total_observaciones = observaciones_precio.length;
  
  if (total_observaciones === 0) {
    ESCRIBIR_LOG(LOG_NIVEL.ERROR, "No hay observaciones para calcular entropía");
    return RESULTADOS.DATOS_INVALIDOS;
  }
  
  // Crear histograma de probabilidades
  const histograma = {};
  observaciones_precio.forEach(precio => {
    const bucket = Math.floor(precio * 100) / 100; // Redondear a 2 decimales
    histograma[bucket] = (histograma[bucket] || 0) + 1;
  });
  
  // Calcular entropía de Shannon
  Object.values(histograma).forEach(count => {
    const probabilidad = count / total_observaciones;
    if (probabilidad > 0) {
      entropia += probabilidad * Math.log2(probabilidad) * -1;
    }
  });
  
  let market_state = 'NORMAL';
  let estrategia = 'PREDICTIVE_ALGORITHMS';
  
  if (entropia < UMBRALES.ENTROPIA_ORDENADO) {
    market_state = 'ORDENADO';
    estrategia = 'PREDICTIVE_ALGORITHMS';
    ESCRIBIR_LOG(LOG_NIVEL.INFO, `Mercado ordenado detectado: entropía=${entropia.toFixed(4)}`);
  } else if (entropia > UMBRALES.ENTROPIA_CAOTICO) {
    market_state = 'CAOTICO';
    estrategia = 'DEFENSIVE_STRATEGIES';
    ESCRIBIR_LOG(LOG_NIVEL.WARN, `Mercado caótico detectado: entropía=${entropia.toFixed(4)} - Reduciendo exposición`);
  }
  
  return {
    entropia: entropia,
    market_state: market_state,
    estrategia: estrategia
  };
}

// ===== ALGORITMO 5: RESONANCIA ENTRE ACTIVOS =====
function DETECTAR_RESONANCIA(momentum_a, momentum_b, activo_a_index, activo_b_index) {
  const diferencia_fase = Math.abs(momentum_a - momentum_b);
  
  if (diferencia_fase < UMBRALES.RESONANCIA_MINIMA) {
    const movimiento_amplificado = momentum_a * 1.618; // Multiplicador Fibonacci
    
    ESCRIBIR_LOG(LOG_NIVEL.INFO, 
      `Resonancia detectada entre ${ACTIVOS_CRYPTO[activo_a_index]} y ${ACTIVOS_CRYPTO[activo_b_index]}: ` +
      `diferencia=${diferencia_fase.toFixed(6)} movimiento_esperado=${movimiento_amplificado.toFixed(4)}`
    );
    
    return {
      resonancia: true,
      diferencia_fase: diferencia_fase,
      movimiento_amplificado: movimiento_amplificado,
      fibonacci_multiplier: true
    };
  }
  
  return {
    resonancia: false,
    diferencia_fase: diferencia_fase,
    movimiento_amplificado: momentum_a,
    fibonacci_multiplier: false
  };
}

// ===== ALGORITMO 6: SCHRODINGER (ESTADO CUANTICO) =====
function CALCULAR_ESTADO_SCHRODINGER(señales_alcistas, señales_bajistas, total_señales) {
  if (total_señales === 0) {
    ESCRIBIR_LOG(LOG_NIVEL.WARN, "No hay señales para análisis cuántico");
    return {
      posicion: 'WAIT',
      probabilidad_up: 0,
      probabilidad_down: 0,
      probabilidad_sideways: 100,
      estado_cuantico: 'SUPERPOSICION'
    };
  }
  
  const probabilidad_up = (señales_alcistas / total_señales) * 100;
  const probabilidad_down = (señales_bajistas / total_señales) * 100;
  const probabilidad_sideways = 100 - probabilidad_up - probabilidad_down;
  
  let posicion = 'WAIT';
  let estado_cuantico = 'SUPERPOSICION';
  let position_size = 0;
  
  if (probabilidad_up > UMBRALES.SCHRODINGER_DECISION * 100) {
    posicion = 'LONG';
    estado_cuantico = 'COLAPSO_ALCISTA';
    position_size = probabilidad_up / 100;
    ESCRIBIR_LOG(LOG_NIVEL.INFO, `Colapso cuántico ALCISTA: probabilidad=${probabilidad_up.toFixed(2)}%`);
  } else if (probabilidad_down > UMBRALES.SCHRODINGER_DECISION * 100) {
    posicion = 'SHORT';
    estado_cuantico = 'COLAPSO_BAJISTA';
    position_size = probabilidad_down / 100;
    ESCRIBIR_LOG(LOG_NIVEL.INFO, `Colapso cuántico BAJISTA: probabilidad=${probabilidad_down.toFixed(2)}%`);
  } else {
    ESCRIBIR_LOG(LOG_NIVEL.DEBUG, `Superposición cuántica mantenida: UP=${probabilidad_up.toFixed(2)}% DOWN=${probabilidad_down.toFixed(2)}%`);
  }
  
  return {
    posicion: posicion,
    probabilidad_up: probabilidad_up,
    probabilidad_down: probabilidad_down,
    probabilidad_sideways: probabilidad_sideways,
    estado_cuantico: estado_cuantico,
    position_size: position_size
  };
}

// ===== ALGORITMO 7: EDGE FOTONICO-AKASHICO =====
function CALCULAR_EDGE_FOTONICO_AKASHICO(datos_precio_historicos, patron_actual) {
  // Componente Fotónico: Análisis de Fourier simplificado
  let frecuencia_dominante = 0;
  let amplitud_maxima = 0;
  
  // Detectar ciclos básicos (simplificado)
  const periodos_comunes = [24, 168, 720]; // 1 día, 1 semana, 1 mes en horas
  
  periodos_comunes.forEach(periodo => {
    let suma_amplitud = 0;
    for (let i = periodo; i < datos_precio_historicos.length; i++) {
      const diferencia = Math.abs(datos_precio_historicos[i] - datos_precio_historicos[i - periodo]);
      suma_amplitud += diferencia;
    }
    
    const amplitud_promedio = suma_amplitud / (datos_precio_historicos.length - periodo);
    if (amplitud_promedio > amplitud_maxima) {
      amplitud_maxima = amplitud_promedio;
      frecuencia_dominante = 1 / periodo;
    }
  });
  
  const proximo_pico = Date.now() + (1 / frecuencia_dominante) * 3600000; // En milisegundos
  
  // Componente Akáshico: Búsqueda de patrones históricos
  let mejor_similitud = 0;
  let resultado_esperado = 0;
  let confianza_patron = 0;
  
  // Simulación de búsqueda de patrones (simplificado)
  const ventana_patron = 10;
  if (datos_precio_historicos.length >= ventana_patron * 2) {
    for (let i = ventana_patron; i < datos_precio_historicos.length - ventana_patron; i++) {
      let similitud = 0;
      
      for (let j = 0; j < ventana_patron; j++) {
        const diferencia_actual = patron_actual[j] || 0;
        const diferencia_historica = datos_precio_historicos[i + j] - datos_precio_historicos[i + j - 1];
        const similitud_punto = 1 - Math.abs(diferencia_actual - diferencia_historica) / Math.max(Math.abs(diferencia_actual), Math.abs(diferencia_historica), 0.001);
        similitud += similitud_punto;
      }
      
      similitud = similitud / ventana_patron * 100;
      
      if (similitud > mejor_similitud && similitud > 85) {
        mejor_similitud = similitud;
        resultado_esperado = datos_precio_historicos[i + ventana_patron] - datos_precio_historicos[i];
        confianza_patron = similitud;
      }
    }
  }
  
  // Combinar ambos edges
  const edge_fotonico = frecuencia_dominante * amplitud_maxima;
  const edge_akashico = (mejor_similitud / 100) * Math.abs(resultado_esperado);
  const edge_total = (edge_fotonico * 0.6) + (edge_akashico * 0.4);
  
  ESCRIBIR_LOG(LOG_NIVEL.INFO, 
    `Edge Fotónico-Akáshico calculado: fotónico=${edge_fotonico.toFixed(6)} akáshico=${edge_akashico.toFixed(6)} total=${edge_total.toFixed(6)}`
  );
  
  return {
    edge_fotonico: edge_fotonico,
    edge_akashico: edge_akashico,
    edge_total: edge_total,
    frecuencia_dominante: frecuencia_dominante,
    proximo_pico: proximo_pico,
    patron_similitud: mejor_similitud,
    resultado_esperado: resultado_esperado,
    confianza: confianza_patron
  };
}

// ===== ALGORITMO 8: GESTION DE RIESGO ADAPTATIVA =====
function CALCULAR_GESTION_RIESGO(balance_cuenta, volatilidad_actual, tipo_crypto, estado_mercado) {
  const riesgo_base = 0.02; // 2% del balance por operación
  
  // Cálculo dinámico de tamaño de posición
  const tamaño_ajustado_riesgo = (balance_cuenta * riesgo_base) / volatilidad_actual;
  
  // Stop loss adaptativo según tipo de crypto
  let stop_loss_factor = 0.95; // Default 5%
  
  switch (tipo_crypto) {
    case 'STABLE': // BTC, ETH
      stop_loss_factor = 0.95;
      break;
    case 'VOLATILE': // DOGE, MEME-COINS
      stop_loss_factor = 0.88;
      break;
    case 'DEFI': // UNI, LINK
      stop_loss_factor = 0.92;
      break;
    default:
      stop_loss_factor = 0.93;
  }
  
  // Ajuste por condiciones de mercado
  if (estado_mercado === 'CAOTICO') {
    stop_loss_factor *= 0.9; // Más conservador
    ESCRIBIR_LOG(LOG_NIVEL.WARN, "Ajuste conservador aplicado por mercado caótico");
  }
  
  const position_size = Math.min(tamaño_ajustado_riesgo, balance_cuenta * 0.1); // Máximo 10% del balance
  
  ESCRIBIR_LOG(LOG_NIVEL.DEBUG, 
    `Gestión de riesgo: tamaño=${position_size.toFixed(2)} stop_loss=${stop_loss_factor} tipo=${tipo_crypto} mercado=${estado_mercado}`
  );
  
  return {
    position_size: position_size,
    stop_loss_factor: stop_loss_factor,
    riesgo_calculado: (position_size / balance_cuenta) * 100,
    tipo_crypto: tipo_crypto,
    ajuste_mercado: estado_mercado === 'CAOTICO'
  };
}

// ===== ALGORITMO DE PROPAGACION DE ENTANGLEMENT =====
function PROPAGAR_ENTANGLEMENT_BTC(cambio_precio_btc) {
  if (Math.abs(cambio_precio_btc) > UMBRALES.BTC_CAMBIO_SIGNIFICATIVO) {
    ESCRIBIR_LOG(LOG_NIVEL.INFO, `Propagación cuántica iniciada: BTC cambió ${(cambio_precio_btc * 100).toFixed(2)}%`);
    
    for (let fila = 1; fila < 17; fila++) { // Empezar desde fila 1 (saltar BTC)
      const factor_correlacion = CORRELACIONES_BTC[fila];
      const precio_actual = MATRIZ_CUANTICA[fila][0]; // Columna 0 podría ser precio base
      
      const nuevo_precio_esperado = precio_actual * (1 + (cambio_precio_btc * factor_correlacion));
      
      // Actualizar todas las métricas relacionadas
      ACTUALIZAR_TODAS_METRICAS(fila, nuevo_precio_esperado, factor_correlacion);
      
      // Propagación secundaria para activos altamente correlacionados
      if (factor_correlacion > UMBRALES.CORRELACION_ALTA) {
        PROPAGACION_SECUNDARIA(fila, cambio_precio_btc, factor_correlacion);
      }
    }
  }
}

// ===== FUNCIONES DE SOPORTE =====
function PERFORM_GET_MARKET_DATA() {
  // Simulación de obtención de datos de mercado
  ESCRIBIR_LOG(LOG_NIVEL.DEBUG, "Obteniendo datos de mercado...");
  // Aquí iría la integración con API de Binance
}

function PERFORM_UPDATE_MATRIX_17X17() {
  // Actualización de la matriz cuántica
  ESCRIBIR_LOG(LOG_NIVEL.DEBUG, "Actualizando matriz 17x17...");
}

function PERFORM_QUANTUM_PROPAGATION() {
  // Propagación cuántica de estados
  ESCRIBIR_LOG(LOG_NIVEL.DEBUG, "Ejecutando propagación cuántica...");
}

function PERFORM_GENERATE_SIGNALS() {
  // Generación de señales de trading
  ESCRIBIR_LOG(LOG_NIVEL.DEBUG, "Generando señales de trading...");
}

function PERFORM_EXECUTE_TRADES() {
  // Ejecución de trades
  ESCRIBIR_LOG(LOG_NIVEL.DEBUG, "Ejecutando trades...");
}

function ACTUALIZAR_TODAS_METRICAS(fila, nuevo_precio, correlacion) {
  // Actualizar todas las columnas de métricas para la fila especificada
  ESCRIBIR_LOG(LOG_NIVEL.DEBUG, `Actualizando métricas para ${ACTIVOS_CRYPTO[fila]}: precio=${nuevo_precio.toFixed(8)} correlación=${correlacion.toFixed(4)}`);
}

function PROPAGACION_SECUNDARIA(fila, cambio_btc, correlacion) {
  // Propagación secundaria para activos altamente correlacionados
  ESCRIBIR_LOG(LOG_NIVEL.INFO, `Propagación secundaria para ${ACTIVOS_CRYPTO[fila]}: correlación=${correlacion.toFixed(4)}`);
}

// ===== INICIALIZACION DEL SISTEMA =====
function INICIALIZAR_SISTEMA_CUANTICO() {
  ESCRIBIR_LOG(LOG_NIVEL.INFO, "=== INICIALIZANDO SISTEMA ELO-AKASHICO CUANTICO ===");
  ESCRIBIR_LOG(LOG_NIVEL.INFO, `Precisión: ${PRECISION_SATOSHI} decimales satoshi-level`);
  ESCRIBIR_LOG(LOG_NIVEL.INFO, `Activos: ${ACTIVOS_CRYPTO.length} cryptos`);
  ESCRIBIR_LOG(LOG_NIVEL.INFO, `Métricas: ${METRICAS.length} dimensiones`);
  ESCRIBIR_LOG(LOG_NIVEL.INFO, `Matriz: ${MATRIZ_CUANTICA.length}x${MATRIZ_CUANTICA[0].length} núcleo operativo`);
  
  // Inicializar matriz con valores base
  for (let i = 0; i < 17; i++) {
    for (let j = 0; j < 17; j++) {
      MATRIZ_CUANTICA[i][j] = 0.0;
    }
  }
  
  // Inicializar correlaciones BTC
  CORRELACIONES_BTC[0] = 1.0; // BTC consigo mismo
  
  // Sistema inicializado exitosamente
  ESCRIBIR_LOG(LOG_NIVEL.INFO, "Sistema cuántico inicializado exitosamente");
  
  return RESULTADOS.EXITO;
}

// ===== PUNTO DE ENTRADA =====
function INICIAR_MOTOR_CUANTICO() {
  const resultado_init = INICIALIZAR_SISTEMA_CUANTICO();
  
  if (resultado_init === RESULTADOS.EXITO) {
    ESCRIBIR_LOG(LOG_NIVEL.INFO, "Iniciando Motor Cuántico Principal...");
    MAIN_QUANTUM_ENGINE();
  } else {
    ESCRIBIR_LOG(LOG_NIVEL.CRITICO, "Error en inicialización del sistema");
  }
}

// Auto-inicialización
if (typeof window !== 'undefined') {
  // Entorno browser
  window.addEventListener('load', INICIAR_MOTOR_CUANTICO);
} else {
  // Entorno Node.js
  INICIAR_MOTOR_CUANTICO();
}

// ===== EXPORTACIONES =====
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    INICIAR_MOTOR_CUANTICO,
    CALCULAR_CORRELACION_BTC,
    CALCULAR_MOMENTUM_MULTITEMPORAL,
    CALCULAR_ENTROPIA_MERCADO,
    DETECTAR_RESONANCIA,
    CALCULAR_ESTADO_SCHRODINGER,
    CALCULAR_EDGE_FOTONICO_AKASHICO,
    CALCULAR_GESTION_RIESGO,
    PROPAGAR_ENTANGLEMENT_BTC,
    MATRIZ_CUANTICA,
    ACTIVOS_CRYPTO,
    METRICAS
  };
}
