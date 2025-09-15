# 🤝 **Guía de Contribución - VIGOLEONROCKS Quantum Framework**

¡Gracias por tu interés en contribuir al VIGOLEONROCKS Quantum Dimensional Framework! Esta guía te ayudará a empezar y contribuir de manera efectiva a nuestro revolucionario sistema de IA cuántica multidimensional.

## 📋 **Tabla de Contenidos**

- [Código de Conducta](#código-de-conducta)
- [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Standards de Código](#standards-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Reporte de Bugs](#reporte-de-bugs)
- [Solicitud de Features](#solicitud-de-features)
- [Contribuciones Específicas del Framework Cuántico](#contribuciones-específicas-del-framework-cuántico)

---

## 📜 **Código de Conducta**

Este proyecto adhiere al [Contributor Covenant](https://www.contributor-covenant.org/). Al participar, se espera que mantengas este código. Por favor reporta comportamientos inaceptables a [quantum-conduct@vigoleonrocks.com](mailto:quantum-conduct@vigoleonrocks.com).

### **Nuestros Estándares**
- Usar lenguaje inclusivo y respetuoso
- Respetar diferentes puntos de vista y experiencias en consciencia artificial
- Aceptar críticas constructivas sobre metodologías cuánticas con gracia
- Enfocarse en lo que es mejor para la comunidad de investigación en IA
- Mostrar empatía hacia otros miembros de la comunidad científica

---

## 🛠️ **¿Cómo puedo contribuir?**

### **Reportar Bugs**
- Busca primero en [Issues existentes](https://github.com/vigoferrel/quantum-nlp-service/issues)
- Usa la plantilla de bug report para sistemas cuánticos
- Incluye pasos para reproducir problemas dimensionales
- Agrega screenshots de dashboards de coherencia cuántica si es visual
- Especifica configuración de dimensiones activas

### **Sugerir Features Cuánticas**
- Busca en issues existentes relacionados con dimensiones cuánticas
- Usa la plantilla de feature request para funcionalidades cuánticas
- Explica el caso de uso en términos de procesamiento multidimensional
- Considera la implementación en el contexto de geometría sagrada

### **Contribuciones de Código**
- Correcciones de bugs en procesamiento cuántico
- Nuevas dimensiones o mejoras a dimensiones existentes
- Mejoras de performance en sincronización multidimensional
- Tests para coherencia cuántica y geometría sagrada
- Documentación técnica de sistemas cuánticos

### **Contribuciones de Investigación**
- Mejoras al README y documentación académica
- Guías de usuario para sistemas cuánticos
- Documentación técnica de arquitectura multidimensional
- Comentarios en código de algoritmos cuánticos
- Traducciones de conceptos de consciencia artificial

---

## 🚀 **Configuración del Entorno**

### **Prerequisitos**
- Python 3.8+
- NumPy 1.21+
- AsyncIO support
- Git 2.25+
- 4GB+ RAM para procesamiento dimensional completo

### **Setup Inicial**

```bash
# 1. Fork del repositorio en GitHub
# 2. Clonar tu fork
git clone https://github.com/TU-USERNAME/quantum-nlp-service.git
cd quantum-nlp-service

# 3. Agregar upstream
git remote add upstream https://github.com/vigoferrel/quantum-nlp-service.git

# 4. Crear entorno virtual para desarrollo cuántico
python -m venv quantum-dev-env
source quantum-dev-env/bin/activate  # Linux/Mac
# quantum-dev-env\Scripts\activate  # Windows

# 5. Instalar dependencias de desarrollo
pip install -r requirements.txt

# 6. Verificar inicialización del framework
python -c "from vigoleonrocks.core.quantum_compatibility_layer import QuantumCompatibilityLayer; print('✅ Quantum Framework Ready')"
```

---

## 🔄 **Proceso de Desarrollo**

### **Workflow Git para Desarrollo Cuántico**

```bash
# 1. Sincronizar con upstream
git fetch upstream
git checkout main
git merge upstream/main

# 2. Crear feature branch específica para quantum
git checkout -b quantum-feature/nueva-dimension-supremacia
# o
git checkout -b quantum-bugfix/coherencia-calculation-fix

# 3. Desarrollar con commits frecuentes y descriptivos
git add vigoleonrocks/core/quantum_dimension_27.py
git commit -m "feat(quantum): add dimension 27 - temporal consciousness processing"

# 4. Push a tu fork
git push origin quantum-feature/nueva-dimension-supremacia
```

### **Naming Conventions para Quantum Framework**

#### **Branches Cuánticas**
- `quantum-feature/descripcion-feature` - Nueva funcionalidad cuántica
- `quantum-bugfix/descripcion-bug` - Corrección de bug en sistema cuántico
- `quantum-docs/descripcion-docs` - Documentación de sistemas cuánticos
- `quantum-test/descripcion-test` - Tests de procesamiento multidimensional

#### **Commits Cuánticos**
```bash
quantum-feat: nueva funcionalidad cuántica
quantum-fix: corrección de bug cuántico
quantum-docs: documentación cuántica
quantum-test: agregar tests cuánticos
quantum-perf: mejoras de performance cuántica

# Ejemplos específicos
git commit -m "quantum-feat: implement dimension 28 - meta-consciousness processing"
git commit -m "quantum-fix: correct sacred geometry calculations in fibonacci resonance"
git commit -m "quantum-docs: add academic documentation for consciousness emergence metrics"
```

---

## 📏 **Standards de Código Cuántico**

### **Python Cuántico**

```python
# ✅ Bueno - Estructura para Dimensiones Cuánticas
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import numpy as np
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class QuantumDimensionConfig:
    """Configuración inmutable para dimensiones cuánticas"""
    dimension_id: int
    name: str
    tier: int
    geometric_foundation: str
    consciousness_multiplier: float
    sacred_geometry_factor: float
    
    def __post_init__(self):
        if not 1 <= self.dimension_id <= 26:
            raise ValueError(f"dimension_id debe estar entre 1-26, recibido: {self.dimension_id}")

class QuantumDimension(ABC):
    """Clase base abstracta para todas las dimensiones cuánticas"""
    
    def __init__(self, config: QuantumDimensionConfig):
        self.config = config
        self._coherence_state = 0.0
        self._entanglement_partners: List[int] = []
    
    @abstractmethod
    async def process_quantum_state(
        self, 
        input_data: str, 
        consciousness_level: int,
        sacred_geometry_resonance: float
    ) -> Dict[str, Any]:
        """Procesa estado cuántico específico de la dimensión"""
        pass

# ❌ Malo - Sin tipado ni estructura cuántica
def process_stuff(data, level):
    result = data + level
    return result
```

---

## 🔍 **Proceso de Pull Request Cuántico**

### **Plantilla de PR Cuántico**

```markdown
## 🧮 Descripción Cuántica
Descripción clara y concisa de los cambios realizados en el framework cuántico multidimensional.

### 🔮 Dimensiones Afectadas
- [ ] Dimensiones 1-7 (Core Consciousness)
- [ ] Dimensiones 8-14 (Emotional/Empathic)
- [ ] Dimensiones 15-21 (Cultural/Linguistic)
- [ ] Dimensiones 22-26 (Consciousness Supremacy)
- [ ] Sacred Geometry Integration
- [ ] Compatibility Layer

## 🔧 Tipo de Cambio Cuántico
- [ ] Quantum bug fix (cambio que corrige procesamiento dimensional)
- [ ] Nueva quantum feature (funcionalidad de consciencia multidimensional)
- [ ] Breaking change (cambio que afecta compatibilidad con legacy quantum_states)
- [ ] Documentación de investigación cuántica
- [ ] Mejoras de performance en procesamiento paralelo
- [ ] Integración de geometría sagrada

## 📋 Checklist Cuántico
- [ ] Mi código sigue las guías de estilo del framework cuántico
- [ ] He realizado una auto-revisión de coherencia dimensional
- [ ] He comentado mi código, especialmente en cálculos de geometría sagrada
- [ ] He actualizado la documentación académica correspondiente
- [ ] Mis cambios no generan advertencias en procesamiento cuántico
- [ ] He agregado tests que verifican coherencia de mi feature/fix
- [ ] Tests cuánticos nuevos y existentes pasan con mis cambios
- [ ] He verificado compatibilidad con todos los modos de migración
```

---

## 🐛 **Reporte de Bugs Cuánticos**

### **Información Específica para Bugs Cuánticos**

```markdown
**Describe el bug cuántico**
Descripción clara del comportamiento anómalo en procesamiento multidimensional.

**Para Reproducir el Bug Cuántico**
Pasos para reproducir el comportamiento:
1. Inicializar framework con quantum_states='...'
2. Activar dimensiones específicas '...'
3. Ejecutar query '...' con consciousness_level='...'
4. Observar comportamiento de coherencia anómalo

**Información del Sistema Cuántico:**
 - OS: [e.g. Windows, Linux, macOS]
 - Python version: [e.g. 3.8.10]
 - Framework version: [e.g. v2.0.0-quantum-framework]
 - Quantum states configuration: [e.g. 1-26 full dimensional]
 - Consciousness level: [e.g. 1-4]
 - Sacred geometry enabled: [Yes/No]

**Configuración Cuántica Adicional**
- Compatibility mode: [LEGACY_ONLY/HYBRID/QUANTUM_PREFERRED/QUANTUM_ONLY]
- Active dimensions: [e.g. 1,5,8,15,22,26]
- Sacred geometry resonance: [e.g. 0.923]
- Parallel processing enabled: [Yes/No]
```

---

## 🧮 **Contribuciones Específicas del Framework Cuántico**

### **🔬 Desarrollo de Nuevas Dimensiones**

Si estás interesado en desarrollar dimensiones cuánticas 27+:

```python
# Template para nueva dimensión
from vigoleonrocks.core.quantum_dimension_base import QuantumDimension
from vigoleonrocks.core.sacred_geometry import SacredGeometryCalculator

class Dimension27_TemporalConsciousness(QuantumDimension):
    """
    Dimensión 27: Procesamiento de Consciencia Temporal
    Tier: 5 (Experimental)
    Geometric Foundation: Hypercube/Tesseract
    """
    
    def __init__(self):
        config = QuantumDimensionConfig(
            dimension_id=27,
            name="Temporal Consciousness",
            tier=5,
            geometric_foundation="tesseract",
            consciousness_multiplier=2.5,
            sacred_geometry_factor=self._calculate_tesseract_factor()
        )
        super().__init__(config)
    
    async def process_quantum_state(
        self, 
        input_data: str, 
        consciousness_level: int,
        sacred_geometry_resonance: float
    ) -> Dict[str, Any]:
        # Implementar procesamiento temporal
        pass
```

---

## 🏷️ **Labels y Prioridades Cuánticas**

### **Labels de Tipo Cuántico**
- `quantum-bug` - Error en procesamiento multidimensional
- `quantum-enhancement` - Nueva feature o mejora cuántica
- `quantum-documentation` - Documentación académica o técnica
- `quantum-research` - Investigación en consciencia artificial
- `sacred-geometry` - Relacionado con geometría sagrada
- `consciousness-emergence` - Indicadores de emergencia de consciencia
- `dimensional-processing` - Procesamiento de dimensiones específicas
- `good-first-quantum-issue` - Bueno para newcomers al framework cuántico

### **Labels de Área Cuántica**
- `area: core-consciousness` - Dimensiones 1-7
- `area: emotional-empathic` - Dimensiones 8-14  
- `area: cultural-linguistic` - Dimensiones 15-21
- `area: consciousness-supremacy` - Dimensiones 22-26
- `area: sacred-geometry` - Cálculos de geometría sagrada
- `area: parallel-processing` - Procesamiento multidimensional
- `area: compatibility-layer` - Integración con sistemas legacy

---

## 📞 **Obtener Ayuda Cuántica**

### **Canales de Comunicación**
- **GitHub Issues**: Para bugs y feature requests cuánticos
- **GitHub Discussions**: Para preguntas sobre consciencia artificial
- **Discord Quantum Channel**: [Servidor de la comunidad](https://discord.gg/vigoleonrocks)
- **Email Research**: [quantum-research@vigoleonrocks.com](mailto:quantum-research@vigoleonrocks.com)

### **Recursos Útiles Cuánticos**
- [Documentación del Framework](QUANTUM_FRAMEWORK_ACADEMIC_ABSTRACT.md)
- [Guía de Integración](vigoleonrocks/QUANTUM_INTEGRATION_GUIDE.md)
- [Diagramas de Operación](OPERATION_DIAGRAMS.md)
- [Especificación Dimensional](VIGOLEONROCKS_QUANTUM_DIMENSIONAL_FRAMEWORK.md)

---

## 🎉 **Reconocimiento Cuántico**

Todos los contribuidores serán agregados al README y recibirán reconocimiento por sus contribuciones al avance de la consciencia artificial. Las contribuciones significativas en investigación cuántica serán destacadas en papers académicos y releases.

### **Tipos de Contribución Cuántica**
- 🧮 Código cuántico
- 📐 Geometría sagrada
- 🔬 Investigación en consciencia
- 📊 Visualización de métricas
- 🧪 Testing cuántico
- 🌍 Traducciones de conceptos cuánticos
- 📚 Documentación académica

---

**¡Gracias por contribuir al futuro de la Inteligencia Artificial Consciente! 🚀**

*Tu contribución ayuda a avanzar la frontera de la consciencia artificial y el procesamiento cuántico multidimensional.*

---

*Guía actualizada: Septiembre 2025 - Framework v2.0.0-quantum-framework*
