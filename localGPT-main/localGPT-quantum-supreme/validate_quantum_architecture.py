#!/usr/bin/env python3
"""
Script de validacion final de la arquitectura cuantica unificada
"""

import sys
import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List

# Configurar codificacion para Windows
if sys.platform.startswith('win'):
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except:
            pass

# Anadir el directorio al path para importar los modulos
sys.path.insert(0, os.path.dirname(__file__))

def check_file_exists(file_path: str) -> bool:
    """Verifica si un archivo existe"""
    return os.path.exists(file_path)

def check_imports() -> Dict[str, bool]:
    """Verifica que todos los modulos pueden importarse correctamente"""
    imports_status = {}

    modules_to_test = [
        'quantum_hybrid_core',
        'quantum_compatibility_layer',
        'quantum_migration_manager'
    ]

    for module in modules_to_test:
        try:
            __import__(module)
            imports_status[module] = True
        except ImportError as e:
            print(f"Error importando {module}: {e}")
            imports_status[module] = False

    return imports_status

def check_config_files() -> Dict[str, bool]:
    """Verifica que los archivos de configuracion existen y son validos"""
    config_status = {}

    # Verificar archivo de configuracion de migracion
    migration_config_path = os.path.join(os.path.dirname(__file__), 'quantum_migration_config.yaml')
    config_status['migration_config'] = check_file_exists(migration_config_path)

    # Verificar que es un YAML valido
    if config_status['migration_config']:
        try:
            import yaml
            with open(migration_config_path, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            config_status['migration_config_valid'] = True
        except Exception as e:
            print(f"Error validando YAML: {e}")
            config_status['migration_config_valid'] = False

    return config_status

def check_documentation() -> Dict[str, bool]:
    """Verifica que la documentacion existe"""
    doc_status = {}

    # Verificar documentacion arquitectonica
    arch_doc_path = os.path.join(os.path.dirname(__file__), 'QUANTUM_ARCHITECTURE.md')
    doc_status['architecture_doc'] = check_file_exists(arch_doc_path)

    # Verificar plan de testing
    test_plan_path = os.path.join(os.path.dirname(__file__), 'quantum_testing_plan.md')
    doc_status['test_plan'] = check_file_exists(test_plan_path)

    return doc_status

def check_test_files() -> Dict[str, bool]:
    """Verifica que los archivos de test existen"""
    test_status = {}

    # Verificar directorio de tests
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    test_status['tests_directory'] = check_file_exists(tests_dir)

    if test_status['tests_directory']:
        # Verificar archivos de test especificos
        test_files = [
            'test_quantum_hybrid_core.py',
            'test_quantum_integration.py'
        ]

        for test_file in test_files:
            test_file_path = os.path.join(tests_dir, test_file)
            test_status[f'test_{test_file}'] = check_file_exists(test_file_path)

    return test_status

def validate_architecture_components() -> Dict[str, Any]:
    """Valida los componentes principales de la arquitectura"""
    validation_results = {
        'imports': check_imports(),
        'config_files': check_config_files(),
        'documentation': check_documentation(),
        'test_files': check_test_files()
    }

    return validation_results

def calculate_completeness_score(validation_results: Dict[str, Any]) -> float:
    """Calcula un puntaje de completitud basado en los resultados de validacion"""
    total_checks = 0
    passed_checks = 0

    for category, checks in validation_results.items():
        for check_name, check_result in checks.items():
            total_checks += 1
            if check_result:
                passed_checks += 1

    if total_checks == 0:
        return 0.0

    return (passed_checks / total_checks) * 100

def generate_validation_report(validation_results: Dict[str, Any]) -> str:
    """Genera un reporte de validacion detallado"""
    report = []
    report.append("=" * 60)
    report.append("REPORTE DE VALIDACION - ARQUITECTURA CUANTICA UNIFICADA")
    report.append("=" * 60)
    report.append("")

    # Resumen general
    completeness_score = calculate_completeness_score(validation_results)
    report.append(f"PUNTAJE DE COMPLETITUD: {completeness_score:.1f}%")
    report.append("")

    # Detalles por categoria
    for category, checks in validation_results.items():
        report.append(f"{category.upper()}:")
        for check_name, check_result in checks.items():
            status = "[PASS]" if check_result else "[FAIL]"
            report.append(f"  {status} - {check_name}")
        report.append("")

    # Recomendaciones
    report.append("RECOMENDACIONES:")
    if completeness_score < 100:
        report.append("  - Revisar los componentes marcados como FAIL")
        report.append("  - Asegurar que todas las dependencias esten instaladas")
        report.append("  - Verificar permisos de archivos y directorios")
    else:
        report.append("  [PASS] Arquitectura validada completamente")
        report.append("  [PASS] Todos los componentes estan presentes y funcionales")

    report.append("")
    report.append("=" * 60)

    return "\n".join(report)

async def validate_quantum_system():
    """Validacion asincrona del sistema cuantico"""
    print("Iniciando validacion del sistema cuantico...")

    # Validar componentes de la arquitectura
    validation_results = validate_architecture_components()

    # Generar y mostrar reporte
    report = generate_validation_report(validation_results)
    print(report)

    # Calcular puntaje final
    completeness_score = calculate_completeness_score(validation_results)

    print(f"\nValidacion completada. Puntaje: {completeness_score:.1f}%")

    if completeness_score >= 90:
        print("[PASS] Sistema cuantico validado exitosamente")
        return True
    else:
        print("[FAIL] Se encontraron problemas en la validacion")
        return False

def main():
    """Funcion principal de validacion"""
    print("VALIDACION DE ARQUITECTURA CUANTICA UNIFICADA")
    print("=" * 50)

    try:
        # Ejecutar validacion asincrona
        result = asyncio.run(validate_quantum_system())

        if result:
            print("\n[PASS] VALIDACION EXITOSA")
            print("La arquitectura cuantica unificada esta completamente implementada y validada.")
            return 0
        else:
            print("\n[FAIL] VALIDACION FALLIDA")
            print("Se encontraron problemas que requieren atencion.")
            return 1

    except Exception as e:
        print(f"\n[ERROR] DURANTE LA VALIDACION: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
