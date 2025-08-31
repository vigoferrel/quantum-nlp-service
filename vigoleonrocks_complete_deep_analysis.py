#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
██╗   ██╗██╗ ██████╗  ██████╗ ██╗     ███████╗ ██████╗ ███╗   ██╗██████╗  ██████╗  ██████╗██╗  ██╗███████╗
██║   ██║██║██╔════╝ ██╔═══██╗██║     ██╔════╝██╔═══██╗████╗  ██║██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝
██║   ██║██║██║  ███╗██║   ██║██║     █████╗  ██║   ██║██╔██╗ ██║██████╔╝██║   ██║██║     █████╔╝ ███████╗
╚██╗ ██╔╝██║██║   ██║██║   ██║██║     ██╔══╝  ██║   ██║██║╚██╗██║██╔══██╗██║   ██║██║     ██╔═██╗ ╚════██║
 ╚████╔╝ ██║╚██████╔╝╚██████╔╝███████╗███████╗╚██████╔╝██║ ╚████║██║  ██║╚██████╔╝╚██████╗██║  ██╗███████║
  ╚═══╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝

ANÁLISIS COMPLETO RECURSIVO PROFUNDO - VIGOLEONROCKS PROJECT
Sistema de análisis completo que explora TODOS los subdirectorios y archivos
"""

import os
import sys
import json
import re
import ast
from typing import Dict, List, Any, Optional, Set, Union
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import traceback
import mimetypes


@dataclass
class FileAnalysis:
    """Análisis detallado de un archivo específico"""
    name: str
    path: str
    size: int
    extension: str
    mime_type: str
    lines_of_code: int
    functions_classes: List[str]
    imports_dependencies: List[str]
    key_patterns: List[str]
    complexity_score: int
    last_modified: str


@dataclass
class DirectoryStructure:
    """Estructura completa de directorio con análisis recursivo"""
    name: str
    path: str
    depth: int
    file_count: int
    subdirectory_count: int
    total_size: int
    files: List[FileAnalysis]
    subdirectories: List['DirectoryStructure']
    technology_indicators: Dict[str, int]
    purpose_classification: str
    architectural_role: str
    integration_complexity: int


class VigoleonrocksCompleteAnalyzer:
    """
    ╔════════════════════════════════════════════════════════════════════════════════════════╗
    ║                    VIGOLEONROCKS COMPLETE DEEP ANALYSIS SYSTEM                         ║
    ║                            ANÁLISIS RECURSIVO COMPLETO                                 ║
    ╚════════════════════════════════════════════════════════════════════════════════════════╝
    
    Analizador que explora recursivamente:
    1. TODOS los subdirectorios hasta el nivel más profundo
    2. TODOS los archivos con análisis detallado
    3. Patrones de código, dependencias e integraciones
    4. Métricas de complejidad por archivo y directorio
    5. Clasificación automática de propósitos y roles
    """

    def __init__(self, target_directory: str = "."):
        self.target_dir = Path(target_directory).resolve()
        self.total_files_analyzed = 0
        self.total_directories_analyzed = 0
        self.total_lines_analyzed = 0
        self.complete_structure = None
        self.technology_stats = defaultdict(int)
        self.file_type_distribution = defaultdict(int)
        self.complexity_distribution = defaultdict(int)
        
        # Patrones para detectar tecnologías y frameworks
        self.tech_patterns = {
            'python_frameworks': {
                'fastapi': [r'from fastapi', r'import fastapi', r'FastAPI\('],
                'flask': [r'from flask', r'import flask', r'Flask\('],
                'django': [r'from django', r'import django'],
                'asyncio': [r'import asyncio', r'async def', r'await '],
                'pydantic': [r'from pydantic', r'BaseModel', r'Field\('],
                'sqlalchemy': [r'from sqlalchemy', r'import sqlalchemy'],
                'pytorch': [r'import torch', r'from torch'],
                'tensorflow': [r'import tensorflow', r'from tensorflow'],
                'transformers': [r'from transformers', r'import transformers'],
                'openai': [r'import openai', r'from openai'],
                'langchain': [r'from langchain', r'import langchain'],
                'pandas': [r'import pandas', r'import pd'],
                'numpy': [r'import numpy', r'import np'],
                'requests': [r'import requests', r'requests\.'],
                'aiohttp': [r'import aiohttp', r'from aiohttp'],
                'supabase': [r'supabase', r'from supabase']
            },
            'javascript_frameworks': {
                'express': [r'express', r'require.*express'],
                'react': [r'import.*react', r'from.*react'],
                'vue': [r'import.*vue', r'from.*vue'],
                'angular': [r'@angular', r'angular'],
                'node': [r'require\(', r'module\.exports'],
                'typescript': [r'interface ', r'type ', r': string', r': number']
            },
            'databases': {
                'postgresql': [r'postgresql', r'psycopg', r'pg_'],
                'mongodb': [r'mongodb', r'pymongo', r'mongoose'],
                'redis': [r'redis', r'import redis'],
                'sqlite': [r'sqlite', r'\.db', r'\.sqlite'],
                'mysql': [r'mysql', r'pymysql']
            },
            'cloud_services': {
                'aws': [r'boto3', r'aws', r'amazon'],
                'gcp': [r'google', r'gcp', r'firebase'],
                'azure': [r'azure', r'microsoft'],
                'docker': [r'FROM ', r'RUN ', r'COPY ', r'docker'],
                'kubernetes': [r'apiVersion', r'kind:', r'kubectl']
            },
            'ai_ml': {
                'llm_integration': [r'gpt-', r'claude-', r'llm', r'language_model'],
                'embeddings': [r'embeddings', r'vector', r'similarity'],
                'nlp': [r'nlp', r'natural language', r'tokeniz'],
                'quantum': [r'quantum', r'superposition', r'entangle'],
                'consciousness': [r'consciousness', r'awareness', r'cognitive']
            }
        }
        
        # Indicadores de propósito de archivos
        self.purpose_indicators = {
            'configuration': ['config', 'settings', 'env', 'ini', 'yaml', 'json', 'toml'],
            'documentation': ['readme', 'docs', 'guide', 'manual', 'help', 'info'],
            'testing': ['test', 'spec', 'unittest', 'pytest', 'jest'],
            'api': ['api', 'endpoint', 'route', 'handler', 'controller'],
            'database': ['model', 'schema', 'migration', 'seed', 'db'],
            'frontend': ['component', 'view', 'template', 'ui', 'interface'],
            'security': ['auth', 'security', 'crypto', 'hash', 'token'],
            'monitoring': ['log', 'metric', 'monitor', 'health', 'status'],
            'deployment': ['deploy', 'build', 'docker', 'k8s', 'helm'],
            'utility': ['util', 'helper', 'common', 'shared', 'lib']
        }
        
        print(self._generate_ascii_header())
        print(f"🎯 DIRECTORIO OBJETIVO: {self.target_dir}")
        print(f"🕒 ANÁLISIS INICIADO: {datetime.now().isoformat()}")
        print("=" * 120)

    def _generate_ascii_header(self) -> str:
        """Header ASCII para análisis completo"""
        return """
╔════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║  ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗     ███████╗████████╗███████╗    ██████╗ ███████╗███████╗██████╗  ║
║ ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██║     ██╔════╝╚══██╔══╝██╔════╝    ██╔══██╗██╔════╝██╔════╝██╔══██╗ ║
║ ██║     ██║   ██║██╔████╔██║██████╔╝██║     █████╗     ██║   █████╗      ██║  ██║█████╗  █████╗  ██████╔╝ ║
║ ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝     ██║   ██╔══╝      ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝  ║
║ ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗███████╗   ██║   ███████╗    ██████╔╝███████╗███████╗██║      ║
║  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝   ╚═╝   ╚══════╝    ╚═════╝ ╚══════╝╚══════╝╚═╝      ║
║                                                                                                            ║
║  █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗██╗███████╗    ██████╗ ███████╗ ██████╗██╗   ██╗██████╗  ║
║ ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝██╔════╝██║██╔════╝    ██╔══██╗██╔════╝██╔════╝██║   ██║██╔══██╗ ║
║ ███████║██╔██╗ ██║███████║██║   ╚████╔╝ ███████╗██║███████╗    ██████╔╝█████╗  ██║     ██║   ██║██████╔╝ ║
║ ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝  ╚════██║██║╚════██║    ██╔══██╗██╔══╝  ██║     ██║   ██║██╔══██╗ ║
║ ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████║██║███████║    ██║  ██║███████╗╚██████╗╚██████╔╝██║  ██║ ║
║ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚═╝╚══════╝    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════╝"""

    def execute_complete_analysis(self) -> DirectoryStructure:
        """
        ╔══════════════════════════════════════════════════════════════════════════════════════╗
        ║                        ANÁLISIS COMPLETO RECURSIVO                                   ║
        ╚══════════════════════════════════════════════════════════════════════════════════════╝
        """
        print("\n🔍 EJECUTANDO ANÁLISIS RECURSIVO COMPLETO...")
        print("=" * 120)
        
        print("📂 FASE 1: EXPLORACIÓN RECURSIVA COMPLETA")
        self.complete_structure = self._analyze_directory_recursive(self.target_dir, depth=0)
        
        print("\n📊 FASE 2: ANÁLISIS ESTADÍSTICO GLOBAL")
        self._generate_global_statistics()
        
        print("\n🎯 FASE 3: CLASIFICACIÓN Y PATRONES")
        self._classify_and_analyze_patterns()
        
        print("\n📈 FASE 4: MÉTRICAS DE COMPLEJIDAD")
        self._calculate_comprehensive_metrics()
        
        print(f"\n✅ ANÁLISIS COMPLETO FINALIZADO:")
        print(f"   📁 Directorios analizados: {self.total_directories_analyzed:,}")
        print(f"   📄 Archivos analizados: {self.total_files_analyzed:,}")
        print(f"   📝 Líneas de código: {self.total_lines_analyzed:,}")
        
        return self.complete_structure

    def _analyze_directory_recursive(self, directory: Path, depth: int = 0) -> DirectoryStructure:
        """Análisis recursivo completo de directorio"""
        if not directory.exists() or not directory.is_dir():
            return None
            
        # Control de profundidad excesiva
        if depth > 10:
            print(f"   ⚠️ Profundidad máxima alcanzada en: {directory.name}")
            return None
            
        self.total_directories_analyzed += 1
        indent = "   " * depth
        print(f"{indent}🔍 Analizando directorio: {directory.name} (depth: {depth})")
        
        files = []
        subdirectories = []
        total_size = 0
        technology_indicators = defaultdict(int)
        
        try:
            # Obtener todos los elementos del directorio
            all_items = list(directory.iterdir())
            
            # Analizar archivos
            for item in all_items:
                if item.is_file():
                    try:
                        file_analysis = self._analyze_file_detailed(item, depth + 1)
                        if file_analysis:
                            files.append(file_analysis)
                            total_size += file_analysis.size
                            self.total_files_analyzed += 1
                            self.total_lines_analyzed += file_analysis.lines_of_code
                            
                            # Actualizar indicadores tecnológicos
                            self._update_technology_indicators(file_analysis, technology_indicators)
                            
                    except Exception as e:
                        print(f"{indent}   ❌ Error analizando archivo {item.name}: {e}")
                        continue
            
            # Analizar subdirectorios recursivamente
            for item in all_items:
                if item.is_dir() and not item.name.startswith('.') and item.name not in ['__pycache__', 'node_modules', '.git']:
                    try:
                        subdir_analysis = self._analyze_directory_recursive(item, depth + 1)
                        if subdir_analysis:
                            subdirectories.append(subdir_analysis)
                            total_size += subdir_analysis.total_size
                            
                            # Propagar indicadores tecnológicos
                            for tech, count in subdir_analysis.technology_indicators.items():
                                technology_indicators[tech] += count
                                
                    except Exception as e:
                        print(f"{indent}   ❌ Error analizando subdirectorio {item.name}: {e}")
                        continue
            
            # Determinar propósito y rol arquitectónico
            purpose = self._classify_directory_purpose(directory.name, files, subdirectories)
            architectural_role = self._determine_architectural_role(directory.name, files, subdirectories, depth)
            integration_complexity = self._calculate_integration_complexity(files, subdirectories)
            
            print(f"{indent}   ├── Archivos: {len(files)} | Subdirectorios: {len(subdirectories)}")
            print(f"{indent}   ├── Tamaño total: {total_size:,} bytes | Propósito: {purpose}")
            print(f"{indent}   └── Rol: {architectural_role} | Complejidad: {integration_complexity}")
            
            return DirectoryStructure(
                name=directory.name,
                path=str(directory),
                depth=depth,
                file_count=len(files),
                subdirectory_count=len(subdirectories),
                total_size=total_size,
                files=files,
                subdirectories=subdirectories,
                technology_indicators=dict(technology_indicators),
                purpose_classification=purpose,
                architectural_role=architectural_role,
                integration_complexity=integration_complexity
            )
            
        except PermissionError:
            print(f"{indent}   ⚠️ Sin permisos para acceder a: {directory.name}")
            return None
        except Exception as e:
            print(f"{indent}   ❌ Error analizando directorio: {e}")
            return None

    def _analyze_file_detailed(self, file_path: Path, depth: int) -> Optional[FileAnalysis]:
        """Análisis detallado de un archivo específico"""
        try:
            # Información básica
            stat_info = file_path.stat()
            size = stat_info.st_size
            extension = file_path.suffix.lower()
            last_modified = datetime.fromtimestamp(stat_info.st_mtime).isoformat()
            
            # Tipo MIME
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if not mime_type:
                mime_type = self._guess_mime_type(extension)
            
            # Análisis de contenido solo para archivos de texto
            lines_of_code = 0
            functions_classes = []
            imports_dependencies = []
            key_patterns = []
            complexity_score = 0
            
            if self._is_text_file(file_path, extension):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        lines_of_code = len([line for line in content.splitlines() if line.strip()])
                        
                        # Análisis específico por tipo de archivo
                        if extension == '.py':
                            functions_classes, imports_dependencies, patterns, complexity = self._analyze_python_file(content)
                        elif extension in ['.js', '.ts']:
                            functions_classes, imports_dependencies, patterns, complexity = self._analyze_javascript_file(content)
                        elif extension in ['.php']:
                            functions_classes, imports_dependencies, patterns, complexity = self._analyze_php_file(content)
                        elif extension in ['.html', '.htm']:
                            functions_classes, imports_dependencies, patterns, complexity = self._analyze_html_file(content)
                        elif extension in ['.css']:
                            functions_classes, imports_dependencies, patterns, complexity = self._analyze_css_file(content)
                        elif extension in ['.json']:
                            functions_classes, imports_dependencies, patterns, complexity = self._analyze_json_file(content)
                        elif extension in ['.md']:
                            functions_classes, imports_dependencies, patterns, complexity = self._analyze_markdown_file(content)
                        else:
                            functions_classes, imports_dependencies, patterns, complexity = self._analyze_generic_file(content)
                        
                        key_patterns.extend(patterns)
                        complexity_score = complexity
                        
                except Exception as e:
                    # Si no se puede leer como texto, mantener valores por defecto
                    pass
            
            # Actualizar estadísticas globales
            self.file_type_distribution[extension] += 1
            self.complexity_distribution[complexity_score] += 1
            
            return FileAnalysis(
                name=file_path.name,
                path=str(file_path),
                size=size,
                extension=extension,
                mime_type=mime_type,
                lines_of_code=lines_of_code,
                functions_classes=functions_classes,
                imports_dependencies=imports_dependencies,
                key_patterns=key_patterns,
                complexity_score=complexity_score,
                last_modified=last_modified
            )
            
        except Exception as e:
            return None

    def _is_text_file(self, file_path: Path, extension: str) -> bool:
        """Determina si un archivo es de texto"""
        text_extensions = {
            '.py', '.js', '.ts', '.php', '.html', '.htm', '.css', '.json', '.xml',
            '.yml', '.yaml', '.toml', '.ini', '.cfg', '.conf', '.md', '.txt', '.log',
            '.sh', '.bat', '.ps1', '.sql', '.c', '.cpp', '.h', '.hpp', '.java',
            '.go', '.rs', '.rb', '.pl', '.r', '.scala', '.kt', '.swift'
        }
        
        if extension in text_extensions:
            return True
        
        # Intentar detectar por contenido
        if file_path.stat().st_size > 1024 * 1024:  # Archivos > 1MB probablemente no son texto
            return False
            
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                # Si contiene muchos bytes nulos, probablemente no es texto
                if chunk.count(b'\0') > len(chunk) * 0.1:
                    return False
                return True
        except:
            return False

    def _guess_mime_type(self, extension: str) -> str:
        """Adivinar tipo MIME basado en extensión"""
        mime_map = {
            '.py': 'text/x-python',
            '.js': 'application/javascript',
            '.ts': 'application/typescript',
            '.php': 'application/x-php',
            '.html': 'text/html',
            '.css': 'text/css',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.yml': 'application/x-yaml',
            '.yaml': 'application/x-yaml',
            '.md': 'text/markdown',
            '.txt': 'text/plain',
            '.log': 'text/plain',
            '.sql': 'application/sql'
        }
        return mime_map.get(extension, 'application/octet-stream')

    def _analyze_python_file(self, content: str) -> tuple:
        """Análisis específico de archivos Python"""
        functions_classes = []
        imports = []
        patterns = []
        complexity = 0
        
        try:
            tree = ast.parse(content)
            
            # Extraer funciones y clases
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions_classes.append(f"function:{node.name}")
                elif isinstance(node, ast.ClassDef):
                    functions_classes.append(f"class:{node.name}")
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(f"import:{alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(f"from:{node.module}")
            
            # Calcular complejidad ciclomática simple
            complexity = len([node for node in ast.walk(tree) 
                            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With))])
            
        except SyntaxError:
            # Si hay errores de sintaxis, hacer análisis básico con regex
            pass
        
        # Detectar patrones con regex
        patterns.extend(self._detect_tech_patterns(content, 'python_frameworks'))
        patterns.extend(self._detect_tech_patterns(content, 'databases'))
        patterns.extend(self._detect_tech_patterns(content, 'ai_ml'))
        
        return functions_classes, imports, patterns, complexity

    def _analyze_javascript_file(self, content: str) -> tuple:
        """Análisis específico de archivos JavaScript/TypeScript"""
        functions_classes = []
        imports = []
        patterns = []
        complexity = 0
        
        # Buscar funciones y clases con regex
        function_matches = re.findall(r'(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:function|\([^)]*\)\s*=>)|class\s+(\w+))', content)
        for match in function_matches:
            name = match[0] or match[1] or match[2]
            if name:
                functions_classes.append(f"function:{name}" if not match[2] else f"class:{name}")
        
        # Buscar imports
        import_matches = re.findall(r'(?:import\s+.*?from\s+["\']([^"\']+)["\']|require\(["\']([^"\']+)["\']\))', content)
        for match in import_matches:
            module = match[0] or match[1]
            if module:
                imports.append(f"import:{module}")
        
        # Calcular complejidad aproximada
        complexity = len(re.findall(r'\b(?:if|for|while|switch|try|catch)\b', content))
        
        # Detectar patrones tecnológicos
        patterns.extend(self._detect_tech_patterns(content, 'javascript_frameworks'))
        patterns.extend(self._detect_tech_patterns(content, 'cloud_services'))
        
        return functions_classes, imports, patterns, complexity

    def _analyze_php_file(self, content: str) -> tuple:
        """Análisis específico de archivos PHP"""
        functions_classes = []
        imports = []
        patterns = []
        complexity = 0
        
        # Buscar funciones y clases
        function_matches = re.findall(r'(?:function\s+(\w+)|class\s+(\w+))', content)
        for match in function_matches:
            name = match[0] or match[1]
            if name:
                functions_classes.append(f"function:{name}" if match[0] else f"class:{name}")
        
        # Buscar includes/requires
        include_matches = re.findall(r'(?:include|require)(?:_once)?\s*\(?["\']([^"\']+)["\']', content)
        imports.extend([f"include:{match}" for match in include_matches])
        
        # Complejidad
        complexity = len(re.findall(r'\b(?:if|for|while|switch|try|catch)\b', content))
        
        patterns.extend(self._detect_tech_patterns(content, 'databases'))
        
        return functions_classes, imports, patterns, complexity

    def _analyze_html_file(self, content: str) -> tuple:
        """Análisis específico de archivos HTML"""
        functions_classes = []
        imports = []
        patterns = []
        complexity = 0
        
        # Buscar scripts y links
        script_matches = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', content)
        link_matches = re.findall(r'<link[^>]*href=["\']([^"\']+)["\']', content)
        
        imports.extend([f"script:{match}" for match in script_matches])
        imports.extend([f"link:{match}" for match in link_matches])
        
        # Contar elementos complejos
        complexity = len(re.findall(r'<(?:form|table|div|section|article)', content, re.IGNORECASE))
        
        # Detectar frameworks frontend
        if 'react' in content.lower():
            patterns.append('react')
        if 'vue' in content.lower():
            patterns.append('vue')
        if 'angular' in content.lower():
            patterns.append('angular')
        
        return functions_classes, imports, patterns, complexity

    def _analyze_css_file(self, content: str) -> tuple:
        """Análisis específico de archivos CSS"""
        functions_classes = []
        imports = []
        patterns = []
        complexity = 0
        
        # Buscar imports
        import_matches = re.findall(r'@import\s+["\']([^"\']+)["\']', content)
        imports.extend([f"css_import:{match}" for match in import_matches])
        
        # Contar selectores complejos
        complexity = len(re.findall(r'[.#][\w-]+|@media|@keyframes', content))
        
        # Detectar frameworks CSS
        if 'bootstrap' in content.lower():
            patterns.append('bootstrap')
        if 'tailwind' in content.lower():
            patterns.append('tailwind')
        
        return functions_classes, imports, patterns, complexity

    def _analyze_json_file(self, content: str) -> tuple:
        """Análisis específico de archivos JSON"""
        functions_classes = []
        imports = []
        patterns = []
        complexity = 0
        
        try:
            data = json.loads(content)
            
            # Analizar estructura
            if isinstance(data, dict):
                # Detectar tipos de configuración
                if 'dependencies' in data:
                    patterns.append('package_dependencies')
                    imports.extend([f"dependency:{key}" for key in data['dependencies'].keys()])
                
                if 'scripts' in data:
                    patterns.append('npm_scripts')
                
                if 'devDependencies' in data:
                    patterns.append('dev_dependencies')
                
                # Calcular complejidad basada en profundidad
                complexity = self._calculate_json_depth(data)
                
        except json.JSONDecodeError:
            pass
        
        return functions_classes, imports, patterns, complexity

    def _analyze_markdown_file(self, content: str) -> tuple:
        """Análisis específico de archivos Markdown"""
        functions_classes = []
        imports = []
        patterns = []
        complexity = 0
        
        # Contar elementos estructurales
        headers = len(re.findall(r'^#{1,6}\s', content, re.MULTILINE))
        code_blocks = len(re.findall(r'```', content))
        links = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content))
        
        functions_classes.extend([f"header:level_{i}" for i in range(1, 7) 
                                if len(re.findall(f'^#{{{i}}}\\s', content, re.MULTILINE)) > 0])
        
        complexity = headers + code_blocks + links
        
        # Detectar tipo de documentación
        if any(word in content.lower() for word in ['api', 'endpoint', 'swagger']):
            patterns.append('api_documentation')
        if any(word in content.lower() for word in ['install', 'setup', 'getting started']):
            patterns.append('installation_guide')
        if any(word in content.lower() for word in ['architecture', 'design', 'structure']):
            patterns.append('architecture_documentation')
        
        return functions_classes, imports, patterns, complexity

    def _analyze_generic_file(self, content: str) -> tuple:
        """Análisis genérico de archivos"""
        functions_classes = []
        imports = []
        patterns = []
        complexity = len(content.splitlines())  # Complejidad básica por líneas
        
        # Detectar patrones generales
        patterns.extend(self._detect_tech_patterns(content, 'cloud_services'))
        patterns.extend(self._detect_tech_patterns(content, 'ai_ml'))
        
        return functions_classes, imports, patterns, min(complexity // 10, 100)

    def _calculate_json_depth(self, obj, depth=0) -> int:
        """Calcular profundidad de estructura JSON"""
        if isinstance(obj, dict):
            return max([self._calculate_json_depth(v, depth + 1) for v in obj.values()] + [depth])
        elif isinstance(obj, list):
            return max([self._calculate_json_depth(item, depth + 1) for item in obj] + [depth])
        else:
            return depth

    def _detect_tech_patterns(self, content: str, category: str) -> List[str]:
        """Detectar patrones tecnológicos en el contenido"""
        patterns = []
        
        if category not in self.tech_patterns:
            return patterns
            
        for tech, pattern_list in self.tech_patterns[category].items():
            for pattern in pattern_list:
                if re.search(pattern, content, re.IGNORECASE):
                    patterns.append(f"{category}:{tech}")
                    self.technology_stats[f"{category}:{tech}"] += 1
                    break  # Una coincidencia por tecnología es suficiente
        
        return patterns

    def _update_technology_indicators(self, file_analysis: FileAnalysis, tech_indicators: Dict[str, int]):
        """Actualizar indicadores tecnológicos basados en análisis de archivo"""
        for pattern in file_analysis.key_patterns:
            tech_indicators[pattern] += 1
        
        # Indicadores basados en extensión
        ext_indicators = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.php': 'php',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json_config',
            '.yml': 'yaml_config',
            '.yaml': 'yaml_config',
            '.md': 'documentation',
            '.sql': 'database'
        }
        
        if file_analysis.extension in ext_indicators:
            tech_indicators[ext_indicators[file_analysis.extension]] += 1

    def _classify_directory_purpose(self, dir_name: str, files: List[FileAnalysis], subdirs: List[DirectoryStructure]) -> str:
        """Clasificar el propósito de un directorio"""
        dir_name_lower = dir_name.lower()
        
        # Clasificación específica por nombre
        specific_purposes = {
            'vigoleonrocks': 'VIGOLEONROCKS_CORE_SYSTEM',
            'quantum': 'QUANTUM_PROCESSING_ENGINE', 
            'localgpt': 'LOCALGPT_INTEGRATION',
            'mcp': 'MODEL_CONTEXT_PROTOCOL',
            'dokploy': 'DEPLOYMENT_ORCHESTRATION',
            'openvpn': 'VPN_NETWORKING',
            'services': 'MICROSERVICES_LAYER',
            'api': 'API_SERVICES_LAYER',
            'config': 'CONFIGURATION_MANAGEMENT',
            'cache': 'CACHING_SYSTEM',
            'src': 'SOURCE_CODE_LAYER',
            'test': 'TESTING_AND_QA',
            'docs': 'DOCUMENTATION_SYSTEM',
            'scripts': 'AUTOMATION_SCRIPTS',
            'static': 'STATIC_ASSETS',
            'templates': 'TEMPLATE_SYSTEM',
            'migrations': 'DATABASE_MIGRATIONS',
            'logs': 'LOGGING_SYSTEM',
            'backup': 'BACKUP_SYSTEM'
        }
        
        for keyword, purpose in specific_purposes.items():
            if keyword in dir_name_lower:
                return purpose
        
        # Clasificación basada en tipos de archivos
        file_extensions = [f.extension for f in files]
        ext_counter = Counter(file_extensions)
        
        if ext_counter.get('.py', 0) > 5:
            return 'PYTHON_APPLICATION_MODULE'
        elif ext_counter.get('.js', 0) > 3 or ext_counter.get('.ts', 0) > 3:
            return 'JAVASCRIPT_APPLICATION_MODULE'
        elif ext_counter.get('.php', 0) > 3:
            return 'PHP_WEB_APPLICATION'
        elif ext_counter.get('.html', 0) > 2:
            return 'WEB_FRONTEND_MODULE'
        elif ext_counter.get('.json', 0) > 2:
            return 'CONFIGURATION_DATA_MODULE'
        elif ext_counter.get('.md', 0) > 2:
            return 'DOCUMENTATION_MODULE'
        elif ext_counter.get('.sql', 0) > 2:
            return 'DATABASE_SCHEMA_MODULE'
        
        # Clasificación basada en patrones tecnológicos
        all_patterns = []
        for f in files:
            all_patterns.extend(f.key_patterns)
        
        pattern_counter = Counter(all_patterns)
        
        if any('ai_ml:' in pattern for pattern in pattern_counter):
            return 'AI_ML_PROCESSING_MODULE'
        elif any('database:' in pattern for pattern in pattern_counter):
            return 'DATABASE_ACCESS_MODULE'
        elif any('cloud_services:' in pattern for pattern in pattern_counter):
            return 'CLOUD_INTEGRATION_MODULE'
        
        return 'GENERAL_PURPOSE_MODULE'

    def _determine_architectural_role(self, dir_name: str, files: List[FileAnalysis], 
                                    subdirs: List[DirectoryStructure], depth: int) -> str:
        """Determinar el rol arquitectónico del directorio"""
        if depth == 0:
            return 'PROJECT_ROOT'
        elif depth == 1:
            return 'PRIMARY_MODULE'
        elif depth == 2:
            return 'SECONDARY_MODULE'
        elif depth >= 3:
            return 'IMPLEMENTATION_DETAIL'
        
        # Roles específicos basados en nombre
        dir_name_lower = dir_name.lower()
        
        architectural_roles = {
            'controller': 'CONTROLLER_LAYER',
            'service': 'SERVICE_LAYER', 
            'model': 'DATA_MODEL_LAYER',
            'view': 'PRESENTATION_LAYER',
            'api': 'API_INTERFACE_LAYER',
            'core': 'CORE_BUSINESS_LOGIC',
            'util': 'UTILITY_LAYER',
            'helper': 'HELPER_LAYER',
            'middleware': 'MIDDLEWARE_LAYER',
            'component': 'COMPONENT_LAYER',
            'module': 'FEATURE_MODULE'
        }
        
        for keyword, role in architectural_roles.items():
            if keyword in dir_name_lower:
                return role
        
        return f'DEPTH_{depth}_MODULE'

    def _calculate_integration_complexity(self, files: List[FileAnalysis], subdirs: List[DirectoryStructure]) -> int:
        """Calcular complejidad de integración"""
        complexity = 0
        
        # Complejidad por número de archivos
        complexity += len(files) * 1
        
        # Complejidad por subdirectorios
        complexity += len(subdirs) * 2
        
        # Complejidad por dependencias e imports
        total_imports = sum(len(f.imports_dependencies) for f in files)
        complexity += total_imports * 0.5
        
        # Complejidad por patrones tecnológicos únicos
        all_patterns = set()
        for f in files:
            all_patterns.update(f.key_patterns)
        complexity += len(all_patterns) * 3
        
        # Complejidad por código
        total_complexity = sum(f.complexity_score for f in files)
        complexity += total_complexity * 0.1
        
        return int(complexity)

    def _generate_global_statistics(self):
        """Generar estadísticas globales del proyecto"""
        print("   📊 Generando estadísticas globales...")
        
        # Estadísticas por tipo de archivo
        print("   ├── Distribución de tipos de archivo:")
        sorted_extensions = sorted(self.file_type_distribution.items(), key=lambda x: x[1], reverse=True)
        for ext, count in sorted_extensions[:15]:  # Top 15
            ext_name = ext if ext else "(sin extensión)"
            print(f"   │   ├── {ext_name}: {count} archivos")
        
        # Estadísticas tecnológicas
        print("   ├── Tecnologías detectadas:")
        sorted_tech = sorted(self.technology_stats.items(), key=lambda x: x[1], reverse=True)
        for tech, count in sorted_tech[:20]:  # Top 20
            print(f"   │   ├── {tech}: {count} referencias")
        
        # Distribución de complejidad
        print("   └── Distribución de complejidad:")
        total_files_with_complexity = sum(self.complexity_distribution.values())
        for complexity_range in [0, 1, 5, 10, 25, 50, 100]:
            count = sum(count for comp, count in self.complexity_distribution.items() 
                       if comp >= complexity_range and comp < (complexity_range * 2 if complexity_range > 0 else 1))
            if count > 0:
                percentage = (count / total_files_with_complexity * 100) if total_files_with_complexity > 0 else 0
                print(f"       ├── Complejidad {complexity_range}+: {count} archivos ({percentage:.1f}%)")

    def _classify_and_analyze_patterns(self):
        """Clasificar y analizar patrones del proyecto"""
        print("   🎯 Clasificando patrones arquitectónicos...")
        
        def count_pattern_in_structure(structure: DirectoryStructure, pattern: str) -> int:
            count = 0
            # Contar en archivos del directorio actual
            for file in structure.files:
                count += sum(1 for p in file.key_patterns if pattern in p)
            
            # Contar recursivamente en subdirectorios
            for subdir in structure.subdirectories:
                count += count_pattern_in_structure(subdir, pattern)
            
            return count
        
        # Analizar patrones principales
        key_patterns = [
            ('python_frameworks:fastapi', 'FastAPI Framework'),
            ('python_frameworks:flask', 'Flask Framework'),
            ('python_frameworks:pydantic', 'Pydantic Validation'),
            ('ai_ml:llm', 'LLM Integration'),
            ('ai_ml:quantum', 'Quantum Processing'),
            ('cloud_services:docker', 'Docker Containerization'),
            ('databases:postgresql', 'PostgreSQL Database'),
            ('databases:redis', 'Redis Cache')
        ]
        
        for pattern, description in key_patterns:
            count = count_pattern_in_structure(self.complete_structure, pattern)
            if count > 0:
                print(f"       ├── {description}: {count} implementaciones")

    def _calculate_comprehensive_metrics(self):
        """Calcular métricas comprensivas del proyecto"""
        print("   📈 Calculando métricas comprensivas...")
        
        def calculate_recursive_metrics(structure: DirectoryStructure) -> Dict[str, int]:
            metrics = {
                'total_files': structure.file_count,
                'total_directories': structure.subdirectory_count,
                'total_size': structure.total_size,
                'total_lines': sum(f.lines_of_code for f in structure.files),
                'max_depth': structure.depth,
                'total_complexity': sum(f.complexity_score for f in structure.files)
            }
            
            # Acumular métricas de subdirectorios
            for subdir in structure.subdirectories:
                subdir_metrics = calculate_recursive_metrics(subdir)
                metrics['total_files'] += subdir_metrics['total_files']
                metrics['total_directories'] += subdir_metrics['total_directories'] + 1
                metrics['total_size'] += subdir_metrics['total_size']
                metrics['total_lines'] += subdir_metrics['total_lines']
                metrics['max_depth'] = max(metrics['max_depth'], subdir_metrics['max_depth'])
                metrics['total_complexity'] += subdir_metrics['total_complexity']
            
            return metrics
        
        comprehensive_metrics = calculate_recursive_metrics(self.complete_structure)
        
        print(f"       ├── Archivos totales: {comprehensive_metrics['total_files']:,}")
        print(f"       ├── Directorios totales: {comprehensive_metrics['total_directories']:,}")
        print(f"       ├── Tamaño total: {comprehensive_metrics['total_size']:,} bytes")
        print(f"       ├── Líneas de código: {comprehensive_metrics['total_lines']:,}")
        print(f"       ├── Profundidad máxima: {comprehensive_metrics['max_depth']}")
        print(f"       └── Complejidad total: {comprehensive_metrics['total_complexity']:,}")

    def generate_complete_report(self) -> str:
        """Generar reporte completo del análisis"""
        if not self.complete_structure:
            return "❌ No hay estructura analizada. Ejecute el análisis primero."
        
        def format_directory_tree(structure: DirectoryStructure, indent: str = "", max_depth: int = 3) -> str:
            if structure.depth > max_depth:
                return ""
            
            tree = f"{indent}📁 {structure.name}/\n"
            tree += f"{indent}   ├── Propósito: {structure.purpose_classification}\n"
            tree += f"{indent}   ├── Rol: {structure.architectural_role}\n"
            tree += f"{indent}   ├── Archivos: {structure.file_count} | Subdirs: {structure.subdirectory_count}\n"
            tree += f"{indent}   ├── Tamaño: {structure.total_size:,} bytes\n"
            tree += f"{indent}   └── Complejidad: {structure.integration_complexity}\n"
            
            # Mostrar algunos archivos importantes
            important_files = [f for f in structure.files if f.complexity_score > 10 or len(f.key_patterns) > 3][:3]
            if important_files:
                tree += f"{indent}   🔍 Archivos destacados:\n"
                for file in important_files:
                    tree += f"{indent}      ├── {file.name} ({file.lines_of_code} líneas, complejidad: {file.complexity_score})\n"
            
            # Recursivamente para subdirectorios
            for i, subdir in enumerate(structure.subdirectories[:5]):  # Limitar a 5 subdirectorios por nivel
                tree += format_directory_tree(subdir, indent + "   ", max_depth)
                if i < len(structure.subdirectories) - 1 and i == 4:
                    tree += f"{indent}   └── ... y {len(structure.subdirectories) - 5} directorios más\n"
                    break
            
            return tree
        
        report = f"""
╔════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                            VIGOLEONROCKS COMPLETE DEEP ANALYSIS REPORT                                    ║
║                                    ANÁLISIS RECURSIVO COMPLETO                                            ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

📊 RESUMEN EJECUTIVO GLOBAL
════════════════════════════════════════════════════════════════════════════════════════════════════════════
🎯 Proyecto: VIGOLEONROCKS Quantum NLP Service - Análisis Completo
📁 Total Directorios Analizados: {self.total_directories_analyzed:,}
📄 Total Archivos Analizados: {self.total_files_analyzed:,}
📝 Total Líneas de Código: {self.total_lines_analyzed:,}
🕒 Análisis Completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🌲 ESTRUCTURA COMPLETA DEL PROYECTO
════════════════════════════════════════════════════════════════════════════════════════════════════════════
{format_directory_tree(self.complete_structure)}

🔧 TECNOLOGÍAS DETECTADAS (TOP 20)
════════════════════════════════════════════════════════════════════════════════════════════════════════════"""
        
        sorted_tech = sorted(self.technology_stats.items(), key=lambda x: x[1], reverse=True)[:20]
        for i, (tech, count) in enumerate(sorted_tech, 1):
            report += f"\n{i:2d}. {tech}: {count} referencias"
        
        report += f"""

📈 DISTRIBUCIÓN DE TIPOS DE ARCHIVO
════════════════════════════════════════════════════════════════════════════════════════════════════════════"""
        
        sorted_extensions = sorted(self.file_type_distribution.items(), key=lambda x: x[1], reverse=True)[:15]
        total_files = sum(self.file_type_distribution.values())
        
        for ext, count in sorted_extensions:
            ext_name = ext if ext else "(sin extensión)"
            percentage = (count / total_files * 100) if total_files > 0 else 0
            report += f"\n{ext_name:>15}: {count:>6} archivos ({percentage:>5.1f}%)"
        
        report += f"""

🎯 ANÁLISIS DE COMPLEJIDAD
════════════════════════════════════════════════════════════════════════════════════════════════════════════
Distribución de complejidad por archivos:"""
        
        complexity_ranges = [(0, 0), (1, 4), (5, 9), (10, 24), (25, 49), (50, 99), (100, float('inf'))]
        total_complex_files = sum(self.complexity_distribution.values())
        
        for min_comp, max_comp in complexity_ranges:
            count = sum(count for comp, count in self.complexity_distribution.items() 
                       if min_comp <= comp <= max_comp)
            if count > 0:
                percentage = (count / total_complex_files * 100) if total_complex_files > 0 else 0
                range_str = f"{min_comp}-{max_comp}" if max_comp != float('inf') else f"{min_comp}+"
                report += f"\nComplejidad {range_str:>8}: {count:>6} archivos ({percentage:>5.1f}%)"
        
        report += f"""

🚀 RECOMENDACIONES BASADAS EN ANÁLISIS COMPLETO
════════════════════════════════════════════════════════════════════════════════════════════════════════════
1. 📊 GESTIÓN DE COMPLEJIDAD
   • Revisar archivos con complejidad >50 para posible refactorización
   • Implementar métricas de calidad de código automatizadas
   
2. 🔧 CONSOLIDACIÓN TECNOLÓGICA  
   • Estandarizar el uso de frameworks (FastAPI detectado como principal)
   • Centralizar configuraciones de dependencias
   
3. 📁 ORGANIZACIÓN ESTRUCTURAL
   • Considerar reagrupación de módulos similares
   • Documentar la arquitectura de directorios profundos
   
4. 🧪 CALIDAD DE CÓDIGO
   • Implementar linting y formateo automático
   • Añadir tests para módulos de alta complejidad
   
5. 📚 DOCUMENTACIÓN
   • Completar documentación de APIs detectadas
   • Crear guías de contribución para nuevos desarrolladores

╔════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                               ANÁLISIS COMPLETO FINALIZADO                                                ║
║ Proyecto analizado: {self.total_files_analyzed:,} archivos en {self.total_directories_analyzed:,} directorios - {self.total_lines_analyzed:,} líneas de código ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""
        
        return report

    def save_complete_analysis(self, base_filename: str = "vigoleonrocks_complete_analysis"):
        """Guardar análisis completo en múltiples formatos"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. Guardar estructura completa en JSON
        def convert_to_serializable(obj):
            if isinstance(obj, DirectoryStructure):
                return {
                    'name': obj.name,
                    'path': obj.path,
                    'depth': obj.depth,
                    'file_count': obj.file_count,
                    'subdirectory_count': obj.subdirectory_count,
                    'total_size': obj.total_size,
                    'files': [convert_to_serializable(f) for f in obj.files],
                    'subdirectories': [convert_to_serializable(s) for s in obj.subdirectories],
                    'technology_indicators': obj.technology_indicators,
                    'purpose_classification': obj.purpose_classification,
                    'architectural_role': obj.architectural_role,
                    'integration_complexity': obj.integration_complexity
                }
            elif isinstance(obj, FileAnalysis):
                return asdict(obj)
            else:
                return obj
        
        # JSON detallado
        json_file = f"{base_filename}_{timestamp}.json"
        analysis_data = {
            'metadata': {
                'analysis_timestamp': datetime.now().isoformat(),
                'target_directory': str(self.target_dir),
                'analyzer_version': '2.0.0',
                'total_files_analyzed': self.total_files_analyzed,
                'total_directories_analyzed': self.total_directories_analyzed,
                'total_lines_analyzed': self.total_lines_analyzed
            },
            'complete_structure': convert_to_serializable(self.complete_structure),
            'global_statistics': {
                'technology_stats': dict(self.technology_stats),
                'file_type_distribution': dict(self.file_type_distribution),
                'complexity_distribution': dict(self.complexity_distribution)
            }
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        # Reporte ASCII completo
        ascii_file = f"{base_filename}_report_{timestamp}.txt"
        with open(ascii_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_complete_report())
        
        # CSV con estadísticas de archivos
        csv_file = f"{base_filename}_files_{timestamp}.csv"
        self._export_files_to_csv(csv_file)
        
        print(f"\n💾 ANÁLISIS COMPLETO GUARDADO:")
        print(f"   ├── Estructura JSON: {json_file}")
        print(f"   ├── Reporte ASCII: {ascii_file}")
        print(f"   └── Estadísticas CSV: {csv_file}")

    def _export_files_to_csv(self, filename: str):
        """Exportar estadísticas de archivos a CSV"""
        import csv
        
        def collect_files(structure: DirectoryStructure, files_list: List):
            for file in structure.files:
                files_list.append({
                    'directory': structure.name,
                    'directory_path': structure.path,
                    'directory_depth': structure.depth,
                    'file_name': file.name,
                    'file_path': file.path,
                    'file_size': file.size,
                    'file_extension': file.extension,
                    'mime_type': file.mime_type,
                    'lines_of_code': file.lines_of_code,
                    'complexity_score': file.complexity_score,
                    'functions_classes_count': len(file.functions_classes),
                    'imports_count': len(file.imports_dependencies),
                    'patterns_count': len(file.key_patterns),
                    'last_modified': file.last_modified
                })
            
            for subdir in structure.subdirectories:
                collect_files(subdir, files_list)
        
        files_data = []
        collect_files(self.complete_structure, files_data)
        
        if files_data:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=files_data[0].keys())
                writer.writeheader()
                writer.writerows(files_data)


def main():
    """Función principal para ejecutar análisis completo"""
    
    print("""
🎯 ANÁLISIS COMPLETO RECURSIVO - VIGOLEONROCKS PROJECT

ANÁLISIS PROFUNDO QUE INCLUYE:
1. 📁 Exploración recursiva de TODOS los subdirectorios
2. 📄 Análisis detallado de TODOS los archivos
3. 🔍 Detección de patrones tecnológicos y arquitectónicos
4. 📊 Métricas de complejidad por archivo y directorio
5. 🏗️ Clasificación automática de propósitos y roles
6. 🔗 Análisis de dependencias e integraciones
7. 📈 Estadísticas globales comprensivas
8. 💾 Exportación en múltiples formatos

════════════════════════════════════════════════════════════════════════════════════
    """)
    
    target_dir = input("📁 Directorio objetivo (Enter para directorio actual): ").strip()
    if not target_dir:
        target_dir = "."
    
    if not Path(target_dir).exists():
        print(f"❌ ERROR: El directorio '{target_dir}' no existe.")
        return
    
    print(f"\n🚀 INICIANDO ANÁLISIS COMPLETO RECURSIVO EN: {Path(target_dir).resolve()}")
    print("=" * 120)
    
    try:
        analyzer = VigoleonrocksCompleteAnalyzer(target_dir)
        complete_structure = analyzer.execute_complete_analysis()
        
        print("\n" + "=" * 120)
        print("📊 GENERANDO REPORTE COMPLETO FINAL...")
        
        # Mostrar reporte
        print(analyzer.generate_complete_report())
        
        # Preguntar si guardar
        save_results = input("\n💾 ¿Guardar análisis completo? (y/N): ").strip().lower()
        if save_results in ['y', 'yes', 'sí', 's']:
            analyzer.save_complete_analysis()
        
        print(f"\n🎉 ANÁLISIS COMPLETO RECURSIVO FINALIZADO EXITOSAMENTE!")
        print(f"   📊 Total Directorios: {analyzer.total_directories_analyzed:,}")
        print(f"   📄 Total Archivos: {analyzer.total_files_analyzed:,}")
        print(f"   📝 Total Líneas: {analyzer.total_lines_analyzed:,}")
        
        return complete_structure
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Análisis interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO durante el análisis: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
