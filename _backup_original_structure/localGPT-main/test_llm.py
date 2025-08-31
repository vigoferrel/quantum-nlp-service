#!/usr/bin/env python3

import os
import sys

# Configurar variables de entorno
os.environ['SUPABASE_URL'] = 'https://hrvxsaolaxnqltomqaud.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhydnhzYW9sYXhucWx0b21xYXVkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTE0NTgwMSwiZXhwIjoyMDY2NzIxODAxfQ.SUZszjxj8I6r4yf7tE-VNlvfrp3wlaNlU4HzYdhXyoc'

from supabase import create_client

# Crear cliente Supabase
supabase_client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

def test_llm():
    try:
        print("🔧 Probando LLM...")
        response = supabase_client.table('vigoleonrocks_conversations').select('count').execute()
        print(f"📊 Resultado de la consulta: {response.data}")

        print("⚙️ Ejecutando inferencia LLM...")
        llm_response = supabase_client.rpc('vigoleonrocks_inference', {
            'prompt': 'Hola, ¿puedes presentarte?',
            'context': '',
            'model_config': 'quantum-xl'
        }).execute()

        if llm_response.error:
            print(f"❌ Error en la inferencia: {llm_response.error.message}")
        else:
            print(f"🧠 Respuesta del LLM: {llm_response.data}")

    except Exception as exc:
        print(f"❌ Error ejecutando prueba de LLM: {exc}")

if __name__ == "__main__":
    test_llm()
