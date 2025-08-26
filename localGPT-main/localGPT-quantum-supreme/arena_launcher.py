import subprocess
import time
import sys
import os

def run_arena():
    """
    Lanza el servidor de Quantum Supreme, espera a que se inicie,
    ejecuta la arena de benchmarks y luego apaga el servidor.
    Un orquestador robusto e independiente de la shell.
    """
    print("🏟️  Preparando la Arena: Orquestador de Benchmarks Iniciado 🏟️")

    # Define las rutas a los scripts para que sea portable
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(base_dir, "localgpt_quantum_supreme.py")
    arena_script = os.path.join(base_dir, "benchmark_arena.py")

    server_process = None

    try:
        # 1. Invocar al Titán (Servidor) en segundo plano
        print("▶️  Despertando al Titán (Servidor LocalGPT Quantum Supreme)...")
        # Usamos Popen para tener control sobre el proceso
        server_process = subprocess.Popen([sys.executable, server_script])

        # 2. Esperar el Amanecer
        wait_time = 7
        print(f"⌛ Dando al Titán {wait_time} segundos para prepararse...")
        time.sleep(wait_time)

        # 3. Desatar al Gladiador (Benchmark)
        print("\n⚔️  ¡El Gladiador entra en la Arena! Ejecutando benchmark... ⚔️\n")
        # Usamos run porque queremos esperar a que este proceso termine
        benchmark_result = subprocess.run([sys.executable, arena_script], capture_output=True, text=True, check=False)

        # Imprimir la salida del benchmark en tiempo real (si es posible) o al final
        print("--- Salida de la Arena ---")
        print(benchmark_result.stdout)
        if benchmark_result.stderr:
            print("\n--- Errores en la Arena ---")
            print(benchmark_result.stderr)
        print("--------------------------")

    except FileNotFoundError as e:
        print(f"❌ Error: No se encontró el script. ¿Estás en el directorio correcto? Detalle: {e}")
    except Exception as e:
        print(f"Anomalía catastrófica en la arena: {e}")
    finally:
        # 4. Garantizar la Paz
        if server_process:
            print("\n⏹️  La batalla ha terminado. Poniendo al Titán a descansar...")
            server_process.terminate()
            server_process.wait()
            print("El Titán descansa. La Arena está en silencio.")

if __name__ == "__main__":
    run_arena()
