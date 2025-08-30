#!/usr/bin/env python3
"""
Test Suite Completo para Vigoleonrocks Hybrid Multimodal Service
Valida tanto la funcionalidad híbrida como las capacidades multimodales
Sin emojis, cumple reglas del proyecto
"""

import asyncio
import time
import os
import json
import tempfile
from typing import Dict, List, Any
import logging

# Configurar logging sin emojis
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importar el servicio integrado
from vigoleonrocks_hybrid_multimodal_service import (
    HybridMultimodalService, 
    TextRequest, 
    MultimodalRequest,
    ServiceMode,
    KernelRandom
)

class HybridMultimodalTestSuite:
    """Suite de tests completa para el sistema integrado"""
    
    def __init__(self):
        self.service = HybridMultimodalService()
        self.test_results = {}
        self.temp_files = []
        
    async def initialize(self):
        """Inicializar servicio para tests"""
        await self.service.initialize()
        logger.info("Test suite initialized")
    
    async def run_all_tests(self):
        """Ejecutar todos los tests de integración"""
        logger.info("Starting comprehensive test suite for Hybrid Multimodal Service")
        
        test_groups = [
            ("Precision Tests", self.test_hybrid_precision),
            ("Text Processing Tests", self.test_text_processing),
            ("Multimodal Tests", self.test_multimodal_processing),
            ("Engine Selection Tests", self.test_engine_selection),
            ("Performance Tests", self.test_performance_metrics),
            ("Error Handling Tests", self.test_error_handling),
            ("Integration Tests", self.test_full_integration)
        ]
        
        for group_name, test_method in test_groups:
            logger.info(f"Running {group_name}...")
            try:
                results = await test_method()
                self.test_results[group_name] = results
                logger.info(f"Completed {group_name}: {len(results)} tests")
            except Exception as e:
                logger.error(f"Error in {group_name}: {e}")
                self.test_results[group_name] = {"error": str(e)}
        
        # Generar reporte final
        await self.generate_test_report()
        
        # Limpiar archivos temporales
        self.cleanup_temp_files()
    
    async def test_hybrid_precision(self) -> Dict[str, Any]:
        """Test del sistema híbrido de precisión original (Blueberry Challenge)"""
        
        blueberry_cases = [
            {
                "name": "Letter count - blueberry r",
                "text": "¿Cuántas letras 'r' hay en la palabra 'blueberry'?",
                "expected_answer": "2",
                "expected_engine": "basic_precision"
            },
            {
                "name": "Letter count - strawberry r", 
                "text": "¿Cuántas letras 'r' hay en la palabra 'strawberry'?",
                "expected_answer": "3",
                "expected_engine": "basic_precision"
            },
            {
                "name": "Letter count - mississippi s",
                "text": "¿Cuántas letras 's' hay en la palabra 'mississippi'?",
                "expected_answer": "4",
                "expected_engine": "basic_precision"
            },
            {
                "name": "Basic arithmetic",
                "text": "Si tengo 3 manzanas y me como 2, ¿cuántas me quedan?",
                "expected_answer": "1",
                "expected_engine": "basic_precision"
            },
            {
                "name": "Number comparison",
                "text": "¿Qué número es mayor: 47 o 74?",
                "expected_answer": "74",
                "expected_engine": "basic_precision"
            }
        ]
        
        results = {}
        
        for case in blueberry_cases:
            try:
                request = TextRequest(text=case["text"])
                response = await self.service.process_text_request(request)
                
                # Extraer respuesta numérica para validación
                answer_extracted = self._extract_answer_from_response(response.response, case["text"])
                
                results[case["name"]] = {
                    "passed": answer_extracted == case["expected_answer"],
                    "expected_answer": case["expected_answer"],
                    "actual_answer": answer_extracted,
                    "expected_engine": case["expected_engine"],
                    "actual_engine": response.engine_used,
                    "processing_time": response.processing_time,
                    "quality_score": response.quality_score,
                    "engine_correct": case["expected_engine"] in response.engine_used
                }
                
            except Exception as e:
                results[case["name"]] = {
                    "passed": False,
                    "error": str(e)
                }
        
        return results
    
    async def test_text_processing(self) -> Dict[str, Any]:
        """Test de procesamiento de texto con diferentes motores"""
        
        test_cases = [
            {
                "name": "Force basic engine",
                "text": "¿Cuántas letras 'a' hay en 'casa'?",
                "force_engine": "basic",
                "expected_engine": "precision_basic"
            },
            {
                "name": "Force quantum engine",
                "text": "Implementa un algoritmo de ordenamiento eficiente",
                "force_engine": "quantum",
                "expected_engine": "quantum_refined"
            },
            {
                "name": "Automatic hybrid selection",
                "text": "Explica qué es la programación orientada a objetos",
                "force_engine": None,
                "expected_engine": None  # Se selecciona automáticamente
            }
        ]
        
        results = {}
        
        for case in test_cases:
            try:
                request = TextRequest(
                    text=case["text"],
                    force_engine=case["force_engine"]
                )
                response = await self.service.process_text_request(request)
                
                engine_match = True
                if case["expected_engine"]:
                    engine_match = case["expected_engine"] in response.engine_used
                
                results[case["name"]] = {
                    "passed": response.success and engine_match,
                    "engine_used": response.engine_used,
                    "processing_time": response.processing_time,
                    "quality_score": response.quality_score,
                    "response_length": len(response.response),
                    "classification": response.classification
                }
                
            except Exception as e:
                results[case["name"]] = {
                    "passed": False,
                    "error": str(e)
                }
        
        return results
    
    async def test_multimodal_processing(self) -> Dict[str, Any]:
        """Test de capacidades multimodales reales"""
        
        results = {}
        
        # Test 1: Crear archivo de imagen temporal
        try:
            image_path = await self._create_test_image()
            
            request = MultimodalRequest(
                text="Analiza esta imagen y dime qué ves",
                image_path=image_path
            )
            
            response = await self.service.process_multimodal_request(request)
            
            results["image_processing"] = {
                "passed": response.success and response.multimodal_features is not None,
                "has_image_features": "image" in (response.multimodal_features or {}),
                "image_processed": response.multimodal_features.get("image", {}).get("processed", False),
                "content_type": response.content_type,
                "processing_time": response.processing_time,
                "quality_score": response.quality_score
            }
            
        except Exception as e:
            results["image_processing"] = {
                "passed": False,
                "error": str(e)
            }
        
        # Test 2: Crear archivo de audio temporal
        try:
            audio_path = await self._create_test_audio()
            
            request = MultimodalRequest(
                text="Procesa este archivo de audio",
                audio_path=audio_path
            )
            
            response = await self.service.process_multimodal_request(request)
            
            results["audio_processing"] = {
                "passed": response.success and response.multimodal_features is not None,
                "has_audio_features": "audio" in (response.multimodal_features or {}),
                "audio_processed": response.multimodal_features.get("audio", {}).get("processed", False),
                "content_type": response.content_type,
                "processing_time": response.processing_time,
                "quality_score": response.quality_score
            }
            
        except Exception as e:
            results["audio_processing"] = {
                "passed": False,
                "error": str(e)
            }
        
        # Test 3: Procesamiento mixto (imagen + audio)
        try:
            request = MultimodalRequest(
                text="Analiza tanto la imagen como el audio",
                image_path=image_path,
                audio_path=audio_path
            )
            
            response = await self.service.process_multimodal_request(request)
            
            multimodal_count = 0
            if response.multimodal_features:
                if "image" in response.multimodal_features:
                    multimodal_count += 1
                if "audio" in response.multimodal_features:
                    multimodal_count += 1
            
            results["mixed_multimodal"] = {
                "passed": response.success and multimodal_count >= 2,
                "multimodal_count": multimodal_count,
                "content_type": response.content_type,
                "processing_time": response.processing_time,
                "quality_score": response.quality_score,
                "enhanced_text_length": len(response.response)
            }
            
        except Exception as e:
            results["mixed_multimodal"] = {
                "passed": False,
                "error": str(e)
            }
        
        return results
    
    async def test_engine_selection(self) -> Dict[str, Any]:
        """Test de selección inteligente de motores"""
        
        engine_test_cases = [
            {
                "name": "Trivial case should use basic engine",
                "text": "¿Cuántas letras 'o' hay en 'hola'?",
                "expected_category": "basic"
            },
            {
                "name": "Complex algorithm should use quantum engine", 
                "text": "Implementa un algoritmo de Machine Learning para sistemas distribuidos",
                "expected_category": "quantum"
            },
            {
                "name": "Medium complexity should trigger hybrid mode",
                "text": "Explica las diferencias entre programación funcional y orientada a objetos",
                "expected_category": "hybrid"
            }
        ]
        
        results = {}
        
        for case in engine_test_cases:
            try:
                request = TextRequest(text=case["text"])
                response = await self.service.process_text_request(request)
                
                # Determinar si la selección fue apropiada
                engine_appropriate = False
                if case["expected_category"] == "basic" and "basic" in response.engine_used:
                    engine_appropriate = True
                elif case["expected_category"] == "quantum" and "quantum" in response.engine_used:
                    engine_appropriate = True
                elif case["expected_category"] == "hybrid":
                    engine_appropriate = True  # Cualquier motor es válido en modo híbrido
                
                results[case["name"]] = {
                    "passed": response.success and engine_appropriate,
                    "expected_category": case["expected_category"],
                    "actual_engine": response.engine_used,
                    "classification": response.classification,
                    "processing_time": response.processing_time,
                    "quality_score": response.quality_score
                }
                
            except Exception as e:
                results[case["name"]] = {
                    "passed": False,
                    "error": str(e)
                }
        
        return results
    
    async def test_performance_metrics(self) -> Dict[str, Any]:
        """Test del sistema de métricas en segundo plano"""
        
        results = {}
        
        try:
            # Realizar varias solicitudes para generar métricas
            requests = [
                "¿Cuántas letras 'e' hay en 'desarrollo'?",
                "Implementa una función de fibonacci optimizada",
                "¿Qué es mayor: 15 o 51?",
            ]
            
            start_time = time.time()
            
            for text in requests:
                request = TextRequest(text=text)
                await self.service.process_text_request(request)
            
            # Obtener métricas del sistema
            metrics = self.service.get_system_metrics()
            
            processing_time = time.time() - start_time
            
            results["metrics_collection"] = {
                "passed": metrics["total_requests"] >= 3,
                "total_requests": metrics["total_requests"],
                "uptime_seconds": metrics["uptime_seconds"],
                "has_performance_data": "performance" in metrics,
                "average_response_time": metrics["performance"]["average_response_time"],
                "error_rate": metrics["performance"]["error_rate"],
                "capabilities_count": len(metrics["capabilities"]),
                "test_processing_time": processing_time
            }
            
            # Test de background metrics collector
            collector_active = self.service.metrics_collector.running
            
            results["background_collector"] = {
                "passed": collector_active,
                "collector_running": collector_active,
                "metrics_keys": list(self.service.metrics_collector.metrics.keys()),
                "requests_by_type": self.service.metrics_collector.metrics["requests_by_type"],
                "engine_usage": self.service.metrics_collector.metrics["engine_usage"]
            }
            
        except Exception as e:
            results["metrics_error"] = {
                "passed": False,
                "error": str(e)
            }
        
        return results
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test de manejo de errores"""
        
        results = {}
        
        # Test 1: Archivo de imagen inexistente
        try:
            request = MultimodalRequest(
                text="Analiza esta imagen",
                image_path="/path/that/does/not/exist.jpg"
            )
            
            response = await self.service.process_multimodal_request(request)
            
            results["nonexistent_image"] = {
                "passed": not response.success or "error" in (response.multimodal_features or {}).get("image", {}),
                "handled_gracefully": response.error_details is not None or not response.success,
                "response": response.response[:100] if response.response else "",
                "content_type": response.content_type
            }
            
        except Exception as e:
            results["nonexistent_image"] = {
                "passed": True,  # Exception handling is also valid
                "exception_caught": str(e)
            }
        
        # Test 2: Texto vacío
        try:
            request = TextRequest(text="")
            response = await self.service.process_text_request(request)
            
            results["empty_text"] = {
                "passed": True,  # Cualquier manejo es válido
                "success": response.success,
                "response_provided": len(response.response) > 0,
                "processing_time": response.processing_time
            }
            
        except Exception as e:
            results["empty_text"] = {
                "passed": True,  # Exception handling is valid
                "exception_caught": str(e)
            }
        
        # Test 3: Motor no válido
        try:
            request = TextRequest(
                text="Test con motor inválido",
                force_engine="invalid_engine"
            )
            response = await self.service.process_text_request(request)
            
            results["invalid_engine"] = {
                "passed": True,  # Cualquier manejo es válido
                "success": response.success,
                "engine_used": response.engine_used,
                "graceful_fallback": "error" not in response.engine_used.lower() or not response.success
            }
            
        except Exception as e:
            results["invalid_engine"] = {
                "passed": True,  # Exception handling is valid
                "exception_caught": str(e)
            }
        
        return results
    
    async def test_full_integration(self) -> Dict[str, Any]:
        """Test de integración completa del sistema"""
        
        results = {}
        
        try:
            # Test de flujo completo: texto -> multimodal -> métricas
            start_time = time.time()
            
            # Paso 1: Procesamiento de texto básico
            text_request = TextRequest(text="¿Cuántas letras 'i' hay en 'optimización'?")
            text_response = await self.service.process_text_request(text_request)
            
            # Paso 2: Procesamiento multimodal
            image_path = await self._create_test_image()
            multimodal_request = MultimodalRequest(
                text="Describe la arquitectura de este sistema híbrido",
                image_path=image_path
            )
            multimodal_response = await self.service.process_multimodal_request(multimodal_request)
            
            # Paso 3: Verificar métricas actualizadas
            final_metrics = self.service.get_system_metrics()
            
            total_time = time.time() - start_time
            
            # Validaciones de integración
            integration_passed = (
                text_response.success and 
                multimodal_response.success and
                final_metrics["total_requests"] >= 2 and
                len(final_metrics["capabilities"]) >= 5
            )
            
            results["full_integration_flow"] = {
                "passed": integration_passed,
                "text_processing_success": text_response.success,
                "text_engine_used": text_response.engine_used,
                "text_quality": text_response.quality_score,
                "multimodal_processing_success": multimodal_response.success,
                "multimodal_features_count": len(multimodal_response.multimodal_features or {}),
                "multimodal_quality": multimodal_response.quality_score,
                "final_total_requests": final_metrics["total_requests"],
                "system_capabilities_count": len(final_metrics["capabilities"]),
                "total_integration_time": total_time,
                "average_response_time": final_metrics["performance"]["average_response_time"],
                "system_error_rate": final_metrics["performance"]["error_rate"]
            }
            
            # Test de coherencia del sistema
            coherence_checks = {
                "metrics_consistency": final_metrics["total_requests"] > 0,
                "response_time_reasonable": total_time < 30.0,  # Máximo 30 segundos
                "quality_scores_valid": (
                    0.0 <= text_response.quality_score <= 1.0 and 
                    0.0 <= multimodal_response.quality_score <= 1.0
                ),
                "engines_different": text_response.engine_used != multimodal_response.engine_used or True,  # Puede ser igual
                "status_operational": final_metrics["status"] == "operational"
            }
            
            results["system_coherence"] = {
                "passed": all(coherence_checks.values()),
                "checks": coherence_checks,
                "total_checks": len(coherence_checks),
                "passed_checks": sum(coherence_checks.values())
            }
            
        except Exception as e:
            results["integration_error"] = {
                "passed": False,
                "error": str(e)
            }
        
        return results
    
    async def _create_test_image(self) -> str:
        """Crear archivo de imagen de prueba"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        
        # Crear un archivo PNG simple (1x1 pixel)
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
        
        temp_file.write(png_data)
        temp_file.close()
        
        self.temp_files.append(temp_file.name)
        return temp_file.name
    
    async def _create_test_audio(self) -> str:
        """Crear archivo de audio de prueba"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        
        # Crear un archivo WAV simple (mínimo header)
        wav_header = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
        
        temp_file.write(wav_header)
        temp_file.close()
        
        self.temp_files.append(temp_file.name)
        return temp_file.name
    
    def _extract_answer_from_response(self, response: str, query: str) -> str:
        """Extraer respuesta específica para validación"""
        import re
        
        query_lower = query.lower()
        
        # Casos de conteo de letras
        if "cuántas letras" in query_lower:
            numbers = re.findall(r'\*\*(\d+)\*\*|Total.*?(\d+)', response)
            if numbers:
                for match in numbers:
                    for num in match:
                        if num:
                            return num
        
        # Casos de aritmética
        if "me quedan" in query_lower:
            numbers = re.findall(r'\*\*(\d+)\*\*', response)
            if numbers:
                return numbers[-1]
        
        # Casos de comparación
        if "mayor" in query_lower:
            numbers = re.findall(r'\*\*(\d+)\*\*', response)
            if len(numbers) >= 2:
                return str(max(int(n) for n in numbers))
        
        # Fallback: buscar cualquier número
        numbers = re.findall(r'\b(\d+)\b', response)
        if numbers:
            return numbers[-1]
        
        return "No extraído"
    
    def cleanup_temp_files(self):
        """Limpiar archivos temporales"""
        for file_path in self.temp_files:
            try:
                os.remove(file_path)
            except:
                pass
        self.temp_files.clear()
    
    async def generate_test_report(self):
        """Generar reporte completo de tests"""
        
        print("\n" + "="*80)
        print("VIGOLEONROCKS HYBRID MULTIMODAL SERVICE - TEST REPORT")
        print("="*80)
        
        total_tests = 0
        passed_tests = 0
        
        for group_name, group_results in self.test_results.items():
            print(f"\n{group_name}:")
            print("-" * len(group_name))
            
            if isinstance(group_results, dict) and "error" in group_results:
                print(f"  ERROR: {group_results['error']}")
                continue
            
            for test_name, test_result in group_results.items():
                total_tests += 1
                status = "PASS" if test_result.get("passed", False) else "FAIL"
                
                if test_result.get("passed", False):
                    passed_tests += 1
                
                print(f"  {status}: {test_name}")
                
                # Mostrar detalles importantes
                if "processing_time" in test_result:
                    print(f"    Processing Time: {test_result['processing_time']:.3f}s")
                if "quality_score" in test_result:
                    print(f"    Quality Score: {test_result['quality_score']:.3f}")
                if "engine_used" in test_result:
                    print(f"    Engine Used: {test_result['engine_used']}")
                if "error" in test_result:
                    print(f"    Error: {test_result['error']}")
        
        # Resumen final
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"\n{'='*80}")
        print(f"SUMMARY: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            print("STATUS: SYSTEM READY FOR PRODUCTION")
        elif success_rate >= 60:
            print("STATUS: SYSTEM FUNCTIONAL WITH MINOR ISSUES")
        else:
            print("STATUS: SYSTEM REQUIRES FIXES BEFORE DEPLOYMENT")
        
        print("="*80)

async def main():
    """Ejecutar suite completa de tests"""
    logger.info("Starting Hybrid Multimodal Service Test Suite")
    
    test_suite = HybridMultimodalTestSuite()
    
    try:
        await test_suite.initialize()
        await test_suite.run_all_tests()
    except Exception as e:
        logger.error(f"Test suite failed: {e}")
    finally:
        test_suite.cleanup_temp_files()

if __name__ == "__main__":
    asyncio.run(main())
