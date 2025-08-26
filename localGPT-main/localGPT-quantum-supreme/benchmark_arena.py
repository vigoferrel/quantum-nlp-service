import requests
import json
import re
import evaluate
from datasets import load_dataset
from tqdm import tqdm

class QuantumSupremeGladiator:
    """
    Un adaptador que presenta a nuestro LocalGPT Quantum Supreme
    como un gladiador en la arena de benchmarks.
    """
    def __init__(self, api_url="http://localhost:8000/"):
        self.api_url = api_url

    def predict(self, prompt: str) -> str:
        """
        Envía una consulta a la API del sistema unificado y devuelve la respuesta.
        """
        payload = {"query": prompt}
        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "[SIN RESPUESTA]")
        except requests.RequestException as e:
            return f"[ERROR DE CONEXIÓN: {e}]"
        except json.JSONDecodeError:
            return "[ERROR DE JSON EN RESPUESTA]"

def run_benchmark():
    """
    Ejecuta el benchmark GSM8K en nuestro gladiador y muestra los resultados.
    """
    print("Bienvenidos a la Arena de Benchmarks del Quantum Supreme.")
    print("Forjando al gladiador...")
    gladiator = QuantumSupremeGladiator()

    print("Cargando el campo de batalla (dataset gsm8k)...")
    try:
        # Usaremos solo una pequeña porción para una prueba rápida
        dataset = load_dataset("gsm8k", "main", split='test[:1%]')
        print(f"Campo de batalla listo. {len(dataset)} preguntas nos esperan.")
    except Exception as e:
        print(f"Error fatal: No se pudo cargar el dataset. ¿Hay conexión a internet?")
        print(f"Detalle: {e}")
        return

    print("Cargando las reglas del combate (métrica de accuracy)...")
    accuracy_metric = evaluate.load("accuracy")

    predictions = []
    references = []

    print("¡QUE COMIENCE EL COMBATE!")
    # Usamos tqdm para una barra de progreso
    for item in tqdm(dataset, desc="Procesando gsm8k"):
        question = item['question']
        answer = item['answer']

        # El gladiador hace su predicción
        prediction = gladiator.predict(question)
        predictions.append(prediction)

        # La respuesta correcta es la referencia
        # Extraemos solo el número final para una comparación justa
        reference_answer = answer.split("####")[-1].strip()
        references.append(reference_answer)

    print("\nEl combate ha terminado. Calculando el resultado...")

    # una función para extraer solo el número final de la predicción.
    def extract_answer(text):
        """
        Una función de extracción robusta que limpia y convierte la respuesta a un formato comparable.
        Maneja números, comas, puntos y texto irrelevante.
        """
        try:
            # Eliminar comas de miles y cualquier texto que no sea un número o un punto decimal
            # Tomamos la última secuencia de números que encontremos.
            # Esto es más robusto contra frases como "La respuesta es 1,234.56, pero podría ser..."
            text_str = str(text).replace(',', '')
            matches = re.findall(r'-?[\d\.]+', text_str)

            if not matches:
                return "0" # Devolver un valor numérico por defecto si no se encuentra nada

            # Convertir a float primero para manejar decimales, luego a int si es un número entero.
            # Las respuestas de gsm8k suelen ser enteros.
            num = float(matches[-1])
            return str(int(num))
        except (ValueError, IndexError):
            # Si algo sale mal, devolvemos "0" para no romper el cálculo de la métrica.
            return "0"

    cleaned_predictions = [extract_answer(p) for p in predictions]

    # Calcular la puntuación de precisión
    results = accuracy_metric.compute(predictions=cleaned_predictions, references=references)

    print("\n--- RESULTADOS DE LA ARENA ---")
    print(f"Benchmark: GSM8K (una muestra del 1%)")
    print(f"Gladiador: LocalGPT Quantum Supreme Unificado")
    print(f"Precisión (Accuracy): {results['accuracy']:.2%}")
    print("------------------------------------")
    print("\nAnálisis de algunas respuestas:")
    for i in range(min(5, len(dataset))):
        print(f"  Pregunta: {dataset[i]['question']}")
        print(f"  Respuesta Esperada: {references[i]}")
        print(f"  Respuesta del Gladiador: {cleaned_predictions[i]} (Original: {predictions[i][:100]}...)")
        print("-" * 20)


if __name__ == "__main__":
    run_benchmark()
