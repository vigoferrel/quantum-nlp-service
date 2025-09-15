#!/usr/bin/env python3
"""
🧪 Test rápido del manejo dinámico de CLIP en MultimodalAIManager
Verifica que el sistema funciona correctamente con/sin CLIP
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio actual al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent))

from multimodal_ai_manager import MultimodalAIManager, CLIP_AVAILABLE

async def test_multimodal_clip_handling():
    """Prueba el manejo dinámico de CLIP"""
    print("🔍 Testando manejo dinámico de CLIP en MultimodalAIManager")
    print(f"📊 Estado de CLIP: {'✅ Disponible' if CLIP_AVAILABLE else '❌ No disponible'}")
    
    try:
        # Inicializar manager
        manager = MultimodalAIManager()
        print(f"🚀 Manager inicializado en dispositivo: {manager.device}")
        
        # Obtener estado del sistema
        status = manager.get_system_status()
        
        print("\n📋 Estado del Sistema:")
        print(f"  - Dispositivo: {status['device']}")
        print(f"  - Modelos cargados: {status['models_loaded']}")
        print(f"  - Modelos habilitados: {len(status['models_enabled'])}")
        print(f"  - Modelos deshabilitados: {len(status['models_disabled'])}")
        
        print("\n🎯 Capacidades:")
        for capability, available in status['capabilities'].items():
            emoji = "✅" if available else "❌"
            print(f"  - {capability}: {emoji}")
        
        print("\n🔗 Estado de CLIP:")
        if 'clip_status' in status:
            clip_status = status['clip_status']
            print(f"  - Disponible: {'✅' if clip_status['available'] else '❌'}")
            print(f"  - Habilitado: {'✅' if clip_status['enabled'] else '❌'}")
            print(f"  - Cargado: {'✅' if clip_status['loaded'] else '❌'}")
            print(f"  - Modelo ID: {clip_status['model_id']}")
            
            if 'error' in clip_status:
                print(f"  - Error: {clip_status['error']}")
        
        # Mostrar modelos deshabilitados por falta de CLIP
        if not CLIP_AVAILABLE and 'clip_vit' in status['models_disabled']:
            print("\n⚠️  CLIP está deshabilitado por falta de biblioteca")
            print("   Para habilitarlo: pip install clip-by-openai")
        
        # Intentar cargar CLIP (debería fallar graciosamente si no está disponible)
        print("\n🔄 Intentando cargar modelo CLIP...")
        try:
            clip_loaded = await manager.ensure_model_loaded("clip_vit")
            if clip_loaded:
                print("✅ CLIP cargado exitosamente")
            else:
                print("❌ CLIP no se pudo cargar (esperado si no está disponible)")
        except Exception as e:
            print(f"❌ Error cargando CLIP: {e} (esperado si no está disponible)")
        
        # Limpiar recursos
        await manager.cleanup()
        print("\n✅ Test completado exitosamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_multimodal_clip_handling())
    exit_code = 0 if success else 1
    sys.exit(exit_code)
