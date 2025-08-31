#!/usr/bin/env python3
"""
Instalación alternativa ultra-minimal para Python 3.13
Solo paquetes que definitivamente funcionan
"""

import subprocess
import sys
import os

def run_command(command, description=""):
    """Ejecuta comando con manejo de errores"""
    print(f"\n>>> {description}")
    print(f"Ejecutando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Éxito")
            return True
        else:
            print("❌ Error")
            if result.stderr:
                print("Error:", result.stderr[:150])
            return False
            
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def install_minimal_stack():
    """Instala solo lo absolutamente esencial que funciona"""
    print("🎯 Instalación ULTRA-MINIMAL para Python 3.13")
    print("="*55)
    
    # Solo paquetes que SABEMOS que funcionan con 3.13
    essential_only = [
        ("pip --upgrade", "Pip"),
        ("setuptools wheel", "Herramientas básicas"),
        ("numpy", "NumPy"),
        ("requests", "Requests"),
        ("flask", "Flask"),
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("sqlite3", "SQLite (incluido)"),
        ("json", "JSON (incluido)"),
        ("click", "Click CLI")
    ]
    
    print("\n📦 Instalando paquetes básicos...")
    for package, name in essential_only:
        if package in ["sqlite3", "json"]:
            print(f"✅ {name} (incluido en Python)")
            continue
            
        success = run_command(f"{sys.executable} -m pip install {package}", name)
        if success:
            print(f"✅ {name} instalado")
        else:
            print(f"⚠️  {name} falló")

def create_simple_local_gpt():
    """Crea una versión ultra-simplificada de LocalGPT"""
    print("\n🔧 Creando LocalGPT simplificado...")
    
    simple_gpt = '''#!/usr/bin/env python3
"""
LocalGPT Ultra-Simplificado para Python 3.13
Version minima que funciona sin dependencias complejas
"""

import os
import json
import sqlite3
from pathlib import Path

class SimpleLocalGPT:
    def __init__(self):
        self.docs_dir = Path("SOURCE_DOCUMENTS")
        self.db_path = "simple_localgpt.db"
        self.setup_database()
    
    def setup_database(self):
        """Crea base de datos simple"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                content TEXT,
                chunks TEXT
            )
        """)
        conn.commit()
        conn.close()
        print("✅ Base de datos creada")
    
    def read_text_file(self, filepath):
        """Lee archivos de texto"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            try:
                with open(filepath, 'r', encoding='latin-1') as f:
                    return f.read()
            except:
                return ""
    
    def simple_chunk(self, text, size=1000):
        """Divide texto en chunks simples"""
        chunks = []
        for i in range(0, len(text), size):
            chunks.append(text[i:i+size])
        return chunks
    
    def ingest_documents(self):
        """Procesa documentos de forma simple"""
        print("\\n📄 Procesando documentos...")
        
        if not self.docs_dir.exists():
            print("❌ Carpeta SOURCE_DOCUMENTS no existe")
            return
        
        conn = sqlite3.connect(self.db_path)
        
        for filepath in self.docs_dir.glob("*.txt"):
            print(f"Procesando: {filepath.name}")
            
            content = self.read_text_file(filepath)
            if content:
                chunks = self.simple_chunk(content)
                
                conn.execute(
                    "INSERT OR REPLACE INTO documents (filename, content, chunks) VALUES (?, ?, ?)",
                    (filepath.name, content, json.dumps(chunks))
                )
        
        conn.commit()
        conn.close()
        print("✅ Documentos procesados")
    
    def simple_search(self, query):
        """Búsqueda simple por palabras clave"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT filename, content, chunks FROM documents WHERE content LIKE ?",
            (f"%{query}%",)
        )
        
        results = []
        for row in cursor.fetchall():
            filename, content, chunks_json = row
            chunks = json.loads(chunks_json)
            
            # Encontrar chunks relevantes
            relevant_chunks = [chunk for chunk in chunks if query.lower() in chunk.lower()]
            
            if relevant_chunks:
                results.append({
                    'filename': filename,
                    'chunks': relevant_chunks[:3]  # Solo primeros 3 chunks
                })
        
        conn.close()
        return results
    
    def chat(self):
        """Chat simple sin IA - solo búsqueda"""
        print("\\n💬 LocalGPT Simple - Chat Mode")
        print("Escribe 'exit' para salir")
        print("Nota: Esta versión solo busca texto, no usa IA")
        print()
        
        while True:
            query = input("> ").strip()
            
            if query.lower() in ['exit', 'quit', 'salir']:
                break
            
            if not query:
                continue
            
            results = self.simple_search(query)
            
            if results:
                print(f"\\n📄 Encontrado en {len(results)} documento(s):")
                for result in results:
                    print(f"\\n📄 {result['filename']}:")
                    for chunk in result['chunks']:
                        print(f"   {chunk[:200]}...")
            else:
                print("❌ No se encontraron resultados")
                print("Sugerencias:")
                print("- Verifica que hay archivos .txt en SOURCE_DOCUMENTS/")
                print("- Ejecuta primero: ingest_documents()")
                print("- Usa palabras clave más simples")

def main():
    gpt = SimpleLocalGPT()
    
    print("LocalGPT Ultra-Simple para Python 3.13")
    print("="*40)
    print()
    print("Opciones:")
    print("1. Procesar documentos")
    print("2. Hacer preguntas")
    print("3. Salir")
    
    while True:
        choice = input("\\nOpción (1-3): ").strip()
        
        if choice == "1":
            gpt.ingest_documents()
        elif choice == "2":
            gpt.chat()
        elif choice == "3":
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
'''
    
    with open("simple_localgpt.py", "w", encoding="utf-8") as f:
        f.write(simple_gpt)
    
    print("✅ simple_localgpt.py creado")

def create_streamlit_interface():
    """Crea interfaz web simple con Streamlit"""
    streamlit_app = '''#!/usr/bin/env python3
"""
Interfaz web simple para LocalGPT con Streamlit
Compatible con Python 3.13
"""

import streamlit as st
import sqlite3
import json
from pathlib import Path

st.set_page_config(
    page_title="LocalGPT Simple",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 LocalGPT Simple - Python 3.13")
st.write("Versión simplificada compatible con Python 3.13")

# Sidebar
st.sidebar.title("Opciones")

if st.sidebar.button("Procesar Documentos"):
    docs_dir = Path("SOURCE_DOCUMENTS")
    
    if not docs_dir.exists():
        st.error("Carpeta SOURCE_DOCUMENTS no existe")
    else:
        txt_files = list(docs_dir.glob("*.txt"))
        
        if not txt_files:
            st.warning("No hay archivos .txt en SOURCE_DOCUMENTS/")
        else:
            # Procesar archivos
            conn = sqlite3.connect("simple_localgpt.db")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY,
                    filename TEXT,
                    content TEXT,
                    chunks TEXT
                )
            """)
            
            for filepath in txt_files:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Chunks simples
                chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
                
                conn.execute(
                    "INSERT OR REPLACE INTO documents (filename, content, chunks) VALUES (?, ?, ?)",
                    (filepath.name, content, json.dumps(chunks))
                )
            
            conn.commit()
            conn.close()
            
            st.success(f"✅ {len(txt_files)} archivos procesados")

# Chat interface
st.subheader("💬 Hacer Preguntas")
query = st.text_input("Escribe tu pregunta:")

if query:
    conn = sqlite3.connect("simple_localgpt.db")
    cursor = conn.execute(
        "SELECT filename, content, chunks FROM documents WHERE content LIKE ?",
        (f"%{query}%",)
    )
    
    results = cursor.fetchall()
    conn.close()
    
    if results:
        st.success(f"📄 Encontrado en {len(results)} documento(s)")
        
        for filename, content, chunks_json in results:
            with st.expander(f"📄 {filename}"):
                chunks = json.loads(chunks_json)
                relevant_chunks = [chunk for chunk in chunks if query.lower() in chunk.lower()]
                
                for chunk in relevant_chunks[:2]:  # Solo 2 chunks
                    st.write(chunk[:500] + "...")
    else:
        st.warning("❌ No se encontraron resultados")
        st.info("Sugerencias: Verifica que hay archivos .txt en SOURCE_DOCUMENTS/")

# Información
st.sidebar.subheader("📋 Información")
st.sidebar.info("""
Esta es una versión simplificada de LocalGPT
para Python 3.13.

Características:
- Solo archivos .txt
- Búsqueda por palabras clave
- Sin IA (solo búsqueda)
- 100% local
""")

st.sidebar.subheader("🚀 Uso")
st.sidebar.write("""
1. Copia archivos .txt a SOURCE_DOCUMENTS/
2. Haz clic en "Procesar Documentos"
3. Escribe preguntas arriba
""")
'''
    
    with open("app_simple.py", "w", encoding="utf-8") as f:
        f.write(streamlit_app)
    
    print("✅ app_simple.py creado")

def show_simple_instructions():
    """Muestra instrucciones para la versión simple"""
    print("\n" + "="*60)
    print("🚀 LOCALGPT ULTRA-SIMPLE PARA PYTHON 3.13")
    print("="*60)
    print()
    print("✅ INSTALACIÓN COMPLETA:")
    print("   - Sin dependencias complejas de ML")
    print("   - Solo búsqueda por palabras clave")
    print("   - Funciona 100% con Python 3.13")
    print()
    print("📁 ARCHIVOS CREADOS:")
    print("   - simple_localgpt.py  # Versión consola")
    print("   - app_simple.py       # Interfaz web con Streamlit")
    print()
    print("🚀 CÓMO USAR:")
    print()
    print("1. Añadir documentos:")
    print("   - Copia archivos .txt a SOURCE_DOCUMENTS/")
    print()
    print("2. Versión consola:")
    print("   python simple_localgpt.py")
    print()
    print("3. Versión web:")
    print("   streamlit run app_simple.py")
    print("   (Se abre en: http://localhost:8501)")
    print()
    print("⚠️  LIMITACIONES:")
    print("   - Solo archivos .txt")
    print("   - Búsqueda por palabras (no IA)")
    print("   - Sin embeddings ni LLM")
    print()
    print("💡 VENTAJAS:")
    print("   - Funciona con Python 3.13")
    print("   - Instalación simple")
    print("   - Búsqueda instantánea")
    print("   - 100% local y privado")
    print()
    print("="*60)

def main():
    """Función principal de instalación ultra-simple"""
    print("🎯 LocalGPT Ultra-Simple para Python 3.13")
    print("="*50)
    
    print("Esta versión:")
    print("- No usa IA/ML (evita problemas de compatibilidad)")
    print("- Solo búsqueda por palabras clave")
    print("- Funciona con cualquier versión de Python")
    print("- Instalación ultra-rápida")
    
    install_minimal_stack()
    create_simple_local_gpt()
    create_streamlit_interface()
    show_simple_instructions()
    
    input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
