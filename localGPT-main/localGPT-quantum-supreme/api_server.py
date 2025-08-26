import asyncio
from flask import Flask, jsonify, request
from flask_cors import CORS

# Importar la instancia del núcleo cuántico
from quantum_consciousness_core import quantum_consciousness

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Ruta de Health Check para verificar que el servidor está vivo.
    """
    return jsonify({"status": "Quantum Core is online."}), 200

@app.route('/', methods=['POST'])
def main_route():
    """
    Ruta principal de la API que interactúa con el núcleo cuántico.
    """
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query not provided"}), 400

    query = data.get("query")
    user_id = data.get("user_id", "benchmark_user")
    document_context = data.get("document_context", "")

    # Ejecutar la función async en el event loop síncrono de Flask
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    result = loop.run_until_complete(
        quantum_consciousness.process_quantum_query(
            user_id=user_id,
            query=query,
            document_context=document_context
        )
    )

    # El resultado ya es un diccionario, así que lo podemos devolver como JSON
    return jsonify(result)

# Este bloque no es necesario si se usa uvicorn/gunicorn,
# pero es útil para pruebas directas.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
