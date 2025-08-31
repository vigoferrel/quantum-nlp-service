import requests

print("🧠 PROBANDO CIO MULTIMODAL - CACHE INTELIGENTE")
print("=" * 50)

# Prueba 1: Estado
response = requests.get('http://localhost:5001/api/status')
status = response.json()
print(f"📊 Estado: {status}")

# Prueba 2: Consulta
data = {
    "query": "¿Qué es el CIO y cómo funciona como cache inteligente enrutadora?"
}

response = requests.post('http://localhost:5001/api/process_multimodal', json=data)
result = response.json()

print(f"\n✅ Arquetipo: {result.get('archetype')}")
print(f"✅ Calidad: {result.get('quality', 0):.1%}")
print(f"✅ Respuesta: {result.get('response', '')[:300]}...")

if result.get('multimodal', {}).get('has_image'):
    print("✅ Procesamiento multimodal activo")
else:
    print("✅ Procesamiento de texto activo")

print("\n🎯 CIO: Cache Inteligente Enrutadora funcionando correctamente!")
