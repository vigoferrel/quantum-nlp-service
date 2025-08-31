#!/usr/bin/env python3
"""
Simple executor for VIGOLEONROCKS Architect Reorganizer
"""

from vigoleonrocks_architect_reorganizer_fixed import VIGOLEONROCKSArchitectReorganizer
import sys
from pathlib import Path

def main():
    # Set project root to current directory
    project_root = Path(__file__).parent.resolve()
    
    print("🚀 Ejecutando VIGOLEONROCKS Architect Reorganizer")
    print(f"📁 Proyecto: {project_root}")
    print()
    
    # Ask for confirmation
    confirm = input("⚠️ ¿Estás seguro de que quieres ejecutar la reorganización real? (si/no): ")
    if confirm.lower() not in ['si', 'sí', 's', 'yes', 'y']:
        print("❌ Operación cancelada")
        return
    
    # Create reorganizer
    try:
        reorganizer = VIGOLEONROCKSArchitectReorganizer(str(project_root))
        
        # Execute reorganization (not dry run)
        summary = reorganizer.run_complete_reorganization(dry_run=False)
        
        print("\n" + "="*80)
        print("🎉 REORGANIZACIÓN COMPLETADA EXITOSAMENTE")
        print("="*80)
        print(f"⏱️ Duración: {summary['duration_seconds']:.2f} segundos")
        print(f"📊 Componentes analizados: {summary['analysis']['total_dirs']}")
        print(f"📄 Archivos procesados: {summary['analysis']['total_files']:,}")
        print(f"📝 Líneas de código: {summary['analysis']['total_loc']:,}")
        print(f"📁 Archivos movidos: {summary['results']['files_moved']}")
        print(f"✅ Pasos completados: {summary['results']['steps_completed']}")
        
        if summary['results']['errors']:
            print(f"❌ Errores: {len(summary['results']['errors'])}")
            for error in summary['results']['errors']:
                print(f"   • {error}")
        
        print("\n📋 Reportes generados:")
        print("   • vigoleonrocks_reorganization_report.json")
        print("   • vigoleonrocks_reorganization_report.txt")
        print("   • reorganize_vigoleonrocks.ps1")
        print("   • reorganize_vigoleonrocks.py")
        
        print(f"\n📁 Nueva estructura disponible en: _new_optimized_structure/")
        print(f"📦 Backup original en: _backup_original_structure/")
        
    except Exception as e:
        print(f"\n❌ Error durante la reorganización: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
