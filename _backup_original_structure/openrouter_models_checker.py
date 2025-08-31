#!/usr/bin/env python3
"""
Script para consultar la API de OpenRouter y obtener modelos reales disponibles
"""

import requests
import json
import os
from typing import Dict, List, Any

class OpenRouterModelsChecker:
    def __init__(self):
        # API Key de OpenRouter (usar la que ya está configurada)
        self.api_key = "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"
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://quantum-nlp-service.local",
            "X-Title": "Quantum NLP Service"
        }
    
    def get_all_models(self) -> Dict[str, Any]:
        """Obtener todos los modelos disponibles en OpenRouter"""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error obteniendo modelos: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return {"error": str(e)}
    
    def analyze_models(self, models_data: Dict[str, Any]) -> Dict[str, List]:
        """Analizar y categorizar modelos por potencia y costo"""
        
        if "error" in models_data:
            return {"error": models_data["error"]}
        
        models = models_data.get("data", [])
        
        # Categorías de análisis
        categories = {
            "free_models": [],
            "premium_models": [],
            "most_powerful": [],
            "latest_models": [],
            "multimodal_models": [],
            "code_models": [],
            "math_models": [],
            "reasoning_models": []
        }
        
        for model in models:
            model_id = model.get("id", "")
            name = model.get("name", "")
            description = model.get("description", "")
            pricing = model.get("pricing", {})
            context_length = model.get("context_length", 0)
            
            # Información del modelo
            model_info = {
                "id": model_id,
                "name": name,
                "description": description,
                "context_length": context_length,
                "pricing": pricing
            }
            
            # Categorizar por costo
            if pricing.get("prompt") == "0" and pricing.get("completion") == "0":
                categories["free_models"].append(model_info)
            else:
                categories["premium_models"].append(model_info)
            
            # Categorizar por potencia (contexto largo)
            if context_length >= 100000:
                categories["most_powerful"].append(model_info)
            
            # Categorizar por tipo
            if any(keyword in name.lower() for keyword in ["vision", "multimodal", "image"]):
                categories["multimodal_models"].append(model_info)
            
            if any(keyword in name.lower() for keyword in ["code", "coder", "programming"]):
                categories["code_models"].append(model_info)
            
            if any(keyword in name.lower() for keyword in ["math", "mathematical"]):
                categories["math_models"].append(model_info)
            
            if any(keyword in name.lower() for keyword in ["reasoning", "logic"]):
                categories["reasoning_models"].append(model_info)
            
            # Modelos más recientes (2024-2025)
            if any(year in name for year in ["2024", "2025", "3.3", "3.2", "2.0"]):
                categories["latest_models"].append(model_info)
        
        return categories
    
    def print_analysis(self, categories: Dict[str, List]):
        """Imprimir análisis de modelos"""
        
        if "error" in categories:
            print(f"❌ Error: {categories['error']}")
            return
        
        print("🔍 ANÁLISIS DE MODELOS OPENROUTER")
        print("=" * 50)
        
        # Modelos gratuitos
        print(f"\n🆓 MODELOS GRATUITOS ({len(categories['free_models'])}):")
        for model in categories["free_models"][:10]:  # Mostrar solo los primeros 10
            print(f"  • {model['name']} (ID: {model['id']})")
            print(f"    Contexto: {model['context_length']:,} tokens")
            if model['description']:
                print(f"    Descripción: {model['description'][:100]}...")
            print()
        
        # Modelos más potentes
        print(f"\n🚀 MODELOS MÁS POTENTES ({len(categories['most_powerful'])}):")
        for model in categories["most_powerful"][:10]:
            print(f"  • {model['name']} (ID: {model['id']})")
            print(f"    Contexto: {model['context_length']:,} tokens")
            print(f"    Precio: {model['pricing']}")
            print()
        
        # Modelos más recientes
        print(f"\n🆕 MODELOS MÁS RECIENTES ({len(categories['latest_models'])}):")
        for model in categories["latest_models"][:10]:
            print(f"  • {model['name']} (ID: {model['id']})")
            print(f"    Contexto: {model['context_length']:,} tokens")
            print()
        
        # Modelos multimodales
        print(f"\n👁️ MODELOS MULTIMODALES ({len(categories['multimodal_models'])}):")
        for model in categories["multimodal_models"][:5]:
            print(f"  • {model['name']} (ID: {model['id']})")
            print()
        
        # Modelos de código
        print(f"\n💻 MODELOS DE CÓDIGO ({len(categories['code_models'])}):")
        for model in categories["code_models"][:5]:
            print(f"  • {model['name']} (ID: {model['id']})")
            print()
        
        # Resumen
        print(f"\n📊 RESUMEN:")
        print(f"  • Total de modelos gratuitos: {len(categories['free_models'])}")
        print(f"  • Total de modelos premium: {len(categories['premium_models'])}")
        print(f"  • Modelos con contexto >100K: {len(categories['most_powerful'])}")
        print(f"  • Modelos más recientes: {len(categories['latest_models'])}")
    
    def get_model_details(self, model_id: str) -> Dict[str, Any]:
        """Obtener detalles específicos de un modelo"""
        try:
            response = requests.get(
                f"{self.base_url}/models/{model_id}",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}

def main():
    """Función principal"""
    print("🔍 CONSULTANDO MODELOS REALES DE OPENROUTER...")
    print("=" * 60)
    
    checker = OpenRouterModelsChecker()
    
    # Obtener todos los modelos
    print("📡 Obteniendo lista de modelos...")
    models_data = checker.get_all_models()
    
    if "error" in models_data:
        print(f"❌ Error: {models_data['error']}")
        return
    
    print(f"✅ Obtenidos {len(models_data.get('data', []))} modelos")
    
    # Analizar modelos
    print("\n🔍 Analizando modelos...")
    categories = checker.analyze_models(models_data)
    
    # Imprimir análisis
    checker.print_analysis(categories)
    
    # Guardar resultados en archivo
    with open("openrouter_models_analysis.json", "w", encoding="utf-8") as f:
        json.dump({
            "raw_data": models_data,
            "categories": categories
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Análisis guardado en: openrouter_models_analysis.json")

if __name__ == "__main__":
    main()
