#!/usr/bin/env python3
import sys, json
from pathlib import Path

try:
    from constants_adaptive import *
except ImportError:
    print("❌ No se encontró constants_adaptive.py")
    sys.exit(1)

def main():
    print(f"🚀 LocalGPT - Nivel {FUNCTIONALITY_LEVEL}/4")
    print("💬 Chat Simple - Escribe 'exit' para salir")
    
    docs_file = PERSIST_DIRECTORY / "documents.json"
    if not docs_file.exists():
        print("❌ No hay documentos procesados")
        print("Ejecuta: python ingest_adaptive.py")
        return
    
    try:
        with open(docs_file, 'r', encoding='utf-8') as f:
            documents = json.load(f)
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print(f"📄 {len(documents)} documentos cargados")
    
    while True:
        try:
            query = input("> ").strip()
        except KeyboardInterrupt:
            break
        
        if query.lower() in ['exit', 'quit', 'salir']:
            break
        
        if not query:
            continue
        
        results = [d for d in documents if query.lower() in d['content'].lower()]
        
        if results:
            print(f"📄 Encontrado en {len(results)} documento(s):")
            for doc in results[:2]:
                source = Path(doc['metadata']['source']).name
                preview = doc['content'][:300]
                if len(doc['content']) > 300:
                    preview += "..."
                print(f"📄 {source}:")
                print(f"   {preview}")
        else:
            print("❌ No encontrado")
    
    print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()