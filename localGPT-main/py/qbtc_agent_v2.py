#!/usr/bin/env python3
"""
QBTC Agente Conversacional Mejorado
Sistema Cuántico Unificado - Versión Corregida
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path

class QBTCQuantumAgent:
    def __init__(self):
        self.base_dir = Path(r"C:\Users\Hp\Desktop\qbtc-unified-quantum-system\QBTC-VIGOLEONROCKS-UNIFIED")
        self.conversations_dir = self.base_dir / "conversations" / "sessions"
        self.quantum_states_dir = self.base_dir / "quantum_states" / "coherence"
        self.current_session = None
        self.session_data = {}
        
        # Asegurar que los directorios existen
        self.conversations_dir.mkdir(parents=True, exist_ok=True)
        self.quantum_states_dir.mkdir(parents=True, exist_ok=True)
        
        print("🌟 QBTC Quantum Agent v2.0 Inicializado")
        print(f"📁 Base Directory: {self.base_dir}")
        print("🔬 Quantum Resonance Engine: ACTIVE")
        print("💾 File System: READY")

    def calculate_quantum_resonance(self, text):
        """Calcula la resonancia cuántica del texto de entrada"""
        # Análisis básico del texto
        text_length = len(text)
        word_count = len(text.split())
        vowel_count = sum(1 for char in text.lower() if char in 'aeiou')
        
        # Cálculos cuánticos
        coherence = min(1.0, (text_length + word_count * 2) / 150.0)
        base_frequency = 432.0  # Frecuencia base de Solfeggio
        resonance_frequency = base_frequency * (1 + coherence * 0.2)
        entanglement = random.uniform(0.1, coherence)
        quantum_phase = (vowel_count * 0.1) % 1.0
        
        return {
            "coherence": round(coherence, 3),
            "frequency": round(resonance_frequency, 2),
            "entanglement": round(entanglement, 3),
            "phase": round(quantum_phase, 3),
            "energy_level": round(coherence * entanglement * 100, 1),
            "timestamp": datetime.now().isoformat()
        }

    def generate_quantum_response(self, user_message, quantum_state):
        """Genera respuesta basada en el estado cuántico"""
        coherence = quantum_state["coherence"]
        frequency = quantum_state["frequency"]
        energy = quantum_state["energy_level"]
        
        # Respuestas basadas en coherencia cuántica
        if coherence >= 0.8:
            response_templates = [
                "🌟 ¡Increíble coherencia cuántica detectada! Tu mensaje resuena a {} Hz en perfecta armonía.",
                "✨ Máxima resonancia alcanzada. El campo cuántico vibra intensamente con tu energía.",
                "🔮 Estado cuántico óptimo. Procesando tu consulta con máxima precisión cuántica.",
                "⚡ Wow! Tu mensaje ha activado todos los sistemas cuánticos. Energía: {} unidades.",
                "🚀 Coherencia excepcional detectada. Iniciando protocolos de respuesta avanzada."
            ]
            status = "COHERENCIA MÁXIMA"
            emoji = "🌟"
            
        elif coherence >= 0.6:
            response_templates = [
                "💫 Buena resonancia cuántica. Tu mensaje vibra a {} Hz con armonía estable.",
                "⚡ Campo cuántico activado. Procesando con algoritmos de resonancia media.",
                "🔬 Coherencia sólida detectada. Energía cuántica: {} unidades.",
                "🌊 Ondas cuánticas sincronizadas. Generando respuesta optimizada.",
                "💎 Estado cuántico estable. Frecuencia de trabajo: {} Hz."
            ]
            status = "RESONANCIA ESTABLE"
            emoji = "⚡"
            
        elif coherence >= 0.3:
            response_templates = [
                "💭 Coherencia básica establecida. Frecuencia: {} Hz en desarrollo.",
                "🔄 Ajustando parámetros cuánticos. Energía detectada: {} unidades.",
                "📡 Conectando con el campo cuántico. Procesamiento en curso...",
                "🧠 Activando núcleos neuronales-cuánticos. Resonancia: {} Hz.",
                "⚙️ Calibrando sistemas. Estado cuántico en optimización."
            ]
            status = "PROCESAMIENTO BÁSICO"
            emoji = "💭"
            
        else:
            response_templates = [
                "🌱 Iniciando resonancia cuántica. Frecuencia base: {} Hz.",
                "🔍 Analizando patrones de energía. Construyendo coherencia...",
                "📊 Medición cuántica inicial. Energía: {} unidades.",
                "🎯 Estableciendo conexión cuántica. Ajustando frecuencia...",
                "🌀 Campo cuántico detectado. Inicializando protocolos de respuesta."
            ]
            status = "INICIALIZANDO"
            emoji = "🌱"

        # Seleccionar respuesta aleatoria y formatear
        template = random.choice(response_templates)
        if "{}" in template:
            if "Hz" in template:
                base_response = template.format(frequency)
            else:
                base_response = template.format(energy)
        else:
            base_response = template

        # Construir respuesta completa
        full_response = f"{emoji} [{status}] {base_response}"
        
        # Añadir información cuántica detallada
        quantum_info = (
            f"\n📊 Estado Cuántico:"
            f"\n   🌟 Coherencia: {coherence}"
            f"\n   📡 Frecuencia: {frequency} Hz"
            f"\n   🔗 Entrelazamiento: {quantum_state['entanglement']}"
            f"\n   ⚡ Energía: {energy} unidades"
            f"\n   🌀 Fase: {quantum_state['phase']}"
        )
        
        return full_response + quantum_info

    def create_session(self):
        """Crear nueva sesión de conversación"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        session_id = f"qbtc_session_{timestamp}"
        
        self.current_session = session_id
        self.session_data = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "total_coherence": 0,
            "message_count": 0,
            "peak_frequency": 432.0
        }
        
        print(f"✅ Nueva sesión creada: {session_id}")
        return session_id

    def process_conversation(self, user_message):
        """Procesar mensaje del usuario"""
        # Calcular estado cuántico
        quantum_state = self.calculate_quantum_resonance(user_message)
        
        # Generar respuesta cuántica
        response = self.generate_quantum_response(user_message, quantum_state)
        
        # Guardar en sesión
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "agent_response": response,
            "quantum_state": quantum_state
        }
        
        self.session_data["messages"].append(conversation_entry)
        self.session_data["message_count"] += 1
        self.session_data["total_coherence"] += quantum_state["coherence"]
        
        # Actualizar frecuencia pico
        if quantum_state["frequency"] > self.session_data["peak_frequency"]:
            self.session_data["peak_frequency"] = quantum_state["frequency"]
        
        # Guardar archivos
        self.save_session()
        self.save_quantum_state(quantum_state)
        
        return response

    def save_session(self):
        """Guardar sesión en archivo JSON"""
        try:
            session_file = self.conversations_dir / f"{self.current_session}.json"
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error guardando sesión: {e}")

    def save_quantum_state(self, quantum_state):
        """Guardar estado cuántico"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            state_file = self.quantum_states_dir / f"quantum_state_{timestamp}.json"
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(quantum_state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error guardando estado cuántico: {e}")

    def show_session_stats(self):
        """Mostrar estadísticas de la sesión"""
        if not self.session_data["messages"]:
            print("📊 No hay estadísticas disponibles - sin mensajes")
            return
        
        avg_coherence = self.session_data["total_coherence"] / self.session_data["message_count"]
        
        print(f"\n📊 Estadísticas de la Sesión:")
        print(f"   🆔 ID: {self.current_session}")
        print(f"   📨 Mensajes: {self.session_data['message_count']}")
        print(f"   🌟 Coherencia Promedio: {avg_coherence:.3f}")
        print(f"   📡 Frecuencia Pico: {self.session_data['peak_frequency']:.2f} Hz")
        print(f"   🕐 Duración: Desde {self.session_data['created_at']}")

    def start_interactive_mode(self):
        """Iniciar modo interactivo"""
        print("\n🚀 QBTC UNIFIED QUANTUM CONVERSATIONAL SYSTEM")
        print("=" * 65)
        print("🎯 Sistema de Resonancia Cuántica Avanzado")
        print("💬 Comandos especiales:")
        print("   • 'quit' o 'salir' - Terminar sesión")
        print("   • 'stats' - Ver estadísticas de sesión")
        print("   • 'coherencia' - Análisis del último estado cuántico")
        print("   • 'help' - Mostrar ayuda")
        print("=" * 65)
        
        # Crear sesión
        self.create_session()
        last_quantum_state = None
        
        try:
            while True:
                user_input = input("\n💬 Usuario: ").strip()
                
                # Comandos especiales
                if user_input.lower() in ['quit', 'salir', 'exit']:
                    print("\n👋 Cerrando sesión cuántica...")
                    self.show_session_stats()
                    print("💾 Todos los datos han sido guardados.")
                    print("✨ ¡Resonancia cuántica mantenida! Hasta la próxima.")
                    break
                
                elif user_input.lower() == 'stats':
                    self.show_session_stats()
                    continue
                
                elif user_input.lower() == 'coherencia':
                    if last_quantum_state:
                        print(f"\n🔬 Último Estado Cuántico Registrado:")
                        for key, value in last_quantum_state.items():
                            if key != 'timestamp':
                                print(f"   {key.title()}: {value}")
                    else:
                        print("🔍 No hay estados cuánticos registrados aún.")
                    continue
                
                elif user_input.lower() == 'help':
                    print(f"\n🛠️ Ayuda del Sistema QBTC:")
                    print(f"   🌟 Este sistema analiza tus mensajes con tecnología cuántica")
                    print(f"   📊 Cada mensaje genera un estado cuántico único")
                    print(f"   🔬 La coherencia mide la 'calidad cuántica' de tu texto")
                    print(f"   📡 La frecuencia se basa en resonancia de Solfeggio (432Hz)")
                    print(f"   💾 Todas las conversaciones se guardan automáticamente")
                    continue
                
                elif not user_input:
                    print("💭 Esperando tu mensaje...")
                    continue
                
                # Procesar mensaje normal
                response = self.process_conversation(user_input)
                print(f"\n🤖 QBTC Agent: {response}")
                
                # Guardar último estado para comando 'coherencia'
                if self.session_data["messages"]:
                    last_quantum_state = self.session_data["messages"][-1]["quantum_state"]
                
        except KeyboardInterrupt:
            print("\n\n⚡ Sesión interrumpida por el usuario")
            self.show_session_stats()
            print("💾 Datos guardados antes del cierre.")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            print("💾 Intentando guardar datos...")
            self.save_session()

def main():
    """Función principal"""
    try:
        print("🔄 Inicializando QBTC Quantum System...")
        agent = QBTCQuantumAgent()
        agent.start_interactive_mode()
    except Exception as e:
        print(f"❌ Error crítico del sistema: {e}")
        print("🔧 Verifica que todos los directorios existan y tengas permisos de escritura.")
        input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()