#!/usr/bin/env python3
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar la clase del servidor
from vigoleonrocks_server import VIGOLEONROCKSServer

def test_direct():
    print("🔍 PROBANDO FUNCIÓN DIRECTAMENTE")
    print("=" * 50)
    
    # Crear instancia del servidor
    server = VIGOLEONROCKSServer()
    
    # Probar diferentes combinaciones
    tests = [
        ("greeting", 1),
        ("greeting", 5),
        ("greeting", 10),
        ("support", 1),
        ("support", 5),
        ("support", 10),
        ("gratitude", 1),
        ("gratitude", 5),
        ("gratitude", 10)
    ]
    
    for template_type, empathy_level in tests:
        response = server.generate_empathic_response(template_type, empathy_level)
        print(f"📝 Template: {template_type}, Nivel: {empathy_level}")
        print(f"💬 Respuesta: {response}")
        print("-" * 50)

if __name__ == "__main__":
    test_direct()
