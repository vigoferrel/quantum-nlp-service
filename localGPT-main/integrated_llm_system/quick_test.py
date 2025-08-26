#!/usr/bin/env python3
"""
QUICK TEST - Prueba rapida del sistema integrado
"""

import asyncio
from integrate import LLMCore, AgentSystem

async def test_llm():
    print("Testing LLM Core...")
    llm = LLMCore()
    response = await llm.generate("Hola, esto es una prueba")
    print(f"LLM Response: {response[:100]}...")

def test_agents():
    print("Testing Agent System...")
    agents = AgentSystem()
    result = agents.create_agent("analyst", "Analizar requerimientos")
    print(f"Agent Result: {result}")

def main():
    print("=" * 40)
    print("QUICK TEST - INTEGRATED LLM SYSTEM")
    print("=" * 40)
    
    # Test LLM
    asyncio.run(test_llm())
    
    # Test Agents
    test_agents()
    
    print("\nTests completados!")

if __name__ == "__main__":
    main()
