#!/usr/bin/env python3
import sys, json
from pathlib import Path

try:
    from constants_adaptive import *
except ImportError:
    print("❌ No se encontró constants_adaptive.py")
    sys.exit(1)

def main():
    print(f"🚀 LocalGPT Ingest - Nivel {FUNCTIONALITY_LEVEL}/4")
    
    if not SOURCE_DIRECTORY.exists():
        SOURCE_DIRECTORY.mkdir()
        print("📁 SOURCE_DOCUMENTS creado - añade archivos")
        return
    
    txt_files = list(SOURCE_DIRECTORY.glob("*.txt"))
    if not txt_files:
        print("⚠️  No hay archivos .txt en SOURCE_DOCUMENTS/")
        return
    
    print(f"📄 Procesando {len(txt_files)} archivos...")
    docs = []
    
    for file in txt_files:
        print(f"  📄 {file.name}")
        try:
            with open(file, 'r', encoding='utf-8') as f:
                docs.append({
                    "content": f.read(),
                    "metadata": {"source": str(file)}
                })
        except Exception as e:
            print(f"  ⚠️  Error: {e}")
    
    with open(PERSIST_DIRECTORY / "documents.json", 'w', encoding='utf-8') as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(docs)} documentos procesados")
    print("Siguiente: python run_adaptive.py")

if __name__ == "__main__":
    main()