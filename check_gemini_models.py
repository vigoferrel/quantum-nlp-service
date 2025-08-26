#!/usr/bin/env python3
"""
🔍 CHECK GEMINI MODELS
Verificar modelos Gemini disponibles con precios
"""

import requests
import json

def check_gemini_models():
    """Verifica modelos Gemini disponibles"""
    
    api_key = "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"
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            models = response.json()
            
            print("🔍 MODELOS GEMINI DISPONIBLES EN OPENROUTER")
            print("=" * 60)
            
            gemini_models = []
            
            for model in models.get('data', []):
                model_id = model.get('id', '')
                
                if 'gemini' in model_id.lower():
                    pricing = model.get('pricing', {})
                    prompt_price = pricing.get('prompt', 'N/A')
                    completion_price = pricing.get('completion', 'N/A')
                    
                    gemini_models.append({
                        'id': model_id,
                        'prompt_price': prompt_price,
                        'completion_price': completion_price,
                        'context_length': model.get('context_length', 'N/A')
                    })
            
            # Ordenar por precio (más barato primero)
            gemini_models.sort(key=lambda x: float(x['prompt_price']) if x['prompt_price'] != 'N/A' else float('inf'))
            
            for i, model in enumerate(gemini_models, 1):
                print(f"{i:2d}. {model['id']}")
                print(f"    💰 Prompt: ${model['prompt_price']}/1M tokens")
                print(f"    💰 Completion: ${model['completion_price']}/1M tokens")
                print(f"    📏 Context: {model['context_length']} tokens")
                print()
            
            # Encontrar el más barato
            if gemini_models:
                cheapest = gemini_models[0]
                print(f"🏆 MÁS BARATO: {cheapest['id']}")
                print(f"💰 Precio: ${cheapest['prompt_price']}/1M tokens input")
                print(f"💰 Precio: ${cheapest['completion_price']}/1M tokens output")
            
            return gemini_models
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return []
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return []

if __name__ == "__main__":
    check_gemini_models()
