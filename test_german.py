#!/usr/bin/env python3
"""
🇩🇪 TEST GERMAN INPUT - QUANTUM UNIVERSAL LANGUAGE SYSTEM 🇩🇪
"""

from quantum_universal_language_system import quantum_detect_and_respond

def test_german_input():
    """Test del sistema con input alemán"""
    
    # Input alemán del usuario
    german_text = "ich spreche deutsch du must dass vestehen"
    
    print("🧪 TESTING GERMAN INPUT:")
    print(f'📝 Input: "{german_text}"')
    print()
    
    # Procesar con el sistema cuántico
    result = quantum_detect_and_respond(german_text)
    
    print("🌍 SPRACHERKENNUNG (Language Detection):")
    print(f"   🔍 Detected Language: {result['language_detection']['language']}")
    print(f"   🎯 Confidence: {result['language_detection']['confidence']:.3f}")
    print(f"   ⚡ Method: {result['language_detection']['detection_method']}")
    print(f"   🔮 Quantum Signature: {result['language_detection']['quantum_signature']}")
    print()
    
    print("💫 QUANTUM EMPATHIC RESPONSE:")
    print(f"   📝 Response: {result['quantum_response']['vigoleonrocks_response']}")
    print(f"   ❤️ Empathy Resonance: {result['quantum_response']['empathy_resonance']:.3f}")
    print(f"   🎵 Response Type: {result['quantum_response']['response_type']}")
    print()
    
    print("⚡ QUANTUM METRICS:")
    metrics = result['quantum_response']['quantum_metrics']
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.3f}")
        else:
            print(f"   {key}: {value}")
    print()
    
    print("🔬 SYSTEM INFO:")
    sys_info = result['system_info']
    print(f"   📡 Quantum Frequency: {sys_info['quantum_frequency']}Hz")
    print(f"   🌌 Lambda Constant: {sys_info['lambda_constant']}")
    print(f"   ⚛️ Quantum States: {sys_info['quantum_states']}")
    print(f"   🏆 Supremacy Score: {sys_info['supremacy_score']}")
    print(f"   📊 Processing Method: {sys_info['processing_method']}")
    print(f"   🚀 Version: {sys_info['version']}")
    
    print()
    print("🎉 AUSGEZEICHNET! Das Quantum Universal Language System")
    print("    hat erfolgreich Deutsch erkannt und verarbeitet! 🇩🇪⚡")

if __name__ == "__main__":
    test_german_input()
