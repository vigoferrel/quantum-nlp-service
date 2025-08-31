#!/usr/bin/env python3
"""
🧹 VIGOLEONROCKS Repository Cleanup Script
==========================================

Script para limpiar archivos redundantes y mantener solo los componentes
esenciales del modelo unificado VIGOLEONROCKS.

🎓 Academic Research Project by Oscar Ferrel Bustos
🏛️ Pontificia Universidad Católica de Chile
"""

import os
import shutil
from pathlib import Path
from typing import List, Set

# Archivos y directorios esenciales de VIGOLEONROCKS
ESSENTIAL_FILES = {
    # Core VIGOLEONROCKS files
    "vigoleonrocks_unified_model.py",
    "vigoleonrocks_quantum_multimodal_core.py", 
    "vigoleonrocks_unified_multimodal_api.py",
    "vigoleonrocks_multimodal_benchmark_suite.py",
    "vigoleonrocks_ultimate_complete_demo.py",
    
    # Academic documentation
    "README.md",
    "VIGOLEONROCKS_Paper_Castellano.md",
    "README_MULTIMODAL.md",
    "ARCHITECTURE.md",
    "INSTALLATION.md",
    
    # Essential config/deployment
    ".env",
    ".env.example", 
    ".gitignore",
    "requirements.txt",
    "cleanup_repository.py",
    
    # License and academic
    "LICENSE",
    "CONTRIBUTING.md"
}

# Directorios a mantener (con contenido esencial)
ESSENTIAL_DIRECTORIES = {
    ".git",
    "static",
    "templates"  # Si existen para la API
}

# Archivos a eliminar (patrones redundantes o legacy)
REDUNDANT_PATTERNS = [
    # Legacy/old versions
    "vigoleonrocks_complete_demo.py",  # Superseded by ultimate version
    "vigoleonrocks_ultimate_multimodal_demo.py",  # Superseded by complete version
    "vigoleonrocks_unified_api.py",  # Superseded by multimodal API
    
    # Old system files
    "advanced_conversational_engine.py",
    "advanced_llm_evaluation_suite.py", 
    "advanced_monitor.py",
    "advanced_multimodal_server_backup.py",
    "advanced_multimodal_server_fixed.py",
    "advanced_nlp_engine.py",
    
    # Development/testing files
    "academic_paper_generator.py",
    "analisis_capacidades_potenciales.py",
    "analisis_detallado_sistema.py",
    "api_auth_system.py",
    "auto_deploy_ssh.py",
    "cache_manager.py",
    "check_claude_models.py",
    "check_gemini_models.py",
    
    # CIO system files (replaced by VIGOLEONROCKS)
    "cio_multimodal_extension.py",
    "cio_multimodal_extension_corrected.py",
    "cio_multimodal_extension_final.py",
    "cio_multimodal_extension_fixed.py",
    "cio_multimodal_extension_optimized.py",
    "cio_multimodal_server.py",
    "cio_multimodal_server_corrected.py",
    "cio_multimodal_server_fixed.py",
    "cio_multimodal_server_optimized.py",
    "cio_premium_quality_system.py",
    "cio_quantum_revolution_system.py",
    
    # Deployment test files
    "connection_monitor.py",
    "correccion_serializacion_avanzada.py",
    "correccion_serializacion_especifica.py",
    "create_favicon.py",
    "debug_advanced_system.py",
    "deploy_cloud_hosting.py",
    "deploy_remote.py", 
    "deploy_simple.py",
    "deploy_vps_supremacy.py",
    "deploy_vps_supremacy_fixed.py",
    "despliegue_rapido.py",
    "diagnostico_detallado_sistema.py",
    
    # Evaluation files (replaced by benchmark suite)
    "evaluacion_competitiva_completa.py",
    "execute_evaluation_benchmark.py",
    "exhaustive_impossible_evaluation.py",
    "final_implementation_system.py",
    "gemini_cio_integration_system.py",
    "gemini_cio_simple_test.py",
    "gemini_membrane_integration_system.py",
    "generador_sistema_optimizado.py",
    "generate_deploy.py",
    "home_field_domination.py",
    "hostinger_api.py",
    "immediate_implementation_system.py",
    
    # Implementation phases (completed)
    "implementacion_supremacia_fase1.py",
    "implementacion_supremacia_fase2.py", 
    "implementacion_supremacia_fase3.py",
    "industry_benchmark_system.py",
    "install_dependencies.py",
    "install_quantum_edge.py",
    
    # Live comparison files (integrated in benchmark suite)
    "latest_llm_comparison.py",
    "launch_essence.py",
    "launch_essence_final.py", 
    "launch_essence_real.py",
    "live_api_comparison.py",
    "live_benchmark_comparison.py",
    "live_competitor_benchmark.py",
    "live_performance_test.py"
]

# Documentos legacy/redundantes
REDUNDANT_DOCS = [
    # Analysis documents (superseded by final paper)
    "ANALISIS_STACK_COMPLETO_VIGOLEONROCKS.md",
    "ANALISIS_STACK_VIGOLEONROCKS.md",
    "API_USAGE_GUIDE.md",  # Will be in API docs
    "CHANGELOG.md",  # Git history is sufficient
    
    # API Keys (should not be in repo)
    "CLAVES_API_kjacome24.md",
    "CLAVES_API_ocferrel.md",
    
    # Implementation reports (completed)
    "INFORME_FASE2_COMPLETADA.md",
    "INFORME_FINAL_IMPLEMENTACION_COMPLETA.md",
    "INFORME_FINAL_OPTIMIZACION.md",
    "INFORME_FINAL_OPTIMIZACION_COMPLETADA.md",
    "INFORME_INGENIERIA_INVERSA_RESULTADOS.md",
    "INFORME_REVISION_SUPREMACIA.md",
    
    # Deployment guides (superseded)
    "OPENROUTER_PROVIDER_README.md",
    "PRODUCTION_DEPLOYMENT_GUIDE.md",
    "README_DEPLOYMENT.md",
    "README_QBTC_LAUNCHER.md",
    
    # Planning documents (completed)
    "PLAN_ACTIVACION_COMPLETO_VIGOLEONROCKS.md",
    "PLAN_ACTIVACION_VIGOLEONROCKS.md",
    "PLAN_BASES_TECNICAS_CONTEXTO_OPTIMIZADO.md",
    "PLAN_DESPLIEGUE_DOKPLOY.md",
    "PLAN_DIMENSIONAMIENTO_VIGOLEONROCKS_PROVIDER.md",
    "PLAN_EVALUACION_PERFORMANCE.md",
    "PLAN_EVALUACION_PERFORMANCE_ACTUALIZADA.md",
    "PLAN_IMPLEMENTACION_INMEDIATO.md",
    "PLAN_MAXIMIZACION_VANGUARDIA_2025.md",
    "PLAN_OPTIMIZACION_OPENROUTER_MEMBRANA_IONICA.md",
    "PROPUESTA_GLOBAL_VIGOLEONROCKS_INTEGRADA.md",
    
    # Reports (can be kept as examples but not in main branch)
    "REPORTE_EVALUACION_COMPETITIVA.json",
    "REPORTE_FASE1_SUPREMACIA.json", 
    "REPORTE_FASE2_OPTIMIZACION.json",
    "REPORTE_FINAL_SUPREMACIA_COMPLETA.json",
    "RESUMEN_INGENIERIA_INVERSA_EXITOSA.md",
    
    # Demo results (generated files)
    "VIGOLEONROCKS_Demo_Report_20250829_220643.json",
    "VIGOLEONROCKS_Academic_Paper.md"  # Duplicate of Spanish version
]

# Directories to remove completely
REDUNDANT_DIRECTORIES = [
    "localGPT-main",  # External project, not part of VIGOLEONROCKS
    "__pycache__",
    ".pytest_cache",
    "dist",
    "build",
    "*.egg-info"
]

def cleanup_repository():
    """Limpiar repositorio manteniendo solo archivos esenciales"""
    repo_path = Path(".")
    removed_files = []
    removed_dirs = []
    
    print("🧹 VIGOLEONROCKS Repository Cleanup")
    print("="*50)
    print("🎓 Cleaning up to keep only essential unified model components...")
    print()
    
    # Remove redundant Python files
    for pattern in REDUNDANT_PATTERNS:
        file_path = repo_path / pattern
        if file_path.exists():
            try:
                file_path.unlink()
                removed_files.append(pattern)
                print(f"🗑️  Removed: {pattern}")
            except Exception as e:
                print(f"❌ Could not remove {pattern}: {e}")
    
    # Remove redundant documentation
    for doc in REDUNDANT_DOCS:
        doc_path = repo_path / doc  
        if doc_path.exists():
            try:
                doc_path.unlink()
                removed_files.append(doc)
                print(f"📄 Removed doc: {doc}")
            except Exception as e:
                print(f"❌ Could not remove {doc}: {e}")
    
    # Remove redundant directories
    for dir_pattern in REDUNDANT_DIRECTORIES:
        if "*" in dir_pattern:
            # Handle wildcard patterns
            for path in repo_path.glob(dir_pattern):
                if path.is_dir():
                    try:
                        shutil.rmtree(path)
                        removed_dirs.append(str(path))
                        print(f"📁 Removed directory: {path}")
                    except Exception as e:
                        print(f"❌ Could not remove directory {path}: {e}")
        else:
            dir_path = repo_path / dir_pattern
            if dir_path.exists() and dir_path.is_dir():
                try:
                    shutil.rmtree(dir_path)
                    removed_dirs.append(dir_pattern)
                    print(f"📁 Removed directory: {dir_pattern}")
                except Exception as e:
                    print(f"❌ Could not remove directory {dir_pattern}: {e}")
    
    print("\n✅ CLEANUP COMPLETED!")
    print("="*50)
    print(f"🗑️  Files removed: {len(removed_files)}")
    print(f"📁 Directories removed: {len(removed_dirs)}")
    print("\n🌟 VIGOLEONROCKS repository is now clean and focused!")
    print("🎓 Only essential unified model components remain.")
    
    # List remaining essential files
    print("\n📋 ESSENTIAL FILES KEPT:")
    print("-"*30)
    for file in sorted(ESSENTIAL_FILES):
        file_path = repo_path / file
        if file_path.exists():
            print(f"✅ {file}")
        else:
            print(f"⚠️  {file} (missing)")
    
    return removed_files, removed_dirs

if __name__ == "__main__":
    cleanup_repository()
