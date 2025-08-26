#!/usr/bin/env python3
"""
🔍 CHECK CLAUDE MODELS
Verificar modelos Claude disponibles en OpenRouter
"""

import requests
import json

def check_claude_models():
    """Verifica modelos Claude disponibles"""
    api_key = "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"
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            models = response.json()["data"]
            
            print("🔍 MODELOS CLAUDE DISPONIBLES EN OPENROUTER:")
            print("=" * 60)
            
            claude_models = []
            for model in models:
                if "claude" in model["id"].lower():
                    claude_models.append({
                        "id": model["id"],
                        "name": model.get("name", "N/A"),
                        "context_length": model.get("context_length", "N/A"),
                        "pricing": model.get("pricing", {}),
                        "description": model.get("description", "N/A")
                    })
            
            if claude_models:
                for i, model in enumerate(claude_models, 1):
                    print(f"\n{i}. {model['id']}")
                    print(f"   Nombre: {model['name']}")
                    print(f"   Contexto: {model['context_length']}")
                    print(f"   Descripción: {model['description'][:100]}...")
                    if model['pricing']:
                        input_price = model['pricing'].get('input', 'N/A')
                        output_price = model['pricing'].get('output', 'N/A')
                        print(f"   Precio Input: ${input_price}/1M tokens")
                        print(f"   Precio Output: ${output_price}/1M tokens")
            else:
                print("❌ No se encontraron modelos Claude")
            
            # Mostrar también modelos premium generales
            print(f"\n🏆 MODELOS PREMIUM DISPONIBLES:")
            print("=" * 60)
            
            premium_models = []
            for model in models:
                model_id = model["id"].lower()
                if any(brand in model_id for brand in ["claude", "gpt-4", "gpt-5", "gemini-2.5"]):
                    premium_models.append({
                        "id": model["id"],
                        "name": model.get("name", "N/A"),
                        "context_length": model.get("context_length", "N/A")
                    })
            
            for i, model in enumerate(premium_models[:10], 1):  # Top 10
                print(f"{i}. {model['id']} (Contexto: {model['context_length']})")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_claude_models()
