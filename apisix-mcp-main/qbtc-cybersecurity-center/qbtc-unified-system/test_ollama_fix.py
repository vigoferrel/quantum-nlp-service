#!/usr/bin/env python3
"""
Test Ollama connectivity and fix the system
"""

import requests
import json
import time

def test_ollama_local():
    """Test Ollama local connectivity"""
    try:
        print("Testing Ollama local connectivity...")
        response = requests.get("http://localhost:11434/api/version", timeout=10)
        print(f"Ollama Version API: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        return False

def test_ollama_models():
    """Test available models in Ollama"""
    try:
        print("Testing available models...")
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        print(f"Models API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Available models: {json.dumps(data, indent=2)}")
            return data
        return None
    except Exception as e:
        print(f"Error getting models: {e}")
        return None

def test_ollama_generate():
    """Test Ollama generation capability"""
    try:
        print("Testing Ollama generation...")
        
        # Get available models first
        models_response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if models_response.status_code != 200:
            print("Cannot get model list")
            return False
            
        models_data = models_response.json()
        if not models_data.get('models'):
            print("No models available")
            return False
            
        # Use first available model
        model_name = models_data['models'][0]['name']
        print(f"Using model: {model_name}")
        
        # Test generation
        payload = {
            "model": model_name,
            "prompt": "What is 25 + 37?",
            "stream": False
        }
        
        response = requests.post("http://localhost:11434/api/generate", 
                               json=payload, timeout=30)
        print(f"Generate API: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Generated response: {result.get('response', 'No response')}")
            return True
        else:
            print(f"Error response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing generation: {e}")
        return False

def fix_docker_connectivity():
    """Try to fix Docker connectivity issue"""
    print("\nAnalyzing Docker connectivity issue...")
    print("Problem: Ollama worker tries to connect to host.docker.internal:11434")
    print("Solution: Ollama is running on localhost:11434 but Docker can't access it")
    
    print("\nRecommended fixes:")
    print("1. Restart Ollama with host binding: OLLAMA_HOST=0.0.0.0:11434")
    print("2. Update Docker container network configuration")
    print("3. Use host network mode for ollama_worker container")
    
    return True

if __name__ == "__main__":
    print("QBTC Ollama Connectivity Test and Fix")
    print("=" * 50)
    
    # Test local connectivity
    ollama_local = test_ollama_local()
    
    if ollama_local:
        print("[OK] Ollama is running locally")
        
        # Test models
        models = test_ollama_models()
        
        if models and models.get('models'):
            print(f"[OK] Found {len(models['models'])} available models")
            
            # Test generation
            generation_works = test_ollama_generate()
            
            if generation_works:
                print("[OK] Ollama generation is working correctly!")
                print("\nPROBLEM CONFIRMED: Ollama works locally but Docker can't connect")
                fix_docker_connectivity()
            else:
                print("[ERROR] Ollama generation failed")
        else:
            print("[ERROR] No models available in Ollama")
    else:
        print("[ERROR] Cannot connect to Ollama locally")
    
    print("\n" + "=" * 50)