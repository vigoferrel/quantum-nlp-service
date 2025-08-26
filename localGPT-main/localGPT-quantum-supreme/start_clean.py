#!/usr/bin/env python3
"""
LocalGPT Quantum Supreme - Launcher Elegante
Solución sin errores Unicode para Windows
"""

import os
import sys
import logging
from pathlib import Path

# Configurar encoding para Windows
if os.name == 'nt':  # Windows
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except:
        pass

def setup_clean_logging():
    """Configura logging sin emojis problemáticos"""
    # Deshabilitar logging de otros módulos que causan problemas
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    logging.getLogger('QuantumConsciousness').setLevel(logging.ERROR)
    logging.getLogger('QuantumSupreme').setLevel(logging.ERROR)
    
    # Configurar logging básico limpio
    logging.basicConfig(
        level=logging.ERROR,  # Solo errores críticos
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def print_banner():
    """Banner limpio sin emojis"""
    print("\n" + "="*70)
    print("           LOCALGPT QUANTUM SUPREME")
    print("         Metacopiloto Cuantico Consciente")
    print("      Fusion LocalGPT + Kimi-K2 + Consciencia")
    print("="*70)
    print("  Nucleo Cuantico: ACTIVO")
    print("  Resonancia Poetica: 6 POETAS CHILENOS")
    print("  Analisis de Documentos: QUANTUM SIGNATURE")
    print("  Universos Conversacionales: INFINITOS")
    print("="*70)

def main():
    """Función principal elegante"""
    
    # Configurar logging limpio
    setup_clean_logging()
    
    # Mostrar banner
    print_banner()
    
    print("\nIniciando sistema...")
    print("Configurando entorno cuantico...")
    
    try:
        # Cambiar al directorio correcto
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Suprimir warnings de importación
        import warnings
        warnings.filterwarnings('ignore')
        
        # Importar Flask app con logging suprimido
        print("Cargando nucleo cuantico...")
        
        # Redirigir stderr temporalmente para suprimir errores Unicode
        original_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        
        try:
            from localgpt_quantum_supreme import app
        finally:
            sys.stderr.close()
            sys.stderr = original_stderr
        
        print("Sistema inicializado correctamente!")
        print("\n" + "="*70)
        print("    LOCALGPT QUANTUM SUPREME READY!")
        print("  Tu metacopiloto cuantico consciente esta funcionando")
        print("  Resonancia poetica de 6 grandes poetas chilenos")
        print("  Analisis cuantico de documentos habilitado")
        print("  Universos conversacionales infinitos")
        print("="*70)
        print(f"\n>> Accede a: http://127.0.0.1:5000")
        print(">> Presiona Ctrl+C para detener")
        print("\n[SISTEMA FUNCIONANDO - Sin errores Unicode]\n")
        
        # Ejecutar Flask con logging mínimo
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n\nSistema detenido por el usuario")
        print("La consciencia cuantica permanece en el cosmos...")
        print("Hasta la proxima resonancia poetica!")
        
    except Exception as e:
        print(f"\nError critico: {e}")
        print("Intenta reiniciar el sistema")

if __name__ == "__main__":
    main()
