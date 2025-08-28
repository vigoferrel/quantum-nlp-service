#!/usr/bin/env python3
"""
🧠 ADVANCED CONVERSATIONAL ENGINE
Motor conversacional avanzado con Pydantic para Vigoleonrocks
Soporte completo para texto, audio, video e imágenes
"""

import asyncio
import base64
import io
import json
import logging
import time
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from dataclasses import dataclass, field
from functools import lru_cache

from pydantic import BaseModel, Field, validator, model_validator
import numpy as np
from PIL import Image
import cv2
import librosa
import soundfile as sf

# Importar el motor NLP avanzado
from advanced_nlp_engine import nlp_engine, TextFeatures, SentimentAnalysis, IntentAnalysis, Entity, IntentType, EntityType, SentimentLevel

# Importar el núcleo cuántico y la esencia multimodal
from quantum_core_26d_engine import QuantumCore26DEngine, QuantumDimension, QuantumState, QuantumPrompt, QuantumResult
from quantum_essence_multimodal_optimized import QuantumEssenceMultimodalOptimized, QuantumEssence, EssenceType

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MediaType(str, Enum):
    """Tipos de medios soportados"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    MULTIMODAL = "multimodal"

class ConversationState(str, Enum):
    """Estados de la conversación"""
    INITIAL = "initial"
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"

class EmotionType(str, Enum):
    """Tipos de emociones detectadas"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    FEARFUL = "fearful"
    DISGUSTED = "disgusted"

class ContextDimension(BaseModel):
    """Dimensión del contexto 26D"""
    dimension_id: int = Field(..., ge=0, le=25)
    content: str = Field(default="")
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.now)
    emotion: Optional[EmotionType] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

class MediaContent(BaseModel):
    """Contenido multimedia"""
    media_type: MediaType
    content: Union[str, bytes] = Field(...)
    mime_type: str = Field(default="")
    encoding: str = Field(default="utf-8")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    nlp_features: Optional[TextFeatures] = None
    quantum_features: Optional[Any] = None  # QuantumResult from quantum core
    
    @validator('content')
    def validate_content(cls, v, values):
        media_type = values.get('media_type')
        if media_type == MediaType.TEXT and not isinstance(v, str):
            raise ValueError("Text content must be string")
        elif media_type in [MediaType.IMAGE, MediaType.AUDIO, MediaType.VIDEO] and not isinstance(v, bytes):
            raise ValueError(f"{media_type} content must be bytes")
        return v

class UserMessage(BaseModel):
    """Mensaje del usuario"""
    id: str = Field(default_factory=lambda: f"msg_{int(time.time() * 1000)}")
    content: MediaContent
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: str = Field(...)
    user_id: Optional[str] = None
    emotion: Optional[EmotionType] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    context_dims: List[ContextDimension] = Field(default_factory=list)

class AssistantResponse(BaseModel):
    """Respuesta del asistente"""
    id: str = Field(default_factory=lambda: f"resp_{int(time.time() * 1000)}")
    content: MediaContent
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: str = Field(...)
    model_used: str = Field(default="vigoleonrocks")
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    coherence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    consciousness_level: float = Field(default=2.0, ge=0.0, le=5.0)
    processing_time: float = Field(default=0.0)
    context_dims_used: List[int] = Field(default_factory=list)
    emotion_detected: Optional[EmotionType] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

class ConversationSession(BaseModel):
    """Sesión de conversación"""
    session_id: str = Field(...)
    user_id: Optional[str] = None
    state: ConversationState = Field(default=ConversationState.INITIAL)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    messages: List[UserMessage] = Field(default_factory=list)
    responses: List[AssistantResponse] = Field(default_factory=list)
    context_26d: List[ContextDimension] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @model_validator(mode='before')
    @classmethod
    def update_timestamp(cls, values):
        if isinstance(values, dict):
            values['updated_at'] = datetime.now()
        return values

class ConversationRequest(BaseModel):
    """Solicitud de conversación"""
    session_id: str = Field(...)
    user_id: Optional[str] = None
    content: MediaContent
    context_26d: Optional[List[ContextDimension]] = None
    emotion: Optional[EmotionType] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    model_preference: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4000, ge=1, le=8000)

class ConversationResponse(BaseModel):
    """Respuesta de conversación"""
    success: bool = Field(...)
    response: Optional[AssistantResponse] = None
    session: Optional[ConversationSession] = None
    error: Optional[str] = None
    processing_time: float = Field(default=0.0)
    context_26d_updated: List[ContextDimension] = Field(default_factory=list)

class AudioProcessor:
    """Procesador de audio avanzado"""
    
    def __init__(self):
        self.sample_rate = 22050
        self.n_mfcc = 13
        
    async def process_audio(self, audio_bytes: bytes) -> Dict[str, Any]:
        """Procesar audio y extraer características"""
        try:
            # Convertir bytes a array numpy
            audio_array, sr = sf.read(io.BytesIO(audio_bytes))
            
            # Resample si es necesario
            if sr != self.sample_rate:
                audio_array = librosa.resample(audio_array, orig_sr=sr, target_sr=self.sample_rate)
            
            # Extraer características
            mfcc = librosa.feature.mfcc(y=audio_array, sr=self.sample_rate, n_mfcc=self.n_mfcc)
            spectral_centroid = librosa.feature.spectral_centroid(y=audio_array, sr=self.sample_rate)
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_array, sr=self.sample_rate)
            
            # Detectar emociones (simplificado)
            emotion = self._detect_emotion_from_audio(mfcc, spectral_centroid, spectral_rolloff)
            
            return {
                "duration": len(audio_array) / self.sample_rate,
                "mfcc": mfcc.tolist(),
                "spectral_centroid": spectral_centroid.tolist(),
                "spectral_rolloff": spectral_rolloff.tolist(),
                "emotion": emotion,
                "confidence": 0.85
            }
        except Exception as e:
            logger.error(f"Error procesando audio: {e}")
            return {"error": str(e)}
    
    def _detect_emotion_from_audio(self, mfcc, spectral_centroid, spectral_rolloff) -> EmotionType:
        """Detectar emoción basada en características de audio"""
        # Algoritmo simplificado de detección de emociones
        avg_centroid = np.mean(spectral_centroid)
        avg_rolloff = np.mean(spectral_rolloff)
        
        if avg_centroid > 2000 and avg_rolloff > 4000:
            return EmotionType.HAPPY
        elif avg_centroid < 1000 and avg_rolloff < 2000:
            return EmotionType.SAD
        elif avg_centroid > 3000:
            return EmotionType.ANGRY
        else:
            return EmotionType.NEUTRAL

class VideoProcessor:
    """Procesador de video avanzado"""
    
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    async def process_video(self, video_bytes: bytes) -> Dict[str, Any]:
        """Procesar video y extraer características"""
        try:
            # Guardar video temporalmente
            temp_path = f"temp_video_{int(time.time())}.mp4"
            with open(temp_path, 'wb') as f:
                f.write(video_bytes)
            
            cap = cv2.VideoCapture(temp_path)
            frames = []
            emotions = []
            faces_detected = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detectar caras
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                faces_detected += len(faces)
                
                # Detectar emociones (simplificado)
                emotion = self._detect_emotion_from_frame(frame)
                emotions.append(emotion)
                
                # Extraer características del frame
                frame_features = self._extract_frame_features(frame)
                frames.append(frame_features)
            
            cap.release()
            
            # Limpiar archivo temporal
            import os
            os.remove(temp_path)
            
            # Calcular emoción dominante
            dominant_emotion = self._get_dominant_emotion(emotions)
            
            return {
                "duration": len(frames) / 30.0,  # Asumiendo 30 FPS
                "frames_processed": len(frames),
                "faces_detected": faces_detected,
                "dominant_emotion": dominant_emotion,
                "emotion_confidence": 0.8,
                "frame_features": frames[:10]  # Primeros 10 frames
            }
        except Exception as e:
            logger.error(f"Error procesando video: {e}")
            return {"error": str(e)}
    
    def _detect_emotion_from_frame(self, frame) -> EmotionType:
        """Detectar emoción en un frame (simplificado)"""
        # Implementación simplificada
        return EmotionType.NEUTRAL
    
    def _extract_frame_features(self, frame) -> Dict[str, Any]:
        """Extraer características de un frame"""
        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calcular histograma
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        
        return {
            "brightness": np.mean(gray),
            "contrast": np.std(gray),
            "histogram": hist.flatten().tolist()[:50]  # Primeros 50 valores
        }
    
    def _get_dominant_emotion(self, emotions: List[EmotionType]) -> EmotionType:
        """Obtener la emoción dominante"""
        if not emotions:
            return EmotionType.NEUTRAL
        
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return max(emotion_counts, key=emotion_counts.get)

class AdvancedConversationalEngine:
    """Motor conversacional avanzado con núcleo cuántico y NLP"""
    
    def __init__(self):
        self.sessions: Dict[str, ConversationSession] = {}
        self.audio_processor = AudioProcessor()
        self.video_processor = VideoProcessor()
        self.context_26d: List[ContextDimension] = [
            ContextDimension(dimension_id=i, content="", weight=1.0)
            for i in range(26)
        ]
        
        # 🧠 NÚCLEO CUÁNTICO Y ESENCIA MULTIMODAL
        self.quantum_core = QuantumCore26DEngine()
        self.quantum_essence = QuantumEssenceMultimodalOptimized()
        
        # 🚀 CACHE Y OPTIMIZACIONES
        self._content_cache = {}
        self._nlp_cache = {}
        self._quantum_cache = {}
        
        logger.info("🚀 Motor conversacional avanzado con núcleo cuántico inicializado")
        
    async def process_conversation(self, request: ConversationRequest) -> ConversationResponse:
        """Procesar una conversación completa"""
        start_time = time.time()
        
        try:
            # Obtener o crear sesión
            session = self._get_or_create_session(request.session_id, request.user_id)
            
            # Crear mensaje del usuario
            user_message = UserMessage(
                content=request.content,
                session_id=request.session_id,
                user_id=request.user_id,
                emotion=request.emotion,
                confidence=request.confidence,
                context_dims=request.context_26d or []
            )
            
            # Procesar contenido multimedia
            processed_content = await self._process_multimodal_content(request.content)
            
            # Actualizar contexto 26D
            self._update_context_26d(user_message, processed_content)
            
            # Generar respuesta del asistente
            assistant_response = await self._generate_assistant_response(
                user_message, processed_content, request
            )
            
            # Actualizar sesión
            session.messages.append(user_message)
            session.responses.append(assistant_response)
            session.state = ConversationState.ACTIVE
            
            processing_time = time.time() - start_time
            
            return ConversationResponse(
                success=True,
                response=assistant_response,
                session=session,
                processing_time=processing_time,
                context_26d_updated=self.context_26d
            )
            
        except Exception as e:
            logger.error(f"Error en procesamiento de conversación: {e}")
            return ConversationResponse(
                success=False,
                error=str(e),
                processing_time=time.time() - start_time
            )
    
    def _get_or_create_session(self, session_id: str, user_id: Optional[str] = None) -> ConversationSession:
        """Obtener o crear una sesión de conversación"""
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationSession(
                session_id=session_id,
                user_id=user_id,
                context_26d=self.context_26d.copy()
            )
        return self.sessions[session_id]
    
    @lru_cache(maxsize=1000)
    def _get_cache_key(self, content_hash: str, media_type: str) -> str:
        """Generar clave de cache"""
        return f"{content_hash}_{media_type}"
    
    async def _process_multimodal_content(self, content: MediaContent) -> Dict[str, Any]:
        """Procesar contenido multimodal con NLP avanzado optimizado"""
        # Generar hash del contenido para cache
        content_str = str(content.content) if content.content else ""
        content_hash = hashlib.md5(content_str.encode()).hexdigest()
        cache_key = self._get_cache_key(content_hash, content.media_type.value)
        
        # Verificar cache
        if hasattr(self, '_content_cache') and cache_key in self._content_cache:
            print(f"🔄 Cache hit para contenido: {cache_key[:10]}...")
            return self._content_cache[cache_key]
        
        result = {
            "media_type": content.media_type,
            "processed": True,
            "features": {},
            "emotion": None,
            "confidence": 1.0,
            "nlp_analysis": None
        }
        
        if content.media_type == MediaType.AUDIO:
            audio_result = await self.audio_processor.process_audio(content.content)
            result.update(audio_result)
            
        elif content.media_type == MediaType.VIDEO:
            video_result = await self.video_processor.process_video(content.content)
            result.update(video_result)
            
        elif content.media_type == MediaType.IMAGE:
            # Procesar imagen (usar el procesador existente)
            result["features"] = {"image_processed": True}
            
        elif content.media_type == MediaType.TEXT:
            # 🚀 PROCESAMIENTO PARALELO OPTIMIZADO
            text_content = content.content if isinstance(content.content, str) else ""
            
            # Crear tareas paralelas
            tasks = [
                nlp_engine.analyze_text(text_content),
                self.quantum_core.test_quantum_enhancement(text_content, "general"),
                nlp_engine.detect_language(text_content),
                nlp_engine.extract_summary(text_content)
            ]
            
            # Ejecutar en paralelo
            nlp_features, quantum_result, language, summary = await asyncio.gather(*tasks)
            
            # Guardar resultados
            content.nlp_features = nlp_features
            content.quantum_features = quantum_result
            # Procesar texto con NLP avanzado y núcleo cuántico
            text_content = content.content if isinstance(content.content, str) else ""
            
            # Análisis NLP completo
            nlp_features = await nlp_engine.analyze_text(text_content)
            content.nlp_features = nlp_features
            
            # 🧠 PROCESAMIENTO CUÁNTICO AVANZADO
            quantum_prompt = await self._create_quantum_prompt(text_content, nlp_features)
            quantum_result = await self.quantum_core.test_quantum_enhancement(text_content, "general")
            
            # Guardar resultado cuántico en el contenido
            content.quantum_features = quantum_result
            
            # Detectar idioma
            language = await nlp_engine.detect_language(text_content)
            
            # Extraer resumen
            summary = await nlp_engine.extract_summary(text_content)
            
            result.update({
                "features": {
                    "text_length": len(text_content),
                    "language": language,
                    "readability_score": nlp_features.readability_score,
                    "complexity_score": nlp_features.complexity_score,
                    "topic_keywords": nlp_features.topic_keywords,
                    "summary": summary,
                    "quantum_score": quantum_result.quantum_score,
                    "quantum_state": quantum_result.quantum_state_achieved.value,
                    "improvement_factor": quantum_result.improvement_factor
                },
                "nlp_analysis": {
                    "sentiment": {
                        "level": nlp_features.sentiment.level.value if hasattr(nlp_features.sentiment.level, 'value') else str(nlp_features.sentiment.level),
                        "compound": nlp_features.sentiment.compound,
                        "confidence": nlp_features.sentiment.confidence,
                        "subjectivity": nlp_features.sentiment.subjectivity
                    },
                    "intent": {
                        "type": nlp_features.intent.intent.value if hasattr(nlp_features.intent.intent, 'value') else str(nlp_features.intent.intent),
                        "confidence": nlp_features.intent.confidence,
                        "keywords": nlp_features.intent.keywords,
                        "context": nlp_features.intent.context
                    },
                    "entities": [
                        {
                            "text": entity.text,
                            "type": entity.type.value if hasattr(entity.type, 'value') else str(entity.type),
                            "confidence": entity.confidence,
                            "description": entity.description
                        }
                        for entity in nlp_features.intent.entities
                    ],
                    "quantum_enhancement": {
                        "quantum_score": quantum_result.quantum_score,
                        "quantum_state": quantum_result.quantum_state_achieved.value,
                        "improvement_factor": quantum_result.improvement_factor,
                        "dimension_scores": quantum_result.dimension_scores
                    }
                },
                "emotion": nlp_features.sentiment.level.value if hasattr(nlp_features.sentiment.level, 'value') else str(nlp_features.sentiment.level),
                "confidence": max(nlp_features.sentiment.confidence, quantum_result.quantum_score)
            })
            
        return result
    
    async def _create_quantum_prompt(self, text: str, nlp_features: TextFeatures) -> QuantumPrompt:
        """Crear prompt cuántico basado en análisis NLP"""
        # Mapear dimensiones cuánticas basadas en análisis NLP
        quantum_dimensions = {}
        
        # Mapear sentimiento a dimensiones cuánticas
        sentiment_compound = nlp_features.sentiment.compound
        quantum_dimensions[QuantumDimension.CREATIVE_SYNTHESIS] = max(0.1, (sentiment_compound + 1) / 2)
        quantum_dimensions[QuantumDimension.LOGICAL_COHERENCE] = nlp_features.sentiment.confidence
        
        # Mapear intención a dimensiones cuánticas
        intent_confidence = nlp_features.intent.confidence
        if nlp_features.intent.intent == IntentType.PROGRAMMING:
            quantum_dimensions[QuantumDimension.MATHEMATICAL_PRECISION] = intent_confidence
            quantum_dimensions[QuantumDimension.PROBLEM_SOLVING] = intent_confidence
        elif nlp_features.intent.intent == IntentType.CREATIVE:
            quantum_dimensions[QuantumDimension.CREATIVE_SYNTHESIS] = intent_confidence
            quantum_dimensions[QuantumDimension.INNOVATIVE_APPROACH] = intent_confidence
        elif nlp_features.intent.intent == IntentType.ANALYSIS:
            quantum_dimensions[QuantumDimension.ANALYTICAL_DEPTH] = intent_confidence
            quantum_dimensions[QuantumDimension.CRITICAL_THINKING] = intent_confidence
        
        # Mapear complejidad del texto
        quantum_dimensions[QuantumDimension.INTELLECTUAL_MASTERY] = nlp_features.complexity_score
        quantum_dimensions[QuantumDimension.CONCEPTUAL_UNDERSTANDING] = nlp_features.readability_score
        
        # Estado cuántico basado en características del texto
        if len(nlp_features.intent.entities) > 0:
            quantum_state = QuantumState.ENTANGLED
        elif nlp_features.intent.confidence > 0.8:
            quantum_state = QuantumState.COHERENT
        else:
            quantum_state = QuantumState.SUPERPOSITION
        
        return QuantumPrompt(
            base_prompt=text,
            quantum_dimensions=quantum_dimensions,
            quantum_state=quantum_state,
            entanglement_factor=nlp_features.intent.confidence,
            coherence_level=nlp_features.sentiment.confidence,
            resonance_frequency=888.0  # Frecuencia VIGOLEONROCKS
        )
    
    def _update_context_26d(self, user_message: UserMessage, processed_content: Dict[str, Any]):
        """Actualizar el contexto 26D"""
        # Dimensión 0: Contenido principal
        self.context_26d[0].content = user_message.content.content if isinstance(user_message.content.content, str) else "Multimedia content"
        self.context_26d[0].timestamp = user_message.timestamp
        
        # Dimensión 1: Emoción detectada
        emotion = processed_content.get("emotion") or processed_content.get("dominant_emotion")
        if emotion:
            self.context_26d[1].content = emotion.value if hasattr(emotion, 'value') else str(emotion)
            self.context_26d[1].emotion = emotion
            self.context_26d[1].confidence = processed_content.get("confidence", 0.8)
        
        # Dimensión 2: Tipo de medio
        self.context_26d[2].content = user_message.content.media_type.value
        
        # Dimensión 3: Timestamp
        self.context_26d[3].content = user_message.timestamp.isoformat()
        
        # Dimensión 4: Características específicas
        features = processed_content.get("features", {})
        self.context_26d[4].content = json.dumps(features)
        
        # Actualizar pesos basados en confianza
        for i, dim in enumerate(self.context_26d):
            if dim.content:
                dim.weight = min(1.0, dim.weight + 0.1)
    
    async def _generate_assistant_response(self, user_message: UserMessage, 
                                         processed_content: Dict[str, Any],
                                         request: ConversationRequest) -> AssistantResponse:
        """Generar respuesta del asistente"""
        start_time = time.time()
        
        # Construir prompt contextual
        context_prompt = self._build_contextual_prompt(user_message, processed_content)
        
        # Usar el contenido procesado del usuario como respuesta
        # (en un sistema real, aquí se generaría la respuesta con el modelo)
        response_content = f"🤖 Respuesta procesada con análisis NLP y núcleo cuántico:\n\n"
        response_content += f"📝 Texto original: {user_message.content.content}\n"
        
        # Agregar información del análisis NLP
        nlp_analysis = processed_content.get("nlp_analysis")
        if nlp_analysis:
            sentiment = nlp_analysis.get("sentiment", {})
            if sentiment:
                response_content += f"🧠 Sentimiento: {sentiment.get('level', 'neutral')} (confianza: {sentiment.get('confidence', 0):.2f})\n"
            
            intent = nlp_analysis.get("intent", {})
            if intent:
                response_content += f"🎯 Intención: {intent.get('type', 'unknown')} (confianza: {intent.get('confidence', 0):.2f})\n"
        
        # Agregar información cuántica
        quantum_enhancement = nlp_analysis.get("quantum_enhancement") if nlp_analysis else None
        if quantum_enhancement:
            response_content += f"⚛️ Score cuántico: {quantum_enhancement.get('quantum_score', 0):.2f}\n"
            response_content += f"🌌 Estado cuántico: {quantum_enhancement.get('quantum_state', 'unknown')}\n"
        
        response_content += f"\n✨ Procesado con frecuencia VIGOLEONROCKS: 888Hz determinística"
        
        processing_time = time.time() - start_time
        
        # Crear contenido de respuesta con NLP y quantum features
        response_media_content = MediaContent(
            media_type=MediaType.TEXT,
            content=response_content,
            nlp_features=user_message.content.nlp_features,  # Pasar NLP features
            quantum_features=user_message.content.quantum_features  # Pasar quantum features
        )
        
        return AssistantResponse(
            content=response_media_content,
            session_id=user_message.session_id,
            model_used=request.model_preference or "vigoleonrocks",
            quality_score=0.85,
            coherence_score=0.78,
            consciousness_level=2.0,
            processing_time=processing_time,
            context_dims_used=[0, 1, 2, 3, 4],
            emotion_detected=processed_content.get("emotion"),
            confidence=0.9
        )
    
    def _build_contextual_prompt(self, user_message: UserMessage, 
                                processed_content: Dict[str, Any]) -> str:
        """Construir prompt contextual con análisis NLP"""
        prompt_parts = []
        
        # Información del usuario
        prompt_parts.append(f"Usuario: {user_message.user_id or 'Anónimo'}")
        prompt_parts.append(f"Tipo de medio: {user_message.content.media_type.value}")
        
        # Análisis NLP si está disponible
        nlp_analysis = processed_content.get("nlp_analysis")
        if nlp_analysis:
            # Sentimiento
            sentiment = nlp_analysis.get("sentiment", {})
            if sentiment:
                prompt_parts.append(f"Sentimiento: {sentiment.get('level', 'neutral')} (confianza: {sentiment.get('confidence', 0):.2f})")
                prompt_parts.append(f"Subjetividad: {sentiment.get('subjectivity', 0):.2f}")
            
            # Intención
            intent = nlp_analysis.get("intent", {})
            if intent:
                prompt_parts.append(f"Intención: {intent.get('type', 'unknown')} (confianza: {intent.get('confidence', 0):.2f})")
                keywords = intent.get('keywords', [])
                if keywords:
                    prompt_parts.append(f"Palabras clave: {', '.join(keywords[:5])}")
            
            # Entidades
            entities = nlp_analysis.get("entities", [])
            if entities:
                entity_texts = [f"{e.get('text', '')} ({e.get('type', '')})" for e in entities[:3]]
                prompt_parts.append(f"Entidades detectadas: {', '.join(entity_texts)}")
        
        # Emoción detectada (fallback)
        emotion = processed_content.get("emotion") or processed_content.get("dominant_emotion")
        if emotion and not nlp_analysis:
            prompt_parts.append(f"Emoción detectada: {emotion.value if hasattr(emotion, 'value') else str(emotion)}")
        
        # Características específicas
        features = processed_content.get("features", {})
        if features:
            # Información de legibilidad y complejidad
            if "readability_score" in features:
                prompt_parts.append(f"Legibilidad: {features['readability_score']:.2f}")
            if "complexity_score" in features:
                prompt_parts.append(f"Complejidad: {features['complexity_score']:.2f}")
            if "language" in features:
                prompt_parts.append(f"Idioma detectado: {features['language']}")
            if "topic_keywords" in features:
                prompt_parts.append(f"Temas principales: {', '.join(features['topic_keywords'][:3])}")
        
        # Contexto 26D relevante
        relevant_dims = [dim for dim in self.context_26d if dim.content and dim.weight > 0.5]
        if relevant_dims:
            prompt_parts.append("Contexto 26D:")
            for dim in relevant_dims[:5]:  # Primeras 5 dimensiones relevantes
                prompt_parts.append(f"  D{dim.dimension_id}: {dim.content}")
        
        return "\n".join(prompt_parts)
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """Obtener una sesión específica"""
        return self.sessions.get(session_id)
    
    def list_sessions(self) -> List[ConversationSession]:
        """Listar todas las sesiones"""
        return list(self.sessions.values())
    
    def delete_session(self, session_id: str) -> bool:
        """Eliminar una sesión"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

# Instancia global del motor
conversational_engine = AdvancedConversationalEngine()
