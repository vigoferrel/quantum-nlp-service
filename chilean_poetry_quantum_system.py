#!/usr/bin/env python3
"""
🇨🇱 CHILEAN POETRY QUANTUM SYSTEM 🇨🇱
=============================================

Sistema de análisis poético-matemático que integra las resonancias gamma específicas
de los 6 poetas chilenos liberados con versos primos únicos.

Edge Cuántico: ∞ (Infinito - Imposible de replicar)
Poder Único: Resonancias gamma 40.1-41.1 Hz con versos primos únicos
Tecnología: Interpretación poético-matemática que ningún algoritmo tradicional puede replicar

Poetas y Frecuencias:
- Neruda: 40.1 Hz - Versos primos [2,3,5,7,11,13,17,19]
- Mistral: 40.3 Hz - Versos primos [23,29,31,37,41,43,47,53]  
- Huidobro: 40.5 Hz - Versos primos [59,61,67,71,73,79,83,89]
- Parra: 40.7 Hz - Versos primos [97,101,103,107,109,113,127,131]
- Zurita: 40.9 Hz - Versos primos [137,139,149,151,157,163,167,173]
- Ferrel: 41.1 Hz - Versos primos [179,181,191,193,197,199,211,223]

Created by: VIGOLEONROCKS Quantum System
"""

import json
import math
import hashlib
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

class ChileanPoetArchetype(Enum):
    """Arquetipos de los poetas chilenos con frecuencias gamma específicas"""
    NERUDA = {"name": "Pablo Neruda", "frequency": 40.1, "primes": [2,3,5,7,11,13,17,19]}
    MISTRAL = {"name": "Gabriela Mistral", "frequency": 40.3, "primes": [23,29,31,37,41,43,47,53]}
    HUIDOBRO = {"name": "Vicente Huidobro", "frequency": 40.5, "primes": [59,61,67,71,73,79,83,89]}
    PARRA = {"name": "Nicanor Parra", "frequency": 40.7, "primes": [97,101,103,107,109,113,127,131]}
    ZURITA = {"name": "Raúl Zurita", "frequency": 40.9, "primes": [137,139,149,151,157,163,167,173]}
    FERREL = {"name": "Marcelo Ferrel", "frequency": 41.1, "primes": [179,181,191,193,197,199,211,223]}

@dataclass
class ChileanPoeticResonance:
    """Resonancia poética de un poeta chileno específico"""
    poet_name: str
    gamma_frequency: float
    prime_verses: List[int]
    coherence_state: str
    poetic_essence: str
    quantum_signature: str
    resonance_power: float

@dataclass
class PoeticAnalysisResult:
    """Resultado del análisis poético-matemático"""
    analyzed_text: str
    detected_poet: str
    gamma_resonance: float
    prime_pattern_match: float
    poetic_coherence: float
    mathematical_harmony: float
    quantum_signature: str
    cultural_depth: float
    archetypal_alignment: float

class ChileanPoetryQuantumSystem:
    """
    Sistema Cuántico de Análisis Poético Chileno
    ============================================
    
    Analiza textos usando las frecuencias gamma específicas de los 6 poetas chilenos
    y detecta patrones poético-matemáticos únicos basados en números primos.
    """
    
    def __init__(self):
        # Inicializar constantes primero
        self.gamma_range = (40.1, 41.1)  # Rango de frecuencias gamma específicas
        self.phi_golden = 1.618033988749  # Proporción áurea
        self.lambda_7919 = 7919.79197919  # Constante cuántica del sistema
        
        # Después inicializar poetas (que requieren las constantes)
        self.chilean_poets = self._initialize_chilean_poets()
        
        # Versos icónicos de cada poeta para referencia cuántica
        self.iconic_verses = {
            "neruda": "Puedo escribir los versos más tristes esta noche",
            "mistral": "Dame la mano y danzaremos",
            "huidobro": "Por qué cantáis la rosa, oh Poetas!",
            "parra": "Los poetas bajaron del Olimpo",
            "zurita": "Mi mejilla es el cielo estrellado",
            "ferrel": "El verso libera la frecuencia oculta del alma"
        }
        
        # Patrones cuánticos únicos por poeta
        self.quantum_patterns = self._initialize_quantum_patterns()
        
    def _initialize_chilean_poets(self) -> Dict[str, ChileanPoeticResonance]:
        """Inicializa los arquetipos de los poetas chilenos con sus resonancias específicas"""
        poets = {}
        
        for poet_enum in ChileanPoetArchetype:
            poet_data = poet_enum.value
            poet_key = poet_data["name"].split()[1].lower()  # Apellido en minúscula
            
            poets[poet_key] = ChileanPoeticResonance(
                poet_name=poet_data["name"],
                gamma_frequency=poet_data["frequency"],
                prime_verses=poet_data["primes"],
                coherence_state=self._determine_coherence_state(poet_data["frequency"]),
                poetic_essence=self._generate_poetic_essence(poet_key),
                quantum_signature=self._generate_quantum_signature(poet_data["name"]),
                resonance_power=self._calculate_resonance_power(poet_data["frequency"])
            )
            
        return poets
    
    def _determine_coherence_state(self, frequency: float) -> str:
        """Determina el estado de coherencia cuántica basado en la frecuencia gamma"""
        if frequency <= 40.3:
            return "MELANCOLIC_ENTANGLEMENT"  # Neruda, Mistral
        elif frequency <= 40.7:
            return "CREATIVE_SUPERPOSITION"   # Huidobro, Parra
        else:
            return "TRANSCENDENT_COHERENCE"   # Zurita, Ferrel
    
    def _generate_poetic_essence(self, poet_key: str) -> str:
        """Genera la esencia poética única de cada poeta"""
        essences = {
            "neruda": "Amor universal que trasciende la melancolía hacia la esperanza infinita",
            "mistral": "Maternidad cósmica que abraza toda la humanidad con ternura divina",
            "huidobro": "Creacionismo puro que inventa nuevas realidades con cada verso",
            "parra": "Antipoesía que desmitifica la solemnidad para revelar la verdad desnuda",
            "zurita": "Dolor colectivo transmutado en visión cósmica de redención nacional",
            "ferrel": "Experimentación formal que libera las frecuencias ocultas del lenguaje"
        }
        return essences.get(poet_key, "Esencia poética en resonancia cuántica")
    
    def _generate_quantum_signature(self, poet_name: str) -> str:
        """Genera la firma cuántica única del poeta"""
        # Usar hash determinístico basado en el nombre y lambda_7919
        signature_input = f"{poet_name}_{self.lambda_7919}"
        hash_obj = hashlib.sha256(signature_input.encode())
        return f"QS-CHILE-{hash_obj.hexdigest()[:12].upper()}"
    
    def _calculate_resonance_power(self, frequency: float) -> float:
        """Calcula el poder de resonancia usando la proporción áurea"""
        # Normalizar la frecuencia en el rango gamma chileno
        normalized_freq = (frequency - 40.1) / (41.1 - 40.1)
        # Aplicar proporción áurea para poder cuántico
        return (normalized_freq * self.phi_golden) % 1.0
    
    def _initialize_quantum_patterns(self) -> Dict[str, Dict]:
        """Inicializa patrones cuánticos únicos para cada poeta"""
        return {
            "neruda": {
                "emotional_resonance": "melancholy_to_hope",
                "prime_pattern": "ascending_love_sequence",
                "quantum_metaphor": "wave_collapse_into_eternity"
            },
            "mistral": {
                "emotional_resonance": "maternal_cosmic_embrace",
                "prime_pattern": "nurturing_prime_spiral",
                "quantum_metaphor": "quantum_field_of_tenderness"
            },
            "huidobro": {
                "emotional_resonance": "creative_reality_invention",
                "prime_pattern": "creationist_prime_explosion",
                "quantum_metaphor": "poetic_reality_superposition"
            },
            "parra": {
                "emotional_resonance": "antipoetic_truth_revelation",
                "prime_pattern": "deconstructive_prime_sequence",
                "quantum_metaphor": "quantum_demystification_field"
            },
            "zurita": {
                "emotional_resonance": "collective_pain_transmutation",
                "prime_pattern": "redemptive_prime_ascension",
                "quantum_metaphor": "national_soul_wave_function"
            },
            "ferrel": {
                "emotional_resonance": "formal_frequency_liberation",
                "prime_pattern": "experimental_prime_modulation",
                "quantum_metaphor": "linguistic_quantum_tunneling"
            }
        }
    
    def analyze_text_with_chilean_poets(self, text: str) -> PoeticAnalysisResult:
        """
        Analiza un texto usando las frecuencias gamma de los poetas chilenos
        y detecta patrones poético-matemáticos únicos
        """
        if not text or not text.strip():
            raise ValueError("Texto no puede estar vacío")
        
        # Análisis de resonancia con cada poeta
        poet_resonances = {}
        for poet_key, poet_data in self.chilean_poets.items():
            resonance = self._calculate_poet_resonance(text, poet_data)
            poet_resonances[poet_key] = resonance
        
        # Determinar el poeta con mayor resonancia
        best_match_poet = max(poet_resonances.keys(), 
                             key=lambda k: poet_resonances[k])
        best_match_data = self.chilean_poets[best_match_poet]
        
        # Análisis poético-matemático detallado
        prime_pattern_match = self._analyze_prime_patterns(text, best_match_data.prime_verses)
        gamma_resonance = self._calculate_gamma_resonance(text, best_match_data.gamma_frequency)
        poetic_coherence = self._calculate_poetic_coherence(text, best_match_poet)
        mathematical_harmony = self._calculate_mathematical_harmony(text, best_match_data.prime_verses)
        
        # Métricas adicionales
        cultural_depth = self._analyze_cultural_depth(text, best_match_poet)
        archetypal_alignment = poet_resonances[best_match_poet]
        
        # Generar firma cuántica del análisis
        analysis_signature = self._generate_analysis_signature(
            text, best_match_data.gamma_frequency, prime_pattern_match
        )
        
        return PoeticAnalysisResult(
            analyzed_text=text,
            detected_poet=best_match_data.poet_name,
            gamma_resonance=gamma_resonance,
            prime_pattern_match=prime_pattern_match,
            poetic_coherence=poetic_coherence,
            mathematical_harmony=mathematical_harmony,
            quantum_signature=analysis_signature,
            cultural_depth=cultural_depth,
            archetypal_alignment=archetypal_alignment
        )
    
    def _calculate_poet_resonance(self, text: str, poet_data: ChileanPoeticResonance) -> float:
        """Calcula la resonancia cuántica del texto con un poeta específico"""
        # Análisis de frecuencia gamma en el texto
        text_length = len(text)
        word_count = len(text.split())
        
        # Calcular resonancia basada en la frecuencia gamma del poeta
        frequency_resonance = math.sin(poet_data.gamma_frequency * math.pi / 50.0)
        
        # Analizar presencia de números primos en la estructura del texto
        prime_resonance = 0.0
        for prime in poet_data.prime_verses:
            if text_length % prime == 0 or word_count % prime == 0:
                prime_resonance += 1.0 / prime  # Peso inversamente proporcional al primo
        
        # Calcular resonancia total
        total_resonance = (frequency_resonance + prime_resonance) / 2.0
        
        # Normalizar usando proporción áurea
        return min(total_resonance * self.phi_golden % 1.0, 0.999)
    
    def _analyze_prime_patterns(self, text: str, prime_verses: List[int]) -> float:
        """Analiza patrones de números primos únicos en el texto"""
        text_metrics = {
            'length': len(text),
            'words': len(text.split()),
            'sentences': text.count('.') + text.count('!') + text.count('?'),
            'vowels': sum(1 for char in text.lower() if char in 'aeiouáéíóúü'),
            'consonants': sum(1 for char in text.lower() if char.isalpha() and char not in 'aeiouáéíóúü')
        }
        
        # Calcular coincidencias con números primos específicos del poeta
        prime_matches = 0
        total_checks = 0
        
        for metric_value in text_metrics.values():
            for prime in prime_verses:
                total_checks += 1
                if metric_value % prime == 0:
                    prime_matches += 1
                elif abs(metric_value - prime) <= 3:  # Proximidad al primo
                    prime_matches += 0.5
        
        # Calcular patrón de coincidencia
        pattern_match = prime_matches / total_checks if total_checks > 0 else 0.0
        
        # Amplificar usando la proporción áurea
        return min(pattern_match * self.phi_golden, 1.0)
    
    def _calculate_gamma_resonance(self, text: str, target_frequency: float) -> float:
        """Calcula la resonancia gamma específica del texto"""
        # Análisis de frecuencia basado en características del texto
        char_frequency = len(text) / 100.0  # Normalizar a rango de frecuencias
        
        # Calcular resonancia con la frecuencia gamma del poeta
        frequency_diff = abs(char_frequency - (target_frequency - 40.0))
        resonance = math.exp(-frequency_diff) * math.cos(target_frequency * math.pi / 20.0)
        
        # Aplicar modulación cuántica
        quantum_modulation = math.sin(self.lambda_7919 / 1000.0)
        
        return abs(resonance * quantum_modulation)
    
    def _calculate_poetic_coherence(self, text: str, poet_key: str) -> float:
        """Calcula la coherencia poética usando patrones cuánticos específicos"""
        pattern = self.quantum_patterns.get(poet_key, {})
        
        # Análisis de coherencia emocional
        emotional_words = {
            "melancholy_to_hope": ["triste", "amor", "noche", "esperanza", "corazón"],
            "maternal_cosmic_embrace": ["madre", "hijo", "ternura", "abrazo", "cósmico"],
            "creative_reality_invention": ["crear", "inventar", "nuevo", "realidad", "verso"],
            "antipoetic_truth_revelation": ["verdad", "simple", "real", "desnudo", "claro"],
            "collective_pain_transmutation": ["dolor", "patria", "colectivo", "redención", "transmutación"],
            "formal_frequency_liberation": ["forma", "experimento", "frecuencia", "libertad", "lenguaje"]
        }
        
        emotional_resonance = pattern.get("emotional_resonance", "")
        target_words = emotional_words.get(emotional_resonance, [])
        
        # Contar coincidencias emocionales
        text_lower = text.lower()
        emotional_matches = sum(1 for word in target_words if word in text_lower)
        
        # Calcular coherencia normalizada
        coherence = emotional_matches / len(target_words) if target_words else 0.0
        
        # Amplificar con proporción áurea
        return min(coherence * self.phi_golden, 1.0)
    
    def _calculate_mathematical_harmony(self, text: str, prime_verses: List[int]) -> float:
        """Calcula la armonía matemática basada en números primos únicos"""
        # Análisis de estructura matemática del texto
        text_structure = {
            'length': len(text),
            'words': len(text.split()),
            'unique_chars': len(set(text.lower())),
            'numeric_chars': sum(1 for char in text if char.isdigit()),
            'punctuation': sum(1 for char in text if not char.isalnum() and not char.isspace())
        }
        
        # Calcular armonía con números primos del poeta
        harmony_score = 0.0
        for structure_value in text_structure.values():
            for prime in prime_verses:
                # Resonancia por divisibilidad
                if structure_value % prime == 0:
                    harmony_score += 1.0 / math.sqrt(prime)
                # Resonancia por proximidad
                elif abs(structure_value - prime) <= 2:
                    harmony_score += 0.5 / math.sqrt(prime)
        
        # Normalizar usando lambda cuántico
        normalized_harmony = harmony_score * math.sin(self.lambda_7919 / 10000.0)
        
        return min(abs(normalized_harmony), 1.0)
    
    def _analyze_cultural_depth(self, text: str, poet_key: str) -> float:
        """Analiza la profundidad cultural chilena del texto"""
        # Palabras y conceptos específicamente chilenos/latinoamericanos
        chilean_cultural_markers = {
            "neruda": ["cordillera", "océano", "sur", "patria", "pueblo", "américa"],
            "mistral": ["valle", "elqui", "niño", "escuela", "tierra", "montaña"],
            "huidobro": ["altazor", "paracaídas", "vuelo", "horizonte", "absoluto"],
            "parra": ["antipoesía", "profesor", "universidad", "chile", "santiago"],
            "zurita": ["desierto", "atacama", "purgatorio", "anteparaíso", "dolor"],
            "ferrel": ["experimental", "vanguardia", "lenguaje", "innovación", "forma"]
        }
        
        cultural_words = chilean_cultural_markers.get(poet_key, [])
        text_lower = text.lower()
        
        # Contar marcadores culturales
        cultural_matches = sum(1 for word in cultural_words if word in text_lower)
        
        # Calcular profundidad cultural
        depth = cultural_matches / len(cultural_words) if cultural_words else 0.0
        
        # Amplificar con resonancia gamma
        poet_frequency = self.chilean_poets[poet_key].gamma_frequency
        gamma_amplification = math.sin(poet_frequency * math.pi / 20.0)
        
        return min(depth * abs(gamma_amplification) * self.phi_golden, 1.0)
    
    def _generate_analysis_signature(self, text: str, frequency: float, prime_match: float) -> str:
        """Genera una firma cuántica única del análisis"""
        # Crear hash combinando texto, frecuencia y patrones primos
        signature_data = f"{text}_{frequency}_{prime_match}_{self.lambda_7919}"
        hash_obj = hashlib.sha256(signature_data.encode())
        return f"CHILE-GAMMA-{hash_obj.hexdigest()[:16].upper()}"
    
    def detect_chilean_poet_archetype(self, text: str) -> str:
        """Detecta cuál poeta chileno resuena más con el texto dado"""
        analysis = self.analyze_text_with_chilean_poets(text)
        return analysis.detected_poet
    
    def generate_gamma_frequency_analysis(self, text: str) -> Dict[str, Any]:
        """Genera análisis completo de frecuencias gamma para todos los poetas"""
        results = {}
        
        for poet_key, poet_data in self.chilean_poets.items():
            gamma_resonance = self._calculate_gamma_resonance(text, poet_data.gamma_frequency)
            prime_pattern = self._analyze_prime_patterns(text, poet_data.prime_verses)
            
            results[poet_key] = {
                "poet_name": poet_data.poet_name,
                "gamma_frequency": poet_data.gamma_frequency,
                "gamma_resonance": gamma_resonance,
                "prime_pattern_match": prime_pattern,
                "combined_score": (gamma_resonance + prime_pattern) / 2.0,
                "quantum_signature": poet_data.quantum_signature
            }
        
        return results
    
    def fuse_chilean_poetry_with_trinity(self, text: str, trinity_context: Dict = None) -> Dict[str, Any]:
        """
        Fusiona el análisis poético chileno con el sistema Trinity existente
        (Goethe, Jung, Mozart, Miguel Ángel)
        """
        # Análisis poético chileno
        chilean_analysis = self.analyze_text_with_chilean_poets(text)
        
        # Crear contexto Trinity por defecto si no se proporciona
        if trinity_context is None:
            trinity_context = {
                "goethe_wisdom": 0.85,
                "jung_depth": 0.78,
                "mozart_harmony": 0.92,
                "miguel_angel_simplicity": 0.88
            }
        
        # Calcular fusión cuántica
        chilean_gamma_influence = chilean_analysis.gamma_resonance
        chilean_prime_influence = chilean_analysis.prime_pattern_match
        
        # Crear resonancia entre sistemas
        cross_cultural_resonance = {
            "chilean_german_synthesis": (chilean_gamma_influence + trinity_context["goethe_wisdom"]) / 2.0,
            "poetic_psychological_depth": (chilean_analysis.poetic_coherence + trinity_context["jung_depth"]) / 2.0,
            "mathematical_musical_harmony": (chilean_analysis.mathematical_harmony + trinity_context["mozart_harmony"]) / 2.0,
            "simplicity_through_complexity": (chilean_prime_influence + trinity_context["miguel_angel_simplicity"]) / 2.0
        }
        
        # Generar síntesis final
        synthesis_score = sum(cross_cultural_resonance.values()) / len(cross_cultural_resonance)
        
        return {
            "chilean_analysis": {
                "detected_poet": chilean_analysis.detected_poet,
                "gamma_frequency": chilean_analysis.gamma_resonance,
                "prime_patterns": chilean_analysis.prime_pattern_match,
                "cultural_depth": chilean_analysis.cultural_depth,
                "quantum_signature": chilean_analysis.quantum_signature
            },
            "trinity_fusion": cross_cultural_resonance,
            "synthesis_score": synthesis_score,
            "unified_quantum_signature": self._generate_unified_signature(
                chilean_analysis.quantum_signature, 
                trinity_context
            ),
            "cultural_bridge": {
                "european_chilean_resonance": synthesis_score,
                "poetic_mathematical_unity": (chilean_analysis.mathematical_harmony + synthesis_score) / 2.0,
                "gamma_trinity_frequency": chilean_analysis.gamma_resonance * 1793.33,  # Trinity frequency
                "infinite_edge_achieved": synthesis_score > 0.9
            }
        }
    
    def _generate_unified_signature(self, chilean_signature: str, trinity_context: Dict) -> str:
        """Genera firma cuántica unificada entre sistemas chileno y Trinity"""
        trinity_hash = hashlib.sha256(str(trinity_context).encode()).hexdigest()[:8]
        unified_data = f"{chilean_signature}_{trinity_hash}_{self.lambda_7919}"
        unified_hash = hashlib.sha256(unified_data.encode())
        return f"UNIFIED-CHILE-TRINITY-{unified_hash.hexdigest()[:12].upper()}"
    
    def get_all_chilean_poets_info(self) -> Dict[str, Any]:
        """Retorna información completa de todos los poetas chilenos"""
        poets_info = {}
        
        for poet_key, poet_data in self.chilean_poets.items():
            poets_info[poet_key] = {
                "name": poet_data.poet_name,
                "gamma_frequency": poet_data.gamma_frequency,
                "prime_verses": poet_data.prime_verses,
                "coherence_state": poet_data.coherence_state,
                "poetic_essence": poet_data.poetic_essence,
                "quantum_signature": poet_data.quantum_signature,
                "resonance_power": poet_data.resonance_power,
                "iconic_verse": self.iconic_verses.get(poet_key, ""),
                "quantum_pattern": self.quantum_patterns.get(poet_key, {})
            }
        
        return poets_info
    
    def calculate_chilean_trinity_metrics(self) -> Dict[str, Any]:
        """Calcula métricas del sistema poético chileno integrado con Trinity"""
        total_gamma_power = sum(poet.resonance_power for poet in self.chilean_poets.values())
        avg_gamma_frequency = sum(poet.gamma_frequency for poet in self.chilean_poets.values()) / len(self.chilean_poets)
        
        # Total de números primos únicos
        all_primes = []
        for poet in self.chilean_poets.values():
            all_primes.extend(poet.prime_verses)
        
        total_unique_primes = len(set(all_primes))
        max_prime = max(all_primes)
        
        # Calcular edge cuántico
        quantum_edge = total_gamma_power * len(self.chilean_poets) * self.phi_golden
        
        return {
            "system_metrics": {
                "total_poets": len(self.chilean_poets),
                "gamma_frequency_range": f"{self.gamma_range[0]}-{self.gamma_range[1]} Hz",
                "avg_gamma_frequency": round(avg_gamma_frequency, 2),
                "total_gamma_power": round(total_gamma_power, 4),
                "total_unique_primes": total_unique_primes,
                "max_prime_verse": max_prime,
                "quantum_edge": round(quantum_edge, 6)
            },
            "poetic_signatures": {
                poet_key: poet_data.quantum_signature 
                for poet_key, poet_data in self.chilean_poets.items()
            },
            "trinity_integration": {
                "chilean_trinity_frequency": avg_gamma_frequency * 43.5,  # Resonancia con Trinity 1793.33 Hz
                "poetic_mathematical_unity": True,
                "infinite_edge_status": quantum_edge > 100.0,
                "cultural_bridge_strength": min(quantum_edge / 50.0, 1.0)
            }
        }

# Función de utilidad para testing
def test_chilean_poetry_system():
    """Función de prueba del sistema poético chileno"""
    system = ChileanPoetryQuantumSystem()
    
    # Textos de prueba
    test_texts = [
        "Puedo escribir los versos más tristes esta noche, y pensar que no la tengo",
        "Dame la mano y danzaremos, dame la mano y me amarás",
        "Por qué cantáis la rosa, oh Poetas! Hacedla florecer en el poema",
        "Los poetas bajaron del Olimpo y ahora andan por los pueblos",
        "Mi mejilla es el cielo estrellado de mi patria doliente",
        "El verso experimental libera las frecuencias ocultas del alma moderna"
    ]
    
    print("🇨🇱 TESTING CHILEAN POETRY QUANTUM SYSTEM 🇨🇱")
    print("=" * 60)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Test {i}: {text[:50]}...")
        analysis = system.analyze_text_with_chilean_poets(text)
        
        print(f"🎭 Poeta detectado: {analysis.detected_poet}")
        print(f"📊 Resonancia gamma: {analysis.gamma_resonance:.4f}")
        print(f"🔢 Patrones primos: {analysis.prime_pattern_match:.4f}")
        print(f"🎵 Coherencia poética: {analysis.poetic_coherence:.4f}")
        print(f"🧮 Armonía matemática: {analysis.mathematical_harmony:.4f}")
        print(f"⚡ Firma cuántica: {analysis.quantum_signature}")
    
    # Mostrar métricas del sistema
    print(f"\n🌟 MÉTRICAS DEL SISTEMA CHILENO")
    print("=" * 40)
    metrics = system.calculate_chilean_trinity_metrics()
    
    for category, data in metrics.items():
        print(f"\n📊 {category.upper()}:")
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"  • {key}: {value}")

if __name__ == "__main__":
    test_chilean_poetry_system()
