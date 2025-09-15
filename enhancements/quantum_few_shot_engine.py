"""
🎯⚛️ QUANTUM FEW-SHOT LEARNING ENGINE ⚛️🎯
============================================
Advanced few-shot learning system using quantum coherence-based
pattern matching and multidimensional similarity scoring.

Features:
- Domain-specific exemplar storage (MMLU domains)
- Quantum similarity scoring across 26 dimensions
- Adaptive learning from successful patterns
- Cross-domain knowledge transfer
- Quantum coherence-based example selection
- Multidimensional embeddings for better matching

Author: VIGOLEONROCKS Quantum Development Team
Version: 1.0.0 - Few-Shot Supremacy
"""

import re
import json
import math
import time
import hashlib
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from enum import Enum
import numpy as np

class MMLUDomain(Enum):
    # STEM Domains
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    COMPUTER_SCIENCE = "computer_science"
    ENGINEERING = "engineering"
    
    # Humanities
    HISTORY = "history"
    PHILOSOPHY = "philosophy"
    LITERATURE = "literature"
    LINGUISTICS = "linguistics"
    
    # Social Sciences
    PSYCHOLOGY = "psychology"
    SOCIOLOGY = "sociology"
    ECONOMICS = "economics"
    POLITICAL_SCIENCE = "political_science"
    
    # Professional
    LAW = "law"
    MEDICINE = "medicine"
    BUSINESS = "business"
    
    # General
    GENERAL = "general"

@dataclass
class QuantumExemplar:
    """Individual few-shot example with quantum properties"""
    query: str
    response: str
    domain: MMLUDomain
    difficulty: str  # easy, medium, hard
    quantum_embedding: List[float]  # 26-dimensional quantum embedding
    success_rate: float  # How often this example leads to correct answers
    coherence_score: float
    creation_time: float
    usage_count: int = 0
    last_used: float = 0.0
    
    @property
    def effectiveness_score(self) -> float:
        """Calculate overall effectiveness of this exemplar"""
        recency_factor = 1.0 / (1.0 + (time.time() - self.last_used) / 86400)  # Decay over days
        usage_factor = min(self.usage_count / 10.0, 1.0)  # Cap at 10 uses
        return (self.success_rate * 0.5 + 
                self.coherence_score * 0.3 + 
                recency_factor * 0.1 + 
                usage_factor * 0.1)

@dataclass
class SimilarityMatch:
    """Result of quantum similarity matching"""
    exemplar: QuantumExemplar
    similarity_score: float
    dimension_scores: Dict[int, float]  # Per-dimension similarity scores
    pattern_matches: List[str]  # Specific patterns that matched

class QuantumFewShotLearningEngine:
    """Advanced few-shot learning with quantum coherence"""
    
    def __init__(self, max_exemplars_per_domain: int = 100):
        self.max_exemplars_per_domain = max_exemplars_per_domain
        
        # Exemplar storage by domain
        self.exemplars: Dict[MMLUDomain, List[QuantumExemplar]] = defaultdict(list)
        
        # Pattern recognition components
        self.pattern_extractors = self._initialize_pattern_extractors()
        self.quantum_dimensions = self._initialize_quantum_dimensions()
        
        # Performance tracking
        self.domain_performance: Dict[MMLUDomain, Dict[str, float]] = defaultdict(dict)
        self.cross_domain_transfers = defaultdict(int)
        
        print("🎯⚛️ Quantum Few-Shot Learning Engine initialized")
    
    def _initialize_pattern_extractors(self) -> Dict[str, callable]:
        """Initialize pattern extraction functions"""
        return {
            'question_type': self._extract_question_type,
            'key_concepts': self._extract_key_concepts,
            'complexity_level': self._extract_complexity_level,
            'reasoning_pattern': self._extract_reasoning_pattern,
            'domain_vocabulary': self._extract_domain_vocabulary,
            'structure_pattern': self._extract_structure_pattern
        }
    
    def _initialize_quantum_dimensions(self) -> Dict[int, str]:
        """Initialize 26 quantum dimensions for embedding"""
        return {
            1: "factual_knowledge",
            2: "conceptual_understanding", 
            3: "analytical_reasoning",
            4: "problem_solving",
            5: "pattern_recognition",
            6: "causal_relationships",
            7: "temporal_reasoning",
            8: "spatial_reasoning",
            9: "logical_inference",
            10: "mathematical_reasoning",
            11: "linguistic_patterns",
            12: "semantic_similarity",
            13: "syntactic_structure",
            14: "contextual_awareness",
            15: "domain_expertise",
            16: "cross_domain_transfer",
            17: "abstraction_level",
            18: "complexity_handling",
            19: "uncertainty_tolerance",
            20: "creative_thinking",
            21: "critical_evaluation",
            22: "evidence_assessment",
            23: "hypothesis_formation",
            24: "explanation_quality",
            25: "coherence_maintenance",
            26: "quantum_resonance"
        }
    
    def learn_from_example(self, query: str, response: str, domain: MMLUDomain, 
                          difficulty: str = "medium", success_rate: float = 1.0) -> str:
        """Learn from a successful query-response pair"""
        
        # Generate quantum embedding
        embedding = self._generate_quantum_embedding(query, response, domain)
        
        # Calculate coherence score
        coherence = self._calculate_quantum_coherence(query, response, embedding)
        
        # Create exemplar
        exemplar = QuantumExemplar(
            query=query,
            response=response,
            domain=domain,
            difficulty=difficulty,
            quantum_embedding=embedding,
            success_rate=success_rate,
            coherence_score=coherence,
            creation_time=time.time()
        )
        
        # Store exemplar
        self._store_exemplar(exemplar)
        
        # Update domain performance
        self._update_domain_performance(domain, difficulty, success_rate)
        
        return f"Learned exemplar with coherence {coherence:.3f}"
    
    def find_similar_examples(self, query: str, domain: MMLUDomain, 
                            top_k: int = 5) -> List[SimilarityMatch]:
        """Find the most similar examples using quantum similarity"""
        
        query_embedding = self._generate_query_embedding(query, domain)
        matches = []
        
        # Search in primary domain
        primary_matches = self._search_domain(query, query_embedding, domain)
        matches.extend(primary_matches)
        
        # Cross-domain search for additional insights
        cross_domain_matches = self._cross_domain_search(query, query_embedding, domain)
        matches.extend(cross_domain_matches)
        
        # Sort by similarity score and quantum coherence
        matches.sort(key=lambda x: x.similarity_score * x.exemplar.coherence_score, reverse=True)
        
        # Update usage statistics
        for match in matches[:top_k]:
            match.exemplar.usage_count += 1
            match.exemplar.last_used = time.time()
        
        return matches[:top_k]
    
    def generate_few_shot_prompt(self, query: str, domain: MMLUDomain, 
                               num_examples: int = 3) -> str:
        """Generate few-shot prompt with best examples"""
        
        similar_matches = self.find_similar_examples(query, domain, num_examples)
        
        if not similar_matches:
            return f"Query: {query}\n\nNo similar examples found. Using quantum reasoning..."
        
        # Build few-shot prompt
        prompt_parts = ["Few-shot examples for quantum-enhanced reasoning:"]
        prompt_parts.append("")
        
        for i, match in enumerate(similar_matches, 1):
            exemplar = match.exemplar
            prompt_parts.append(f"Example {i} (Similarity: {match.similarity_score:.2f}, "
                              f"Domain: {exemplar.domain.value}):")
            prompt_parts.append(f"Q: {exemplar.query}")
            prompt_parts.append(f"A: {exemplar.response}")
            prompt_parts.append("")
        
        # Add current query
        prompt_parts.append("Now answer this query using quantum reasoning and the patterns above:")
        prompt_parts.append(f"Q: {query}")
        prompt_parts.append("A: ")
        
        return "\n".join(prompt_parts)
    
    def adaptive_learning_update(self, query: str, domain: MMLUDomain, 
                               response: str, success: bool):
        """Update learning based on query success/failure"""
        
        # Find the examples that were used for this query
        similar_matches = self.find_similar_examples(query, domain, 3)
        
        # Update success rates
        for match in similar_matches:
            if success:
                # Boost success rate of good examples
                match.exemplar.success_rate = min(1.0, 
                    match.exemplar.success_rate * 1.05 + 0.02)
            else:
                # Reduce success rate of examples that led to failure
                match.exemplar.success_rate = max(0.1,
                    match.exemplar.success_rate * 0.95 - 0.02)
        
        # If successful, potentially learn this new example
        if success and len(response) > 50:  # Substantial response
            coherence = self._calculate_quantum_coherence(query, response, 
                                                        self._generate_query_embedding(query, domain))
            if coherence > 0.7:  # High coherence threshold
                self.learn_from_example(query, response, domain, "medium", 0.8)
    
    def _generate_quantum_embedding(self, query: str, response: str, 
                                  domain: MMLUDomain) -> List[float]:
        """Generate 26-dimensional quantum embedding"""
        
        embedding = []
        text = f"{query} {response}".lower()
        
        for dim_id, dim_name in self.quantum_dimensions.items():
            if dim_name == "factual_knowledge":
                # Count factual indicators
                factual_words = ['is', 'are', 'was', 'were', 'fact', 'true', 'false']
                score = sum(1 for word in factual_words if word in text) / 10.0
                
            elif dim_name == "mathematical_reasoning":
                # Count mathematical terms
                math_words = ['equation', 'calculate', 'formula', 'number', 'solve', '+', '-', '*', '/']
                score = sum(1 for word in math_words if word in text) / 15.0
                
            elif dim_name == "logical_inference":
                # Count logical connectors
                logic_words = ['because', 'therefore', 'thus', 'since', 'if', 'then', 'implies']
                score = sum(1 for word in logic_words if word in text) / 10.0
                
            elif dim_name == "complexity_handling":
                # Based on sentence length and vocabulary diversity
                words = text.split()
                unique_words = len(set(words))
                score = min(1.0, (len(words) / 100.0) * (unique_words / len(words) if words else 0))
                
            elif dim_name == "domain_expertise":
                # Domain-specific vocabulary scoring
                score = self._calculate_domain_expertise_score(text, domain)
                
            elif dim_name == "quantum_resonance":
                # Special quantum dimension based on overall coherence patterns
                score = self._calculate_quantum_resonance(query, response, domain)
                
            else:
                # Generic scoring based on text patterns
                score = self._calculate_generic_dimension_score(text, dim_name)
            
            # Apply golden ratio normalization
            phi = (1 + math.sqrt(5)) / 2
            normalized_score = min(1.0, score * phi / 2.0)
            embedding.append(normalized_score)
        
        return embedding
    
    def _generate_query_embedding(self, query: str, domain: MMLUDomain) -> List[float]:
        """Generate embedding for a query only"""
        return self._generate_quantum_embedding(query, "", domain)
    
    def _calculate_quantum_similarity(self, embedding1: List[float], 
                                    embedding2: List[float]) -> float:
        """Calculate quantum-enhanced similarity between embeddings"""
        
        if len(embedding1) != len(embedding2):
            return 0.0
        
        # Cosine similarity with quantum weighting
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        magnitude1 = math.sqrt(sum(a * a for a in embedding1))
        magnitude2 = math.sqrt(sum(b * b for b in embedding2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        cosine_sim = dot_product / (magnitude1 * magnitude2)
        
        # Quantum enhancement using sacred geometry
        phi = (1 + math.sqrt(5)) / 2
        quantum_boost = 1.0 + (cosine_sim / phi) * 0.2
        
        return min(1.0, cosine_sim * quantum_boost)
    
    def _search_domain(self, query: str, query_embedding: List[float], 
                      domain: MMLUDomain) -> List[SimilarityMatch]:
        """Search for similar examples within a specific domain"""
        
        matches = []
        domain_exemplars = self.exemplars.get(domain, [])
        
        for exemplar in domain_exemplars:
            similarity = self._calculate_quantum_similarity(query_embedding, 
                                                          exemplar.quantum_embedding)
            
            # Pattern-based matching
            pattern_matches = self._find_pattern_matches(query, exemplar.query)
            
            # Calculate dimension-specific scores
            dimension_scores = {}
            for i, (emb1, emb2) in enumerate(zip(query_embedding, exemplar.quantum_embedding)):
                dimension_scores[i+1] = abs(emb1 - emb2)  # Lower difference = higher similarity
            
            if similarity > 0.3:  # Minimum similarity threshold
                match = SimilarityMatch(
                    exemplar=exemplar,
                    similarity_score=similarity,
                    dimension_scores=dimension_scores,
                    pattern_matches=pattern_matches
                )
                matches.append(match)
        
        return matches
    
    def _cross_domain_search(self, query: str, query_embedding: List[float], 
                           primary_domain: MMLUDomain) -> List[SimilarityMatch]:
        """Search across other domains for transferable knowledge"""
        
        cross_matches = []
        
        # Define domain transfer weights
        transfer_weights = {
            MMLUDomain.MATHEMATICS: {MMLUDomain.PHYSICS: 0.8, MMLUDomain.COMPUTER_SCIENCE: 0.7},
            MMLUDomain.PHYSICS: {MMLUDomain.MATHEMATICS: 0.8, MMLUDomain.CHEMISTRY: 0.6},
            MMLUDomain.BIOLOGY: {MMLUDomain.CHEMISTRY: 0.7, MMLUDomain.MEDICINE: 0.8},
            MMLUDomain.HISTORY: {MMLUDomain.POLITICAL_SCIENCE: 0.6, MMLUDomain.SOCIOLOGY: 0.5},
            # Add more transfer relationships as needed
        }
        
        related_domains = transfer_weights.get(primary_domain, {})
        
        for domain, weight in related_domains.items():
            domain_matches = self._search_domain(query, query_embedding, domain)
            
            # Apply cross-domain weight penalty
            for match in domain_matches[:2]:  # Limit cross-domain matches
                match.similarity_score *= weight
                cross_matches.append(match)
                self.cross_domain_transfers[f"{primary_domain.value}->{domain.value}"] += 1
        
        return cross_matches
    
    def _store_exemplar(self, exemplar: QuantumExemplar):
        """Store exemplar with capacity management"""
        
        domain_exemplars = self.exemplars[exemplar.domain]
        domain_exemplars.append(exemplar)
        
        # Maintain capacity limit
        if len(domain_exemplars) > self.max_exemplars_per_domain:
            # Remove least effective exemplars
            domain_exemplars.sort(key=lambda x: x.effectiveness_score, reverse=True)
            self.exemplars[exemplar.domain] = domain_exemplars[:self.max_exemplars_per_domain]
    
    def _calculate_quantum_coherence(self, query: str, response: str, 
                                   embedding: List[float]) -> float:
        """Calculate quantum coherence for query-response pair"""
        
        # Base coherence from embedding variance
        variance = sum((x - 0.5) ** 2 for x in embedding) / len(embedding)
        base_coherence = 1.0 - min(1.0, variance * 4.0)  # Lower variance = higher coherence
        
        # Length and complexity bonuses
        response_quality = min(1.0, len(response) / 200.0)  # Reward substantial responses
        query_clarity = min(1.0, len(query.split()) / 20.0)  # Reward clear questions
        
        # Sacred geometry enhancement
        phi = (1 + math.sqrt(5)) / 2
        coherence = (base_coherence * 0.6 + response_quality * 0.2 + query_clarity * 0.2) * phi / 2.0
        
        return min(1.0, coherence)
    
    def _extract_question_type(self, text: str) -> List[str]:
        """Extract question type patterns"""
        patterns = []
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['what', 'which', 'who']):
            patterns.append('factual')
        if any(word in text_lower for word in ['how', 'why']):
            patterns.append('explanatory')
        if any(word in text_lower for word in ['compare', 'contrast', 'difference']):
            patterns.append('comparative')
        if any(word in text_lower for word in ['analyze', 'evaluate', 'assess']):
            patterns.append('analytical')
        
        return patterns
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key conceptual terms"""
        # Simplified concept extraction
        words = re.findall(r'\b[A-Z][a-z]+\b', text)  # Capitalized words
        concepts = [word.lower() for word in words if len(word) > 3]
        return list(set(concepts))[:10]  # Top 10 unique concepts
    
    def _extract_complexity_level(self, text: str) -> str:
        """Determine complexity level of text"""
        word_count = len(text.split())
        unique_words = len(set(text.lower().split()))
        avg_word_length = sum(len(word) for word in text.split()) / word_count if word_count else 0
        
        complexity_score = (word_count / 50.0) + (unique_words / word_count if word_count else 0) + (avg_word_length / 10.0)
        
        if complexity_score > 2.0:
            return "hard"
        elif complexity_score > 1.0:
            return "medium"
        else:
            return "easy"
    
    def _extract_reasoning_pattern(self, text: str) -> List[str]:
        """Extract reasoning patterns from text"""
        patterns = []
        text_lower = text.lower()
        
        reasoning_indicators = {
            'deductive': ['therefore', 'thus', 'hence', 'consequently'],
            'inductive': ['example', 'instance', 'pattern', 'trend'],
            'causal': ['because', 'since', 'due to', 'causes', 'leads to'],
            'comparative': ['similar', 'different', 'unlike', 'whereas', 'however']
        }
        
        for pattern_type, indicators in reasoning_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                patterns.append(pattern_type)
        
        return patterns
    
    def _extract_domain_vocabulary(self, text: str) -> List[str]:
        """Extract domain-specific vocabulary"""
        # Domain vocabulary dictionaries (simplified)
        domain_terms = {
            'mathematics': ['equation', 'formula', 'theorem', 'proof', 'derivative'],
            'physics': ['energy', 'force', 'momentum', 'quantum', 'wave'],
            'biology': ['cell', 'organism', 'evolution', 'genetics', 'protein'],
            'chemistry': ['molecule', 'reaction', 'compound', 'element', 'bond']
        }
        
        found_terms = []
        text_lower = text.lower()
        
        for domain, terms in domain_terms.items():
            for term in terms:
                if term in text_lower:
                    found_terms.append(f"{domain}:{term}")
        
        return found_terms
    
    def _extract_structure_pattern(self, text: str) -> List[str]:
        """Extract structural patterns from text"""
        patterns = []
        
        # Question patterns
        if text.strip().endswith('?'):
            patterns.append('interrogative')
        
        # List patterns
        if any(marker in text for marker in ['1.', '2.', 'a)', 'b)', '•', '-']):
            patterns.append('enumerated')
        
        # Definition patterns
        if any(phrase in text.lower() for phrase in ['is defined as', 'refers to', 'means that']):
            patterns.append('definitional')
        
        return patterns
    
    def _calculate_domain_expertise_score(self, text: str, domain: MMLUDomain) -> float:
        """Calculate domain expertise score"""
        domain_keywords = {
            MMLUDomain.MATHEMATICS: ['equation', 'theorem', 'proof', 'derivative', 'integral', 'matrix'],
            MMLUDomain.PHYSICS: ['energy', 'force', 'quantum', 'relativity', 'electromagnetic'],
            MMLUDomain.BIOLOGY: ['cell', 'DNA', 'evolution', 'organism', 'protein', 'genetics'],
            MMLUDomain.CHEMISTRY: ['molecule', 'reaction', 'compound', 'bond', 'catalyst'],
            MMLUDomain.COMPUTER_SCIENCE: ['algorithm', 'data structure', 'programming', 'software'],
            MMLUDomain.HISTORY: ['century', 'war', 'civilization', 'empire', 'revolution'],
            MMLUDomain.PHILOSOPHY: ['ethics', 'metaphysics', 'logic', 'consciousness', 'morality']
        }
        
        keywords = domain_keywords.get(domain, [])
        if not keywords:
            return 0.5  # Default for unknown domains
        
        matches = sum(1 for keyword in keywords if keyword in text.lower())
        return min(1.0, matches / len(keywords))
    
    def _calculate_quantum_resonance(self, query: str, response: str, 
                                   domain: MMLUDomain) -> float:
        """Calculate special quantum resonance score"""
        # Fibonacci-based scoring
        fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21]
        
        query_words = len(query.split())
        response_words = len(response.split())
        
        # Find closest Fibonacci numbers
        query_fib_distance = min(abs(query_words - fib) for fib in fib_sequence)
        response_fib_distance = min(abs(response_words - fib) for fib in fib_sequence)
        
        # Calculate resonance based on Fibonacci alignment
        total_distance = query_fib_distance + response_fib_distance
        max_distance = max(fib_sequence)
        
        resonance = 1.0 - (total_distance / max_distance)
        return max(0.0, min(1.0, resonance))
    
    def _calculate_generic_dimension_score(self, text: str, dimension_name: str) -> float:
        """Calculate score for generic dimensions"""
        # Simplified scoring based on text characteristics
        words = text.split()
        word_count = len(words)
        unique_words = len(set(words))
        
        # Different scoring strategies for different dimensions
        if 'reasoning' in dimension_name:
            return min(1.0, (unique_words / word_count) if word_count else 0)
        elif 'knowledge' in dimension_name:
            return min(1.0, word_count / 100.0)
        elif 'understanding' in dimension_name:
            return min(1.0, (word_count * unique_words) / 1000.0)
        else:
            return 0.5  # Default score
    
    def _find_pattern_matches(self, query1: str, query2: str) -> List[str]:
        """Find matching patterns between two queries"""
        matches = []
        
        # Simple word overlap
        words1 = set(query1.lower().split())
        words2 = set(query2.lower().split())
        overlap = words1.intersection(words2)
        
        if len(overlap) > 2:
            matches.append(f"word_overlap:{len(overlap)}")
        
        # Length similarity
        len_diff = abs(len(query1) - len(query2))
        if len_diff < 20:
            matches.append("similar_length")
        
        # Question type similarity
        if query1.strip().endswith('?') and query2.strip().endswith('?'):
            matches.append("both_questions")
        
        return matches
    
    def _update_domain_performance(self, domain: MMLUDomain, difficulty: str, 
                                 success_rate: float):
        """Update performance tracking for domain"""
        key = f"{difficulty}_success_rate"
        current = self.domain_performance[domain].get(key, 0.5)
        # Exponential moving average
        self.domain_performance[domain][key] = current * 0.9 + success_rate * 0.1
    
    def get_domain_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the few-shot learning system"""
        stats = {
            'total_exemplars': sum(len(exemplars) for exemplars in self.exemplars.values()),
            'domain_counts': {domain.value: len(exemplars) 
                            for domain, exemplars in self.exemplars.items()},
            'domain_performance': {domain.value: perf 
                                 for domain, perf in self.domain_performance.items()},
            'cross_domain_transfers': dict(self.cross_domain_transfers),
            'avg_coherence_by_domain': {}
        }
        
        # Calculate average coherence by domain
        for domain, exemplars in self.exemplars.items():
            if exemplars:
                avg_coherence = sum(ex.coherence_score for ex in exemplars) / len(exemplars)
                stats['avg_coherence_by_domain'][domain.value] = round(avg_coherence, 3)
        
        return stats
    
    def preload_common_examples(self):
        """Preload common MMLU-style examples for bootstrapping"""
        common_examples = [
            # Mathematics
            {
                'query': 'What is the derivative of x^2?',
                'response': 'The derivative of x^2 is 2x, using the power rule where d/dx[x^n] = nx^(n-1).',
                'domain': MMLUDomain.MATHEMATICS,
                'difficulty': 'easy'
            },
            {
                'query': 'Solve the quadratic equation x^2 - 5x + 6 = 0',
                'response': 'Using factoring: (x-2)(x-3) = 0, so x = 2 or x = 3. We can verify: 2^2 - 5(2) + 6 = 0 ✓',
                'domain': MMLUDomain.MATHEMATICS,
                'difficulty': 'medium'
            },
            
            # Physics
            {
                'query': 'What is Newton\'s second law of motion?',
                'response': 'Newton\'s second law states that F = ma, where force equals mass times acceleration. This means the acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.',
                'domain': MMLUDomain.PHYSICS,
                'difficulty': 'easy'
            },
            
            # Biology
            {
                'query': 'What is the function of mitochondria?',
                'response': 'Mitochondria are the powerhouses of the cell. They generate ATP through cellular respiration, converting glucose and oxygen into energy that cells can use for their metabolic processes.',
                'domain': MMLUDomain.BIOLOGY,
                'difficulty': 'medium'
            },
            
            # Computer Science
            {
                'query': 'What is the time complexity of binary search?',
                'response': 'Binary search has O(log n) time complexity because it eliminates half of the remaining elements in each step, leading to a logarithmic number of operations relative to the input size.',
                'domain': MMLUDomain.COMPUTER_SCIENCE,
                'difficulty': 'medium'
            },
            
            # History
            {
                'query': 'When did World War II end?',
                'response': 'World War II ended on September 2, 1945, with Japan\'s formal surrender aboard the USS Missouri in Tokyo Bay, following the atomic bombings of Hiroshima and Nagasaki.',
                'domain': MMLUDomain.HISTORY,
                'difficulty': 'easy'
            }
        ]
        
        for example in common_examples:
            self.learn_from_example(
                example['query'],
                example['response'],
                example['domain'],
                example['difficulty'],
                success_rate=0.95  # High confidence for curated examples
            )
        
        print(f"✅ Preloaded {len(common_examples)} common examples across domains")
    
    def get_loaded_examples_count(self) -> int:
        """Retorna el número total de ejemplos cargados en el sistema"""
        return sum(len(exemplars) for exemplars in self.exemplars.values())
    
    def enhance_query_with_examples(self, query: str, domain: str = "general", 
                                  num_examples: int = 3) -> Dict[str, Any]:
        """Enhance a query with few-shot examples"""
        start_time = time.time()
        
        # Convert domain string to MMLUDomain
        try:
            if domain == "general":
                mmlu_domain = MMLUDomain.COMPUTER_SCIENCE  # Default fallback
            else:
                mmlu_domain = MMLUDomain(domain)
        except ValueError:
            mmlu_domain = MMLUDomain.COMPUTER_SCIENCE  # Fallback
        
        # Find similar examples
        similar_matches = self.find_similar_examples(query, mmlu_domain, num_examples)
        
        # Generate enhanced query with examples
        if similar_matches:
            enhanced_query = self.generate_few_shot_prompt(query, mmlu_domain, num_examples)
            
            # Calculate metrics
            avg_similarity = sum(match.similarity_score for match in similar_matches) / len(similar_matches)
            avg_coherence = sum(match.exemplar.coherence_score for match in similar_matches) / len(similar_matches)
            
            # Extract pattern information
            all_patterns = []
            for match in similar_matches:
                all_patterns.extend(match.pattern_matches)
            
            similar_patterns = list(set(all_patterns))
            
        else:
            enhanced_query = query
            avg_similarity = 0.0
            avg_coherence = 0.0
            similar_patterns = []
        
        computation_time = time.time() - start_time
        
        return {
            'enhanced_query': enhanced_query,
            'examples_count': len(similar_matches),
            'quantum_coherence': avg_coherence,
            'pattern_match_score': avg_similarity,
            'domain_confidence': self.domain_performance.get(mmlu_domain, {}).get('medium_success_rate', 0.5),
            'similar_patterns': similar_patterns,
            'cross_domain_insights': [],  # Placeholder for cross-domain insights
            'computation_time': computation_time
        }

# Example usage and testing
if __name__ == "__main__":
    engine = QuantumFewShotLearningEngine()
    
    print("🎯⚛️ QUANTUM FEW-SHOT LEARNING ENGINE TEST ⚛️🎯")
    print("=" * 60)
    
    # Preload common examples
    engine.preload_common_examples()
    
    # Test learning from new examples
    print("\n📚 Testing learning from examples...")
    new_examples = [
        {
            'query': 'What is the integral of sin(x)?',
            'response': 'The integral of sin(x) is -cos(x) + C, where C is the constant of integration.',
            'domain': MMLUDomain.MATHEMATICS
        },
        {
            'query': 'Explain photosynthesis',
            'response': 'Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen, using chlorophyll as a catalyst.',
            'domain': MMLUDomain.BIOLOGY
        }
    ]
    
    for example in new_examples:
        result = engine.learn_from_example(
            example['query'],
            example['response'], 
            example['domain']
        )
        print(f"  {result}")
    
    # Test finding similar examples
    print("\n🔍 Testing similarity search...")
    test_query = "How do you differentiate x^3?"
    matches = engine.find_similar_examples(test_query, MMLUDomain.MATHEMATICS, top_k=3)
    
    for i, match in enumerate(matches, 1):
        print(f"  Match {i}: Similarity {match.similarity_score:.3f}")
        print(f"    Query: {match.exemplar.query[:50]}...")
        print(f"    Patterns: {match.pattern_matches}")
    
    # Test few-shot prompt generation
    print("\n📝 Testing few-shot prompt generation...")
    prompt = engine.generate_few_shot_prompt(test_query, MMLUDomain.MATHEMATICS, 2)
    print("Generated prompt (first 300 chars):")
    print(prompt[:300] + "..." if len(prompt) > 300 else prompt)
    
    # Test adaptive learning
    print("\n🔄 Testing adaptive learning...")
    engine.adaptive_learning_update(test_query, MMLUDomain.MATHEMATICS, 
                                   "The derivative of x^3 is 3x^2", success=True)
    print("  Updated exemplar success rates based on feedback")
    
    # Display statistics
    print("\n📊 System Statistics:")
    stats = engine.get_domain_stats()
    print(f"  Total exemplars: {stats['total_exemplars']}")
    print(f"  Domain distribution: {stats['domain_counts']}")
    print(f"  Average coherence by domain: {stats['avg_coherence_by_domain']}")
    
    print("\n🎯✨ Few-Shot Learning Engine test completed successfully!")
