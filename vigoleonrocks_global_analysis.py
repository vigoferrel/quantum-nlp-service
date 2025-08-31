#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
██╗   ██╗██╗ ██████╗  ██████╗ ██╗     ███████╗ ██████╗ ███╗   ██╗██████╗  ██████╗  ██████╗██╗  ██╗███████╗
██║   ██║██║██╔════╝ ██╔═══██╗██║     ██╔════╝██╔═══██╗████╗  ██║██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝
██║   ██║██║██║  ███╗██║   ██║██║     █████╗  ██║   ██║██╔██╗ ██║██████╔╝██║   ██║██║     █████╔╝ ███████╗
╚██╗ ██╔╝██║██║   ██║██║   ██║██║     ██╔══╝  ██║   ██║██║╚██╗██║██╔══██╗██║   ██║██║     ██╔═██╗ ╚════██║
 ╚████╔╝ ██║╚██████╔╝╚██████╔╝███████╗███████╗╚██████╔╝██║ ╚████║██║  ██║╚██████╔╝╚██████╗██║  ██╗███████║
  ╚═══╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝

ANÁLISIS GLOBAL COMPLETO DE SUBDIRECTORIOS - VIGOLEONROCKS PROJECT
Sistema de análisis arquitectónico completo para el panorama global del proyecto
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional, Set, Union
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import traceback


@dataclass
class DirectoryAnalysis:
    """Análisis completo de un directorio"""
    name: str
    path: str
    file_count: int
    subdirectory_count: int
    total_lines: int
    file_types: Dict[str, int]
    primary_languages: List[str]
    key_files: List[str]
    purpose: str
    architecture_level: str
    dependencies: List[str]
    integration_points: List[str]


@dataclass
class ProjectArchitecture:
    """Arquitectura completa del proyecto"""
    root_analysis: DirectoryAnalysis
    subdirectories: List[DirectoryAnalysis]
    technology_stack: Dict[str, List[str]]
    integration_map: Dict[str, List[str]]
    complexity_metrics: Dict[str, Any]
    architectural_patterns: List[str]
    deployment_structure: Dict[str, Any]


class VigoleonrocksGlobalAnalyzer:
    """
    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                    VIGOLEONROCKS GLOBAL ARCHITECTURAL ANALYZER                       ║
    ║                            PANORAMA COMPLETO DEL PROYECTO                            ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝
    
    Analizador arquitectónico completo que examina:
    1. Estructura completa de directorios
    2. Patrones arquitectónicos y tecnológicos
    3. Integraciones y dependencias
    4. Métricas de complejidad
    5. Patrones de deployment y configuración
    """

    def __init__(self, target_directory: str = "."):
        self.target_dir = Path(target_directory).resolve()
        self.analysis_results = {}
        self.directory_analyses = []
        self.technology_patterns = {
            'python': ['.py'],
            'javascript': ['.js', '.ts', '.jsx', '.tsx'],
            'web': ['.html', '.css', '.php'],
            'config': ['.json', '.yml', '.yaml', '.toml', '.ini', '.env'],
            'docker': ['Dockerfile', 'docker-compose.yml', '.dockerignore'],
            'markdown': ['.md', '.rst'],
            'shell': ['.sh', '.bat', '.ps1'],
            'database': ['.sql', '.db', '.sqlite'],
            'compiled': ['.c', '.h', '.cpp', '.hpp'],
            'package': ['package.json', 'requirements.txt', 'pyproject.toml', 'setup.py']
        }
        
        print(self._generate_ascii_header())
        print(f"🎯 DIRECTORIO RAÍZ: {self.target_dir}")
        print(f"🕒 ANÁLISIS INICIADO: {datetime.now().isoformat()}")
        print("=" * 100)

    def _generate_ascii_header(self) -> str:
        """Header ASCII para el análisis global"""
        return """
╔══════════════════════════════════════════════════════════════════════════════════════════╗
║   ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗         █████╗ ███╗   ██╗ █████╗ ██╗     ║
║  ██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║        ██╔══██╗████╗  ██║██╔══██╗██║     ║
║  ██║  ███╗██║     ██║   ██║██████╔╝███████║██║        ███████║██╔██╗ ██║███████║██║     ║
║  ██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║        ██╔══██║██║╚██╗██║██╔══██║██║     ║
║  ╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗   ██║  ██║██║ ╚████║██║  ██║███████╗║
║   ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝║
║                                                                                          ║
║  ██╗   ██╗██╗ ██████╗  ██████╗ ██╗     ███████╗ ██████╗ ███╗   ██╗██████╗  ██████╗      ║
║  ██║   ██║██║██╔════╝ ██╔═══██╗██║     ██╔════╝██╔═══██╗████╗  ██║██╔══██╗██╔═══██╗     ║
║  ██║   ██║██║██║  ███╗██║   ██║██║     █████╗  ██║   ██║██╔██╗ ██║██████╔╝██║   ██║     ║
║  ╚██╗ ██╔╝██║██║   ██║██║   ██║██║     ██╔══╝  ██║   ██║██║╚██╗██║██╔══██╗██║   ██║     ║
║   ╚████╔╝ ██║╚██████╔╝╚██████╔╝███████╗███████╗╚██████╔╝██║ ╚████║██║  ██║╚██████╔╝     ║
║    ╚═══╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝      ║
║                                                                                          ║
║  ██████╗  ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗                           ║
║  ██╔══██╗██╔══██╗██╔═══██╗     ██╔╝██╔════╝██╔════╝╚══██╔══╝                           ║
║  ██████╔╝██████╔╝██║   ██║     ██║ █████╗  ██║        ██║                              ║
║  ██╔═══╝ ██╔══██╗██║   ██║██   ██║ ██╔══╝  ██║        ██║                              ║
║  ██║     ██║  ██║╚██████╔╝╚█████╔╝ ███████╗╚██████╗   ██║                              ║
║  ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝  ╚══════╝ ╚═════╝   ╚═╝                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝"""

    def execute_global_analysis(self) -> ProjectArchitecture:
        """
        ╔══════════════════════════════════════════════════════════════════════════════╗
        ║                        ANÁLISIS GLOBAL COMPLETO                              ║
        ╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print("\n🔍 EJECUTANDO ANÁLISIS ARQUITECTÓNICO GLOBAL...")
        print("=" * 100)
        
        # FASE 1: Análisis del directorio raíz
        print("🏠 FASE 1: ANÁLISIS DIRECTORIO RAÍZ")
        root_analysis = self._analyze_directory(self.target_dir, is_root=True)
        
        # FASE 2: Análisis de subdirectorios principales
        print("\n📁 FASE 2: ANÁLISIS SUBDIRECTORIOS PRINCIPALES")
        subdirectories = self._analyze_all_subdirectories()
        
        # FASE 3: Mapeo de tecnologías y stack
        print("\n🔧 FASE 3: MAPEO DE STACK TECNOLÓGICO")
        technology_stack = self._analyze_technology_stack()
        
        # FASE 4: Análisis de integraciones
        print("\n🔗 FASE 4: ANÁLISIS DE INTEGRACIONES")
        integration_map = self._analyze_integrations()
        
        # FASE 5: Métricas de complejidad
        print("\n📊 FASE 5: MÉTRICAS DE COMPLEJIDAD")
        complexity_metrics = self._calculate_complexity_metrics()
        
        # FASE 6: Patrones arquitectónicos
        print("\n🏗️ FASE 6: IDENTIFICACIÓN PATRONES ARQUITECTÓNICOS")
        architectural_patterns = self._identify_architectural_patterns()
        
        # FASE 7: Estructura de deployment
        print("\n🚀 FASE 7: ANÁLISIS ESTRUCTURA DE DEPLOYMENT")
        deployment_structure = self._analyze_deployment_structure()
        
        # FASE 8: Consolidación final
        print("\n📋 FASE 8: CONSOLIDACIÓN RESULTADOS")
        return self._consolidate_analysis(
            root_analysis, subdirectories, technology_stack, 
            integration_map, complexity_metrics, architectural_patterns, deployment_structure
        )

    def _analyze_directory(self, directory: Path, is_root: bool = False) -> DirectoryAnalysis:
        """Análisis completo de un directorio específico"""
        if not directory.exists():
            return None
            
        print(f"   🔍 Analizando: {directory.name}")
        
        # Contadores básicos
        files = list(directory.glob('*'))
        file_count = len([f for f in files if f.is_file()])
        subdirectory_count = len([f for f in files if f.is_dir() and not f.name.startswith('.')])
        
        # Análisis de tipos de archivo
        file_types = defaultdict(int)
        total_lines = 0
        key_files = []
        
        for file_path in files:
            if file_path.is_file():
                file_ext = file_path.suffix.lower()
                file_name = file_path.name.lower()
                
                # Contar por extensión
                file_types[file_ext] += 1
                
                # Identificar archivos clave
                if self._is_key_file(file_name):
                    key_files.append(file_path.name)
                
                # Contar líneas (solo para archivos de texto)
                try:
                    if file_ext in ['.py', '.js', '.ts', '.html', '.css', '.php', '.md', '.txt', '.json', '.yml', '.yaml']:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            total_lines += sum(1 for _ in f)
                except Exception:
                    pass
        
        # Determinar lenguajes primarios
        primary_languages = self._determine_primary_languages(file_types)
        
        # Determinar propósito del directorio
        purpose = self._determine_directory_purpose(directory.name, key_files, file_types)
        
        # Determinar nivel arquitectónico
        architecture_level = self._determine_architecture_level(directory.name, is_root)
        
        # Analizar dependencias
        dependencies = self._analyze_dependencies(directory)
        
        # Puntos de integración
        integration_points = self._identify_integration_points(directory)
        
        return DirectoryAnalysis(
            name=directory.name,
            path=str(directory),
            file_count=file_count,
            subdirectory_count=subdirectory_count,
            total_lines=total_lines,
            file_types=dict(file_types),
            primary_languages=primary_languages,
            key_files=key_files,
            purpose=purpose,
            architecture_level=architecture_level,
            dependencies=dependencies,
            integration_points=integration_points
        )

    def _analyze_all_subdirectories(self) -> List[DirectoryAnalysis]:
        """Análisis de todos los subdirectorios principales"""
        subdirectories = []
        
        for item in self.target_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                analysis = self._analyze_directory(item)
                if analysis:
                    subdirectories.append(analysis)
                    print(f"      ├── {analysis.name}: {analysis.file_count} archivos, {analysis.purpose}")
        
        self.directory_analyses = subdirectories
        return subdirectories

    def _is_key_file(self, filename: str) -> bool:
        """Identifica si un archivo es clave en la arquitectura"""
        key_patterns = [
            'readme', 'license', 'dockerfile', 'docker-compose', 'requirements',
            'package.json', 'pyproject.toml', 'setup.py', 'main.py', 'index',
            'config', 'settings', 'environment', '.env', 'makefile', 'cmakelists',
            'api', 'server', 'client', 'service', 'architecture', 'installation',
            'contributing', 'security', 'terms', 'guide'
        ]
        return any(pattern in filename for pattern in key_patterns)

    def _determine_primary_languages(self, file_types: Dict[str, int]) -> List[str]:
        """Determina los lenguajes principales basado en tipos de archivo"""
        language_mapping = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.php': 'PHP',
            '.html': 'HTML',
            '.css': 'CSS',
            '.c': 'C',
            '.cpp': 'C++',
            '.h': 'C/C++ Header',
            '.sql': 'SQL',
            '.sh': 'Shell Script',
            '.bat': 'Batch Script',
            '.ps1': 'PowerShell',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.yml': 'YAML',
            '.yaml': 'YAML'
        }
        
        # Obtener los 3 tipos de archivo más comunes
        top_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:3]
        languages = []
        
        for ext, count in top_types:
            if ext in language_mapping and count > 0:
                languages.append(language_mapping[ext])
        
        return languages

    def _determine_directory_purpose(self, dir_name: str, key_files: List[str], file_types: Dict[str, int]) -> str:
        """Determina el propósito principal del directorio"""
        dir_name_lower = dir_name.lower()
        
        # Patrones específicos de VIGOLEONROCKS
        if 'vigoleonrocks' in dir_name_lower:
            return "VIGOLEONROCKS Core System"
        elif 'quantum' in dir_name_lower:
            return "Quantum Processing Engine"
        elif 'local' in dir_name_lower and 'gpt' in dir_name_lower:
            return "LocalGPT Integration"
        elif dir_name_lower in ['dokploy-canary']:
            return "Deployment System"
        elif dir_name_lower in ['openvpn-gui-master']:
            return "VPN GUI Application"
        elif dir_name_lower in ['mcp']:
            return "MCP (Model Context Protocol) Service"
        elif dir_name_lower in ['services']:
            return "Microservices Architecture"
        elif dir_name_lower in ['src']:
            return "Source Code"
        elif dir_name_lower in ['config']:
            return "Configuration Management"
        elif dir_name_lower in ['cache']:
            return "Caching System"
        elif 'test' in dir_name_lower:
            return "Testing and Quality Assurance"
        elif 'api' in dir_name_lower:
            return "API Services"
        elif 'web' in dir_name_lower or 'ui' in dir_name_lower:
            return "User Interface"
        
        # Análisis basado en tipos de archivo
        if file_types.get('.py', 0) > 5:
            return "Python Application/Service"
        elif file_types.get('.js', 0) > 5 or file_types.get('.ts', 0) > 5:
            return "JavaScript/TypeScript Application"
        elif file_types.get('.php', 0) > 5:
            return "PHP Web Application"
        elif file_types.get('.html', 0) > 3:
            return "Web Frontend"
        elif 'Dockerfile' in key_files:
            return "Containerized Service"
        elif any('docker-compose' in f for f in key_files):
            return "Docker Orchestration"
        elif 'requirements.txt' in key_files or 'package.json' in key_files:
            return "Application Dependencies"
        
        return "General Purpose Directory"

    def _determine_architecture_level(self, dir_name: str, is_root: bool) -> str:
        """Determina el nivel arquitectónico del directorio"""
        if is_root:
            return "Project Root"
        
        dir_name_lower = dir_name.lower()
        
        if dir_name_lower in ['services', 'microservices']:
            return "Service Layer"
        elif dir_name_lower in ['src', 'source']:
            return "Application Layer"
        elif dir_name_lower in ['config', 'configuration']:
            return "Configuration Layer"
        elif dir_name_lower in ['api', 'apis']:
            return "API Layer"
        elif dir_name_lower in ['ui', 'frontend', 'web']:
            return "Presentation Layer"
        elif dir_name_lower in ['data', 'database', 'db']:
            return "Data Layer"
        elif dir_name_lower in ['cache', 'caching']:
            return "Caching Layer"
        elif dir_name_lower in ['test', 'tests', 'testing']:
            return "Testing Layer"
        elif 'deploy' in dir_name_lower or 'docker' in dir_name_lower:
            return "Deployment Layer"
        elif 'monitor' in dir_name_lower or 'log' in dir_name_lower:
            return "Monitoring Layer"
        else:
            return "Business Logic Layer"

    def _analyze_dependencies(self, directory: Path) -> List[str]:
        """Analiza dependencias del directorio"""
        dependencies = []
        
        # Buscar archivos de dependencias
        dependency_files = [
            'requirements.txt', 'package.json', 'pyproject.toml', 
            'setup.py', 'Pipfile', 'yarn.lock', 'pnpm-lock.yaml'
        ]
        
        for dep_file in dependency_files:
            dep_path = directory / dep_file
            if dep_path.exists():
                dependencies.append(f"Has {dep_file}")
                
                # Análisis específico para algunos archivos
                try:
                    if dep_file == 'requirements.txt':
                        with open(dep_path, 'r') as f:
                            lines = f.readlines()
                            dependencies.append(f"{len(lines)} Python packages")
                    elif dep_file == 'package.json':
                        with open(dep_path, 'r') as f:
                            import json
                            data = json.load(f)
                            dep_count = len(data.get('dependencies', {}))
                            dev_dep_count = len(data.get('devDependencies', {}))
                            dependencies.append(f"{dep_count} npm dependencies, {dev_dep_count} dev dependencies")
                except Exception:
                    pass
        
        return dependencies

    def _identify_integration_points(self, directory: Path) -> List[str]:
        """Identifica puntos de integración del directorio"""
        integration_points = []
        
        # Buscar archivos que indican integraciones
        integration_indicators = [
            ('docker-compose.yml', 'Docker Orchestration'),
            ('Dockerfile', 'Container Integration'),
            ('.github', 'GitHub Actions CI/CD'),
            ('api', 'API Integration'),
            ('database', 'Database Integration'),
            ('config', 'Configuration Management'),
            ('service', 'Service Integration'),
            ('client', 'Client Integration')
        ]
        
        for file_pattern, integration_type in integration_indicators:
            if any(file_pattern.lower() in str(f).lower() for f in directory.glob('*')):
                integration_points.append(integration_type)
        
        return integration_points

    def _analyze_technology_stack(self) -> Dict[str, List[str]]:
        """Analiza el stack tecnológico completo"""
        stack = {
            'Programming Languages': [],
            'Web Technologies': [],
            'Databases': [],
            'Containerization': [],
            'AI/ML Frameworks': [],
            'Testing Frameworks': [],
            'Build Tools': [],
            'Configuration': []
        }
        
        # Consolidar información de todos los directorios
        all_files = []
        for root, dirs, files in os.walk(self.target_dir):
            all_files.extend([os.path.join(root, f) for f in files])
        
        # Analizar patrones tecnológicos
        for file_path in all_files:
            file_name = os.path.basename(file_path).lower()
            file_ext = os.path.splitext(file_name)[1].lower()
            
            # Lenguajes de programación
            if file_ext in ['.py']:
                if 'Python' not in stack['Programming Languages']:
                    stack['Programming Languages'].append('Python')
            elif file_ext in ['.js', '.ts']:
                if 'JavaScript/TypeScript' not in stack['Programming Languages']:
                    stack['Programming Languages'].append('JavaScript/TypeScript')
            elif file_ext in ['.php']:
                if 'PHP' not in stack['Programming Languages']:
                    stack['Programming Languages'].append('PHP')
            elif file_ext in ['.c', '.cpp', '.h']:
                if 'C/C++' not in stack['Programming Languages']:
                    stack['Programming Languages'].append('C/C++')
            
            # Tecnologías web
            if file_ext in ['.html', '.css']:
                if 'HTML/CSS' not in stack['Web Technologies']:
                    stack['Web Technologies'].append('HTML/CSS')
            elif 'fastapi' in file_name or 'flask' in file_name:
                if 'FastAPI/Flask' not in stack['Web Technologies']:
                    stack['Web Technologies'].append('FastAPI/Flask')
            
            # Containerización
            if 'dockerfile' in file_name:
                if 'Docker' not in stack['Containerization']:
                    stack['Containerization'].append('Docker')
            elif 'docker-compose' in file_name:
                if 'Docker Compose' not in stack['Containerization']:
                    stack['Containerization'].append('Docker Compose')
            
            # Frameworks AI/ML
            if 'requirements.txt' in file_name:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        ai_frameworks = ['openai', 'anthropic', 'transformers', 'langchain', 'torch', 'tensorflow']
                        for framework in ai_frameworks:
                            if framework in content and framework not in stack['AI/ML Frameworks']:
                                stack['AI/ML Frameworks'].append(framework)
                except Exception:
                    pass
        
        return stack

    def _analyze_integrations(self) -> Dict[str, List[str]]:
        """Analiza integraciones entre componentes"""
        integrations = {
            'Internal Services': [],
            'External APIs': [],
            'Databases': [],
            'Cloud Services': [],
            'CI/CD': []
        }
        
        # Buscar patrones de integración en el código
        for analysis in self.directory_analyses:
            # Integraciones internas
            if 'api' in analysis.name.lower() or 'service' in analysis.name.lower():
                integrations['Internal Services'].append(f"{analysis.name} - {analysis.purpose}")
            
            # Integraciones externas basadas en dependencias
            for dep in analysis.dependencies:
                if 'openai' in dep.lower() or 'anthropic' in dep.lower():
                    if 'AI Services (OpenAI/Anthropic)' not in integrations['External APIs']:
                        integrations['External APIs'].append('AI Services (OpenAI/Anthropic)')
                
                if 'supabase' in dep.lower():
                    if 'Supabase' not in integrations['Cloud Services']:
                        integrations['Cloud Services'].append('Supabase')
        
        return integrations

    def _calculate_complexity_metrics(self) -> Dict[str, Any]:
        """Calcula métricas de complejidad del proyecto"""
        metrics = {
            'total_files': 0,
            'total_directories': len(self.directory_analyses),
            'total_lines_of_code': 0,
            'average_files_per_directory': 0,
            'complexity_score': 0,
            'technology_diversity': 0,
            'integration_complexity': 0
        }
        
        # Consolidar métricas de todos los directorios
        total_files = sum(analysis.file_count for analysis in self.directory_analyses)
        total_lines = sum(analysis.total_lines for analysis in self.directory_analyses)
        
        metrics['total_files'] = total_files
        metrics['total_lines_of_code'] = total_lines
        metrics['average_files_per_directory'] = total_files / len(self.directory_analyses) if self.directory_analyses else 0
        
        # Calcular diversidad tecnológica
        unique_languages = set()
        for analysis in self.directory_analyses:
            unique_languages.update(analysis.primary_languages)
        metrics['technology_diversity'] = len(unique_languages)
        
        # Calcular complejidad de integraciones
        total_integrations = sum(len(analysis.integration_points) for analysis in self.directory_analyses)
        metrics['integration_complexity'] = total_integrations
        
        # Score de complejidad general (0-100)
        complexity_factors = [
            min(len(self.directory_analyses) / 10, 1) * 20,  # Número de directorios
            min(total_files / 1000, 1) * 30,  # Número de archivos
            min(metrics['technology_diversity'] / 10, 1) * 25,  # Diversidad tecnológica
            min(total_integrations / 20, 1) * 25  # Complejidad de integraciones
        ]
        metrics['complexity_score'] = sum(complexity_factors)
        
        return metrics

    def _identify_architectural_patterns(self) -> List[str]:
        """Identifica patrones arquitectónicos en el proyecto"""
        patterns = []
        
        # Analizar estructura de directorios
        dir_names = [analysis.name.lower() for analysis in self.directory_analyses]
        
        # Microservices
        if 'services' in dir_names:
            patterns.append('Microservices Architecture')
        
        # Layered Architecture
        layers = ['api', 'service', 'data', 'presentation', 'ui']
        if sum(1 for layer in layers if any(layer in name for name in dir_names)) >= 3:
            patterns.append('Layered Architecture')
        
        # Container-based
        has_docker = any('docker' in analysis.key_files for analysis in self.directory_analyses 
                        for file in analysis.key_files if 'docker' in file.lower())
        if has_docker:
            patterns.append('Container-based Deployment')
        
        # AI/ML Pipeline
        ai_indicators = ['quantum', 'ai', 'ml', 'model', 'intelligence']
        if sum(1 for indicator in ai_indicators if any(indicator in name for name in dir_names)) >= 2:
            patterns.append('AI/ML Pipeline Architecture')
        
        # API-first
        if sum(1 for analysis in self.directory_analyses if 'api' in analysis.name.lower()) >= 2:
            patterns.append('API-first Architecture')
        
        # Modular Monolith
        if len(self.directory_analyses) > 5 and not any('service' in name for name in dir_names):
            patterns.append('Modular Monolith')
        
        return patterns

    def _analyze_deployment_structure(self) -> Dict[str, Any]:
        """Analiza la estructura de deployment"""
        deployment = {
            'containerization': False,
            'orchestration': False,
            'ci_cd': False,
            'cloud_ready': False,
            'deployment_scripts': [],
            'configuration_management': False
        }
        
        # Buscar evidencias de deployment
        all_files = []
        for analysis in self.directory_analyses:
            all_files.extend(analysis.key_files)
        
        # Containerización
        if any('dockerfile' in f.lower() for f in all_files):
            deployment['containerization'] = True
        
        # Orquestación
        if any('docker-compose' in f.lower() or 'kubernetes' in f.lower() for f in all_files):
            deployment['orchestration'] = True
        
        # CI/CD
        if any('.github' in analysis.name.lower() or 'ci' in analysis.name.lower() 
               for analysis in self.directory_analyses):
            deployment['ci_cd'] = True
        
        # Scripts de deployment
        script_patterns = ['deploy', 'start', 'launch', 'install']
        deployment_scripts = [f for f in all_files 
                            if any(pattern in f.lower() for pattern in script_patterns)]
        deployment['deployment_scripts'] = deployment_scripts
        
        # Gestión de configuración
        if any('config' in analysis.name.lower() for analysis in self.directory_analyses):
            deployment['configuration_management'] = True
        
        # Cloud ready
        cloud_indicators = ['docker', 'kubernetes', 'aws', 'gcp', 'azure', 'supabase']
        if any(indicator in str(all_files).lower() for indicator in cloud_indicators):
            deployment['cloud_ready'] = True
        
        return deployment

    def _consolidate_analysis(self, root_analysis, subdirectories, technology_stack, 
                            integration_map, complexity_metrics, architectural_patterns, 
                            deployment_structure) -> ProjectArchitecture:
        """Consolida todos los análisis en la arquitectura final"""
        return ProjectArchitecture(
            root_analysis=root_analysis,
            subdirectories=subdirectories,
            technology_stack=technology_stack,
            integration_map=integration_map,
            complexity_metrics=complexity_metrics,
            architectural_patterns=architectural_patterns,
            deployment_structure=deployment_structure
        )

    def generate_global_report(self, architecture: ProjectArchitecture) -> str:
        """Genera reporte global completo"""
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                    VIGOLEONROCKS GLOBAL ARCHITECTURAL ANALYSIS                       ║
║                              PANORAMA COMPLETO DEL PROYECTO                          ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

📊 RESUMEN EJECUTIVO GLOBAL
══════════════════════════════════════════════════════════════════════════════════════
🎯 Proyecto: VIGOLEONROCKS Quantum NLP Service
📁 Directorios Analizados: {len(architecture.subdirectories)}
📄 Archivos Totales: {architecture.complexity_metrics['total_files']}
📝 Líneas de Código: {architecture.complexity_metrics['total_lines_of_code']:,}
🔧 Diversidad Tecnológica: {architecture.complexity_metrics['technology_diversity']} lenguajes/tecnologías
⚡ Score de Complejidad: {architecture.complexity_metrics['complexity_score']:.1f}/100
🏗️ Patrones Arquitectónicos: {len(architecture.architectural_patterns)}

🌟 ANÁLISIS DE SUBDIRECTORIOS PRINCIPALES
══════════════════════════════════════════════════════════════════════════════════════"""
        
        # Top directorios por complejidad
        sorted_dirs = sorted(architecture.subdirectories, 
                           key=lambda x: x.file_count + x.total_lines/1000, reverse=True)[:10]
        
        for i, directory in enumerate(sorted_dirs, 1):
            report += f"""
📁 {i:2d}. {directory.name}
   ├── Propósito: {directory.purpose}
   ├── Nivel Arquitectónico: {directory.architecture_level}
   ├── Archivos: {directory.file_count} | Líneas: {directory.total_lines:,}
   ├── Lenguajes: {', '.join(directory.primary_languages[:3])}
   └── Integraciones: {len(directory.integration_points)} puntos"""

        report += f"""

🔧 STACK TECNOLÓGICO COMPLETO
══════════════════════════════════════════════════════════════════════════════════════"""

        for category, technologies in architecture.technology_stack.items():
            if technologies:
                report += f"""
{category}:
   └── {', '.join(technologies)}"""

        report += f"""

🏗️ PATRONES ARQUITECTÓNICOS IDENTIFICADOS
══════════════════════════════════════════════════════════════════════════════════════"""
        
        for i, pattern in enumerate(architecture.architectural_patterns, 1):
            report += f"\n{i:2d}. {pattern}"

        report += f"""

🔗 MAPA DE INTEGRACIONES
══════════════════════════════════════════════════════════════════════════════════════"""

        for category, integrations in architecture.integration_map.items():
            if integrations:
                report += f"""
{category}:"""
                for integration in integrations:
                    report += f"\n   ├── {integration}"

        report += f"""

🚀 ESTRUCTURA DE DEPLOYMENT
══════════════════════════════════════════════════════════════════════════════════════
Containerización: {'✅' if architecture.deployment_structure['containerization'] else '❌'}
Orquestación: {'✅' if architecture.deployment_structure['orchestration'] else '❌'}
CI/CD: {'✅' if architecture.deployment_structure['ci_cd'] else '❌'}
Cloud Ready: {'✅' if architecture.deployment_structure['cloud_ready'] else '❌'}
Gestión Config: {'✅' if architecture.deployment_structure['configuration_management'] else '❌'}

Scripts de Deployment: {len(architecture.deployment_structure['deployment_scripts'])} detectados"""

        report += f"""

📈 MÉTRICAS DE COMPLEJIDAD DETALLADAS
══════════════════════════════════════════════════════════════════════════════════════
• Total de Directorios: {architecture.complexity_metrics['total_directories']}
• Archivos por Directorio (promedio): {architecture.complexity_metrics['average_files_per_directory']:.1f}
• Complejidad de Integraciones: {architecture.complexity_metrics['integration_complexity']} puntos
• Diversidad Tecnológica: {architecture.complexity_metrics['technology_diversity']} tecnologías distintas

CLASIFICACIÓN DE COMPLEJIDAD:
"""
        
        complexity_score = architecture.complexity_metrics['complexity_score']
        if complexity_score >= 80:
            report += "🔴 ALTA COMPLEJIDAD - Proyecto enterprise con múltiples tecnologías y integraciones"
        elif complexity_score >= 60:
            report += "🟡 COMPLEJIDAD MEDIA-ALTA - Proyecto robusto con buena diversidad tecnológica"
        elif complexity_score >= 40:
            report += "🟢 COMPLEJIDAD MEDIA - Proyecto bien estructurado y manejable"
        else:
            report += "🔵 BAJA COMPLEJIDAD - Proyecto simple y directo"

        report += f"""

🎯 RECOMENDACIONES ARQUITECTÓNICAS
══════════════════════════════════════════════════════════════════════════════════════"""
        
        # Generar recomendaciones basadas en el análisis
        recommendations = self._generate_architectural_recommendations(architecture)
        for i, rec in enumerate(recommendations, 1):
            report += f"\n{i:2d}. {rec}"

        report += f"""

╔══════════════════════════════════════════════════════════════════════════════════════╗
║                         ANÁLISIS GLOBAL COMPLETADO EXITOSAMENTE                      ║
║                           {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                           ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""
        
        return report

    def _generate_architectural_recommendations(self, architecture: ProjectArchitecture) -> List[str]:
        """Genera recomendaciones arquitectónicas"""
        recommendations = []
        
        # Recomendación basada en complejidad
        if architecture.complexity_metrics['complexity_score'] > 70:
            recommendations.append(
                "Considerar refactoring para reducir complejidad - Dividir componentes grandes"
            )
        
        # Recomendación de containerización
        if not architecture.deployment_structure['containerization']:
            recommendations.append(
                "Implementar containerización con Docker para mejorar portabilidad"
            )
        
        # Recomendación de orquestación
        if architecture.deployment_structure['containerization'] and not architecture.deployment_structure['orchestration']:
            recommendations.append(
                "Agregar Docker Compose para orquestación de servicios"
            )
        
        # Recomendación de CI/CD
        if not architecture.deployment_structure['ci_cd']:
            recommendations.append(
                "Implementar pipeline de CI/CD con GitHub Actions"
            )
        
        # Recomendación de documentación
        doc_dirs = [d for d in architecture.subdirectories if 'doc' in d.name.lower()]
        if not doc_dirs:
            recommendations.append(
                "Crear directorio de documentación técnica y arquitectónica"
            )
        
        # Recomendación de testing
        test_files = sum(1 for d in architecture.subdirectories if 'test' in d.name.lower())
        if test_files < 2:
            recommendations.append(
                "Ampliar cobertura de testing - Crear más suites de pruebas"
            )
        
        # Recomendación de configuración
        if not architecture.deployment_structure['configuration_management']:
            recommendations.append(
                "Implementar gestión centralizada de configuración"
            )
        
        return recommendations

    def save_global_analysis(self, architecture: ProjectArchitecture, base_filename: str = "vigoleonrocks_global_analysis"):
        """Guarda el análisis global completo"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Convertir a diccionario para JSON
        analysis_dict = {
            'metadata': {
                'analysis_timestamp': datetime.now().isoformat(),
                'target_directory': str(self.target_dir),
                'analyzer_version': '1.0.0'
            },
            'root_analysis': asdict(architecture.root_analysis),
            'subdirectories': [asdict(d) for d in architecture.subdirectories],
            'technology_stack': architecture.technology_stack,
            'integration_map': architecture.integration_map,
            'complexity_metrics': architecture.complexity_metrics,
            'architectural_patterns': architecture.architectural_patterns,
            'deployment_structure': architecture.deployment_structure
        }
        
        # Guardar JSON detallado
        json_file = f"{base_filename}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_dict, f, indent=2, ensure_ascii=False)
        
        # Guardar reporte ASCII
        ascii_file = f"{base_filename}_report_{timestamp}.txt"
        with open(ascii_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_global_report(architecture))
        
        print(f"\n💾 ANÁLISIS GLOBAL GUARDADO:")
        print(f"   ├── JSON detallado: {json_file}")
        print(f"   └── Reporte ASCII: {ascii_file}")


def main():
    """Ejecución principal del análisis global"""
    
    print("""
🎯 ANÁLISIS ARQUITECTÓNICO GLOBAL - VIGOLEONROCKS PROJECT

FASES DE ANÁLISIS:
1. 🏠 Análisis del directorio raíz
2. 📁 Análisis de subdirectorios principales
3. 🔧 Mapeo del stack tecnológico
4. 🔗 Análisis de integraciones
5. 📊 Cálculo de métricas de complejidad
6. 🏗️ Identificación de patrones arquitectónicos
7. 🚀 Análisis de estructura de deployment
8. 📋 Consolidación y reporte final

═══════════════════════════════════════════════════════════════════════════════════
    """)
    
    # Solicitar directorio objetivo
    target_dir = input("📁 Directorio objetivo (Enter para directorio actual): ").strip()
    if not target_dir:
        target_dir = "."
    
    if not Path(target_dir).exists():
        print(f"❌ ERROR: El directorio '{target_dir}' no existe.")
        return
    
    print(f"\n🚀 INICIANDO ANÁLISIS ARQUITECTÓNICO GLOBAL EN: {Path(target_dir).resolve()}")
    print("=" * 100)
    
    try:
        # Crear analizador y ejecutar análisis
        analyzer = VigoleonrocksGlobalAnalyzer(target_dir)
        architecture = analyzer.execute_global_analysis()
        
        print("\n" + "=" * 100)
        print("📊 GENERANDO REPORTE GLOBAL FINAL...")
        
        # Mostrar reporte
        print(analyzer.generate_global_report(architecture))
        
        # Preguntar si guardar resultados
        save_results = input("\n💾 ¿Guardar análisis global completo? (y/N): ").strip().lower()
        if save_results in ['y', 'yes', 'sí', 's']:
            analyzer.save_global_analysis(architecture)
        
        print("\n🎉 ANÁLISIS ARQUITECTÓNICO GLOBAL COMPLETADO EXITOSAMENTE!")
        print(f"📊 Total Directorios: {len(architecture.subdirectories)}")
        print(f"📄 Total Archivos: {architecture.complexity_metrics['total_files']}")
        print(f"⚡ Score Complejidad: {architecture.complexity_metrics['complexity_score']:.1f}/100")
        
        return architecture
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Análisis interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO durante el análisis: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
