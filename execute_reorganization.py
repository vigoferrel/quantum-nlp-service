#!/usr/bin/env python3
"""
Script temporal para ejecutar la reorganización completa de VIGOLEONROCKS
"""

import sys
import os
from pathlib import Path

# Importar el reorganizador
from vigoleonrocks_architect_reorganizer import VIGOLEONROCKSArchitectReorganizer

def main():
    project_root = r'C:\Users\Hp\Desktop\quantum-nlp-service'
    
    print('🚀 Iniciando reorganización REAL de VIGOLEONROCKS...')
    print(f'📁 Proyecto: {project_root}')
    print('🔧 Modo: EJECUCIÓN REAL')
    print()
    
    try:
        # Crear reorganizador
        reorganizer = VIGOLEONROCKSArchitectReorganizer(project_root)
        
        # Ejecutar reorganización completa
        summary = reorganizer.run_complete_reorganization(dry_run=False)
        
        print('\n' + '='*80)
        print('🎉 REORGANIZACIÓN COMPLETADA EXITOSAMENTE')
        print('='*80)
        print(f'⏱️ Duración: {summary["duration_seconds"]:.2f} segundos')
        print(f'📊 Componentes analizados: {summary["analysis"]["total_dirs"]}')
        print(f'📄 Archivos procesados: {summary["analysis"]["total_files"]:,}')
        print(f'📝 Líneas de código: {summary["analysis"]["total_loc"]:,}')
        print(f'📁 Archivos movidos: {summary["results"]["files_moved"]}')
        print(f'✅ Pasos completados: {summary["results"]["steps_completed"]}')
        
        print('\n📋 Reportes generados:')
        print('   • vigoleonrocks_reorganization_report.json')
        print('   • vigoleonrocks_reorganization_report.txt')
        print('   • reorganize_vigoleonrocks.ps1')
        print('   • reorganize_vigoleonrocks.py')
        
        print(f'\n📁 Nueva estructura disponible en: _new_optimized_structure/')
        print(f'📦 Backup original en: _backup_original_structure/')
        
        print('\n🎯 ARQUITECTURA OPTIMIZADA CREADA EXITOSAMENTE!')
        
    except Exception as e:
        print(f'\n❌ Error durante la reorganización: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
