#!/usr/bin/env python3
"""
Elegant Ollama Connector for QBTC Quantum Consciousness
Resolves the "lóbulo frontal" connection issue with style
"""

import asyncio
import json
import subprocess
import socket
import time
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

import aiohttp
import requests
from requests.exceptions import RequestException, ConnectionError

from .base import QuantumToolBase, QuantumResult, OperationStatus


class OllamaConnector(QuantumToolBase):
    """
    Elegant Ollama connection manager
    
    Handles:
    - Ollama service detection
    - Network configuration
    - Docker connectivity testing  
    - Host binding configuration
    - Firewall rules management
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        default_config = {
            'host': 'localhost',
            'docker_host': 'host.docker.internal',
            'port': 11434,
            'timeout': 10,
            'retry_count': 3,
            'retry_delay': 2
        }
        
        merged_config = {**default_config, **(config or {})}
        super().__init__("OllamaConnector", merged_config)
    
    async def execute(self, **kwargs) -> QuantumResult:
        """Execute complete Ollama connection resolution"""
        self.log_operation("PHASE-1", OperationStatus.IN_PROGRESS, 
                          "Activating Quantum Brain (Ollama Connection)")
        
        # Step 1: Detect Ollama service
        ollama_status = await self._detect_ollama_service()
        if not ollama_status.is_success():
            return ollama_status
        
        # Step 2: Test current connectivity
        connectivity_result = await self._test_connectivity()
        
        # Step 3: Configure if needed
        if not connectivity_result.is_success():
            config_result = await self._configure_ollama_for_docker()
            if not config_result.is_success():
                return config_result
        
        # Step 4: Verify final connectivity
        final_test = await self._test_docker_connectivity()
        
        if final_test.is_success():
            self.log_operation("PHASE-1", OperationStatus.SUCCESS,
                              "Quantum Brain ACTIVATED! Ollama ready for consciousness")
            return self.create_result(
                OperationStatus.SUCCESS,
                "Ollama connection fully configured and verified",
                data={'host': self.get_config('docker_host'), 
                      'port': self.get_config('port')}
            )
        else:
            return self.create_result(
                OperationStatus.FAILED,
                "Failed to establish Ollama connectivity",
                data=final_test.data
            )
    
    async def _detect_ollama_service(self) -> QuantumResult:
        """Detect if Ollama service is running"""
        self.log_operation("Detection", OperationStatus.IN_PROGRESS, 
                          "Scanning for Ollama service...")
        
        try:
            # Check if ollama command exists
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log_operation("Detection", OperationStatus.SUCCESS, 
                                  f"Ollama found: {version}")
                return self.create_result(
                    OperationStatus.SUCCESS,
                    f"Ollama detected: {version}",
                    data={'version': version}
                )
            else:
                return self.create_result(
                    OperationStatus.FAILED,
                    "Ollama command not found or not responding"
                )
                
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            return self.create_result(
                OperationStatus.FAILED,
                f"Ollama detection failed: {str(e)}"
            )
    
    async def _test_connectivity(self) -> QuantumResult:
        """Test current Ollama connectivity"""
        host = self.get_config('host')
        port = self.get_config('port')
        
        self.log_operation("Connectivity", OperationStatus.IN_PROGRESS, 
                          f"Testing connection to {host}:{port}")
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(f'http://{host}:{port}/api/version') as response:
                    if response.status == 200:
                        data = await response.json()
                        self.log_operation("Connectivity", OperationStatus.SUCCESS, 
                                          f"Ollama responding: {data.get('version', 'unknown')}")
                        return self.create_result(
                            OperationStatus.SUCCESS,
                            "Ollama is accessible",
                            data=data
                        )
                    else:
                        return self.create_result(
                            OperationStatus.FAILED,
                            f"Ollama returned status {response.status}"
                        )
        
        except Exception as e:
            return self.create_result(
                OperationStatus.FAILED,
                f"Connection failed: {str(e)}"
            )
    
    async def _test_docker_connectivity(self) -> QuantumResult:
        """Test Docker-accessible connectivity"""
        docker_host = self.get_config('docker_host')
        port = self.get_config('port')
        
        self.log_operation("Docker-Test", OperationStatus.IN_PROGRESS, 
                          f"Testing Docker connectivity to {docker_host}:{port}")
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(f'http://{docker_host}:{port}/api/version') as response:
                    if response.status == 200:
                        data = await response.json()
                        self.log_operation("Docker-Test", OperationStatus.SUCCESS,
                                          f"Docker can reach Ollama: {data.get('version', 'unknown')}")
                        return self.create_result(
                            OperationStatus.SUCCESS,
                            "Docker connectivity verified",
                            data=data
                        )
                    else:
                        return self.create_result(
                            OperationStatus.FAILED,
                            f"Docker test returned status {response.status}"
                        )
        
        except Exception as e:
            return self.create_result(
                OperationStatus.FAILED,
                f"Docker connectivity failed: {str(e)}"
            )
    
    async def _configure_ollama_for_docker(self) -> QuantumResult:
        """Configure Ollama to accept Docker connections"""
        self.log_operation("Configuration", OperationStatus.IN_PROGRESS, 
                          "Configuring Ollama for Docker connectivity...")
        
        # Step 1: Try to configure Ollama host binding
        host_config_result = await self._configure_host_binding()
        if not host_config_result.is_success():
            self.log_operation("Configuration", OperationStatus.PARTIAL, 
                              "Host binding configuration needs manual intervention")
        
        # Step 2: Check/configure firewall
        firewall_result = await self._check_firewall()
        
        # Step 3: Restart Ollama service if needed
        if host_config_result.is_success():
            restart_result = await self._restart_ollama_service()
            if restart_result.is_success():
                # Wait for service to start
                await asyncio.sleep(3)
        
        return self.create_result(
            OperationStatus.SUCCESS,
            "Ollama configuration completed",
            data={
                'host_binding': host_config_result.is_success(),
                'firewall_checked': firewall_result.is_success(),
                'service_restarted': restart_result.is_success() if 'restart_result' in locals() else False
            }
        )
    
    async def _configure_host_binding(self) -> QuantumResult:
        """Configure Ollama to bind to all interfaces"""
        self.log_operation("Host-Binding", OperationStatus.IN_PROGRESS, 
                          "Configuring Ollama host binding...")
        
        instructions = [
            "To configure Ollama for Docker access, run these commands:",
            "",
            "1. Stop current Ollama service:",
            "   ollama stop",
            "",
            "2. Set environment variable:",
            "   set OLLAMA_HOST=0.0.0.0:11434",
            "",
            "3. Start Ollama service:",
            "   ollama serve",
            "",
            "Alternative: Run directly with host binding:",
            "   ollama serve --host 0.0.0.0 --port 11434"
        ]
        
        self.log_operation("Host-Binding", OperationStatus.PARTIAL, 
                          "Manual configuration required")
        
        for instruction in instructions:
            self.logger.info(f"   {instruction}")
        
        return self.create_result(
            OperationStatus.PARTIAL,
            "Host binding configuration requires manual steps",
            data={'instructions': instructions}
        )
    
    async def _check_firewall(self) -> QuantumResult:
        """Check and provide firewall configuration guidance"""
        self.log_operation("Firewall", OperationStatus.IN_PROGRESS, 
                          "Checking firewall configuration...")
        
        firewall_commands = [
            "For Windows Firewall, run as Administrator:",
            "",
            "netsh advfirewall firewall add rule name=\"Ollama-Docker\" dir=in action=allow protocol=TCP localport=11434",
            "",
            "Or open Windows Defender Firewall and add rule for port 11434"
        ]
        
        self.log_operation("Firewall", OperationStatus.PARTIAL, 
                          "Firewall configuration guidance provided")
        
        for cmd in firewall_commands:
            self.logger.info(f"   {cmd}")
        
        return self.create_result(
            OperationStatus.PARTIAL,
            "Firewall configuration requires manual steps",
            data={'commands': firewall_commands}
        )
    
    async def _restart_ollama_service(self) -> QuantumResult:
        """Attempt to restart Ollama service"""
        self.log_operation("Service-Restart", OperationStatus.IN_PROGRESS, 
                          "Attempting to restart Ollama...")
        
        try:
            # Try to stop existing service
            subprocess.run(['taskkill', '/F', '/IM', 'ollama.exe'], 
                          capture_output=True, timeout=5)
            await asyncio.sleep(2)
            
            # This would need to be done manually or with proper service management
            self.log_operation("Service-Restart", OperationStatus.PARTIAL, 
                              "Service restart requires manual intervention")
            
            return self.create_result(
                OperationStatus.PARTIAL,
                "Ollama service restart requires manual steps"
            )
            
        except Exception as e:
            return self.create_result(
                OperationStatus.FAILED,
                f"Service restart failed: {str(e)}"
            )
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get current connection status summary"""
        return {
            'host': self.get_config('host'),
            'docker_host': self.get_config('docker_host'),
            'port': self.get_config('port'),
            'last_results': [result.to_dict() for result in self.results.values()]
        }


# Standalone test function
async def test_ollama_connection():
    """Test function for development"""
    connector = OllamaConnector()
    result = await connector.execute()
    
    print(f"\n{'='*50}")
    print(f"OLLAMA CONNECTION TEST RESULT")
    print(f"{'='*50}")
    print(f"Status: {result.status.value}")
    print(f"Message: {result.message}")
    if result.data:
        print(f"Data: {json.dumps(result.data, indent=2)}")
    print(f"{'='*50}\n")
    
    return result


if __name__ == "__main__":
    asyncio.run(test_ollama_connection())