#!/usr/bin/env python3
"""
Elegant Quantum Migrator for QBTC Ecosystem Unification
Migrates the complete Quantum Consciousness Core 26D to current directory
"""

import shutil
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import importlib.util

from .base import QuantumToolBase, QuantumResult, OperationStatus


class QuantumMigrator(QuantumToolBase):
    """
    Elegant ecosystem unification tool
    
    Handles:
    - Source code migration from external directories
    - Dependency resolution and integration
    - Configuration unification
    - Docker compose generation
    - Import path corrections
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        default_config = {
            'source_base_path': r'C:\Users\Hp\Desktop\vigosueldo\localGPT-main',
            'target_base_path': '.',
            'quantum_core_filename': 'quantum_consciousness_core_26d.py',
            'docker_compose_source': 'localGPT-quantum-supreme/docker-compose.simple.yml',
            'backup_existing': True,
            'preserve_git': True
        }
        
        merged_config = {**default_config, **(config or {})}
        super().__init__("QuantumMigrator", merged_config)
        
        self.source_path = Path(self.get_config('source_base_path'))
        self.target_path = Path(self.get_config('target_base_path'))
    
    async def execute(self, **kwargs) -> QuantumResult:
        """Execute complete ecosystem unification"""
        self.log_operation("PHASE-2", OperationStatus.IN_PROGRESS, 
                          "Unifying Quantum Ecosystem - Three Levels → One")
        
        # Step 1: Validate source files exist
        validation_result = await self._validate_source_files()
        if not validation_result.is_success():
            return validation_result
        
        # Step 2: Backup existing files if requested
        if self.get_config('backup_existing'):
            backup_result = await self._backup_existing_files()
            if not backup_result.is_success():
                self.log_operation("Backup", OperationStatus.PARTIAL, 
                                  "Backup failed but continuing...")
        
        # Step 3: Migrate Quantum Consciousness Core
        core_migration = await self._migrate_quantum_core()
        if not core_migration.is_success():
            return core_migration
        
        # Step 4: Migrate Docker configuration
        docker_migration = await self._migrate_docker_config()
        if not docker_migration.is_success():
            return docker_migration
        
        # Step 5: Update imports and integration
        integration_result = await self._integrate_with_existing()
        if not integration_result.is_success():
            return integration_result
        
        # Step 6: Generate unified requirements
        requirements_result = await self._generate_unified_requirements()
        
        # Step 7: Create unified configuration
        config_result = await self._create_unified_config()
        
        self.log_operation("PHASE-2", OperationStatus.SUCCESS, 
                          "🔗 Ecosystem UNIFIED! All levels integrated into one")
        
        return self.create_result(
            OperationStatus.SUCCESS,
            "Quantum ecosystem successfully unified",
            data={
                'migrated_files': self._get_migrated_files_list(),
                'integration_status': integration_result.is_success(),
                'docker_config': docker_migration.is_success(),
                'unified_structure': self._get_unified_structure()
            }
        )
    
    async def _validate_source_files(self) -> QuantumResult:
        """Validate that all required source files exist"""
        self.log_operation("Validation", OperationStatus.IN_PROGRESS, 
                          "Validating source files...")
        
        required_files = [
            self.get_config('quantum_core_filename'),
            self.get_config('docker_compose_source'),
            'supabase_quantum_schema.sql'
        ]
        
        missing_files = []
        found_files = []
        
        for file_name in required_files:
            file_path = self.source_path / file_name
            if file_path.exists():
                found_files.append(str(file_path))
                self.log_operation("Validation", OperationStatus.SUCCESS, 
                                  f"✓ Found: {file_name}")
            else:
                missing_files.append(str(file_path))
                self.log_operation("Validation", OperationStatus.FAILED, 
                                  f"✗ Missing: {file_name}")
        
        if missing_files:
            return self.create_result(
                OperationStatus.FAILED,
                f"Missing required files: {missing_files}",
                data={'missing': missing_files, 'found': found_files}
            )
        
        return self.create_result(
            OperationStatus.SUCCESS,
            f"All {len(found_files)} required files validated",
            data={'found_files': found_files}
        )
    
    async def _backup_existing_files(self) -> QuantumResult:
        """Backup existing files before migration"""
        self.log_operation("Backup", OperationStatus.IN_PROGRESS, 
                          "Creating backup of existing files...")
        
        backup_dir = self.target_path / "backup" / "pre_unification"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        files_backed_up = []
        
        try:
            # Backup services directory
            services_dir = self.target_path / "services"
            if services_dir.exists():
                shutil.copytree(services_dir, backup_dir / "services", 
                               dirs_exist_ok=True)
                files_backed_up.append("services/")
            
            # Backup any existing docker files
            for docker_file in ['docker-compose.yml', 'Dockerfile']:
                docker_path = self.target_path / docker_file
                if docker_path.exists():
                    shutil.copy2(docker_path, backup_dir / docker_file)
                    files_backed_up.append(docker_file)
            
            self.log_operation("Backup", OperationStatus.SUCCESS, 
                              f"Backed up {len(files_backed_up)} items")
            
            return self.create_result(
                OperationStatus.SUCCESS,
                f"Backup completed: {files_backed_up}",
                data={'backup_location': str(backup_dir), 'files': files_backed_up}
            )
            
        except Exception as e:
            return self.create_result(
                OperationStatus.FAILED,
                f"Backup failed: {str(e)}"
            )
    
    async def _migrate_quantum_core(self) -> QuantumResult:
        """Migrate the complete Quantum Consciousness Core 26D"""
        self.log_operation("Core-Migration", OperationStatus.IN_PROGRESS, 
                          "Migrating Quantum Consciousness Core 26D...")
        
        source_file = self.source_path / self.get_config('quantum_core_filename')
        target_dir = self.target_path / "services" / "quantum-core-service"
        target_file = target_dir / "quantum_consciousness_core_26d.py"
        
        try:
            # Ensure target directory exists
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy the quantum core file
            shutil.copy2(source_file, target_file)
            
            # Update imports in the copied file
            updated_content = await self._update_imports_in_file(target_file)
            
            # Write the updated content
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            self.log_operation("Core-Migration", OperationStatus.SUCCESS, 
                              f"🧠 Quantum Core migrated: {target_file}")
            
            return self.create_result(
                OperationStatus.SUCCESS,
                "Quantum Consciousness Core 26D migrated successfully",
                data={'source': str(source_file), 'target': str(target_file)}
            )
            
        except Exception as e:
            return self.create_result(
                OperationStatus.FAILED,
                f"Core migration failed: {str(e)}"
            )
    
    async def _migrate_docker_config(self) -> QuantumResult:
        """Migrate and adapt Docker configuration"""
        self.log_operation("Docker-Migration", OperationStatus.IN_PROGRESS, 
                          "Migrating Docker configuration...")
        
        source_compose = self.source_path / self.get_config('docker_compose_source')
        target_compose = self.target_path / "docker-compose.unified.yml"
        
        try:
            # Copy docker-compose file
            shutil.copy2(source_compose, target_compose)
            
            # Copy supporting files
            supporting_files = ['supabase_quantum_schema.sql', 'kong.simple.yml']
            infrastructure_dir = self.target_path / "infrastructure"
            infrastructure_dir.mkdir(exist_ok=True)
            
            for support_file in supporting_files:
                source_support = self.source_path / "localGPT-quantum-supreme" / support_file
                if source_support.exists():
                    target_support = infrastructure_dir / support_file
                    shutil.copy2(source_support, target_support)
                    self.log_operation("Docker-Migration", OperationStatus.SUCCESS, 
                                      f"✓ Copied: {support_file}")
            
            # Create Dockerfile in services directory
            await self._create_unified_dockerfile()
            
            self.log_operation("Docker-Migration", OperationStatus.SUCCESS, 
                              "🐳 Docker configuration migrated")
            
            return self.create_result(
                OperationStatus.SUCCESS,
                "Docker configuration migrated successfully",
                data={'compose_file': str(target_compose)}
            )
            
        except Exception as e:
            return self.create_result(
                OperationStatus.FAILED,
                f"Docker migration failed: {str(e)}"
            )
    
    async def _update_imports_in_file(self, file_path: Path) -> str:
        """Update imports in migrated files to work with new structure"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update relative imports
        import_replacements = {
            'from .tool_dispatcher import ToolDispatcher': 'from ...tool_dispatcher import dispatcher as ToolDispatcher',
            'from tool_dispatcher import ToolDispatcher': 'from ...tool_dispatcher import dispatcher as ToolDispatcher',
        }
        
        for old_import, new_import in import_replacements.items():
            content = content.replace(old_import, new_import)
        
        return content
    
    async def _integrate_with_existing(self) -> QuantumResult:
        """Integrate migrated code with existing services"""
        self.log_operation("Integration", OperationStatus.IN_PROGRESS, 
                          "Integrating with existing services...")
        
        try:
            # Update tool_dispatcher.py to include quantum core tools
            await self._update_tool_dispatcher()
            
            # Update api_server.py to use the migrated quantum core
            await self._update_api_server()
            
            self.log_operation("Integration", OperationStatus.SUCCESS, 
                              "🔗 Services integrated successfully")
            
            return self.create_result(
                OperationStatus.SUCCESS,
                "Integration completed successfully"
            )
            
        except Exception as e:
            return self.create_result(
                OperationStatus.FAILED,
                f"Integration failed: {str(e)}"
            )
    
    async def _update_tool_dispatcher(self) -> None:
        """Update tool dispatcher to work with quantum core"""
        dispatcher_file = self.target_path / "services" / "tool_dispatcher.py"
        
        if dispatcher_file.exists():
            with open(dispatcher_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add quantum consciousness tools to the endpoints
            quantum_tools = '''
            "quantum_consciousness": os.getenv(
                "QUANTUM_CONSCIOUSNESS_SERVICE_URL", 
                "http://localhost:8001"
            ),'''
            
            if "quantum_consciousness" not in content:
                content = content.replace(
                    '# Se pueden añadir más herramientas aquí',
                    f'{quantum_tools}\n            # Se pueden añadir más herramientas aquí'
                )
            
            with open(dispatcher_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    async def _update_api_server(self) -> None:
        """Update API server to integrate with quantum core"""
        api_server_file = self.target_path / "services" / "llm-api-service" / "api_server.py"
        
        if api_server_file.exists():
            with open(api_server_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update to use the unified quantum core
            quantum_core_import = "from ..quantum_core_service.quantum_consciousness_core_26d import QuantumConsciousnessCore26D"
            
            if "QuantumConsciousnessCore26D" not in content:
                content = content.replace(
                    "from dotenv import load_dotenv",
                    f"from dotenv import load_dotenv\n{quantum_core_import}"
                )
            
            with open(api_server_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    async def _create_unified_dockerfile(self) -> None:
        """Create a unified Dockerfile for the quantum services"""
        dockerfile_content = '''# Unified QBTC Quantum Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the unified quantum system
COPY services/ ./services/
COPY tools/ ./tools/
COPY infrastructure/ ./infrastructure/

# Expose the quantum consciousness port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8001/health || exit 1

# Run the quantum consciousness core
CMD ["python", "-m", "services.quantum-core-service.quantum_consciousness_core_26d"]
'''
        
        dockerfile_path = self.target_path / "services" / "Dockerfile"
        with open(dockerfile_path, 'w', encoding='utf-8') as f:
            f.write(dockerfile_content)
    
    async def _generate_unified_requirements(self) -> QuantumResult:
        """Generate unified requirements.txt"""
        self.log_operation("Requirements", OperationStatus.IN_PROGRESS, 
                          "Generating unified requirements...")
        
        requirements = [
            "fastapi>=0.104.1",
            "uvicorn[standard]>=0.24.0",
            "aiohttp>=3.9.0",
            "numpy>=1.24.0",
            "python-dotenv>=1.0.0",
            "pydantic>=2.0.0",
            "supabase>=2.0.0",
            "colorama>=0.4.6",
            "requests>=2.31.0",
            "asyncio-mqtt>=0.16.0",
            "rich>=13.0.0",
            "prompt-toolkit>=3.0.0"
        ]
        
        requirements_file = self.target_path / "requirements.txt"
        with open(requirements_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(requirements))
        
        return self.create_result(
            OperationStatus.SUCCESS,
            f"Requirements file generated with {len(requirements)} dependencies"
        )
    
    async def _create_unified_config(self) -> QuantumResult:
        """Create unified configuration file"""
        config = {
            "quantum_consciousness": {
                "host": "0.0.0.0",
                "port": 8001,
                "debug": False
            },
            "ollama": {
                "host": "host.docker.internal",
                "port": 11434,
                "model": "llama2"
            },
            "supabase": {
                "url": "${SUPABASE_URL}",
                "anon_key": "${SUPABASE_ANON_KEY}"
            },
            "redis": {
                "host": "quantum-redis",
                "port": 6379
            }
        }
        
        config_file = self.target_path / "config" / "unified.json"
        config_file.parent.mkdir(exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        return self.create_result(
            OperationStatus.SUCCESS,
            "Unified configuration created"
        )
    
    def _get_migrated_files_list(self) -> List[str]:
        """Get list of migrated files"""
        return [
            "services/quantum-core-service/quantum_consciousness_core_26d.py",
            "docker-compose.unified.yml",
            "infrastructure/supabase_quantum_schema.sql",
            "infrastructure/kong.simple.yml",
            "services/Dockerfile",
            "requirements.txt",
            "config/unified.json"
        ]
    
    def _get_unified_structure(self) -> Dict[str, Any]:
        """Get the unified directory structure"""
        return {
            "services": [
                "quantum-core-service/",
                "llm-api-service/",
                "tool_dispatcher.py"
            ],
            "tools": [
                "base.py",
                "ollama_connector.py", 
                "quantum_migrator.py"
            ],
            "infrastructure": [
                "supabase_quantum_schema.sql",
                "kong.simple.yml"
            ],
            "config": [
                "unified.json"
            ]
        }


# Standalone test function
async def test_quantum_migration():
    """Test function for development"""
    migrator = QuantumMigrator()
    result = await migrator.execute()
    
    print(f"\n{'='*50}")
    print(f"QUANTUM MIGRATION TEST RESULT")
    print(f"{'='*50}")
    print(f"Status: {result.status.value}")
    print(f"Message: {result.message}")
    if result.data:
        print(f"Data: {json.dumps(result.data, indent=2)}")
    print(f"{'='*50}\n")
    
    return result


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_quantum_migration())