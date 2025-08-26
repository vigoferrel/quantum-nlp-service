#!/usr/bin/env python3
"""
QBTC Agente Conversacional
Sistema Cuántico Unificado
"""

import os
import json
from datetime import datetime
from pathlib import Path
import random

class QBTCAgent:
            def __init__(self):
                                self.base_dir = Path(r"C:\Users\Hp\Desktop\qbtc-unified-quantum-system\QBTC-VIGOLEONROCKS-UNIFIED")
                                        self.conversations_dir = self.base_dir / "conversations" / "sessions"
                                                self.quantum_states_dir = self.base_dir / "quantum_states" / "coherence"
                                                        self.sessions = {}
                                                                print(" QBTC Agent inicializado")
                                                                        print(f" Base: {self.base_dir}")
                                                                            
    def quantum_resonance(self, text):
                        """Calcula la resonancia cuántica del texto"""
                                length = len(text)
                                        coherence = min(1.0, length / 100.0)
                                                frequency = 432.0 * (1 + coherence * 0.1)
                                                        entanglement = random.random() * coherence
                                                                
        return {
                    "coherence": coherence,
                                "frequency": frequency,
                                            "entanglement": entanglement,
                                                        "timestamp": datetime.now().isoformat()
                                                                }
                                                                    
    def create_session(self, user_id="demo_user"):
                        session_id = f"qbtc_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                                self.sessions[session_id] = {
                                            "user_id": user_id,
                                                        "messages": [],
                                                                    "created_at": datetime.now().isoformat(),
                                                                                "quantum_state": {"coherence": 0.5}
                                                                                        }
                                                                                                print(f" Sesión creada: {session_id}")
                                                                                                        return session_id
                                                                                                            
    def process_message(self, session_id, message):
                        if session_id not in self.sessions:
                                                return " Sesión no encontrada"
                                                        
        # Calcular resonancia cuántica
                quantum_state = self.quantum_resonance(message)
                        
        # Generar respuesta basada en coherencia
                if quantum_state["coherence"] > 0.8:
                                        responses = [
                                                        " Detectando alta coherencia cuántica en tu mensaje!",
                                                                        " Tu energía textual resuena perfectamente con el campo cuántico",
                                                                                        " Procesamiento cuántico avanzado activado",
                                                                                                        " Resonancia óptima alcanzada - respuesta mejorada"
                                                                                                                    ]
                                                                                                                                prefix = " [COHERENCIA ALTA] "
                                                                                                                                        elif quantum_state["coherence"] > 0.5:
                                                                                                                                                                responses = [
                                                                                                                                                                                " Resonancia cuántica detectada",
                                                                                                                                                                                                " Procesando en el núcleo cuántico QBTC",
                                                                                                                                                                                                                " Analizando patrones de energía textual",
                                                                                                                                                                                                                                " Ondas cuánticas sincronizadas"
                                                                                                                                                                                                                                            ]
                                                                                                                                                                                                                                                        prefix = " [RESONANCIA MEDIA] "
                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                        responses = [
                                                                                                                                                                                                                                                                                                        " Iniciando procesamiento cuántico básico",
                                                                                                                                                                                                                                                                                                                        " Ajustando frecuencia de resonancia",
                                                                                                                                                                                                                                                                                                                                        " Conectando con el campo cuántico",
                                                                                                                                                                                                                                                                                                                                                        " Procesamiento neuronal-cuántico activado"
                                                                                                                                                                                                                                                                                                                                                                    ]
                                                                                                                                                                                                                                                                                                                                                                                prefix = " [PROCESANDO] "
                                                                                                                                                                                                                                                                                                                                                                                        
        base_response = random.choice(responses)
                enhanced_response = f"{prefix}{base_response}"
                        
        # Agregar información cuántica
                quantum_info = f"\n Coherencia: {quantum_state['coherence']:.3f} | Frecuencia: {quantum_state['frequency']:.1f} Hz"
                        final_response = enhanced_response + quantum_info
                                
        # Guardar conversación
                conversation_entry = {
                            "user": message,
                                        "agent": final_response,
                                                    "quantum_state": quantum_state,
                                                                "timestamp": datetime.now().isoformat()
                                                                        }
                                                                                
        self.sessions[session_id]["messages"].append(conversation_entry)
                self.sessions[session_id]["quantum_state"] = quantum_state
                        
        # Guardar en archivo
                self.save_session(session_id)
                        self.save_quantum_state(session_id, quantum_state)
                                
        return final_response
            
    def save_session(self, session_id):
                        try:
                                                session_file = self.conversations_dir / f"{session_id}.json"
                                                            session_file.parent.mkdir(parents=True, exist_ok=True)
                                                                        
            with open(session_file, 'w', encoding='utf-8') as f:
                                        json.dump(self.sessions[session_id], f, indent=2, ensure_ascii=False)
                                                except Exception as e:
                                                                        print(f" Error guardando sesión: {e}")
                                                                            
    def save_quantum_state(self, session_id, quantum_state):
                        try:
                                                state_file = self.quantum_states_dir / f"{session_id}_quantum.json"
                                                            state_file.parent.mkdir(parents=True, exist_ok=True)
                                                                        
            with open(state_file, 'w', encoding='utf-8') as f:
                                        json.dump(quantum_state, f, indent=2, ensure_ascii=False)
                                                except Exception as e:
                                                                        print(f" Error guardando estado cuántico: {e}")
                                                                            
    def get_session_info(self, session_id):
                        if session_id in self.sessions:
                                                session = self.sessions[session_id]
                                                            return {
                                                                            "session_id": session_id,
                                                                                            "messages_count": len(session["messages"]),
                                                                                                            "coherence": session["quantum_state"].get("coherence", 0),
                                                                                                                            "created_at": session["created_at"]
                                                                                                                                        }
                                                                                                                                                return None
                                                                                                                                                    
    def start_interactive_mode(self):
                        print("\n QBTC Unified Quantum Conversational System")
                                print("=" * 60)
                                        print(" Comandos disponibles:")
                                                print("  - 'quit' o 'salir': Terminar sesión")
                                                        print("  - 'status': Ver información de la sesión")
                                                                print("  - 'coherencia': Ver estado cuántico actual")
                                                                        print("=" * 60)
                                                                                
        # Crear sesión
                session_id = self.create_session()
                        
        while True:
                                try:
                                                            user_input = input("\n Tú: ").strip()
                                                                            
                if user_input.lower() in ['quit', 'salir', 'exit']:
                                                print(" ¡Hasta luego! Resonancia cuántica mantenida.")
                                                                    print(f" Sesión guardada: {session_id}")
                                                                                        break
                                                                                                        
                if user_input.lower() == 'status':
                                                info = self.get_session_info(session_id)
                                                                    if info:
                                                                                                        print(f"\n Estado de la Sesión:")
                                                                                                                                print(f"    ID: {info['session_id']}")
                                                                                                                                                        print(f"    Mensajes: {info['messages_count']}")
                                                                                                                                                                                print(f"    Coherencia: {info['coherence']:.3f}")
                                                                                                                                                                                                        print(f"    Creada: {info['created_at']}")
                                                                                                                                                                                                                            continue
                                                                                                                                                                                                                                            
                if user_input.lower() == 'coherencia':
                                                session = self.sessions[session_id]
                                                                    state = session["quantum_state"]
                                                                                        print(f"\n Estado Cuántico Actual:")
                                                                                                            print(f"    Coherencia: {state.get('coherence', 0):.3f}")
                                                                                                                                print(f"    Frecuencia: {state.get('frequency', 432):.1f} Hz")
                                                                                                                                                    print(f"    Entrelazamiento: {state.get('entanglement', 0):.3f}")
                                                                                                                                                                        continue
                                                                                                                                                                                        
                if not user_input:
                                                continue
                                                                
                # Procesar mensaje
                                response = self.process_message(session_id, user_input)
                                                print(f"\n QBTC: {response}")
                                                                
            except KeyboardInterrupt:
                                        print("\n\n Sesión interrumpida por el usuario.")
                                                        break
                                                                    except Exception as e:
                                                                                                print(f" Error: {e}")
                                                                                                
def main():
                try:
                                    print(" Inicializando sistema QBTC...")
                                            agent = QBTCAgent()
                                                    agent.start_interactive_mode()
                                                        except Exception as e:
                                                                            print(f" Error crítico: {e}")
                                                                                    input("Presiona Enter para salir...")
                                                                                    
if __name__ == "__main__":
                main()
                