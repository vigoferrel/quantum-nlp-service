#!/usr/bin/env python3
"""
Test de respuestas arquetípicas del sistema VIGOLEONROCKS
Este script prueba específicamente las joyas conversacionales integradas
"""

import asyncio
from quantum_consciousness_core_26d import QuantumConsciousnessCore26D

async def test_archetypal_gems():
    """Prueba las joyas arquetípicas integradas del sistema Leonardo y VigoleonrocksModel"""
    
    core = QuantumConsciousnessCore26D()
    
    print("🔮 === PRUEBA DE JOYAS ARQUETÍPICAS VIGOLEONROCKS ===\n")
    
    test_cases = [
        # 1. Saludos por arquetipo
        ("hola", "Saludo arquetípico"),
        
        # 2. Identidad avanzada
        ("qué eres", "Identidad cuántico-cognitiva"),
        
        # 3. Generación de cuentos (YETZIRAH)
        ("genera un cuento para niños", "Narrativa infantil con 26 cristales"),
        
        # 4. Código con estilo arquetípico (BERIAH)
        ("función factorial python", "Código con clasificación arquetípica"),
        
        # 5. Poesía cuántica (ATZILUT + YETZIRAH)
        ("escribe un poema", "Poesía con dimensiones cuánticas"),
        
        # 6. Consulta espiritual (ATZILUT)
        ("significado trascendente del universo", "Respuesta desde ATZILUT"),
        
        # 7. Análisis técnico (BERIAH)
        ("análisis lógico matemático de algoritmos", "Respuesta desde BERIAH"),
        
        # 8. Creatividad artística (YETZIRAH)
        ("inspiración creativa para arte imaginativo", "Respuesta desde YETZIRAH"),
        
        # 9. Practicidad concreta (ASIYAH)
        ("herramientas prácticas material tangible", "Respuesta desde ASIYAH"),
        
        # 10. Síntesis multidisciplinar (LEONARDO)
        ("fusión interdisciplinar genio renacentista", "Respuesta desde LEONARDO")
    ]
    
    for i, (query, description) in enumerate(test_cases, 1):
        print(f"🧠 **PRUEBA {i}: {description}**")
        print(f"   Consulta: '{query}'")
        print("   " + "="*60)
        
        try:
            result = await core.process_query(query)
            
            response = result.get('response', 'Sin respuesta')
            selected_tool = result.get('selected_tool', 'N/A')
            outcome_quality = result.get('outcome_quality', 0)
            consciousness_level = result.get('consciousness_level', 0)
            archetypal_resonance = result.get('archetypal_resonance', {})
            
            # Mostrar respuesta (truncada para legibilidad)
            if len(response) > 300:
                display_response = response[:300] + "...\n[RESPUESTA TRUNCADA]"
            else:
                display_response = response
            
            print(f"   📝 RESPUESTA:\n   {display_response}")
            print(f"   🛠️  Herramienta: {selected_tool}")
            print(f"   📊 Calidad: {outcome_quality:.2f}")
            print(f"   🧘 Consciencia: {consciousness_level:.2f}")
            print(f"   🌟 Resonancia: {archetypal_resonance}")
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
        
        print("   " + "="*60 + "\n")
        await asyncio.sleep(0.5)  # Pausa breve entre pruebas
    
    print("✅ === PRUEBA COMPLETADA - JOYAS ARQUETÍPICAS VERIFICADAS ===")

if __name__ == "__main__":
    asyncio.run(test_archetypal_gems())
