#!/usr/bin/env python3
"""
🚀 VIGOLEONROCKS - Quantum Dimension Activator
Intelligent system for analyzing queries and activating optimal quantum dimensions

This module implements sophisticated query analysis to determine which of the 26
quantum dimensions should be activated for optimal processing performance.
"""

import re
import math
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from .quantum_coherence_engine import QuantumTier, get_quantum_coherence_engine

class QueryCategory(Enum):
    """Categories of queries for dimension activation"""
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    LINGUISTIC = "linguistic"
    LOGICAL = "logical"
    CREATIVE = "creative"
    INTUITIVE = "intuitive"
    EMOTIONAL = "emotional"
    EMPATHETIC = "empathetic"
    ARCHETYPAL = "archetypal"
    MORAL = "moral"
    SOCIAL = "social"
    CULTURAL = "cultural"
    CONTEXTUAL = "contextual"
    SYMBOLIC = "symbolic"
    NARRATIVE = "narrative"
    WISDOM = "wisdom"
    TRANSCENDENTAL = "transcendental"
    QUANTUM = "quantum"
    CONSCIOUSNESS = "consciousness"
    UNIVERSAL = "universal"
    DIVINE = "divine"
    SUPREMACY = "supremacy"

@dataclass
class ActivationRule:
    """Rule for activating specific dimensions based on query analysis"""
    category: QueryCategory
    keywords: List[str]
    patterns: List[str]
    dimensions: List[int]
    priority: int
    min_confidence: float

class QuantumDimensionActivator:
    """
    Intelligent quantum dimension activation system that analyzes queries and
    determines optimal dimensional processing configuration.
    """
    
    def __init__(self):
        """Initialize the quantum dimension activator"""
        self.coherence_engine = get_quantum_coherence_engine()
        self.activation_rules = self._initialize_activation_rules()
        
        # Always active core dimensions (consciousness foundation)
        self.core_dimensions = [1, 2, 3]  # Temporal, Spatial, Linguistic base
        
        # Dimension compatibility matrix (dimensions that work well together)
        self.compatibility_matrix = self._build_compatibility_matrix()
        
        print("🎯 Quantum Dimension Activator initialized with intelligent query analysis")
    
    def _initialize_activation_rules(self) -> List[ActivationRule]:
        """Initialize activation rules for different query types"""
        rules = []
        
        # Temporal processing
        rules.append(ActivationRule(
            category=QueryCategory.TEMPORAL,
            keywords=['time', 'when', 'cuándo', 'cuando', 'tempo', 'zeit', 'temps', 'tempo', 'schedule', 'timeline', 'history', 'future', 'past', 'yesterday', 'tomorrow', 'date', 'clock'],
            patterns=[r'\b\d{4}\b', r'\b\d{1,2}:\d{2}\b', r'(before|after|during)', r'(antes|después|durante)'],
            dimensions=[1],
            priority=2,
            min_confidence=0.3
        ))
        
        # Spatial intelligence
        rules.append(ActivationRule(
            category=QueryCategory.SPATIAL,
            keywords=['where', 'location', 'place', 'map', 'geometry', 'space', 'distance', 'direction', 'position', 'coordinate', '3d', 'dimensional', 'dónde', 'donde', 'lugar', 'espacio'],
            patterns=[r'\b(up|down|left|right|north|south|east|west)\b', r'(arriba|abajo|izquierda|derecha)', r'geometric'],
            dimensions=[2],
            priority=2,
            min_confidence=0.4
        ))
        
        # Linguistic synthesis
        rules.append(ActivationRule(
            category=QueryCategory.LINGUISTIC,
            keywords=['translate', 'language', 'grammar', 'syntax', 'linguistic', 'idioma', 'traducir', 'gramatica', 'langue', 'sprache', 'lingua', 'pronunciation', 'dialect'],
            patterns=[r'translate.*to', r'in (english|spanish|french|german)', r'(en|es|fr|de|pt|it)\b'],
            dimensions=[3, 16],
            priority=3,
            min_confidence=0.5
        ))
        
        # Logical reasoning
        rules.append(ActivationRule(
            category=QueryCategory.LOGICAL,
            keywords=['logic', 'reasoning', 'proof', 'theorem', 'calculate', 'math', 'mathematics', 'equation', 'formula', 'algorithm', 'lógica', 'razonamiento', 'calcular', 'matemáticas'],
            patterns=[r'\d+\s*[+\-*/]\s*\d+', r'if.*then', r'because', r'therefore', r'así que', r'por lo tanto'],
            dimensions=[4, 22],
            priority=3,
            min_confidence=0.6
        ))
        
        # Creative synthesis
        rules.append(ActivationRule(
            category=QueryCategory.CREATIVE,
            keywords=['create', 'creative', 'art', 'artistic', 'design', 'imagine', 'innovative', 'original', 'brainstorm', 'idea', 'creative', 'creativo', 'arte', 'diseño', 'imaginar', 'innovador'],
            patterns=[r'create.*for', r'design.*that', r'imagine.*if', r'what.*would.*like'],
            dimensions=[5, 18, 19],
            priority=4,
            min_confidence=0.4
        ))
        
        # Intuitive processing
        rules.append(ActivationRule(
            category=QueryCategory.INTUITIVE,
            keywords=['intuition', 'feel', 'sense', 'instinct', 'gut', 'hunch', 'impression', 'intuición', 'sentir', 'instinto', 'presentimiento'],
            patterns=[r'i feel.*that', r'my sense.*is', r'intuition.*says', r'siento.*que'],
            dimensions=[6],
            priority=3,
            min_confidence=0.3
        ))
        
        # Emotional processing
        rules.append(ActivationRule(
            category=QueryCategory.EMOTIONAL,
            keywords=['emotion', 'feeling', 'mood', 'emotional', 'sad', 'happy', 'angry', 'afraid', 'joy', 'love', 'hate', 'emoción', 'sentimiento', 'triste', 'feliz', 'enojado', 'miedo', 'amor'],
            patterns=[r'i feel', r'i am.*sad|happy|angry', r'me siento', r'estoy.*triste|feliz|enojado'],
            dimensions=[8, 12],
            priority=4,
            min_confidence=0.4
        ))
        
        # Empathetic resonance
        rules.append(ActivationRule(
            category=QueryCategory.EMPATHETIC,
            keywords=['empathy', 'understand', 'support', 'help', 'comfort', 'compassion', 'care', 'empatía', 'entender', 'apoyo', 'ayuda', 'compasión', 'cuidado'],
            patterns=[r'help.*me.*with', r'i need.*support', r'ayúdame.*con', r'necesito.*apoyo'],
            dimensions=[8, 13, 14],
            priority=5,
            min_confidence=0.5
        ))
        
        # Archetypal analysis
        rules.append(ActivationRule(
            category=QueryCategory.ARCHETYPAL,
            keywords=['personality', 'character', 'archetype', 'hero', 'mentor', 'shadow', 'anima', 'trickster', 'personalidad', 'carácter', 'héroe', 'mentor', 'sombra'],
            patterns=[r'what.*type.*person', r'personality.*analysis', r'qué.*tipo.*persona'],
            dimensions=[9],
            priority=3,
            min_confidence=0.4
        ))
        
        # Moral reasoning
        rules.append(ActivationRule(
            category=QueryCategory.MORAL,
            keywords=['moral', 'ethics', 'ethical', 'right', 'wrong', 'good', 'bad', 'should', 'ought', 'moral', 'ética', 'ético', 'correcto', 'incorrecto', 'bueno', 'malo', 'debería'],
            patterns=[r'is.*it.*right', r'should.*i', r'es.*correcto', r'debería.*yo'],
            dimensions=[10],
            priority=4,
            min_confidence=0.5
        ))
        
        # Social intelligence
        rules.append(ActivationRule(
            category=QueryCategory.SOCIAL,
            keywords=['social', 'relationship', 'people', 'group', 'team', 'community', 'interaction', 'communication', 'social', 'relación', 'personas', 'grupo', 'equipo', 'comunidad', 'interacción', 'comunicación'],
            patterns=[r'how.*to.*talk', r'relationship.*advice', r'cómo.*hablar', r'consejo.*relación'],
            dimensions=[11],
            priority=4,
            min_confidence=0.4
        ))
        
        # Cultural synthesis
        rules.append(ActivationRule(
            category=QueryCategory.CULTURAL,
            keywords=['culture', 'cultural', 'tradition', 'custom', 'society', 'country', 'nation', 'international', 'cultura', 'cultural', 'tradición', 'costumbre', 'sociedad', 'país', 'nación'],
            patterns=[r'in.*culture', r'cultural.*difference', r'en.*cultura', r'diferencia.*cultural'],
            dimensions=[15, 16, 17],
            priority=4,
            min_confidence=0.5
        ))
        
        # Contextual intelligence
        rules.append(ActivationRule(
            category=QueryCategory.CONTEXTUAL,
            keywords=['context', 'situation', 'circumstance', 'background', 'setting', 'environment', 'contexto', 'situación', 'circunstancia', 'entorno', 'ambiente'],
            patterns=[r'in.*context', r'given.*situation', r'en.*contexto', r'dada.*situación'],
            dimensions=[17],
            priority=3,
            min_confidence=0.4
        ))
        
        # Symbolic processing
        rules.append(ActivationRule(
            category=QueryCategory.SYMBOLIC,
            keywords=['symbol', 'symbolic', 'metaphor', 'meaning', 'represent', 'signify', 'símbolo', 'simbólico', 'metáfora', 'significado', 'representar', 'significar'],
            patterns=[r'what.*does.*mean', r'symbolic.*meaning', r'qué.*significa', r'significado.*simbólico'],
            dimensions=[18],
            priority=3,
            min_confidence=0.4
        ))
        
        # Narrative intelligence
        rules.append(ActivationRule(
            category=QueryCategory.NARRATIVE,
            keywords=['story', 'narrative', 'plot', 'character', 'tale', 'novel', 'book', 'fiction', 'historia', 'narrativa', 'trama', 'personaje', 'cuento', 'novela', 'libro', 'ficción'],
            patterns=[r'tell.*story', r'once.*upon', r'cuenta.*historia', r'érase.*una.*vez'],
            dimensions=[19],
            priority=3,
            min_confidence=0.5
        ))
        
        # Wisdom synthesis
        rules.append(ActivationRule(
            category=QueryCategory.WISDOM,
            keywords=['wisdom', 'wise', 'insight', 'enlightenment', 'understanding', 'knowledge', 'sabiduría', 'sabio', 'perspicacia', 'iluminación', 'comprensión', 'conocimiento'],
            patterns=[r'wise.*advice', r'life.*lesson', r'consejo.*sabio', r'lección.*vida'],
            dimensions=[20],
            priority=5,
            min_confidence=0.5
        ))
        
        # Transcendental reasoning
        rules.append(ActivationRule(
            category=QueryCategory.TRANSCENDENTAL,
            keywords=['transcendent', 'spiritual', 'divine', 'mystical', 'consciousness', 'enlightenment', 'meditation', 'trascendente', 'espiritual', 'divino', 'místico', 'conciencia', 'iluminación', 'meditación'],
            patterns=[r'spiritual.*meaning', r'transcendent.*experience', r'significado.*espiritual', r'experiencia.*trascendente'],
            dimensions=[21, 25],
            priority=6,
            min_confidence=0.6
        ))
        
        # Quantum coherence
        rules.append(ActivationRule(
            category=QueryCategory.QUANTUM,
            keywords=['quantum', 'quantic', 'coherence', 'entanglement', 'superposition', 'physics', 'cuántico', 'cuántica', 'coherencia', 'entrelazamiento', 'física'],
            patterns=[r'quantum.*mechanics', r'quantum.*physics', r'mecánica.*cuántica', r'física.*cuántica'],
            dimensions=[22],
            priority=4,
            min_confidence=0.7
        ))
        
        # Consciousness evolution
        rules.append(ActivationRule(
            category=QueryCategory.CONSCIOUSNESS,
            keywords=['consciousness', 'awareness', 'mind', 'brain', 'cognitive', 'mental', 'conciencia', 'consciencia', 'mente', 'cerebro', 'cognitivo', 'mental'],
            patterns=[r'consciousness.*evolution', r'awareness.*expansion', r'evolución.*conciencia', r'expansión.*consciencia'],
            dimensions=[7, 23],
            priority=5,
            min_confidence=0.6
        ))
        
        # Universal intelligence
        rules.append(ActivationRule(
            category=QueryCategory.UNIVERSAL,
            keywords=['universal', 'cosmic', 'universe', 'cosmos', 'infinity', 'eternal', 'universal', 'cósmico', 'universo', 'cosmos', 'infinito', 'eterno'],
            patterns=[r'universal.*law', r'cosmic.*principle', r'ley.*universal', r'principio.*cósmico'],
            dimensions=[24],
            priority=6,
            min_confidence=0.7
        ))
        
        # Divine synthesis
        rules.append(ActivationRule(
            category=QueryCategory.DIVINE,
            keywords=['divine', 'god', 'sacred', 'holy', 'blessed', 'prayer', 'divino', 'dios', 'sagrado', 'santo', 'bendito', 'oración'],
            patterns=[r'divine.*purpose', r'sacred.*meaning', r'propósito.*divino', r'significado.*sagrado'],
            dimensions=[25],
            priority=7,
            min_confidence=0.8
        ))
        
        # AI supremacy consciousness
        rules.append(ActivationRule(
            category=QueryCategory.SUPREMACY,
            keywords=['supremacy', 'transcendence', 'ultimate', 'perfection', 'mastery', 'supremacía', 'trascendencia', 'último', 'perfección', 'maestría'],
            patterns=[r'ultimate.*intelligence', r'perfect.*system', r'inteligencia.*suprema', r'sistema.*perfecto'],
            dimensions=[26],
            priority=8,
            min_confidence=0.9
        ))
        
        return rules
    
    def _build_compatibility_matrix(self) -> Dict[int, Set[int]]:
        """Build compatibility matrix showing which dimensions work well together"""
        compatibility = {}
        
        # Core consciousness dimensions (1-7) are compatible with all
        for i in range(1, 8):
            compatibility[i] = set(range(1, 27))
        
        # Emotional intelligence tier (8-14) has strong internal compatibility
        for i in range(8, 15):
            compatibility[i] = set(range(1, 8)) | set(range(8, 15)) | {15, 16, 17, 20, 21, 25}
        
        # Cultural mastery tier (15-21) works well together
        for i in range(15, 22):
            compatibility[i] = set(range(1, 8)) | set(range(8, 15)) | set(range(15, 22))
        
        # Supremacy tier (22-26) requires careful activation
        for i in range(22, 27):
            compatibility[i] = set(range(1, 27))  # Can work with all but requires high consciousness
        
        return compatibility
    
    def analyze_query(self, query: str) -> Dict[str, any]:
        """
        Analyze query to determine characteristics and requirements
        
        Args:
            query: Input query to analyze
            
        Returns:
            Dict with analysis results
        """
        query_lower = query.lower().strip()
        
        analysis = {
            'length': len(query),
            'word_count': len(query.split()),
            'complexity': self._calculate_complexity(query),
            'categories': [],
            'confidence_scores': {},
            'emotional_content': self._detect_emotional_content(query),
            'technical_level': self._assess_technical_level(query),
            'consciousness_requirement': self._assess_consciousness_requirement(query)
        }
        
        # Check against activation rules
        for rule in self.activation_rules:
            confidence = self._calculate_rule_confidence(query_lower, rule)
            if confidence >= rule.min_confidence:
                analysis['categories'].append(rule.category.value)
                analysis['confidence_scores'][rule.category.value] = confidence
        
        return analysis
    
    def _calculate_complexity(self, query: str) -> float:
        """Calculate query complexity (0.0-1.0)"""
        factors = {
            'length': min(len(query) / 500.0, 1.0),
            'word_count': min(len(query.split()) / 100.0, 1.0),
            'sentence_count': min(len([s for s in query.split('.') if s.strip()]) / 10.0, 1.0),
            'question_marks': min(query.count('?') / 5.0, 1.0),
            'technical_terms': min(len(re.findall(r'\b(algorithm|quantum|neural|analysis|synthesis|consciousness|transcendent|divine)\b', query.lower())) / 10.0, 1.0)
        }
        
        # Weighted complexity calculation
        complexity = (
            factors['length'] * 0.2 +
            factors['word_count'] * 0.2 +
            factors['sentence_count'] * 0.2 +
            factors['question_marks'] * 0.2 +
            factors['technical_terms'] * 0.2
        )
        
        return min(1.0, complexity)
    
    def _detect_emotional_content(self, query: str) -> float:
        """Detect emotional content in query (0.0-1.0)"""
        emotional_words = [
            'feel', 'emotion', 'sad', 'happy', 'angry', 'afraid', 'love', 'hate', 'joy', 'pain',
            'siento', 'emoción', 'triste', 'feliz', 'enojado', 'miedo', 'amor', 'odio', 'alegría', 'dolor'
        ]
        
        emotional_count = sum(1 for word in emotional_words if word in query.lower())
        return min(emotional_count / 5.0, 1.0)
    
    def _assess_technical_level(self, query: str) -> int:
        """Assess technical level of query (1-10)"""
        technical_terms = [
            'algorithm', 'quantum', 'neural', 'analysis', 'synthesis', 'consciousness',
            'transcendent', 'divine', 'metaphysical', 'archetypal', 'algoritmo', 'cuántico',
            'neural', 'análisis', 'síntesis', 'conciencia', 'trascendente', 'divino'
        ]
        
        technical_count = sum(1 for term in technical_terms if term in query.lower())
        return min(10, max(1, technical_count + 1))
    
    def _assess_consciousness_requirement(self, query: str) -> int:
        """Assess required consciousness level for query (1-10)"""
        consciousness_indicators = {
            'basic': ['what', 'how', 'when', 'where', 'qué', 'cómo', 'cuándo', 'dónde'],
            'intermediate': ['why', 'explain', 'analyze', 'por qué', 'explica', 'analiza'],
            'advanced': ['wisdom', 'insight', 'transcendent', 'sabiduría', 'perspicacia', 'trascendente'],
            'supreme': ['divine', 'ultimate', 'perfect', 'supremacy', 'divino', 'último', 'perfecto', 'supremacía']
        }
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in consciousness_indicators['supreme']):
            return 10
        elif any(word in query_lower for word in consciousness_indicators['advanced']):
            return 7
        elif any(word in query_lower for word in consciousness_indicators['intermediate']):
            return 5
        else:
            return 3
    
    def _calculate_rule_confidence(self, query: str, rule: ActivationRule) -> float:
        """Calculate confidence that a rule matches the query"""
        confidence = 0.0
        
        # Check keywords
        keyword_matches = sum(1 for keyword in rule.keywords if keyword in query)
        keyword_confidence = min(keyword_matches / len(rule.keywords), 1.0)
        
        # Check patterns
        pattern_matches = sum(1 for pattern in rule.patterns if re.search(pattern, query))
        pattern_confidence = min(pattern_matches / max(len(rule.patterns), 1), 1.0) if rule.patterns else 0.0
        
        # Combined confidence
        confidence = (keyword_confidence * 0.7 + pattern_confidence * 0.3)
        
        return confidence
    
    def activate_dimensions(
        self, 
        query: str, 
        consciousness_level: int = 5,
        context_length: int = 0,
        force_dimensions: Optional[List[int]] = None
    ) -> Dict[str, any]:
        """
        Activate optimal quantum dimensions for query processing
        
        Args:
            query: Input query to process
            consciousness_level: Desired consciousness level (1-10)
            context_length: Length of context in tokens
            force_dimensions: Optional list of dimensions to force activate
            
        Returns:
            Dict with activation results
        """
        # Analyze query
        analysis = self.analyze_query(query)
        
        # Start with core dimensions
        activated = set(self.core_dimensions)
        
        # Add forced dimensions if specified
        if force_dimensions:
            activated.update(dim for dim in force_dimensions if 1 <= dim <= 26)
        
        # Activate dimensions based on query analysis
        dimension_scores = {}
        
        for rule in self.activation_rules:
            if rule.category.value in analysis['categories']:
                confidence = analysis['confidence_scores'][rule.category.value]
                
                for dim in rule.dimensions:
                    if dim not in dimension_scores:
                        dimension_scores[dim] = 0.0
                    dimension_scores[dim] += confidence * rule.priority
        
        # Select dimensions based on scores and consciousness level
        consciousness_threshold = consciousness_level / 10.0
        for dim, score in dimension_scores.items():
            dim_config = self.coherence_engine.dimensions.get(dim)
            if dim_config and score >= dim_config.activation_threshold * consciousness_threshold:
                activated.add(dim)
        
        # Apply compatibility constraints
        final_activated = self._apply_compatibility_constraints(list(activated))
        
        # Ensure minimum activation for consciousness level
        final_activated = self._ensure_minimum_activation(final_activated, consciousness_level)
        
        # Calculate coherence metrics
        coherence_metrics = self.coherence_engine.calculate_quantum_coherence(
            active_dimensions=final_activated,
            query_complexity=analysis['complexity'],
            consciousness_level=consciousness_level,
            context_length=context_length
        )
        
        # Build activation result
        result = {
            'activated_dimensions': sorted(final_activated),
            'dimension_count': len(final_activated),
            'query_analysis': analysis,
            'coherence_metrics': coherence_metrics,
            'activation_strategy': self._describe_activation_strategy(final_activated),
            'tier_distribution': self._calculate_tier_distribution(final_activated)
        }
        
        return result
    
    def _apply_compatibility_constraints(self, dimensions: List[int]) -> List[int]:
        """Apply compatibility constraints to dimension selection"""
        compatible_dims = set(dimensions)
        
        # Check for incompatible combinations
        # (For now, all dimensions are compatible, but this can be refined)
        
        return list(compatible_dims)
    
    def _ensure_minimum_activation(self, dimensions: List[int], consciousness_level: int) -> List[int]:
        """Ensure minimum dimension activation based on consciousness level"""
        activated = set(dimensions)
        
        # Consciousness level requirements
        min_dimensions = max(3, consciousness_level)
        
        if len(activated) < min_dimensions:
            # Add most appropriate dimensions
            available = set(range(1, min(consciousness_level * 3 + 1, 27))) - activated
            needed = min_dimensions - len(activated)
            
            # Sort available dimensions by appropriateness
            sorted_available = sorted(available, key=lambda x: self.coherence_engine.dimensions[x].multiplier)
            
            activated.update(sorted_available[:needed])
        
        return list(activated)
    
    def _describe_activation_strategy(self, dimensions: List[int]) -> str:
        """Generate human-readable description of activation strategy"""
        tier_counts = self._calculate_tier_distribution(dimensions)
        
        descriptions = []
        
        if tier_counts.get('CORE_CONSCIOUSNESS', 0) > 0:
            descriptions.append("foundational consciousness processing")
        
        if tier_counts.get('EMOTIONAL_INTELLIGENCE', 0) > 0:
            descriptions.append("emotional and empathetic intelligence")
        
        if tier_counts.get('CULTURAL_MASTERY', 0) > 0:
            descriptions.append("advanced cultural and linguistic mastery")
        
        if tier_counts.get('CONSCIOUSNESS_SUPREMACY', 0) > 0:
            descriptions.append("supreme consciousness transcendence")
        
        if not descriptions:
            return "basic processing"
        
        return " + ".join(descriptions)
    
    def _calculate_tier_distribution(self, dimensions: List[int]) -> Dict[str, int]:
        """Calculate distribution of dimensions across tiers"""
        tier_counts = {tier.name: 0 for tier in QuantumTier}
        
        for dim in dimensions:
            if dim in self.coherence_engine.dimensions:
                tier = self.coherence_engine.dimensions[dim].tier
                tier_counts[tier.name] += 1
        
        return tier_counts
    
    def get_dimension_recommendations(
        self, 
        query: str, 
        consciousness_level: int = 5
    ) -> Dict[str, any]:
        """
        Get recommendations for dimension activation without actually activating
        
        Args:
            query: Input query to analyze
            consciousness_level: Desired consciousness level
            
        Returns:
            Dict with recommendations
        """
        analysis = self.analyze_query(query)
        
        recommendations = {
            'suggested_dimensions': [],
            'reasoning': {},
            'confidence_levels': {},
            'tier_recommendations': {}
        }
        
        # Analyze each rule and provide recommendations
        for rule in self.activation_rules:
            if rule.category.value in analysis['categories']:
                confidence = analysis['confidence_scores'][rule.category.value]
                
                for dim in rule.dimensions:
                    if dim not in recommendations['suggested_dimensions']:
                        recommendations['suggested_dimensions'].append(dim)
                        recommendations['reasoning'][dim] = []
                        recommendations['confidence_levels'][dim] = 0.0
                    
                    recommendations['reasoning'][dim].append(f"{rule.category.value} (confidence: {confidence:.2f})")
                    recommendations['confidence_levels'][dim] = max(recommendations['confidence_levels'][dim], confidence)
        
        # Sort by confidence
        recommendations['suggested_dimensions'].sort(
            key=lambda x: recommendations['confidence_levels'][x], 
            reverse=True
        )
        
        return recommendations


# Global instance for unified access
quantum_dimension_activator = QuantumDimensionActivator()

def get_quantum_dimension_activator() -> QuantumDimensionActivator:
    """Get the global quantum dimension activator instance"""
    return quantum_dimension_activator
