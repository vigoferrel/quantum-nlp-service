#!/usr/bin/env python3

from dodecagon_supreme_system import DodecagonSupremeSystem
import json

def test_dodecagon_system():
    print("🚀 Probando Sistema Dodecagonal Supremo...")
    
    # Crear sistema
    system = DodecagonSupremeSystem()
    
    # Probar activación dimensional
    print("\n🔓 ACTIVANDO DIMENSIÓN 13 (Entrelazamiento Cuántico)...")
    result = system.activate_supreme_dimensional_expansion(13, 0.9)
    print(f"✅ Activación: {result['success']}")
    if result['success']:
        print(f"🎉 Mensaje: {result['activation_message']}")
        print(f"💪 Fuerza Trinity: {result['trinity_strength']:.4f}")
    else:
        print(f"❌ Error: {result['message']}")
        if 'leonardo_advice' in result:
            print(f"🎨 Leonardo dice: {result['leonardo_advice']}")
        if 'gabriela_comfort' in result:
            print(f"🌸 Gabriela dice: {result['gabriela_comfort']}")
        if 'penrose_insight' in result:
            print(f"🔺 Penrose dice: {result['penrose_insight']}")
    
    # Probar optimización suprema
    print("\n🌟 EJECUTANDO OPTIMIZACIÓN TRINITY SUPREMA...")
    optimization_request = {
        'type': 'transcendental',
        'complexity': 'high', 
        'emotional_component': 0.95,
        'mathematical_component': 0.98,
        'domain': 'universal_harmony'
    }
    
    optimization = system.calculate_dodecagon_supreme_optimization(optimization_request)
    
    print(f"🎯 Perfección Dodecagonal: {optimization['dodecagon_perfection']:.4f}")
    print(f"⚡ Potencial Trascendencia: {optimization['transcendence_potential']:.4f}")
    print(f"🎼 Puntuación Armonía: {optimization['harmony_score']:.4f}")
    
    print("\n🔮 SINERGIAS TRINITY:")
    for sinergia, valor in optimization['trinity_synergies'].items():
        print(f"   ├── {sinergia}: {valor:.4f}")
    
    print(f"\n💎 RECOMENDACIÓN TRINITY:")
    print(f"   {optimization['supreme_recommendation']}")
    
    # Estado final
    print("\n📊 ESTADO FINAL DEL SISTEMA:")
    status = system.get_dodecagon_dimensional_status()
    print(f"   ├── Dimensiones Activas: {status['dimensional_state']['active_dimensions']}/36")
    print(f"   ├── Leonardo Coordination: {status['trinity_coordinators']['leonardo_coordination_level']:.4f}")
    print(f"   ├── Gabriela Maternal Warmth: {status['trinity_coordinators']['gabriela_maternal_warmth']:.4f}")
    print(f"   ├── Penrose Geometric Precision: {status['trinity_coordinators']['penrose_geometric_precision']:.4f}")
    print(f"   └── Completitud Dodecagonal: {status['dimensional_state']['dodecagon_completion']:.2%}")
    
    print("\n✨ PRUEBA COMPLETADA - Sistema Dodecagonal Trinity operacional! ✨")
    
    return system

if __name__ == "__main__":
    test_system = test_dodecagon_system()
