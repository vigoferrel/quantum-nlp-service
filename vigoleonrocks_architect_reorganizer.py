#!/usr/bin/env python3
"""
VIGOLEONROCKS ARCHITECT REORGANIZER
==================================

Sistema avanzado de reorganización arquitectónica del proyecto VIGOLEONROCKS
usando principios de ingeniería inversa para alcanzar el máximo potencial.

Autor: Assistant (Claude 4 Sonnet)
Versión: 2.0.0
Fecha: 2024
"""

import os
import shutil
import json
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, Counter
import re
import ast
import hashlib
import time
from dataclasses import dataclass, asdict
from enum import Enum


class ArchitecturalLayer(Enum):
    """Capas arquitectónicas del sistema"""
    CORE = "core"                    # Núcleo fundamental del sistema
    DOMAIN = "domain"                # Lógica de dominio y modelos
    APPLICATION = "application"      # Capa de aplicación y servicios
    INFRASTRUCTURE = "infrastructure" # Infraestructura y persistencia
    PRESENTATION = "presentation"    # Interfaces y APIs
    INTEGRATION = "integration"      # Integraciones externas
    CONFIGURATION = "configuration"  # Configuración y setup
    DOCUMENTATION = "documentation"  # Documentación y recursos
    TESTING = "testing"             # Testing y QA
    TOOLS = "tools"                 # Herramientas y utilidades
    DEPLOYMENT = "deployment"       # Despliegue y DevOps
    SECURITY = "security"           # Seguridad y autenticación


@dataclass
class ComponentMetrics:
    """Métricas de un componente del sistema"""
    loc: int = 0
    complexity: int = 0
    dependencies: int = 0
    coupling: float = 0.0
    cohesion: float = 0.0
    importance: float = 0.0
    reusability: float = 0.0
    maintainability: float = 0.0


@dataclass
class ArchitecturalComponent:
    """Componente arquitectónico del sistema"""
    name: str
    path: str
    layer: ArchitecturalLayer
    purpose: str
    technologies: List[str]
    files: List[str]
    dependencies: List[str]
    metrics: ComponentMetrics
    recommended_location: str = ""
    restructure_priority: int = 0


class VIGOLEONROCKSArchitectReorganizer:
    """Reorganizador arquitectónico avanzado del proyecto VIGOLEONROCKS"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root).resolve()
        self.backup_dir = self.project_root / "_backup_original_structure"
        self.new_structure_dir = self.project_root / "_new_optimized_structure"
        
        # Configurar logging
        self.setup_logging()
        
        # Datos del análisis
        self.components: List[ArchitecturalComponent] = []
        self.technology_map: Dict[str, List[str]] = {}
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self.complexity_distribution: Dict[str, int] = {}
        
        # Patrones de detección arquitectónica
        self.setup_architectural_patterns()
        
        # Estructura objetivo optimizada
        self.target_structure = self.define_target_architecture()
    
    def setup_logging(self):
        """Configurar sistema de logging"""
        log_file = self.project_root / "vigoleonrocks_reorganizer.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_architectural_patterns(self):
        """Configurar patrones de detección arquitectónica"""
        self.patterns = {
            # Core System Patterns
            'core_models': [
                r'vigoleonrocks.*\.py$',
                r'quantum.*core.*\.py$',
                r'consciousness.*\.py$',
                r'.*unified.*brain.*\.py$',
                r'.*model.*core.*\.py$'
            ],
            
            # Domain Logic Patterns  
            'domain_services': [
                r'.*service.*\.py$',
                r'.*handler.*\.py$',
                r'.*processor.*\.py$',
                r'.*manager.*\.py$',
                r'.*controller.*\.py$'
            ],
            
            # Infrastructure Patterns
            'infrastructure': [
                r'.*database.*\.py$',
                r'.*repository.*\.py$',
                r'.*storage.*\.py$',
                r'.*cache.*\.py$',
                r'.*client.*\.py$',
                r'.*adapter.*\.py$'
            ],
            
            # API & Presentation
            'api_presentation': [
                r'.*api.*\.py$',
                r'.*router.*\.py$',
                r'.*endpoint.*\.py$',
                r'.*view.*\.py$',
                r'.*template.*\.html$',
                r'.*component.*\.(tsx?|jsx?)$'
            ],
            
            # Configuration
            'configuration': [
                r'.*config.*\.py$',
                r'.*settings.*\.py$',
                r'.*env.*\.py$',
                r'\.env.*$',
                r'.*\.yaml$',
                r'.*\.yml$',
                r'.*\.toml$',
                r'.*\.ini$'
            ],
            
            # Testing
            'testing': [
                r'test.*\.py$',
                r'.*test.*\.py$',
                r'.*spec.*\.py$',
                r'conftest\.py$'
            ],
            
            # Documentation
            'documentation': [
                r'.*\.md$',
                r'.*\.rst$',
                r'.*\.txt$',
                r'README.*',
                r'.*docs.*',
                r'.*\.pdf$'
            ],
            
            # Deployment & DevOps
            'deployment': [
                r'Dockerfile.*',
                r'docker-compose.*\.yml$',
                r'.*\.dockerfile$',
                r'.*deployment.*\.yml$',
                r'.*k8s.*\.yml$',
                r'.*helm.*'
            ],
            
            # Security
            'security': [
                r'.*auth.*\.py$',
                r'.*security.*\.py$',
                r'.*crypto.*\.py$',
                r'.*key.*\.py$',
                r'.*token.*\.py$'
            ]
        }
    
    def define_target_architecture(self) -> Dict[str, Dict]:
        """Define la arquitectura objetivo optimizada"""
        return {
            # Núcleo del sistema VIGOLEONROCKS
            'vigoleonrocks-core': {
                'description': 'Núcleo fundamental del modelo VIGOLEONROCKS',
                'layer': ArchitecturalLayer.CORE,
                'subdirs': ['models', 'consciousness', 'quantum', 'unified-brain'],
                'priority': 1
            },
            
            # Dominio y lógica de negocio
            'domain': {
                'description': 'Lógica de dominio y servicios de negocio',
                'layer': ArchitecturalLayer.DOMAIN,
                'subdirs': ['services', 'handlers', 'processors', 'managers'],
                'priority': 2
            },
            
            # Capa de aplicación
            'application': {
                'description': 'Servicios de aplicación y orquestación',
                'layer': ArchitecturalLayer.APPLICATION,
                'subdirs': ['use-cases', 'workflows', 'orchestration'],
                'priority': 3
            },
            
            # Infraestructura
            'infrastructure': {
                'description': 'Infraestructura, persistencia y servicios externos',
                'layer': ArchitecturalLayer.INFRASTRUCTURE,
                'subdirs': ['database', 'storage', 'messaging', 'external-apis'],
                'priority': 4
            },
            
            # APIs y presentación
            'interfaces': {
                'description': 'APIs, interfaces de usuario y presentación',
                'layer': ArchitecturalLayer.PRESENTATION,
                'subdirs': ['rest-api', 'graphql', 'websockets', 'ui', 'cli'],
                'priority': 5
            },
            
            # Integraciones
            'integrations': {
                'description': 'Integraciones con sistemas externos',
                'layer': ArchitecturalLayer.INTEGRATION,
                'subdirs': ['openrouter', 'docker', 'quantum-systems', 'ai-providers'],
                'priority': 6
            },
            
            # Configuración
            'config': {
                'description': 'Configuración del sistema y entornos',
                'layer': ArchitecturalLayer.CONFIGURATION,
                'subdirs': ['environments', 'settings', 'schemas'],
                'priority': 7
            },
            
            # Testing
            'tests': {
                'description': 'Suite de testing completa',
                'layer': ArchitecturalLayer.TESTING,
                'subdirs': ['unit', 'integration', 'e2e', 'performance'],
                'priority': 8
            },
            
            # Documentación
            'docs': {
                'description': 'Documentación técnica y de usuario',
                'layer': ArchitecturalLayer.DOCUMENTATION,
                'subdirs': ['technical', 'user-guides', 'api-docs', 'architecture'],
                'priority': 9
            },
            
            # Herramientas
            'tools': {
                'description': 'Herramientas de desarrollo y utilidades',
                'layer': ArchitecturalLayer.TOOLS,
                'subdirs': ['dev-tools', 'scripts', 'generators', 'analyzers'],
                'priority': 10
            },
            
            # Deployment
            'deployment': {
                'description': 'Configuración de despliegue y DevOps',
                'layer': ArchitecturalLayer.DEPLOYMENT,
                'subdirs': ['docker', 'kubernetes', 'ci-cd', 'monitoring'],
                'priority': 11
            },
            
            # Security
            'security': {
                'description': 'Seguridad, autenticación y autorización',
                'layer': ArchitecturalLayer.SECURITY,
                'subdirs': ['authentication', 'authorization', 'encryption', 'certificates'],
                'priority': 12
            }
        }
    
    def analyze_current_structure(self) -> Dict:
        """Analiza la estructura actual del proyecto"""
        self.logger.info("🔍 Iniciando análisis de estructura actual...")
        
        analysis = {
            'total_dirs': 0,
            'total_files': 0,
            'total_loc': 0,
            'technology_distribution': defaultdict(int),
            'complexity_levels': defaultdict(int),
            'architectural_issues': []
        }
        
        # Analizar recursivamente
        for root, dirs, files in os.walk(self.project_root):
            if self._should_skip_directory(root):
                continue
                
            analysis['total_dirs'] += 1
            
            for file in files:
                if self._should_skip_file(file):
                    continue
                    
                file_path = Path(root) / file
                analysis['total_files'] += 1
                
                # Analizar archivo
                file_analysis = self._analyze_file(file_path)
                analysis['total_loc'] += file_analysis['loc']
                analysis['complexity_levels'][file_analysis['complexity_level']] += 1
                
                # Detectar tecnologías
                for tech in file_analysis['technologies']:
                    analysis['technology_distribution'][tech] += 1
        
        self.logger.info(f"✅ Análisis completado: {analysis['total_dirs']} dirs, {analysis['total_files']} archivos")
        return analysis
    
    def _analyze_file(self, file_path: Path) -> Dict:
        """Analiza un archivo específico"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            return {
                'loc': 0,
                'complexity_level': 'unknown',
                'technologies': [],
                'dependencies': []
            }
        
        lines = content.split('\n')
        loc = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        
        # Detectar tecnologías
        technologies = self._detect_technologies(content, file_path.suffix)
        
        # Calcular complejidad
        complexity_level = self._calculate_complexity_level(content, file_path.suffix)
        
        # Extraer dependencias
        dependencies = self._extract_dependencies(content, file_path.suffix)
        
        return {
            'loc': loc,
            'complexity_level': complexity_level,
            'technologies': technologies,
            'dependencies': dependencies
        }
    
    def _detect_technologies(self, content: str, extension: str) -> List[str]:
        """Detecta las tecnologías utilizadas en un archivo"""
        technologies = []
        
        # Detectores por extensión
        if extension in ['.py']:
            # Python específico
            python_patterns = {
                'fastapi': r'from fastapi|import fastapi',
                'django': r'from django|import django',
                'flask': r'from flask|import flask',
                'asyncio': r'import asyncio|async def|await ',
                'numpy': r'import numpy|from numpy',
                'pandas': r'import pandas|from pandas',
                'torch': r'import torch|from torch',
                'tensorflow': r'import tensorflow|from tensorflow',
                'quantum': r'quantum|qiskit|cirq',
                'consciousness': r'consciousness|awareness|cognitive',
                'nlp': r'nlp|natural language|transformer|bert|gpt',
                'docker': r'docker|container',
                'kubernetes': r'kubernetes|k8s'
            }
            
            for tech, pattern in python_patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    technologies.append(tech)
        
        elif extension in ['.js', '.ts', '.jsx', '.tsx']:
            # JavaScript/TypeScript
            js_patterns = {
                'react': r'import.*react|from.*react',
                'nodejs': r'require\(|module\.exports',
                'express': r'express|app\.get|app\.post',
                'typescript': r'interface |type |declare ',
                'docker': r'docker|container'
            }
            
            for tech, pattern in js_patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    technologies.append(tech)
        
        elif extension in ['.yml', '.yaml']:
            # YAML configurations
            if re.search(r'docker|container', content, re.IGNORECASE):
                technologies.append('docker')
            if re.search(r'kubernetes|k8s', content, re.IGNORECASE):
                technologies.append('kubernetes')
            if re.search(r'version.*compose', content, re.IGNORECASE):
                technologies.append('docker-compose')
        
        return technologies
    
    def _calculate_complexity_level(self, content: str, extension: str) -> str:
        """Calcula el nivel de complejidad de un archivo"""
        if extension == '.py':
            try:
                tree = ast.parse(content)
                
                # Contar estructuras complejas
                complexity_score = 0
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        complexity_score += 1
                    elif isinstance(node, ast.ClassDef):
                        complexity_score += 2
                    elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                        complexity_score += 1
                    elif isinstance(node, ast.Lambda):
                        complexity_score += 1
                
                if complexity_score < 5:
                    return 'low'
                elif complexity_score < 15:
                    return 'medium'
                else:
                    return 'high'
            except:
                pass
        
        # Fallback basado en líneas de código
        loc = len(content.split('\n'))
        if loc < 50:
            return 'low'
        elif loc < 200:
            return 'medium'
        else:
            return 'high'
    
    def _extract_dependencies(self, content: str, extension: str) -> List[str]:
        """Extrae las dependencias de un archivo"""
        dependencies = []
        
        if extension == '.py':
            # Imports de Python
            import_patterns = [
                r'from\s+([a-zA-Z_][a-zA-Z0-9_]*)',
                r'import\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                dependencies.extend(matches)
        
        elif extension in ['.js', '.ts', '.jsx', '.tsx']:
            # Imports de JavaScript/TypeScript
            import_patterns = [
                r'from\s+[\'"]([^"\']+)[\'"]',
                r'require\([\'"]([^"\']+)[\'"]\)',
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                dependencies.extend(matches)
        
        return dependencies
    
    def classify_components(self) -> List[ArchitecturalComponent]:
        """Clasifica todos los componentes del sistema"""
        self.logger.info("🏗️ Clasificando componentes arquitectónicos...")
        
        components = []
        
        for root, dirs, files in os.walk(self.project_root):
            if self._should_skip_directory(root):
                continue
            
            component_path = Path(root)
            component_name = component_path.name
            
            # Analizar archivos del componente
            component_files = []
            technologies = set()
            total_loc = 0
            total_complexity = 0
            
            for file in files:
                if self._should_skip_file(file):
                    continue
                
                file_path = component_path / file
                file_analysis = self._analyze_file(file_path)
                
                component_files.append(str(file_path.relative_to(self.project_root)))
                technologies.update(file_analysis['technologies'])
                total_loc += file_analysis['loc']
                
                if file_analysis['complexity_level'] == 'high':
                    total_complexity += 3
                elif file_analysis['complexity_level'] == 'medium':
                    total_complexity += 2
                else:
                    total_complexity += 1
            
            if not component_files:  # Skip empty directories
                continue
            
            # Clasificar capa arquitectónica
            layer = self._classify_architectural_layer(component_name, component_files, list(technologies))
            
            # Determinar propósito
            purpose = self._determine_component_purpose(component_name, component_files, list(technologies))
            
            # Calcular métricas
            metrics = ComponentMetrics(
                loc=total_loc,
                complexity=total_complexity,
                dependencies=len(set().union(*[self._extract_dependencies(
                    open(component_path / f.split('/')[-1], 'r', encoding='utf-8', errors='ignore').read() 
                    if (component_path / f.split('/')[-1]).exists() else '', 
                    Path(f).suffix
                ) for f in component_files[:5]])),  # Limitar para performance
                coupling=self._calculate_coupling(component_files),
                cohesion=self._calculate_cohesion(component_files, list(technologies)),
                importance=self._calculate_importance(component_name, list(technologies)),
                reusability=self._calculate_reusability(list(technologies)),
                maintainability=self._calculate_maintainability(total_complexity, total_loc)
            )
            
            # Crear componente
            component = ArchitecturalComponent(
                name=component_name,
                path=str(component_path.relative_to(self.project_root)),
                layer=layer,
                purpose=purpose,
                technologies=list(technologies),
                files=component_files,
                dependencies=[],  # Se calculará en otra fase
                metrics=metrics
            )
            
            # Recomendar ubicación
            component.recommended_location = self._recommend_location(component)
            component.restructure_priority = self._calculate_restructure_priority(component)
            
            components.append(component)
        
        self.logger.info(f"✅ Clasificados {len(components)} componentes")
        return components
    
    def _classify_architectural_layer(self, name: str, files: List[str], technologies: List[str]) -> ArchitecturalLayer:
        """Clasifica la capa arquitectónica de un componente"""
        name_lower = name.lower()
        files_content = ' '.join([f.lower() for f in files])
        tech_content = ' '.join([t.lower() for t in technologies])
        
        # Core layer
        if any(pattern in name_lower for pattern in ['vigoleonrocks', 'core', 'quantum', 'consciousness', 'brain']):
            return ArchitecturalLayer.CORE
        
        # Domain layer
        if any(pattern in name_lower for pattern in ['service', 'handler', 'processor', 'manager', 'domain']):
            return ArchitecturalLayer.DOMAIN
        
        # Infrastructure layer
        if any(pattern in name_lower for pattern in ['database', 'storage', 'cache', 'repository', 'client']):
            return ArchitecturalLayer.INFRASTRUCTURE
        
        # Presentation layer
        if any(pattern in name_lower for pattern in ['api', 'router', 'endpoint', 'ui', 'view', 'template']):
            return ArchitecturalLayer.PRESENTATION
        
        # Integration layer
        if any(pattern in name_lower for pattern in ['integration', 'external', 'provider', 'adapter']):
            return ArchitecturalLayer.INTEGRATION
        
        # Configuration layer
        if any(pattern in name_lower for pattern in ['config', 'settings', 'env']):
            return ArchitecturalLayer.CONFIGURATION
        
        # Testing layer
        if any(pattern in name_lower for pattern in ['test', 'spec', 'mock']):
            return ArchitecturalLayer.TESTING
        
        # Documentation layer
        if any(pattern in name_lower for pattern in ['doc', 'readme', 'guide']):
            return ArchitecturalLayer.DOCUMENTATION
        
        # Deployment layer
        if any(pattern in name_lower for pattern in ['docker', 'deploy', 'k8s', 'helm', 'ci']):
            return ArchitecturalLayer.DEPLOYMENT
        
        # Security layer
        if any(pattern in name_lower for pattern in ['auth', 'security', 'crypto', 'key']):
            return ArchitecturalLayer.SECURITY
        
        # Tools layer
        if any(pattern in name_lower for pattern in ['tool', 'script', 'util', 'helper']):
            return ArchitecturalLayer.TOOLS
        
        # Default to application layer
        return ArchitecturalLayer.APPLICATION
    
    def _determine_component_purpose(self, name: str, files: List[str], technologies: List[str]) -> str:
        """Determina el propósito específico de un componente"""
        name_lower = name.lower()
        
        # Propósitos específicos para VIGOLEONROCKS
        if 'vigoleonrocks' in name_lower:
            if any('model' in f.lower() for f in files):
                return "Implementación del modelo de IA VIGOLEONROCKS"
            else:
                return "Componente core del sistema VIGOLEONROCKS"
        
        if 'quantum' in name_lower:
            return "Procesamiento cuántico y computación avanzada"
        
        if 'consciousness' in name_lower:
            return "Simulación de consciencia artificial"
        
        if 'brain' in name_lower:
            return "Sistema de inteligencia artificial unificado"
        
        if 'nlp' in name_lower:
            return "Procesamiento de lenguaje natural"
        
        if 'docker' in name_lower:
            return "Contenedorización y orquestación"
        
        if 'api' in name_lower:
            return "Interface de programación de aplicaciones"
        
        if 'test' in name_lower:
            return "Testing y aseguramiento de calidad"
        
        if 'config' in name_lower:
            return "Configuración del sistema"
        
        if 'doc' in name_lower:
            return "Documentación técnica"
        
        return f"Componente {name_lower} del sistema"
    
    def _calculate_coupling(self, files: List[str]) -> float:
        """Calcula el acoplamiento del componente"""
        # Simplificado - en implementación real sería más complejo
        if len(files) < 2:
            return 0.0
        return min(len(files) * 0.1, 1.0)
    
    def _calculate_cohesion(self, files: List[str], technologies: List[str]) -> float:
        """Calcula la cohesión del componente"""
        # Simplificado - basado en consistencia tecnológica
        if len(technologies) == 0:
            return 0.0
        
        # Más cohesión si usa menos tecnologías diferentes
        cohesion = 1.0 / (1.0 + len(technologies) * 0.1)
        return min(cohesion, 1.0)
    
    def _calculate_importance(self, name: str, technologies: List[str]) -> float:
        """Calcula la importancia del componente"""
        importance = 0.5  # Base
        
        # VIGOLEONROCKS core es crítico
        if 'vigoleonrocks' in name.lower():
            importance += 0.4
        
        # Quantum y consciousness son importantes
        if any(tech in name.lower() for tech in ['quantum', 'consciousness', 'brain']):
            importance += 0.3
        
        # APIs son importantes
        if 'api' in name.lower():
            importance += 0.2
        
        # Tecnologías avanzadas
        advanced_techs = ['quantum', 'consciousness', 'nlp', 'docker', 'kubernetes']
        for tech in technologies:
            if any(adv_tech in tech.lower() for adv_tech in advanced_techs):
                importance += 0.1
        
        return min(importance, 1.0)
    
    def _calculate_reusability(self, technologies: List[str]) -> float:
        """Calcula la reusabilidad del componente"""
        # Simplificado - basado en tecnologías estándar
        standard_techs = ['fastapi', 'docker', 'asyncio', 'numpy', 'pandas']
        score = sum(1 for tech in technologies if any(std in tech.lower() for std in standard_techs))
        return min(score * 0.2, 1.0)
    
    def _calculate_maintainability(self, complexity: int, loc: int) -> float:
        """Calcula la mantenibilidad del componente"""
        if loc == 0:
            return 1.0
        
        # Menos complejo y más líneas = más mantenible (hasta un punto)
        complexity_factor = max(0.1, 1.0 - (complexity * 0.05))
        size_factor = 1.0 if loc < 1000 else max(0.1, 1.0 - ((loc - 1000) * 0.0001))
        
        return min(complexity_factor * size_factor, 1.0)
    
    def _recommend_location(self, component: ArchitecturalComponent) -> str:
        """Recomienda la ubicación óptima para el componente"""
        layer_mapping = {
            ArchitecturalLayer.CORE: 'vigoleonrocks-core',
            ArchitecturalLayer.DOMAIN: 'domain',
            ArchitecturalLayer.APPLICATION: 'application',
            ArchitecturalLayer.INFRASTRUCTURE: 'infrastructure',
            ArchitecturalLayer.PRESENTATION: 'interfaces',
            ArchitecturalLayer.INTEGRATION: 'integrations',
            ArchitecturalLayer.CONFIGURATION: 'config',
            ArchitecturalLayer.TESTING: 'tests',
            ArchitecturalLayer.DOCUMENTATION: 'docs',
            ArchitecturalLayer.TOOLS: 'tools',
            ArchitecturalLayer.DEPLOYMENT: 'deployment',
            ArchitecturalLayer.SECURITY: 'security'
        }
        
        base_location = layer_mapping.get(component.layer, 'misc')
        
        # Refinar la ubicación basada en tecnologías
        if 'vigoleonrocks' in component.name.lower():
            if 'model' in component.name.lower():
                return f"{base_location}/models"
            elif 'quantum' in component.name.lower():
                return f"{base_location}/quantum"
            elif 'consciousness' in component.name.lower():
                return f"{base_location}/consciousness"
            else:
                return f"{base_location}/core"
        
        return base_location
    
    def _calculate_restructure_priority(self, component: ArchitecturalComponent) -> int:
        """Calcula la prioridad de reestructuración (1=alta, 5=baja)"""
        priority = 3  # Neutral
        
        # Alta prioridad para core components
        if component.layer == ArchitecturalLayer.CORE:
            priority = 1
        
        # Alta prioridad para alta importancia
        if component.metrics.importance > 0.8:
            priority = min(priority, 1)
        
        # Media-alta para infrastructure y presentation
        if component.layer in [ArchitecturalLayer.INFRASTRUCTURE, ArchitecturalLayer.PRESENTATION]:
            priority = min(priority, 2)
        
        # Baja prioridad para documentación y testing
        if component.layer in [ArchitecturalLayer.DOCUMENTATION, ArchitecturalLayer.TESTING]:
            priority = max(priority, 4)
        
        return priority
    
    def create_reorganization_plan(self) -> Dict:
        """Crear el plan completo de reorganización"""
        self.logger.info("📋 Creando plan de reorganización...")
        
        # Clasificar componentes
        self.components = self.classify_components()
        
        # Crear plan
        plan = {
            'metadata': {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_components': len(self.components),
                'target_architecture': self.target_structure
            },
            'reorganization_steps': [],
            'expected_benefits': [],
            'risks_and_mitigations': [],
            'component_mappings': {}
        }
        
        # Agrupar por prioridad
        priority_groups = defaultdict(list)
        for component in self.components:
            priority_groups[component.restructure_priority].append(component)
        
        # Crear pasos de reorganización
        step_id = 1
        for priority in sorted(priority_groups.keys()):
            components_group = priority_groups[priority]
            
            step = {
                'step_id': step_id,
                'priority_level': priority,
                'description': f"Reorganizar componentes de prioridad {priority}",
                'components_count': len(components_group),
                'estimated_time': len(components_group) * 2,  # minutos
                'components': []
            }
            
            for component in components_group:
                component_plan = {
                    'current_path': component.path,
                    'recommended_path': component.recommended_location,
                    'component_name': component.name,
                    'layer': component.layer.value,
                    'purpose': component.purpose,
                    'files_count': len(component.files),
                    'technologies': component.technologies,
                    'metrics': asdict(component.metrics)
                }
                
                step['components'].append(component_plan)
                plan['component_mappings'][component.path] = component.recommended_location
            
            plan['reorganization_steps'].append(step)
            step_id += 1
        
        # Beneficios esperados
        plan['expected_benefits'] = [
            "Estructura arquitectónica clara y coherente",
            "Separación efectiva de responsabilidades por capas",
            "Mejor navegabilidad y comprensión del código",
            "Facilita el mantenimiento y evolución del sistema",
            "Optimiza la reutilización de componentes",
            "Reduce el acoplamiento entre módulos",
            "Mejora la escalabilidad del proyecto",
            "Facilita la incorporación de nuevos desarrolladores"
        ]
        
        # Riesgos y mitigaciones
        plan['risks_and_mitigations'] = [
            {
                'risk': 'Ruptura de imports y dependencias',
                'mitigation': 'Crear script de actualización automática de imports'
            },
            {
                'risk': 'Pérdida de historial de git',
                'mitigation': 'Usar git mv para preservar el historial'
            },
            {
                'risk': 'Conflictos con desarrollo activo',
                'mitigation': 'Realizar backup completo y coordinar con equipo'
            },
            {
                'risk': 'Configuraciones hardcoded que fallen',
                'mitigation': 'Identificar y actualizar rutas hardcoded'
            }
        ]
        
        return plan
    
    def execute_reorganization(self, plan: Dict, dry_run: bool = True) -> Dict:
        """Ejecutar la reorganización según el plan"""
        self.logger.info(f"🚀 Ejecutando reorganización (dry_run={dry_run})...")
        
        results = {
            'status': 'success',
            'steps_completed': 0,
            'files_moved': 0,
            'directories_created': 0,
            'errors': [],
            'warnings': []
        }
        
        if not dry_run:
            # Crear backup
            self._create_backup()
            
            # Crear estructura objetivo
            self._create_target_structure()
        
        # Procesar pasos por prioridad
        for step in plan['reorganization_steps']:
            self.logger.info(f"Procesando paso {step['step_id']}: {step['description']}")
            
            try:
                for component_plan in step['components']:
                    current_path = self.project_root / component_plan['current_path']
                    target_path = self.new_structure_dir / component_plan['recommended_path'] / component_plan['component_name']
                    
                    if dry_run:
                        self.logger.info(f"  [DRY RUN] {current_path} -> {target_path}")
                    else:
                        # Mover directorio
                        if current_path.exists():
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(current_path), str(target_path))
                            results['files_moved'] += 1
                            self.logger.info(f"  Movido: {current_path} -> {target_path}")
                
                results['steps_completed'] += 1
                
            except Exception as e:
                error_msg = f"Error en paso {step['step_id']}: {str(e)}"
                results['errors'].append(error_msg)
                self.logger.error(error_msg)
        
        return results
    
    def _create_backup(self):
        """Crear backup de la estructura original"""
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        
        self.logger.info(f"📦 Creando backup en {self.backup_dir}")
        
        # Copiar solo los directorios relevantes, no todo el proyecto
        for item in self.project_root.iterdir():
            if item.name.startswith('_') or item.name.startswith('.'):
                continue
            if item.is_dir():
                shutil.copytree(item, self.backup_dir / item.name)
            else:
                shutil.copy2(item, self.backup_dir)
    
    def _create_target_structure(self):
        """Crear la estructura objetivo"""
        if self.new_structure_dir.exists():
            shutil.rmtree(self.new_structure_dir)
        
        self.logger.info(f"🏗️ Creando estructura objetivo en {self.new_structure_dir}")
        
        for structure_name, structure_info in self.target_structure.items():
            structure_path = self.new_structure_dir / structure_name
            structure_path.mkdir(parents=True, exist_ok=True)
            
            # Crear subdirectorios
            for subdir in structure_info['subdirs']:
                (structure_path / subdir).mkdir(parents=True, exist_ok=True)
            
            # Crear README.md explicativo
            readme_content = f"""# {structure_name.title()}

{structure_info['description']}

## Capa Arquitectónica
{structure_info['layer'].value}

## Subdirectorios
{chr(10).join([f"- `{subdir}`" for subdir in structure_info['subdirs']])}

## Prioridad de Reorganización
{structure_info['priority']}

---
*Generado automáticamente por VIGOLEONROCKS Architect Reorganizer*
"""
            
            (structure_path / "README.md").write_text(readme_content, encoding='utf-8')
    
    def _should_skip_directory(self, dir_path: str) -> bool:
        """Determina si debe saltarse un directorio"""
        skip_patterns = [
            '__pycache__',
            '.git',
            '.venv',
            'venv',
            'node_modules',
            '_backup_',
            '_new_optimized_',
            '.pytest_cache'
        ]
        
        return any(pattern in dir_path for pattern in skip_patterns)
    
    def _should_skip_file(self, filename: str) -> bool:
        """Determina si debe saltarse un archivo"""
        skip_patterns = [
            '.pyc',
            '.pyo',
            '.pyd',
            '__pycache__',
            '.DS_Store',
            'Thumbs.db',
            '.git'
        ]
        
        return any(filename.endswith(pattern) or pattern in filename for pattern in skip_patterns)
    
    def generate_reports(self, analysis: Dict, plan: Dict, results: Dict):
        """Generar reportes completos de la reorganización"""
        self.logger.info("📊 Generando reportes...")
        
        # Reporte principal
        main_report = {
            'project_analysis': analysis,
            'reorganization_plan': plan,
            'execution_results': results,
            'architectural_summary': self._generate_architectural_summary()
        }
        
        # Guardar reporte JSON
        report_file = self.project_root / "vigoleonrocks_reorganization_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(main_report, f, indent=2, ensure_ascii=False, default=str)
        
        # Generar reporte ASCII
        self._generate_ascii_report(analysis, plan, results)
        
        # Generar scripts de migración
        self._generate_migration_scripts(plan)
        
        self.logger.info("✅ Reportes generados exitosamente")
    
    def _generate_architectural_summary(self) -> Dict:
        """Generar resumen arquitectónico"""
        layer_distribution = defaultdict(int)
        technology_distribution = defaultdict(int)
        complexity_distribution = defaultdict(int)
        
        for component in self.components:
            layer_distribution[component.layer.value] += 1
            
            for tech in component.technologies:
                technology_distribution[tech] += 1
            
            if component.metrics.complexity < 5:
                complexity_distribution['low'] += 1
            elif component.metrics.complexity < 15:
                complexity_distribution['medium'] += 1
            else:
                complexity_distribution['high'] += 1
        
        return {
            'layer_distribution': dict(layer_distribution),
            'technology_distribution': dict(technology_distribution),
            'complexity_distribution': dict(complexity_distribution),
            'total_components': len(self.components),
            'high_priority_components': len([c for c in self.components if c.restructure_priority == 1])
        }
    
    def _generate_ascii_report(self, analysis: Dict, plan: Dict, results: Dict):
        """Generar reporte en formato ASCII"""
        report_lines = [
            "=" * 80,
            "VIGOLEONROCKS ARCHITECT REORGANIZER - REPORTE FINAL",
            "=" * 80,
            "",
            f"🕒 Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"📁 Proyecto: {self.project_root}",
            "",
            "ANÁLISIS ACTUAL:",
            "-" * 40,
            f"  📁 Directorios totales: {analysis['total_dirs']:,}",
            f"  📄 Archivos totales: {analysis['total_files']:,}",
            f"  📝 Líneas de código: {analysis['total_loc']:,}",
            "",
            "DISTRIBUCIÓN DE COMPLEJIDAD:",
            "-" * 40
        ]
        
        for level, count in analysis['complexity_levels'].items():
            report_lines.append(f"  {level.upper()}: {count:,} archivos")
        
        report_lines.extend([
            "",
            "TECNOLOGÍAS PRINCIPALES:",
            "-" * 40
        ])
        
        top_techs = sorted(analysis['technology_distribution'].items(), 
                          key=lambda x: x[1], reverse=True)[:10]
        for tech, count in top_techs:
            report_lines.append(f"  {tech}: {count:,} archivos")
        
        report_lines.extend([
            "",
            "PLAN DE REORGANIZACIÓN:",
            "-" * 40,
            f"  🏗️ Pasos totales: {len(plan['reorganization_steps'])}",
            f"  📦 Componentes a mover: {plan['metadata']['total_components']}",
            "",
            "PASOS POR PRIORIDAD:",
        ])
        
        for step in plan['reorganization_steps']:
            report_lines.append(f"  Prioridad {step['priority_level']}: {step['components_count']} componentes")
        
        report_lines.extend([
            "",
            "ESTRUCTURA OBJETIVO:",
            "-" * 40
        ])
        
        for structure_name, structure_info in self.target_structure.items():
            report_lines.append(f"  📁 {structure_name}/")
            for subdir in structure_info['subdirs']:
                report_lines.append(f"    └── {subdir}/")
        
        if results:
            report_lines.extend([
                "",
                "RESULTADOS DE EJECUCIÓN:",
                "-" * 40,
                f"  ✅ Estado: {results['status']}",
                f"  📝 Pasos completados: {results['steps_completed']}",
                f"  📁 Archivos movidos: {results['files_moved']}",
                f"  ⚠️ Errores: {len(results['errors'])}",
                f"  ⚡ Advertencias: {len(results['warnings'])}"
            ])
        
        report_lines.extend([
            "",
            "BENEFICIOS ESPERADOS:",
            "-" * 40
        ])
        
        for benefit in plan['expected_benefits']:
            report_lines.append(f"  ✅ {benefit}")
        
        report_lines.extend([
            "",
            "=" * 80,
            "Fin del reporte - VIGOLEONROCKS Architect Reorganizer v2.0.0",
            "=" * 80
        ])
        
        # Guardar reporte
        ascii_report_file = self.project_root / "vigoleonrocks_reorganization_report.txt"
        with open(ascii_report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
    
    def _generate_migration_scripts(self, plan: Dict):
        """Generar scripts de migración"""
        
        # Script de PowerShell para Windows
        powershell_lines = [
            "# VIGOLEONROCKS Architecture Reorganization Script",
            "# Generated automatically by VIGOLEONROCKS Architect Reorganizer",
            "",
            "param(",
            "    [switch]$DryRun = $false,",
            "    [switch]$CreateBackup = $true",
            ")",
            "",
            "$ErrorActionPreference = 'Stop'",
            "$ProjectRoot = $PSScriptRoot",
            "",
            "Write-Host '🚀 Iniciando reorganización de VIGOLEONROCKS...' -ForegroundColor Green",
            "",
            "# Crear backup si es necesario",
            "if ($CreateBackup) {",
            "    $BackupDir = Join-Path $ProjectRoot '_backup_original_structure'",
            "    Write-Host '📦 Creando backup...' -ForegroundColor Yellow",
            "    if (Test-Path $BackupDir) { Remove-Item $BackupDir -Recurse -Force }",
            "    Copy-Item $ProjectRoot $BackupDir -Recurse -Exclude '_backup_*','_new_optimized_*'",
            "}",
            "",
            "# Crear estructura objetivo",
            "$NewStructureDir = Join-Path $ProjectRoot '_new_optimized_structure'",
            "if (Test-Path $NewStructureDir) { Remove-Item $NewStructureDir -Recurse -Force }",
            "New-Item $NewStructureDir -ItemType Directory | Out-Null",
            ""
        ]
        
        # Agregar comandos de movimiento
        for step in plan['reorganization_steps']:
            powershell_lines.append(f"# Paso {step['step_id']}: {step['description']}")
            for component in step['components']:
                src = component['current_path'].replace('/', '\\')
                dst = component['recommended_path'].replace('/', '\\') + '\\' + component['component_name']
                
                powershell_lines.extend([
                    f"$src = Join-Path $ProjectRoot '{src}'",
                    f"$dst = Join-Path $NewStructureDir '{dst}'",
                    "if (Test-Path $src) {",
                    "    New-Item (Split-Path $dst) -ItemType Directory -Force | Out-Null",
                    "    if ($DryRun) {",
                    f"        Write-Host '[DRY RUN] Movería: {src} -> {dst}' -ForegroundColor Cyan",
                    "    } else {",
                    "        Move-Item $src $dst",
                    f"        Write-Host 'Movido: {component['component_name']}' -ForegroundColor Green",
                    "    }",
                    "}",
                    ""
                ])
        
        powershell_lines.extend([
            "Write-Host '✅ Reorganización completada!' -ForegroundColor Green",
            "Write-Host 'Revisa la nueva estructura en: _new_optimized_structure/' -ForegroundColor Yellow"
        ])
        
        # Guardar script de PowerShell
        ps_script_file = self.project_root / "reorganize_vigoleonrocks.ps1"
        with open(ps_script_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(powershell_lines))
        
        # También generar script de Python
        python_script = f"""#!/usr/bin/env python3
'''
Script de migración automática para VIGOLEONROCKS
Generado por VIGOLEONROCKS Architect Reorganizer
'''

import shutil
import os
from pathlib import Path

def reorganize_vigoleonrocks(dry_run=True):
    project_root = Path(__file__).parent
    backup_dir = project_root / '_backup_original_structure'
    new_structure_dir = project_root / '_new_optimized_structure'
    
    print('🚀 Iniciando reorganización de VIGOLEONROCKS...')
    
    if not dry_run:
        # Crear backup
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        print('📦 Creando backup...')
        shutil.copytree(project_root, backup_dir, ignore=shutil.ignore_patterns('_backup_*', '_new_optimized_*'))
        
        # Crear estructura objetivo  
        if new_structure_dir.exists():
            shutil.rmtree(new_structure_dir)
        new_structure_dir.mkdir()
    
    # Ejecutar movimientos
    movements = {json.dumps(plan['component_mappings'], indent=8)}
    
    for src_path, dst_path in movements.items():
        src = project_root / src_path
        dst = new_structure_dir / dst_path
        
        if dry_run:
            print(f'[DRY RUN] {{src}} -> {{dst}}')
        else:
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                print(f'Movido: {{src.name}}')
    
    print('✅ Reorganización completada!')

if __name__ == '__main__':
    import sys
    dry_run = '--dry-run' in sys.argv
    reorganize_vigoleonrocks(dry_run)
"""
        
        py_script_file = self.project_root / "reorganize_vigoleonrocks.py"
        with open(py_script_file, 'w', encoding='utf-8') as f:
            f.write(python_script)
        
        self.logger.info("📄 Scripts de migración generados")
    
    def run_complete_reorganization(self, dry_run: bool = True) -> Dict:
        """Ejecutar reorganización completa"""
        self.logger.info("🎯 Iniciando reorganización completa de VIGOLEONROCKS")
        
        start_time = time.time()
        
        # Paso 1: Analizar estructura actual
        analysis = self.analyze_current_structure()
        
        # Paso 2: Crear plan de reorganización
        plan = self.create_reorganization_plan()
        
        # Paso 3: Ejecutar reorganización
        results = self.execute_reorganization(plan, dry_run)
        
        # Paso 4: Generar reportes
        self.generate_reports(analysis, plan, results)
        
        end_time = time.time()
        duration = end_time - start_time
        
        summary = {
            'status': 'completed',
            'duration_seconds': duration,
            'dry_run': dry_run,
            'analysis': analysis,
            'plan': plan,
            'results': results
        }
        
        self.logger.info(f"🎉 Reorganización completa en {duration:.2f} segundos")
        return summary


def main():
    """Función principal"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    VIGOLEONROCKS ARCHITECT REORGANIZER                       ║
║                              Versión 2.0.0                                  ║
║                                                                              ║
║  Sistema avanzado de reorganización arquitectónica usando ingeniería        ║
║  inversa para alcanzar el máximo potencial del proyecto VIGOLEONROCKS       ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    import sys
    
    # Configuración por defecto
    project_root = r"C:\Users\Hp\Desktop\quantum-nlp-service"
    dry_run = True
    
    # Procesar argumentos
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    if '--execute' in sys.argv:
        dry_run = False
    
    print(f"📁 Proyecto: {project_root}")
    print(f"🔧 Modo: {'DRY RUN (simulación)' if dry_run else 'EJECUCIÓN REAL'}")
    print()
    
    if not dry_run:
        confirm = input("⚠️ ¿Estás seguro de que quieres ejecutar la reorganización real? (si/no): ")
        if confirm.lower() not in ['si', 'sí', 'yes', 'y']:
            print("❌ Operación cancelada")
            return
    
    # Crear reorganizador
    reorganizer = VIGOLEONROCKSArchitectReorganizer(project_root)
    
    # Ejecutar reorganización completa
    try:
        summary = reorganizer.run_complete_reorganization(dry_run)
        
        print("\n" + "="*80)
        print("🎉 REORGANIZACIÓN COMPLETADA EXITOSAMENTE")
        print("="*80)
        print(f"⏱️ Duración: {summary['duration_seconds']:.2f} segundos")
        print(f"📊 Componentes analizados: {summary['analysis']['total_dirs']}")
        print(f"📄 Archivos procesados: {summary['analysis']['total_files']:,}")
        print(f"📝 Líneas de código: {summary['analysis']['total_loc']:,}")
        
        if not dry_run:
            print(f"📁 Archivos movidos: {summary['results']['files_moved']}")
            print(f"✅ Pasos completados: {summary['results']['steps_completed']}")
        
        print("\n📋 Reportes generados:")
        print("   • vigoleonrocks_reorganization_report.json")
        print("   • vigoleonrocks_reorganization_report.txt")
        print("   • reorganize_vigoleonrocks.ps1")
        print("   • reorganize_vigoleonrocks.py")
        
        if dry_run:
            print("\n💡 Para ejecutar la reorganización real, usa: --execute")
        else:
            print(f"\n📁 Nueva estructura disponible en: _new_optimized_structure/")
            print(f"📦 Backup original en: _backup_original_structure/")
        
    except Exception as e:
        print(f"\n❌ Error durante la reorganización: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
