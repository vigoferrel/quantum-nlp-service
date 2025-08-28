#!/usr/bin/env python3
"""
🧠 ADVANCED NLP ENGINE
Motor de procesamiento de lenguaje natural avanzado para Vigoleonrocks
Capacidades: Análisis de sentimientos, extracción de entidades, clasificación de intenciones
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple, Union
from enum import Enum
from dataclasses import dataclass

import spacy
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Descargar recursos NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class IntentType(str, Enum):
    """Tipos de intenciones detectadas"""
    GREETING = "greeting"
    QUESTION = "question"
    STATEMENT = "statement"
    COMMAND = "command"
    COMPLAINT = "complaint"
    COMPLIMENT = "compliment"
    REQUEST = "request"
    CLARIFICATION = "clarification"
    FAREWELL = "farewell"
    PROGRAMMING = "programming"
    CREATIVE = "creative"
    ANALYSIS = "analysis"

class EntityType(str, Enum):
    """Tipos de entidades"""
    PERSON = "PERSON"
    ORGANIZATION = "ORG"
    LOCATION = "LOC"
    DATE = "DATE"
    TIME = "TIME"
    MONEY = "MONEY"
    PERCENT = "PERCENT"
    QUANTITY = "QUANTITY"
    PROGRAMMING_LANGUAGE = "PROG_LANG"
    TECHNOLOGY = "TECH"
    FRAMEWORK = "FRAMEWORK"
    DATABASE = "DATABASE"

class SentimentLevel(str, Enum):
    """Niveles de sentimiento"""
    VERY_NEGATIVE = "very_negative"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    VERY_POSITIVE = "very_positive"

@dataclass
class Entity:
    """Entidad extraída del texto"""
    text: str
    type: EntityType
    start: int
    end: int
    confidence: float
    description: Optional[str] = None

@dataclass
class SentimentAnalysis:
    """Análisis de sentimientos"""
    compound: float
    positive: float
    negative: float
    neutral: float
    level: SentimentLevel
    confidence: float
    subjectivity: float

@dataclass
class IntentAnalysis:
    """Análisis de intención"""
    intent: IntentType
    confidence: float
    entities: List[Entity]
    keywords: List[str]
    context: Dict[str, Any]

@dataclass
class TextFeatures:
    """Características del texto"""
    tokens: List[str]
    lemmas: List[str]
    pos_tags: List[Tuple[str, str]]
    named_entities: List[Entity]
    sentiment: SentimentAnalysis
    intent: IntentAnalysis
    readability_score: float
    complexity_score: float
    topic_keywords: List[str]

class AdvancedNLPEngine:
    """Motor NLP avanzado con múltiples capacidades"""
    
    def __init__(self):
        # Cargar modelos
        self.nlp_en = spacy.load("en_core_web_sm")
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        
        # Patrones de intención
        self.intent_patterns = {
            IntentType.GREETING: [
                "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
                "hola", "buenos días", "buenas tardes", "buenas noches"
            ],
            IntentType.QUESTION: [
                "what", "how", "why", "when", "where", "who", "which", "can you",
                "qué", "cómo", "por qué", "cuándo", "dónde", "quién", "cuál", "puedes"
            ],
            IntentType.COMMAND: [
                "create", "build", "make", "generate", "write", "code", "program",
                "crear", "construir", "hacer", "generar", "escribir", "programar"
            ],
            IntentType.PROGRAMMING: [
                "function", "class", "method", "algorithm", "data structure", "api",
                "función", "clase", "método", "algoritmo", "estructura de datos"
            ],
            IntentType.CREATIVE: [
                "story", "poem", "creative", "imagine", "describe", "narrative",
                "historia", "poema", "creativo", "imagina", "describe", "narrativa"
            ],
            IntentType.ANALYSIS: [
                "analyze", "explain", "understand", "break down", "examine",
                "analizar", "explicar", "entender", "descomponer", "examinar"
            ]
        }
        
        # Entidades de programación
        self.programming_entities = {
            "languages": ["python", "javascript", "java", "c++", "c#", "go", "rust", "swift", "kotlin"],
            "frameworks": ["react", "angular", "vue", "django", "flask", "spring", "express", "fastapi"],
            "databases": ["mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle", "sql server"],
            "tools": ["git", "docker", "kubernetes", "jenkins", "jira", "vscode", "intellij"]
        }
        
        logger.info("🧠 Motor NLP avanzado inicializado correctamente")
    
    async def analyze_text(self, text: str, language: str = "en") -> TextFeatures:
        """Análisis completo del texto"""
        start_time = time.time()
        
        try:
            # Tokenización
            tokens = word_tokenize(text.lower())
            
            # Lematización
            lemmas = [self.lemmatizer.lemmatize(token) for token in tokens]
            
            # Análisis con SpaCy
            doc = self.nlp_en(text)
            
            # POS tagging
            pos_tags = [(token.text, token.pos_) for token in doc]
            
            # Entidades nombradas
            named_entities = []
            for ent in doc.ents:
                entity = Entity(
                    text=ent.text,
                    type=EntityType(ent.label_),
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=0.8
                )
                named_entities.append(entity)
            
            # Análisis de sentimientos
            sentiment = await self._analyze_sentiment(text)
            
            # Análisis de intención
            intent = await self._analyze_intent(text, tokens, named_entities)
            
            # Características de legibilidad
            readability_score = self._calculate_readability(text)
            complexity_score = self._calculate_complexity(tokens, pos_tags)
            
            # Palabras clave del tema
            topic_keywords = self._extract_topic_keywords(text, tokens)
            
            processing_time = time.time() - start_time
            logger.info(f"✅ Análisis NLP completado en {processing_time:.3f}s")
            
            return TextFeatures(
                tokens=tokens,
                lemmas=lemmas,
                pos_tags=pos_tags,
                named_entities=named_entities,
                sentiment=sentiment,
                intent=intent,
                readability_score=readability_score,
                complexity_score=complexity_score,
                topic_keywords=topic_keywords
            )
            
        except Exception as e:
            logger.error(f"Error en análisis NLP: {e}")
            raise
    
    async def _analyze_sentiment(self, text: str) -> SentimentAnalysis:
        """Análisis de sentimientos avanzado"""
        # VADER Sentiment
        vader_scores = self.sentiment_analyzer.polarity_scores(text)
        
        # TextBlob para subjetividad
        blob = TextBlob(text)
        subjectivity = blob.sentiment.subjectivity
        
        # Determinar nivel de sentimiento
        compound = vader_scores['compound']
        if compound >= 0.5:
            level = SentimentLevel.VERY_POSITIVE
        elif compound >= 0.1:
            level = SentimentLevel.POSITIVE
        elif compound <= -0.5:
            level = SentimentLevel.VERY_NEGATIVE
        elif compound <= -0.1:
            level = SentimentLevel.NEGATIVE
        else:
            level = SentimentLevel.NEUTRAL
        
        confidence = abs(compound) + (1 - subjectivity) / 2
        
        return SentimentAnalysis(
            compound=compound,
            positive=vader_scores['pos'],
            negative=vader_scores['neg'],
            neutral=vader_scores['neu'],
            level=level,
            confidence=confidence,
            subjectivity=subjectivity
        )
    
    async def _analyze_intent(self, text: str, tokens: List[str], entities: List[Entity]) -> IntentAnalysis:
        """Análisis de intención"""
        text_lower = text.lower()
        
        # Detectar intención basada en patrones
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in text_lower:
                    score += 1
            if score > 0:
                intent_scores[intent] = score
        
        # Detectar entidades de programación
        programming_entities = []
        for category, items in self.programming_entities.items():
            for item in items:
                if item in text_lower:
                    entity = Entity(
                        text=item,
                        type=EntityType.PROGRAMMING_LANGUAGE if category == "languages" else EntityType.TECHNOLOGY,
                        start=text_lower.find(item),
                        end=text_lower.find(item) + len(item),
                        confidence=0.9,
                        description=f"{category}: {item}"
                    )
                    programming_entities.append(entity)
        
        # Determinar intención principal
        if intent_scores:
            primary_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(1.0, intent_scores[primary_intent] / 3.0)
        else:
            # Análisis basado en estructura de la oración
            if any(word in text_lower for word in ["?", "what", "how", "why"]):
                primary_intent = IntentType.QUESTION
                confidence = 0.7
            elif any(word in text_lower for word in ["create", "build", "make"]):
                primary_intent = IntentType.COMMAND
                confidence = 0.8
            else:
                primary_intent = IntentType.STATEMENT
                confidence = 0.6
        
        # Extraer palabras clave
        keywords = self._extract_keywords(tokens)
        
        # Contexto
        context = {
            "has_programming_entities": len(programming_entities) > 0,
            "programming_domain": len(programming_entities) > 0,
            "question_mark": "?" in text,
            "exclamation_mark": "!" in text,
            "text_length": len(text)
        }
        
        return IntentAnalysis(
            intent=primary_intent,
            confidence=confidence,
            entities=entities + programming_entities,
            keywords=keywords,
            context=context
        )
    
    def _extract_keywords(self, tokens: List[str]) -> List[str]:
        """Extraer palabras clave"""
        # Filtrar stopwords
        stop_words = set(stopwords.words('english') + stopwords.words('spanish'))
        keywords = [token for token in tokens if token.lower() not in stop_words and len(token) > 2]
        
        # Lematizar keywords
        keywords = [self.lemmatizer.lemmatize(keyword) for keyword in keywords]
        
        return keywords[:10]  # Top 10 keywords
    
    def _calculate_readability(self, text: str) -> float:
        """Calcular puntuación de legibilidad (Flesch Reading Ease)"""
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        syllables = self._count_syllables(text)
        
        if len(sentences) == 0 or len(words) == 0:
            return 0.0
        
        # Flesch Reading Ease
        flesch_score = 206.835 - (1.015 * len(words) / len(sentences)) - (84.6 * syllables / len(words))
        return max(0.0, min(100.0, flesch_score)) / 100.0
    
    def _count_syllables(self, text: str) -> int:
        """Contar sílabas (aproximación)"""
        text = text.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in text:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        return max(1, count)
    
    def _calculate_complexity(self, tokens: List[str], pos_tags: List[Tuple[str, str]]) -> float:
        """Calcular complejidad del texto"""
        if not tokens:
            return 0.0
        
        # Factores de complejidad
        avg_word_length = sum(len(token) for token in tokens) / len(tokens)
        unique_words_ratio = len(set(tokens)) / len(tokens)
        
        # Proporción de palabras complejas (más de 6 caracteres)
        complex_words = sum(1 for token in tokens if len(token) > 6)
        complex_ratio = complex_words / len(tokens)
        
        # Proporción de verbos
        verbs = sum(1 for _, pos in pos_tags if pos.startswith('VB'))
        verb_ratio = verbs / len(pos_tags) if pos_tags else 0
        
        # Puntuación de complejidad (0-1, donde 1 es más complejo)
        complexity = (avg_word_length / 10.0 + unique_words_ratio + complex_ratio + verb_ratio) / 4.0
        return min(1.0, complexity)
    
    def _extract_topic_keywords(self, text: str, tokens: List[str]) -> List[str]:
        """Extraer palabras clave del tema usando TF-IDF"""
        try:
            # Crear vectorizador TF-IDF
            vectorizer = TfidfVectorizer(
                max_features=10,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Vectorizar el texto
            tfidf_matrix = vectorizer.fit_transform([text])
            
            # Obtener características
            feature_names = vectorizer.get_feature_names_out()
            
            # Obtener scores TF-IDF
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Crear pares (palabra, score) y ordenar
            word_scores = list(zip(feature_names, tfidf_scores))
            word_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Retornar top 5 palabras clave
            return [word for word, score in word_scores[:5] if score > 0]
            
        except Exception as e:
            logger.warning(f"Error en extracción de topic keywords: {e}")
            return self._extract_keywords(tokens)[:5]
    
    async def get_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calcular similitud semántica entre dos textos"""
        try:
            # Codificar textos
            embeddings1 = self.sentence_transformer.encode([text1])
            embeddings2 = self.sentence_transformer.encode([text2])
            
            # Calcular similitud coseno
            similarity = cosine_similarity(embeddings1, embeddings2)[0][0]
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculando similitud semántica: {e}")
            return 0.0
    
    async def extract_summary(self, text: str, max_sentences: int = 3) -> str:
        """Extraer resumen del texto"""
        try:
            sentences = sent_tokenize(text)
            
            if len(sentences) <= max_sentences:
                return text
            
            # Codificar oraciones
            embeddings = self.sentence_transformer.encode(sentences)
            
            # Calcular similitud entre oraciones
            similarity_matrix = cosine_similarity(embeddings)
            
            # Calcular puntuación de cada oración
            sentence_scores = []
            for i in range(len(sentences)):
                score = sum(similarity_matrix[i])
                sentence_scores.append((i, score))
            
            # Ordenar por puntuación
            sentence_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Seleccionar top oraciones
            selected_indices = sorted([idx for idx, _ in sentence_scores[:max_sentences]])
            summary = " ".join([sentences[i] for i in selected_indices])
            
            return summary
            
        except Exception as e:
            logger.error(f"Error extrayendo resumen: {e}")
            return text[:200] + "..." if len(text) > 200 else text
    
    async def detect_language(self, text: str) -> str:
        """Detectar idioma del texto"""
        try:
            # Análisis simple basado en palabras comunes
            spanish_words = {"el", "la", "de", "que", "y", "en", "un", "es", "se", "no", "te", "lo", "le", "da", "su", "por", "son", "con", "para", "al", "del", "los", "las", "una", "como", "pero", "sus", "me", "hasta", "hay", "donde", "han", "quien", "están", "estado", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos", "qué", "unos", "yo", "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros"}
            english_words = {"the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"}
            
            text_lower = text.lower()
            words = set(word_tokenize(text_lower))
            
            spanish_count = len(words.intersection(spanish_words))
            english_count = len(words.intersection(english_words))
            
            if spanish_count > english_count:
                return "es"
            elif english_count > spanish_count:
                return "en"
            else:
                return "unknown"
                
        except Exception as e:
            logger.error(f"Error detectando idioma: {e}")
            return "unknown"

# Instancia global del motor NLP
nlp_engine = AdvancedNLPEngine()
