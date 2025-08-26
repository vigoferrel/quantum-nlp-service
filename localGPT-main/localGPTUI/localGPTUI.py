import argparse
import os
import sys
import tempfile
import json
import sqlite3
from pathlib import Path

import requests
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(__name__)
app.secret_key = "LeafmanZSecretKey"

API_HOST = "http://localhost:5110/api"
FALLBACK_MODE = False
SEARCH_COUNT = 0

def init_fallback_db():
    """Inicializa base de datos de fallback si no existe"""
    conn = sqlite3.connect("fallback_documents.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filename TEXT UNIQUE,
            content TEXT,
            chunks TEXT,
            metadata TEXT
        )
    """)
    conn.commit()
    conn.close()

def fallback_search(query):
    """Búsqueda simple en base de datos local"""
    global SEARCH_COUNT
    SEARCH_COUNT += 1
    
    if not Path("fallback_documents.db").exists():
        return {"Prompt": query, "Answer": "No hay documentos. Por favor sube algunos archivos primero.", "Sources": []}
    
    conn = sqlite3.connect("fallback_documents.db")
    cursor = conn.execute(
        "SELECT filename, content, chunks FROM documents WHERE content LIKE ?",
        (f"%{query}%",)
    )
    results = cursor.fetchall()
    conn.close()
    
    if results:
        # Construir respuesta basada en resultados
        answer_parts = []
        sources = []
        
        for filename, content, chunks_json in results[:3]:  # Máximo 3 documentos
            try:
                chunks = json.loads(chunks_json)
                relevant_chunks = [chunk for chunk in chunks if query.lower() in chunk.lower()]
                
                if relevant_chunks:
                    # Tomar los primeros chunks relevantes
                    best_chunk = relevant_chunks[0][:500] + "..."
                    answer_parts.append(f"De {filename}: {best_chunk}")
                    sources.append((filename, best_chunk))
            except:
                # Si hay error al parsear JSON, usar contenido directo
                if query.lower() in content.lower():
                    snippet = content[:500] + "..."
                    answer_parts.append(f"De {filename}: {snippet}")
                    sources.append((filename, snippet))
        
        if answer_parts:
            answer = "\\n\\n".join(answer_parts)
        else:
            answer = "Se encontraron documentos que contienen tu consulta, pero no se pudo extraer información específica relevante."
        
        return {"Prompt": query, "Answer": answer, "Sources": sources}
    else:
        return {"Prompt": query, "Answer": "No se encontró información relevante en los documentos subidos.", "Sources": []}

def fallback_ingest(files):
    """Procesa archivos en modo fallback"""
    init_fallback_db()
    conn = sqlite3.connect("fallback_documents.db")
    
    processed_count = 0
    for file in files:
        try:
            filename = secure_filename(file.filename)
            content = file.read()
            
            # Intentar decodificar como texto
            try:
                if filename.lower().endswith(('.txt', '.md', '.py', '.js', '.html', '.css')):
                    text_content = content.decode('utf-8')
                else:
                    # Para otros archivos, intentar extraer texto básico
                    text_content = content.decode('utf-8', errors='ignore')
            except:
                text_content = str(content)  # Fallback básico
            
            # Crear chunks simples
            chunks = [text_content[i:i+1000] for i in range(0, len(text_content), 800)]
            
            metadata = {
                'size': len(text_content),
                'chunks_count': len(chunks),
                'extension': Path(filename).suffix
            }
            
            conn.execute(
                "INSERT OR REPLACE INTO documents (filename, content, chunks, metadata) VALUES (?, ?, ?, ?)",
                (filename, text_content, json.dumps(chunks), json.dumps(metadata))
            )
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
    
    conn.commit()
    conn.close()
    return processed_count

def get_db_stats():
    """Obtiene estadísticas de la base de datos"""
    if not Path("fallback_documents.db").exists():
        return {"documents": 0, "chunks": 0, "searches": SEARCH_COUNT, "db_size": 0}
    
    try:
        conn = sqlite3.connect("fallback_documents.db")
        
        # Contar documentos
        cursor = conn.execute("SELECT COUNT(*) FROM documents")
        doc_count = cursor.fetchone()[0]
        
        # Contar chunks totales
        cursor = conn.execute("SELECT chunks FROM documents")
        total_chunks = 0
        for row in cursor.fetchall():
            if row[0]:
                try:
                    chunks = json.loads(row[0])
                    total_chunks += len(chunks)
                except:
                    total_chunks += 1  # Si hay error, contar como 1 chunk
        
        conn.close()
        
        # Tamaño del archivo de BD
        db_size = Path("fallback_documents.db").stat().st_size
        
        return {
            "documents": doc_count,
            "chunks": total_chunks,
            "searches": SEARCH_COUNT,
            "db_size": db_size
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {"documents": 0, "chunks": 0, "searches": SEARCH_COUNT, "db_size": 0}

def check_api_connection():
    """Verifica si el API backend está disponible"""
    try:
        response = requests.get(f"{API_HOST}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# API Routes
@app.route('/api/stats')
def api_stats():
    """Endpoint para obtener estadísticas"""
    return jsonify(get_db_stats())

@app.route('/api/clear-db', methods=['POST'])
def api_clear_db():
    """Endpoint para limpiar la base de datos"""
    try:
        if Path("fallback_documents.db").exists():
            os.remove("fallback_documents.db")
        
        global SEARCH_COUNT
        SEARCH_COUNT = 0
        
        return jsonify({"success": True, "message": "Base de datos limpiada exitosamente"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/export-db')
def api_export_db():
    """Endpoint para exportar la base de datos"""
    if Path("fallback_documents.db").exists():
        return send_file("fallback_documents.db", 
                        as_attachment=True, 
                        download_name="localgpt_database.db")
    else:
        return jsonify({"error": "No se encontró base de datos"}), 404

# Static files
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

# PAGES #
@app.route("/", methods=["GET", "POST"])
def home_page():
    global FALLBACK_MODE
    error_message = None
    success_message = None
    
    # Verificar conexión API al inicio
    if not FALLBACK_MODE and not check_api_connection():
        FALLBACK_MODE = True
        error_message = "API backend no disponible. Ejecutando en modo offline con búsqueda básica."
    
    if request.method == "POST":
        if "user_prompt" in request.form:
            user_prompt = request.form["user_prompt"]
            print(f"User Prompt: {user_prompt}")

            if FALLBACK_MODE:
                # Usar búsqueda local
                response_dict = fallback_search(user_prompt)
                return render_template("home.html", 
                                     show_response_modal=True, 
                                     response_dict=response_dict,
                                     error_message="Ejecutando en modo offline",
                                     fallback_mode=True,
                                     **get_db_stats())
            else:
                # Intentar usar API
                try:
                    main_prompt_url = f"{API_HOST}/prompt_route"
                    response = requests.post(main_prompt_url, data={"user_prompt": user_prompt}, timeout=30)
                    print(response.status_code)
                    if response.status_code == 200:
                        return render_template("home.html", 
                                             show_response_modal=True, 
                                             response_dict=response.json(),
                                             **get_db_stats())
                    else:
                        # Fallback a modo local
                        FALLBACK_MODE = True
                        response_dict = fallback_search(user_prompt)
                        return render_template("home.html", 
                                             show_response_modal=True, 
                                             response_dict=response_dict,
                                             error_message="API falló, usando búsqueda offline",
                                             fallback_mode=True,
                                             **get_db_stats())
                except Exception as e:
                    # Fallback a modo local
                    FALLBACK_MODE = True
                    response_dict = fallback_search(user_prompt)
                    return render_template("home.html", 
                                         show_response_modal=True, 
                                         response_dict=response_dict,
                                         error_message=f"Error de API: {str(e)[:100]}. Usando búsqueda offline.",
                                         fallback_mode=True,
                                         **get_db_stats())
                                         
        elif "documents" in request.files:
            files = request.files.getlist("documents")
            
            if not files or all(f.filename == '' for f in files):
                error_message = "No se seleccionaron archivos para subir."
            else:
                if FALLBACK_MODE:
                    # Usar procesamiento local
                    try:
                        processed_count = fallback_ingest(files)
                        success_message = f"Se procesaron exitosamente {processed_count} archivos en modo offline."
                    except Exception as e:
                        error_message = f"Error procesando archivos: {str(e)}"
                else:
                    # Intentar usar API
                    try:
                        if request.form.get("action") == "reset":
                            delete_source_url = f"{API_HOST}/delete_source"
                            response = requests.get(delete_source_url, timeout=10)

                        save_document_url = f"{API_HOST}/save_document"
                        run_ingest_url = f"{API_HOST}/run_ingest"
                        
                        for file in files:
                            filename = secure_filename(file.filename)
                            file.seek(0)  # Reset file pointer
                            with tempfile.SpooledTemporaryFile() as f:
                                f.write(file.read())
                                f.seek(0)
                                response = requests.post(save_document_url, 
                                                        files={"document": (filename, f)}, 
                                                        timeout=30)
                                print(f"Upload response: {response.status_code}")
                        
                        response = requests.get(run_ingest_url, timeout=60)
                        print(f"Ingest response: {response.status_code}")
                        
                        if response.status_code == 200:
                            success_message = f"Se subieron y procesaron exitosamente {len(files)} archivos."
                        else:
                            # Fallback a modo local
                            FALLBACK_MODE = True
                            processed_count = fallback_ingest(files)
                            success_message = f"API falló, se procesaron {processed_count} archivos en modo offline."
                            
                    except Exception as e:
                        # Fallback a modo local
                        FALLBACK_MODE = True
                        try:
                            processed_count = fallback_ingest(files)
                            success_message = f"API falló, se procesaron {processed_count} archivos en modo offline."
                            error_message = f"Error de API: {str(e)[:100]}"
                        except Exception as fallback_error:
                            error_message = f"Tanto API como procesamiento offline fallaron: {str(fallback_error)}"

    # Display the form for GET request
    stats = get_db_stats()
    return render_template(
        "home.html",
        show_response_modal=False,
        response_dict={"Prompt": "None", "Answer": "None", "Sources": []},
        error_message=error_message,
        success_message=success_message,
        fallback_mode=FALLBACK_MODE,
        document_count=stats["documents"],
        total_chunks=stats["chunks"],
        search_count=stats["searches"]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5111, help="Port to run the UI on. Defaults to 5111.")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to run the UI on. Defaults to 127.0.0.1. "
        "Set to 0.0.0.0 to make the UI externally "
        "accessible from other devices.",
    )
    args = parser.parse_args()
    
    # Inicializar la base de datos al inicio
    init_fallback_db()
    
    print("🚀 Iniciando LocalGPT UI en español...")
    print(f"🌐 Accede en: http://{args.host}:{args.port}")
    print("📚 Modo offline disponible automáticamente")
    
    app.run(debug=True, host=args.host, port=args.port)
