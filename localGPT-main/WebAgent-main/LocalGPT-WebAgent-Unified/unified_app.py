#!/usr/bin/env python3
"""
LocalGPT-WebAgent Unified System
Sistema integrado que combina las capacidades de LocalGPT con WebAgent
Desarrollado por QBTC-VIGOLEONROCKS-UNIFIED
"""

import argparse
import os
import sys
import tempfile
import json
import sqlite3
from pathlib import Path
import asyncio
import re
import base64
from datetime import datetime

# Web and AI imports
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
from PIL import Image

# LangChain and Conversational AI imports
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Extend path for WebAgent components
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "WebWalker", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "WebDancer", "demos"))

# WebWalker imports
from agent import WebWalker
from qwen_agent.tools.base import BaseTool, register_tool
from utils import get_info, process_url

# Flask app configuration
app = Flask(__name__)
app.secret_key = "QBTC-VIGOLEONROCKS-LocalGPT-WebAgent-Key"

# Global configuration
API_HOST = "http://localhost:5110/api"
FALLBACK_MODE = False
SEARCH_COUNT = 0
WEB_AGENT_MODE = False

# Database and paths
DATABASE_PATH = "unified_documents.db"
CHROMA_DB_PATH = "unified_chroma_db"
IMAGES_PATH = "static/images"
SCREENSHOTS_PATH = "static/screenshots"

# Conversational AI components
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")
llm_model = Ollama(model="llama2")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

class UnifiedSystem:
    """Sistema unificado que combina LocalGPT y WebAgent"""

    def __init__(self):
        self.init_directories()
        self.init_database()

    def init_directories(self):
        """Inicializa directorios necesarios"""
        for path in [IMAGES_PATH, SCREENSHOTS_PATH, "SOURCE_DOCUMENTS"]:
            if not os.path.exists(path):
                os.makedirs(path)

    def init_database(self):
        """Inicializa base de datos unificada"""
        conn = sqlite3.connect(DATABASE_PATH)
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

        conn.execute("""
            CREATE TABLE IF NOT EXISTS web_sessions (
                id INTEGER PRIMARY KEY,
                session_id TEXT,
                query TEXT,
                website TEXT,
                steps TEXT,
                result TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY,
                query TEXT,
                result_type TEXT,
                result_content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

# Initialize unified system
unified_system = UnifiedSystem()

def fallback_search(query):
    """Búsqueda conversacional avanzada usando RAG"""
    global SEARCH_COUNT
    SEARCH_COUNT += 1
    log_search(query, "conversational_search")

    if not os.path.exists(CHROMA_DB_PATH):
        return {
            "Prompt": query,
            "Answer": "La base de datos de vectores no existe. Por favor, sube documentos para crearla.",
            "Sources": [],
            "Type": "conversational_search_error",
            "Count": 0
        }

    try:
        # Cargar la base de datos de vectores
        vectorstore = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings_model)

        # Crear el retriever
        retriever = vectorstore.as_retriever()

        # Crear la cadena de recuperación conversacional
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm_model,
            retriever=retriever,
            memory=memory
        )

        # Obtener la respuesta
        result = qa_chain({"question": query})
        answer = result["answer"]

        # Extraer fuentes de los documentos recuperados
        sources = []
        if result.get("source_documents"):
            for doc in result["source_documents"]:
                sources.append( (doc.metadata.get("filename", "N/A"), doc.page_content[:200] + "...", doc.metadata.get("extension", "unknown")) )

        return {
            "Prompt": query,
            "Answer": answer,
            "Sources": sources,
            "Type": "conversational_search",
            "Count": len(sources)
        }
    except Exception as e:
        print(f"Error durante la búsqueda conversacional: {e}")
        return {
            "Prompt": query,
            "Answer": f"Error al procesar la búsqueda conversacional: {e}",
            "Sources": [],
            "Type": "conversational_search_error",
            "Count": 0
        }

# Headless version of the WebWalker tool
BUTTON_URL_ADIC = {}
ROOT_URL = ""

def extract_links_with_text_headless(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    # Simplified extraction logic from WebWalker's app.py
    for a_tag in soup.find_all('a', href=True):
        url = a_tag['href']
        text = ''.join(a_tag.stripped_strings)
        if text and "javascript" not in url and not url.endswith(('.jpg', '.png', '.gif', '.jpeg', '.pdf')):
            processed = process_url(ROOT_URL, url)
            if processed.startswith(ROOT_URL):
                links.append({'url': processed, 'text': text})
    unique_links = {f"{item['url']}_{item['text']}": item for item in links}
    info = ""
    for i in list(unique_links.values()):
        BUTTON_URL_ADIC[i["text"]] = i["url"]
        info += "<button>" + i["text"] + "<button>" + "\n"
    return info

@register_tool('visit_page', allow_overwrite=True)
class VisitPageHeadless(BaseTool):
    description = 'A tool that analyzes the content of a webpage and extracts clickable buttons.'
    parameters = [{'name': 'button', 'type': 'string', 'description': 'the button you want to click', 'required': True}]

    def call(self, params: str, **kwargs) -> str:
        global BUTTON_URL_ADIC, ROOT_URL
        try:
            # Simplified param parsing
            button_text = params.split('"button": "')[-1].split('"')[0]
            if button_text in BUTTON_URL_ADIC:
                url = BUTTON_URL_ADIC[button_text]
                html, markdown, screenshot = asyncio.run(get_info(url))
                response_buttons = extract_links_with_text_headless(html)
                response = f"The web information is:\n\n{markdown}\n\nClickable buttons are: {response_buttons}"
                return response
            else:
                return "The button can not be clicked, please retry a new button!"
        except Exception as e:
            return f"Error visiting page: {e}"

def web_agent_search(query, website=None):
    """Búsqueda web REAL usando WebWalker"""
    global SEARCH_COUNT, ROOT_URL, BUTTON_URL_ADIC
    SEARCH_COUNT += 1
    log_search(query, "web_agent_search")

    if not website:
        website = "https://www.google.com"
    ROOT_URL = website
    BUTTON_URL_ADIC = {}

    try:
        # Configure LLM for WebWalker - pointing to our local Ollama
        llm_cfg = {
            'model': "llama2",
            'api_key': "ollama",
            'model_server': "http://localhost:11434/v1",
            'query': query,
            'action_count': 5  # Limit rounds for now
        }

        # Instantiate the agent
        bot = WebWalker(llm=llm_cfg, function_list=["visit_page"])

        # Initial page visit and prompt creation
        html, markdown, screenshot = asyncio.run(get_info(website))
        buttons = extract_links_with_text_headless(html)
        observation = f"website information:\n\n{markdown}\n\nclickable button:\n\n{buttons}\n\nEach button is wrapped in a <button> tag"
        start_prompt = f"query:\n{query} \nofficial website:\n{website}\nObservation:{observation}\n\n"
        messages = [{'role': 'user', 'content': start_prompt}]

        # Run the agent
        response_iterator = bot.run(messages=messages)
        full_response = ""
        sources = [(website, markdown[:200] + "...", "web")]

        for chunk in response_iterator:
            content = chunk[0]["content"]
            full_response += content + "\n---\n"
            if "Final Answer:" in content:
                final_answer = content.split("Final Answer:")[-1].strip()
                break
        else:
            final_answer = "El agente ha terminado su exploración sin una respuesta final explícita. Aquí están sus pensamientos:\n" + full_response

        return {
            "Prompt": query,
            "Answer": final_answer,
            "Sources": sources,
            "Type": "web_search",
            "Count": 1
        }

    except Exception as e:
        return {
            "Prompt": query,
            "Answer": f"Error en la ejecución de WebAgent: {str(e)}",
            "Sources": [],
            "Type": "web_search_error",
            "Count": 0
        }

def hybrid_search(query, website=None):
    """Búsqueda híbrida que combina documentos locales y web"""
    # First try local documents
    doc_result = fallback_search(query)

    # If local search has poor results, try web search
    if doc_result["Count"] == 0 and website:
        web_result = web_agent_search(query, website)

        return {
            "Prompt": query,
            "Answer": f"📚 **Búsqueda Local**: {doc_result['Answer']}\\n\\n🌐 **Búsqueda Web**: {web_result['Answer']}",
            "Sources": doc_result["Sources"] + web_result["Sources"],
            "Type": "hybrid_search"
        }

    return doc_result

def fallback_ingest(files):
    """Procesa y vectoriza archivos en ChromaDB"""
    conn = sqlite3.connect(DATABASE_PATH)
    processed_count = 0
    all_chunks = []
    all_metadatas = []

    for file in files:
        try:
            filename = secure_filename(file.filename)
            content_bytes = file.read()

            text_content, file_type = "", filename.split('.')[-1].lower() if '.' in filename else 'unknown'

            if file_type in ['txt', 'md', 'py', 'js', 'html', 'css', 'json']:
                text_content = content_bytes.decode('utf-8', errors='ignore')
            # TODO: Add specific parsers for PDF, DOCX etc.
            else:
                text_content = f"Contenido del archivo '{filename}' no pudo ser completamente extraido (tipo: {file_type})."

            chunks = create_smart_chunks(text_content, file_type)
            metadata_base = {
                'filename': filename,
                'extension': file_type,
                'upload_date': datetime.now().isoformat(),
            }

            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                chunk_metadata = metadata_base.copy()
                chunk_metadata['chunk_id'] = i
                all_metadatas.append(chunk_metadata)

            # Log to SQLite for record-keeping
            conn.execute(
                "INSERT OR REPLACE INTO documents (filename, content, chunks, metadata) VALUES (?, ?, ?, ?)",
                (filename, text_content, json.dumps(chunks), json.dumps(metadata_base))
            )
            processed_count += 1
        except Exception as e:
            print(f"Error procesando {file.filename}: {e}")

    if all_chunks:
        try:
            # Crear o cargar la base de datos de vectores y añadir los nuevos documentos
            vectorstore = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings_model)
            vectorstore.add_texts(texts=all_chunks, metadatas=all_metadatas)
            vectorstore.persist()
            print(f"Se han añadido {len(all_chunks)} chunks a la base de datos ChromaDB.")
        except Exception as e:
            print(f"Error al ingestar en ChromaDB: {e}")
            raise e

    conn.commit()
    conn.close()
    return processed_count

def create_smart_chunks(text, file_type):
    """Crea chunks inteligentes según el tipo de archivo"""
    if file_type in ['py', 'js']:
        # Code-aware chunking
        lines = text.split('\\n')
        chunks = []
        current_chunk = ""

        for line in lines:
            if len(current_chunk) + len(line) > 800:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += "\\n" + line if current_chunk else line

        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    elif file_type == 'md':
        # Markdown-aware chunking
        sections = re.split(r'\\n#{1,6}\\s+', text)
        chunks = []
        for section in sections:
            if len(section) > 1000:
                # Split large sections
                chunks.extend([section[i:i+1000] for i in range(0, len(section), 800)])
            else:
                chunks.append(section)
        return chunks

    else:
        # Standard chunking
        return [text[i:i+1000] for i in range(0, len(text), 800)]

def log_search(query, search_type):
    """Registra búsquedas en el historial"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(
        "INSERT INTO search_history (query, result_type, result_content) VALUES (?, ?, ?)",
        (query, search_type, "Search logged")
    )
    conn.commit()
    conn.close()

def get_unified_stats():
    """Obtiene estadísticas completas del sistema"""
    if not Path(DATABASE_PATH).exists():
        return {
            "documents": 0, "chunks": 0, "searches": SEARCH_COUNT,
            "web_sessions": 0, "db_size": 0, "search_history": 0
        }

    try:
        conn = sqlite3.connect(DATABASE_PATH)

        # Document stats
        cursor = conn.execute("SELECT COUNT(*) FROM documents")
        doc_count = cursor.fetchone()[0]

        # Chunks count
        cursor = conn.execute("SELECT chunks FROM documents")
        total_chunks = 0
        for row in cursor.fetchall():
            if row[0]:
                try:
                    chunks = json.loads(row[0])
                    total_chunks += len(chunks)
                except:
                    total_chunks += 1

        # Web sessions count
        cursor = conn.execute("SELECT COUNT(*) FROM web_sessions")
        web_sessions = cursor.fetchone()[0]

        # Search history count
        cursor = conn.execute("SELECT COUNT(*) FROM search_history")
        search_history = cursor.fetchone()[0]

        conn.close()

        # Database size
        db_size = Path(DATABASE_PATH).stat().st_size if Path(DATABASE_PATH).exists() else 0

        return {
            "documents": doc_count,
            "chunks": total_chunks,
            "searches": SEARCH_COUNT,
            "web_sessions": web_sessions,
            "search_history": search_history,
            "db_size": db_size
        }

    except Exception as e:
        print(f"Error getting stats: {e}")
        return {
            "documents": 0, "chunks": 0, "searches": SEARCH_COUNT,
            "web_sessions": 0, "db_size": 0, "search_history": 0
        }

def check_api_connection():
    """Verifica conexión con APIs externas"""
    try:
        response = requests.get(f"{API_HOST}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# API Routes
@app.route('/api/stats')
def api_stats():
    """Endpoint para estadísticas unificadas"""
    return jsonify(get_unified_stats())

@app.route('/api/clear-db', methods=['POST'])
def api_clear_db():
    """Endpoint para limpiar base de datos"""
    try:
        if Path(DATABASE_PATH).exists():
            os.remove(DATABASE_PATH)

        # Recreate database
        unified_system.init_database()

        global SEARCH_COUNT
        SEARCH_COUNT = 0

        return jsonify({"success": True, "message": "Base de datos limpiada exitosamente"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/export-db')
def api_export_db():
    """Endpoint para exportar base de datos"""
    if Path(DATABASE_PATH).exists():
        return send_file(DATABASE_PATH,
                        as_attachment=True,
                        download_name="unified_localgpt_webagent.db")
    else:
        return jsonify({"error": "No se encontró base de datos"}), 404

@app.route('/api/search-history')
def api_search_history():
    """Endpoint para historial de búsquedas"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.execute(
            "SELECT query, result_type, timestamp FROM search_history ORDER BY timestamp DESC LIMIT 50"
        )
        history = cursor.fetchall()
        conn.close()

        return jsonify([{
            "query": row[0],
            "type": row[1],
            "timestamp": row[2]
        } for row in history])

    except Exception as e:
        return jsonify({"error": str(e)})

# Static files
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Main route
@app.route("/", methods=["GET", "POST"])
def unified_home():
    """Página principal del sistema unificado"""
    global FALLBACK_MODE, WEB_AGENT_MODE
    error_message = None
    success_message = None

    # Check API connection
    if not FALLBACK_MODE and not check_api_connection():
        FALLBACK_MODE = True
        error_message = "API backend no disponible. Sistema funcionando en modo unificado offline."

    if request.method == "POST":
        if "user_prompt" in request.form:
            user_prompt = request.form["user_prompt"]
            search_mode = request.form.get("search_mode", "local")
            website = request.form.get("website", "")

            print(f"User Prompt: {user_prompt}, Mode: {search_mode}")

            # Choose search method based on mode
            if search_mode == "web" and website:
                response_dict = web_agent_search(user_prompt, website)
            elif search_mode == "hybrid" and website:
                response_dict = hybrid_search(user_prompt, website)
            else:
                response_dict = fallback_search(user_prompt)

            return render_template("unified_home.html",
                                 show_response_modal=True,
                                 response_dict=response_dict,
                                 success_message="Búsqueda completada exitosamente",
                                 fallback_mode=FALLBACK_MODE,
                                 web_agent_mode=WEB_AGENT_MODE,
                                 **get_unified_stats())

        elif "documents" in request.files:
            files = request.files.getlist("documents")

            if not files or all(f.filename == '' for f in files):
                error_message = "No se seleccionaron archivos para subir."
            else:
                try:
                    processed_count = fallback_ingest(files)
                    success_message = f"Se procesaron exitosamente {processed_count} archivos en el sistema unificado."
                except Exception as e:
                    error_message = f"Error procesando archivos: {str(e)}"

    # Display main page
    stats = get_unified_stats()
    return render_template(
        "unified_home.html",
        show_response_modal=False,
        response_dict={"Prompt": "None", "Answer": "None", "Sources": []},
        error_message=error_message,
        success_message=success_message,
        fallback_mode=FALLBACK_MODE,
        web_agent_mode=WEB_AGENT_MODE,
        **stats
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5112,
                       help="Puerto para ejecutar el sistema unificado. Default: 5112.")
    parser.add_argument("--host", type=str, default="127.0.0.1",
                       help="Host para ejecutar el sistema. Default: 127.0.0.1")

    args = parser.parse_args()

    print("🚀 Iniciando LocalGPT-WebAgent Sistema Unificado...")
    print(f"🌐 Accede en: http://{args.host}:{args.port}")
    print("📚 LocalGPT: Búsqueda en documentos locales")
    print("🌍 WebAgent: Navegación web inteligente")
    print("🔄 Modo híbrido disponible")

    app.run(debug=True, host=args.host, port=args.port)
