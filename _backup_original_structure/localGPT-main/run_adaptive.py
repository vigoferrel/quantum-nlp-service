#!/usr/bin/env python3
"""
Run adaptativo - se ajusta a los paquetes disponibles
Generado automáticamente por instalador definitivo
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

# Configuración automática
HAS_ML = True
HAS_STREAMLIT = True

def simple_chat():
    """Chat simple con búsqueda en base de datos"""
    print("💬 LocalGPT Simple - Modo Chat")
    print("Escribe 'exit' para salir")
    print("Nota: Búsqueda por palabras clave (sin IA)")
    print()
    
    if not Path("documents.db").exists():
        print("❌ Base de datos no encontrada")
        print("Ejecuta primero: python ingest_adaptive.py")
        return
    
    conn = sqlite3.connect("documents.db")
    
    while True:
        query = input("> ").strip()
        
        if query.lower() in ['exit', 'quit', 'salir']:
            break
        
        if not query:
            continue
        
        # Búsqueda simple
        cursor = conn.execute(
            "SELECT filename, content, chunks FROM documents WHERE content LIKE ?",
            (f"%{query}%",)
        )
        
        results = cursor.fetchall()
        
        if results:
            print(f"\n📄 Encontrado en {len(results)} documento(s):")
            for filename, content, chunks_json in results[:3]:  # Solo 3 resultados
                print(f"\n📄 {filename}:")
                chunks = json.loads(chunks_json)
                relevant_chunks = [chunk for chunk in chunks if query.lower() in chunk.lower()]
                
                for chunk in relevant_chunks[:2]:  # Solo 2 chunks por archivo
                    print(f"   {chunk[:300]}...")
        else:
            print("❌ No se encontraron resultados")
    
    conn.close()

def web_interface():
    """Interfaz web con Streamlit si está disponible"""
    if not HAS_STREAMLIT:
        print("❌ Streamlit no disponible")
        print("Ejecuta: pip install streamlit")
        return
    
    print("🌐 Iniciando interfaz web...")
    print("Se abrirá en: http://localhost:8501")
    
    # Crear app temporal de Streamlit
    app_content = """
import streamlit as st
import sqlite3
import json
from pathlib import Path

st.title("🤖 LocalGPT Simple")

query = st.text_input("Haz tu pregunta:")

if query:
    if Path("documents.db").exists():
        conn = sqlite3.connect("documents.db")
        cursor = conn.execute(
            "SELECT filename, content FROM documents WHERE content LIKE ?",
            (f"%{query}%",)
        )
        results = cursor.fetchall()
        conn.close()
        
        if results:
            for filename, content in results:
                with st.expander(f"📄 {filename}"):
                    st.write(content[:500] + "...")
        else:
            st.warning("No se encontraron resultados")
    else:
        st.error("Base de datos no encontrada. Ejecuta ingest_adaptive.py primero")
"""
    
    with open("streamlit_app.py", "w", encoding="utf-8") as f:
        f.write(app_content)
    
    os.system("streamlit run streamlit_app.py")

def main():
    print("🚀 LocalGPT - Run Adaptativo")
    print("=" * 35)
    print()
    print("Opciones:")
    print("1. Chat en consola")
    print("2. Interfaz web (Streamlit)")
    print("3. Salir")
    
    while True:
        choice = input("\nOpción (1-3): ").strip()
        
        if choice == "1":
            simple_chat()
        elif choice == "2":
            web_interface()
        elif choice == "3":
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
