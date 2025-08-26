import argparse
import os
import sys
import tempfile
import json
import sqlite3
from pathlib import Path
import logging
from datetime import datetime

import requests
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(__name__)
app.secret_key = "LeafmanZSecretKey"

# Configuración
API_HOST = "http://localhost:5110/api"
FALLBACK_MODE = False
SEARCH_COUNT = 0
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'md', 'py', 'js', 'html', 'css', 'json', 'xml'}

# Crear carpetas necesarias
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(app.root_path, 'static', 'css'), exist_ok=True)
os.makedirs(os.path.join(app.root_path, 'static', 'js'), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_fallback_db():
    """Inicializa base de datos de fallback si no existe"""
    try:
        conn = sqlite3.connect("fallback_documents.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                filename TEXT UNIQUE,
                content TEXT,
                chunks TEXT,
                metadata TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error inicializando base de datos: {e}")

def fallback_search(query):
    """Búsqueda simple en base de datos local"""
    global SEARCH_COUNT
    SEARCH_COUNT += 1
    
    logger.info(f"Búsqueda local: {query}")
    
    if not Path("fallback_documents.db").exists():
        return {
            "Prompt": query, 
            "Answer": "No hay documentos disponibles. Por favor sube algunos archivos primero para poder realizar búsquedas.", 
            "Sources": []
        }
    
    try:
        conn = sqlite3.connect("fallback_documents.db")
        
        # Búsqueda más inteligente
        search_terms = query.lower().split()
        conditions = []
        params = []
        
        for term in search_terms[:5]:  # Máximo 5 términos
            conditions.append("content LIKE ?")
            params.append(f"%{term}%")
        
        if conditions:
            where_clause = " AND ".join(conditions)
            sql = f"SELECT filename, content, chunks, metadata FROM documents WHERE {where_clause} LIMIT 5"
        else:
            sql = "SELECT filename, content, chunks, metadata FROM documents LIMIT 5"
            params = []
        
        cursor = conn.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
        
        if results:
            answer_parts = []
            sources = []
            
            for filename, content, chunks_json, metadata in results:
                try:
                    if chunks_json:
                        chunks = json.loads(chunks_json)
                        # Buscar chunks más relevantes
                        relevant_chunks = []
                        for chunk in chunks:
                            relevance_score = sum(1 for term in search_terms if term in chunk.lower())
                            if relevance_score > 0:
                                relevant_chunks.append((chunk, relevance_score))
                        
                        # Ordenar por relevancia
                        relevant_chunks.sort(key=lambda x: x[1], reverse=True)
                        
                        if relevant_chunks:
                            best_chunk = relevant_chunks[0][0]
                            # Truncar si es muy largo
                            if len(best_chunk) > 400:
                                best_chunk = best_chunk[:400] + "..."
                            
                            answer_parts.append(f"**De {filename}:**\n{best_chunk}")
                            sources.append((filename, best_chunk))
                    else:
                        # Fallback a contenido directo
                        snippet = content[:400] + "..." if len(content) > 400 else content
                        answer_parts.append(f"**De {filename}:**\n{snippet}")
                        sources.append((filename, snippet))
                        
                except Exception as e:
                    logger.error(f"Error procesando documento {filename}: {e}")
                    continue
            
            if answer_parts:
                answer = "\n\n".join(answer_parts)
            else:
                answer = "Se encontraron documentos que podrían contener información relevante, pero no se pudo extraer contenido específico."
            
            return {"Prompt": query, "Answer": answer, "Sources": sources}
        else:
            return {
                "Prompt": query, 
                "Answer": "No se encontró información relevante en los documentos disponibles. Intenta con términos de búsqueda diferentes o sube más documentos.", 
                "Sources": []
            }
            
    except Exception as e:
        logger.error(f"Error en búsqueda fallback: {e}")
        return {
            "Prompt": query, 
            "Answer": f"Error durante la búsqueda: {str(e)}", 
            "Sources": []
        }

def fallback_ingest(files):
    """Procesa archivos en modo fallback"""
    init_fallback_db()
    processed_count = 0
    errors = []
    
    try:
        conn = sqlite3.connect("fallback_documents.db")
        
        for file in files:
            try:
                if not allowed_file(file.filename):
                    errors.append(f"Tipo de archivo no soportado: {file.filename}")
                    continue
                
                filename = secure_filename(file.filename)
                content = file.read()
                
                # Intentar decodificar como texto
                try:
                    if filename.lower().endswith(('.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml')):
                        text_content = content.decode('utf-8')
                    elif filename.lower().endswith('.pdf'):
                        # Para PDFs, intentar extracción básica
                        text_content = content.decode('utf-8', errors='ignore')
                        text_content = f"[Contenido PDF de {filename}]\n" + text_content
                    else:
                        text_content = content.decode('utf-8', errors='ignore')
                except Exception as decode_error:
                    logger.warning(f"Error decodificando {filename}: {decode_error}")
                    text_content = f"[Archivo binario: {filename}]"
                
                # Crear chunks inteligentes (por párrafos y luego por tamaño)
                chunks = []
                paragraphs = text_content.split('\n\n')
                
                current_chunk = ""
                for paragraph in paragraphs:
                    if len(current_chunk) + len(paragraph) < 800:
                        current_chunk += paragraph + "\n\n"
                    else:
                        if current_chunk.strip():
                            chunks.append(current_chunk.strip())
                        current_chunk = paragraph + "\n\n"
                
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                # Si no hay chunks, crear por tamaño fijo
                if not chunks:
                    chunks = [text_content[i:i+1000] for i in range(0, len(text_content), 800)]
                
                metadata = {
                    'size': len(text_content),
                    'chunks_count': len(chunks),
                    'extension': Path(filename).suffix,
                    'upload_date': datetime.now().isoformat()
                }
                
                conn.execute(
                    "INSERT OR REPLACE INTO documents (filename, content, chunks, metadata) VALUES (?, ?, ?, ?)",
                    (filename, text_content, json.dumps(chunks), json.dumps(metadata))
                )
                processed_count += 1
                logger.info(f"Procesado archivo: {filename}")
                
            except Exception as e:
                error_msg = f"Error procesando {file.filename}: {str(e)}"
                errors.append(error_msg)
                logger.error(error_msg)
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error general en procesamiento: {e}")
        errors.append(f"Error general: {str(e)}")
    
    return processed_count, errors

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
                    total_chunks += 1
        
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
        logger.error(f"Error obteniendo estadísticas: {e}")
        return {"documents": 0, "chunks": 0, "searches": SEARCH_COUNT, "db_size": 0}

def check_api_connection():
    """Verifica si el API backend está disponible"""
    try:
        response = requests.get(f"{API_HOST}/health", timeout=3)
        return response.status_code == 200
    except:
        return False

# Rutas para archivos estáticos faltantes
@app.route('/favicon.ico')
def favicon():
    """Servir favicon"""
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir archivos estáticos con manejo de errores"""
    try:
        return send_from_directory(
            os.path.join(app.root_path, 'static'), 
            filename
        )
    except FileNotFoundError:
        logger.warning(f"Archivo estático no encontrado: {filename}")
        return "", 404

# API Routes mejoradas
@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok", 
        "mode": "fallback" if FALLBACK_MODE else "api",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/stats')
def api_stats():
    """Endpoint para obtener estadísticas"""
    stats = get_db_stats()
    stats["fallback_mode"] = FALLBACK_MODE
    return jsonify(stats)

@app.route('/api/clear-db', methods=['POST'])
def api_clear_db():
    """Endpoint para limpiar la base de datos"""
    try:
        if Path("fallback_documents.db").exists():
            os.remove("fallback_documents.db")
        
        global SEARCH_COUNT
        SEARCH_COUNT = 0
        
        logger.info("Base de datos limpiada")
        return jsonify({"success": True, "message": "Base de datos limpiada exitosamente"})
    except Exception as e:
        logger.error(f"Error limpiando base de datos: {e}")
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/export-db')
def api_export_db():
    """Endpoint para exportar la base de datos"""
    if Path("fallback_documents.db").exists():
        return send_file(
            "fallback_documents.db", 
            as_attachment=True, 
            download_name=f"localgpt_database_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        )
    else:
        return jsonify({"error": "No se encontró base de datos"}), 404

# Ruta principal mejorada
@app.route("/", methods=["GET", "POST"])
def home_page():
    global FALLBACK_MODE
    error_message = None
    success_message = None
    
    # Verificar conexión API al inicio
    if not FALLBACK_MODE and not check_api_connection():
        FALLBACK_MODE = True
        error_message = "API backend no disponible. Ejecutando en modo offline con búsqueda básica."
        logger.warning("Cambiando a modo fallback")
    
    if request.method == "POST":
        if "user_prompt" in request.form:
            user_prompt = request.form["user_prompt"].strip()
            
            if not user_prompt:
                error_message = "Por favor ingresa una consulta válida."
            else:
                logger.info(f"Consulta del usuario: {user_prompt}")

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
                        response = requests.post(
                            main_prompt_url, 
                            data={"user_prompt": user_prompt}, 
                            timeout=30
                        )
                        
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
                valid_files = [f for f in files if f.filename != '' and allowed_file(f.filename)]
                
                if not valid_files:
                    error_message = "No se encontraron archivos válidos. Tipos soportados: " + ", ".join(ALLOWED_EXTENSIONS)
                else:
                    if FALLBACK_MODE:
                        # Usar procesamiento local
                        try:
                            processed_count, errors = fallback_ingest(valid_files)
                            if processed_count > 0:
                                success_message = f"Se procesaron exitosamente {processed_count} archivos en modo offline."
                                if errors:
                                    success_message += f" Errores: {len(errors)}"
                            else:
                                error_message = "No se pudieron procesar los archivos: " + "; ".join(errors[:3])
                        except Exception as e:
                            error_message = f"Error procesando archivos: {str(e)}"
                    else:
                        # Intentar usar API
                        try:
                            if request.form.get("action") == "reset":
                                delete_source_url = f"{API_HOST}/delete_source"
                                requests.get(delete_source_url, timeout=10)

                            save_document_url = f"{API_HOST}/save_document"
                            run_ingest_url = f"{API_HOST}/run_ingest"
                            
                            for file in valid_files:
                                filename = secure_filename(file.filename)
                                file.seek(0)
                                with tempfile.SpooledTemporaryFile() as f:
                                    f.write(file.read())
                                    f.seek(0)
                                    response = requests.post(
                                        save_document_url, 
                                        files={"document": (filename, f)}, 
                                        timeout=30
                                    )
                            
                            response = requests.get(run_ingest_url, timeout=60)
                            
                            if response.status_code == 200:
                                success_message = f"Se subieron y procesaron exitosamente {len(valid_files)} archivos."
                            else:
                                # Fallback a modo local
                                FALLBACK_MODE = True
                                processed_count, errors = fallback_ingest(valid_files)
                                success_message = f"API falló, se procesaron {processed_count} archivos en modo offline."
                                
                        except Exception as e:
                            # Fallback a modo local
                            FALLBACK_MODE = True
                            try:
                                processed_count, errors = fallback_ingest(valid_files)
                                success_message = f"API falló, se procesaron {processed_count} archivos en modo offline."
                                if errors:
                                    error_message = f"Algunos errores: {'; '.join(errors[:2])}"
                            except Exception as fallback_error:
                                error_message = f"Error completo: {str(fallback_error)}"

    # Mostrar página principal
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

@app.errorhandler(404)
def not_found_error(error):
    """Manejo de errores 404"""
    logger.warning(f"404 Error: {request.url}")
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores 500"""
    logger.error(f"500 Error: {error}")
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5111, help="Puerto para ejecutar la UI. Por defecto 5111.")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host para ejecutar la UI. Por defecto 127.0.0.1. "
        "Usar 0.0.0.0 para acceso externo desde otros dispositivos.",
    )
    parser.add_argument("--debug", action="store_true", help="Ejecutar en modo debug")
    args = parser.parse_args()
    
    # Inicializar la base de datos al inicio
    init_fallback_db()
    
    print("🚀 Iniciando LocalGPT UI Mejorado...")
    print(f"🌐 Accede en: http://{args.host}:{args.port}")
    print("📚 Modo offline disponible automáticamente")
    print("🔧 Errores corregidos y funcionalidad mejorada")
    
    app.run(debug=args.debug, host=args.host, port=args.port)
