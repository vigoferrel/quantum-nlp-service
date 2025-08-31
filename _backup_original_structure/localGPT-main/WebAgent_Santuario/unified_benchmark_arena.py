import sys
import os
import json
import asyncio
from pathlib import Path

# Add the unified app's directory to the path to import its modules
UNIFIED_APP_DIRECTORY = r"C:\Users\Hp\Desktop\vigosueldo\localGPT-main\WebAgent-main\LocalGPT-WebAgent-Unified"
sys.path.append(UNIFIED_APP_DIRECTORY)

from unified_app import fallback_search, web_agent_search, hybrid_search, fallback_ingest

# Mock file upload object for ingestion
class MockFile:
    def __init__(self, filename, content):
        self.filename = filename
        self._content = content
    
    def read(self):
        return self._content

def setup_test_documents():
    """Create and ingest mock documents for local search."""
    print("--- Configurando documentos de prueba... ---")
    doc1_content = b"La Conferencia Anual de la Asociacion de Linguistica Computacional (ACL) 2025 sera en Bangkok, Tailandia. El general chair es la profesora Lucia Specia."
    doc2_content = b"El Keynote speaker para el track de industria de ACL 2025 es el Dr. Kai-Fu Lee, conocido por su trabajo en Sinovation Ventures."
    
    files = [
        MockFile("acl_2025_info.txt", doc1_content),
        MockFile("acl_2025_industry.txt", doc2_content)
    ]
    
    processed_count = fallback_ingest(files)
    print(f"--- ✅ {processed_count} documentos procesados e ingestados. ---\n")

async def run_benchmark():
    """Runs the benchmark suite and prints a report."""
    
    setup_test_documents()

    report_lines = ["# Reporte de Benchmark del Sistema Unificado", ""]

    # --- Test Case 1: Local RAG Search ---
    report_lines.append("## 1. Busqueda Local (RAG)")
    print("--- Ejecutando Prueba 1: Busqueda Local ---")
    local_query = "¿Quién es el general chair de ACL 2025 según los documentos?"
    result = fallback_search(local_query)
    report_lines.append(f"**Query:** `{local_query}`")
    report_lines.append(f"**Respuesta Obtenida:**")
    report_lines.append(f"> {result['Answer']}")
    report_lines.append(f"**Evaluacion:** {'Pasa' if 'Lucia Specia' in result['Answer'] else 'Falla'}")
    report_lines.append("")

    # --- Test Case 2: WebAgent Search ---
    report_lines.append("## 2. Navegacion Web (WebAgent)")
    print("--- Ejecutando Prueba 2: Navegacion Web ---")
    web_query = "En el sitio de ACL 2025, encuentra el tema especial (special theme)."
    website = "https://2025.aclweb.org/"
    # We need to run the search in an async context
    result = web_agent_search(web_query, website)
    report_lines.append(f"**Query:** `{web_query}` en `{website}`")
    report_lines.append(f"**Respuesta Obtenida:**")
    report_lines.append(f"> {result['Answer']}")
    # This is a bit simplistic, as the real answer might vary.
    report_lines.append(f"**Evaluacion:** {'Pasa' if 'theme' in result['Answer'].lower() else 'Revision Manual'}")
    report_lines.append("")

    # --- Test Case 3: Hybrid Search ---
    report_lines.append("## 3. Busqueda Hibrida")
    print("--- Ejecutando Prueba 3: Busqueda Hibrida ---")
    hybrid_query = "Compara la información del keynote speaker del track de industria en los documentos locales con la información online."
    # The hybrid function currently just combines results, let's test that behavior
    result = hybrid_search(hybrid_query, website)
    report_lines.append(f"**Query:** `{hybrid_query}`")
    report_lines.append(f"**Respuesta Obtenida:**")
    report_lines.append(f"> {result['Answer']}")
    report_lines.append(f"**Evaluacion:** {'Pasa' if 'Kai-Fu Lee' in result['Answer'] and 'ACL' in result['Answer'] else 'Falla'}")
    report_lines.append("")

    # --- Final Report ---
    final_report = "\n".join(report_lines)
    print("\n\n--- REPORTE FINAL ---")
    print(final_report)
    
    with open("benchmark_report.md", "w", encoding="utf-8") as f:
        f.write(final_report)
    
    print("\n--- Reporte guardado en benchmark_report.md ---")

if __name__ == "__main__":
    asyncio.run(run_benchmark())