#!/usr/bin/env python3
"""
Ingest adaptativo - se ajusta a los paquetes disponibles
Generado automáticamente por instalador definitivo
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

# Configuración automática
HAS_ML = True
HAS_LANGCHAIN = True
HAS_CHROMADB = True

def simple_ingest():
    """Ingesta simple sin ML - solo indexación"""
    print("🗃️  Modo Simple: Indexando documentos sin ML...")
    
    docs_dir = Path("SOURCE_DOCUMENTS")
    if not docs_dir.exists():
        docs_dir.mkdir()
        print("📁 Creada carpeta SOURCE_DOCUMENTS")
    
    # Base de datos simple
    conn = sqlite3.connect("documents.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filename TEXT UNIQUE,
            content TEXT,
            chunks TEXT,
            metadata TEXT
        )
    """)
    
    files_processed = 0
    for filepath in docs_dir.glob("*"):
        if filepath.suffix.lower() in ['.txt', '.md', '.py', '.js', '.html', '.css']:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Chunks simples de 1000 caracteres
                chunks = [content[i:i+1000] for i in range(0, len(content), 800)]
                
                metadata = {
                    'size': len(content),
                    'chunks_count': len(chunks),
                    'extension': filepath.suffix
                }
                
                conn.execute(
                    "INSERT OR REPLACE INTO documents (filename, content, chunks, metadata) VALUES (?, ?, ?, ?)",
                    (filepath.name, content, json.dumps(chunks), json.dumps(metadata))
                )
                
                files_processed += 1
                print(f"✅ {filepath.name} ({len(chunks)} chunks)")
                
            except Exception as e:
                print(f"❌ Error con {filepath.name}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Procesados {files_processed} archivos")
    print("✅ Base de datos creada: documents.db")

def ml_ingest():
    """Ingesta con ML si está disponible"""
    print("🤖 Modo ML: Usando embeddings y vectorización...")
    
    try:
        if HAS_LANGCHAIN and HAS_CHROMADB:
            print("Usando Langchain + ChromaDB")
            # Aquí iría el código de ML real
            print("⚠️  Implementación de ML pendiente")
        else:
            print("ML parcial disponible, usando modo híbrido")
            simple_ingest()
    except Exception as e:
        print(f"❌ Error en ML, fallback a modo simple: {e}")
        simple_ingest()

def main():
    print("🗃️  LocalGPT - Ingest Adaptativo")
    print("=" * 40)
    
    if HAS_ML:
        print("🤖 ML disponible - intentando modo avanzado")
        ml_ingest()
    else:
        print("📊 Solo modo simple disponible")
        simple_ingest()

if __name__ == "__main__":
    main()
