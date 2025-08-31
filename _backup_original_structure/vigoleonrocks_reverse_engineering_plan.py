#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
██╗   ██╗██╗ ██████╗  ██████╗ ██╗     ███████╗ ██████╗ ███╗   ██╗██████╗  ██████╗  ██████╗██╗  ██╗███████╗
██║   ██║██║██╔════╝ ██╔═══██╗██║     ██╔════╝██╔═══██╗████╗  ██║██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝
██║   ██║██║██║  ███╗██║   ██║██║     █████╗  ██║   ██║██╔██╗ ██║██████╔╝██║   ██║██║     █████╔╝ ███████╗
╚██╗ ██╔╝██║██║   ██║██║   ██║██║     ██╔══╝  ██║   ██║██║╚██╗██║██╔══██╗██║   ██║██║     ██╔═██╗ ╚════██║
 ╚████╔╝ ██║╚██████╔╝╚██████╔╝███████╗███████╗╚██████╔╝██║ ╚████║██║  ██║╚██████╔╝╚██████╗██║  ██╗███████║
  ╚═══╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝

REVERSE ENGINEERING PLAN - PYDANTIC COMPONENTS ANALYSIS
Sistema de ingeniería inversa específico para componentes Pydantic de VIGOLEONROCKS
"""

import os
import sys
import ast
import json
import re
import inspect
import importlib.util
from typing import Dict, List, Any, Optional, Set, Union
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
import traceback


@dataclass
class PydanticModelInfo:
    """Información detallada de un modelo Pydantic"""
    name: str
    file_path: str
    line_number: int
    fields: List[Dict[str, Any]]
    validators: List[Dict[str, Any]]
    config_options: Dict[str, Any]
    methods: List[str]
    inheritance: List[str]
    decorators: List[str]


@dataclass
class APIEndpointInfo:
    """Información de endpoint de API"""
    method: str
    path: str
    function_name: str
    file_path: str
    line_number: int
    request_model: Optional[str]
    response_model: Optional[str]
    parameters: List[Dict[str, Any]]
    security: List[str]


class VigoleonrocksPydanticAnalyzer:
    """
    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                    VIGOLEONROCKS PYDANTIC REVERSE ENGINEERING                        ║
    ║                            COMPONENTES ESPECIALIZADOS                                ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝
    
    Analizador especializado en componentes Pydantic para:
    1. Modelos de datos (BaseModel classes)
    2. Validadores y Field definitions
    3. Endpoints de FastAPI
    4. Esquemas de request/response
    5. Configuraciones de validación
    """

    def __init__(self, target_directory: str = "."):
        self.target_dir = Path(target_directory).resolve()
        self.pydantic_models: List[PydanticModelInfo] = []
        self.api_endpoints: List[APIEndpointInfo] = []
        self.analysis_results = {}
        
        print(self._generate_ascii_header())
        print(f"🎯 DIRECTORIO OBJETIVO: {self.target_dir}")
        print(f"🕒 ANÁLISIS INICIADO: {datetime.now().isoformat()}")
        print("=" * 88)

    def _generate_ascii_header(self) -> str:
        """Header ASCII especializado"""
        return """
╔══════════════════════════════════════════════════════════════════════════════════════╗
║  ██████╗ ██╗   ██╗██████╗  █████╗ ███╗   ██╗████████╗██╗ ██████╗                   ║
║  ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗████╗  ██║╚══██╔══╝██║██╔════╝                   ║
║  ██████╔╝ ╚████╔╝ ██║  ██║███████║██╔██╗ ██║   ██║   ██║██║                        ║
║  ██╔═══╝   ╚██╔╝  ██║  ██║██╔══██║██║╚██╗██║   ██║   ██║██║                        ║
║  ██║        ██║   ██████╔╝██║  ██║██║ ╚████║   ██║   ██║╚██████╗                   ║
║  ╚═╝        ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝ ╚═════╝                   ║
║                                                                                      ║
║  ██████╗ ███████╗██╗   ██╗███████╗██████╗ ███████╗███████╗                         ║
║  ██╔══██╗██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝                         ║
║  ██████╔╝█████╗  ██║   ██║█████╗  ██████╔╝███████╗█████╗                           ║
║  ██╔══██╗██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝                           ║
║  ██║  ██║███████╗ ╚████╔╝ ███████╗██║  ██║███████║███████╗                         ║
║  ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝                         ║
║                                                                                      ║
║  ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗███████╗██████╗ ██╗███╗   ██╗ ██████╗  ║
║  ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║████╗  ██║██╔════╝  ║
║  █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  █████╗  ██████╔╝██║██╔██╗ ██║██║  ███╗ ║
║  ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  ██╔══╝  ██╔══██╗██║██║╚██╗██║██║   ██║ ║
║  ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗███████╗██║  ██║██║██║ ╚████║╚██████╔╝ ║
║  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝  ║
╚══════════════════════════════════════════════════════════════════════════════════════╝"""

    def execute_comprehensive_analysis(self) -> Dict[str, Any]:
        """
        ╔══════════════════════════════════════════════════════════════════════════════╗
        ║                        ANÁLISIS COMPLETO - PLAN DE EJECUCIÓN                 ║
        ╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print("\n🔍 EJECUTANDO PLAN DE INGENIERÍA INVERSA COMPLETO...")
        print("=" * 88)
        
        # FASE 1: Escaneo de archivos Python
        python_files = self._scan_python_files()
        print(f"📁 ARCHIVOS PYTHON DETECTADOS: {len(python_files)}")
        
        # FASE 2: Análisis específico de Pydantic
        print("\n🧬 FASE 2: ANÁLISIS COMPONENTES PYDANTIC")
        self._analyze_pydantic_models(python_files)
        
        # FASE 3: Análisis de endpoints FastAPI
        print("\n🌐 FASE 3: ANÁLISIS ENDPOINTS FASTAPI")
        self._analyze_fastapi_endpoints(python_files)
        
        # FASE 4: Análisis de dependencias e integraciones
        print("\n🔗 FASE 4: ANÁLISIS DEPENDENCIAS E INTEGRACIONES")
        self._analyze_dependencies_and_integrations(python_files)
        
        # FASE 5: Generación de reporte de ingeniería inversa
        print("\n📊 FASE 5: GENERACIÓN REPORTE COMPLETO")
        return self._generate_comprehensive_report()

    def _scan_python_files(self) -> List[Path]:
        """Escaneo inteligente de archivos Python relevantes"""
        python_files = []
        
        # Patrones de archivos relevantes para análisis Pydantic
        relevant_patterns = [
            "*api*.py", "*server*.py", "*model*.py", "*schema*.py",
            "*request*.py", "*response*.py", "*endpoint*.py",
            "*vigoleonrocks*.py", "*quantum*.py", "*multimodal*.py"
        ]
        
        print("   🔍 Escaneando archivos con patrones relevantes...")
        
        for pattern in relevant_patterns:
            for file_path in self.target_dir.glob(pattern):
                if file_path.is_file() and file_path not in python_files:
                    python_files.append(file_path)
                    print(f"      ├── {file_path.name}")
        
        # Escaneo recursivo en subdirectorios clave
        key_subdirs = ["api", "models", "schemas", "endpoints", "services"]
        for subdir in key_subdirs:
            subdir_path = self.target_dir / subdir
            if subdir_path.exists():
                for file_path in subdir_path.rglob("*.py"):
                    if file_path not in python_files:
                        python_files.append(file_path)
        
        return python_files

    def _analyze_pydantic_models(self, files: List[Path]):
        """
        ╔══════════════════════════════════════════════════════════════════════════╗
        ║                      ANÁLISIS ESPECÍFICO MODELOS PYDANTIC                ║
        ╚══════════════════════════════════════════════════════════════════════════╝
        """
        pydantic_files = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Detectar uso de Pydantic
                if self._contains_pydantic(content):
                    pydantic_files.append(file_path)
                    print(f"   🧬 PYDANTIC DETECTADO: {file_path.name}")
                    
                    # Análisis detallado del archivo
                    models = self._extract_pydantic_models_detailed(file_path, content)
                    self.pydantic_models.extend(models)
                    
            except Exception as e:
                print(f"   ❌ ERROR procesando {file_path.name}: {e}")
        
        print(f"📊 TOTAL MODELOS PYDANTIC: {len(self.pydantic_models)}")
        
        # Mostrar resumen de modelos encontrados
        for model in self.pydantic_models:
            print(f"   ├── {model.name} ({len(model.fields)} campos, {len(model.validators)} validators)")

    def _contains_pydantic(self, content: str) -> bool:
        """Detecta uso de Pydantic en el contenido"""
        pydantic_indicators = [
            'from pydantic import',
            'import pydantic',
            'BaseModel',
            'Field(',
            '@validator',
            'ValidationError'
        ]
        return any(indicator in content for indicator in pydantic_indicators)

    def _extract_pydantic_models_detailed(self, file_path: Path, content: str) -> List[PydanticModelInfo]:
        """Extracción detallada de modelos Pydantic"""
        models = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Verificar si hereda de BaseModel
                    if self._inherits_from_basemodel(node):
                        model_info = self._analyze_pydantic_class_detailed(node, file_path)
                        models.append(model_info)
                        print(f"      ├── BaseModel: {model_info.name}")
                        print(f"      │   ├── Campos: {len(model_info.fields)}")
                        print(f"      │   ├── Validators: {len(model_info.validators)}")
                        print(f"      │   └── Config: {len(model_info.config_options)} opciones")
                        
        except SyntaxError as e:
            print(f"      ❌ Error sintaxis en {file_path.name}: {e}")
        except Exception as e:
            print(f"      ❌ Error analizando {file_path.name}: {e}")
        
        return models

    def _inherits_from_basemodel(self, class_node: ast.ClassDef) -> bool:
        """Verifica si una clase hereda de BaseModel"""
        for base in class_node.bases:
            if isinstance(base, ast.Name) and base.id == 'BaseModel':
                return True
            elif isinstance(base, ast.Attribute) and base.attr == 'BaseModel':
                return True
        return False

    def _analyze_pydantic_class_detailed(self, class_node: ast.ClassDef, file_path: Path) -> PydanticModelInfo:
        """Análisis detallado de una clase Pydantic"""
        
        fields = []
        validators = []
        config_options = {}
        methods = []
        decorators = [ast.unparse(d) for d in class_node.decorator_list]
        inheritance = [ast.unparse(base) for base in class_node.bases]
        
        for node in class_node.body:
            if isinstance(node, ast.AnnAssign):
                # Campo del modelo
                field_info = self._extract_field_detailed(node)
                if field_info:
                    fields.append(field_info)
                    
            elif isinstance(node, ast.FunctionDef):
                # Método o validator
                method_name = node.name
                is_validator = any(
                    isinstance(d, ast.Name) and d.id == 'validator' or
                    isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == 'validator'
                    for d in node.decorator_list
                )
                
                if is_validator:
                    validator_info = {
                        'name': method_name,
                        'line_number': node.lineno,
                        'fields': self._extract_validator_fields(node),
                        'decorators': [ast.unparse(d) for d in node.decorator_list]
                    }
                    validators.append(validator_info)
                else:
                    methods.append(method_name)
                    
            elif isinstance(node, ast.ClassDef) and node.name == 'Config':
                # Configuración del modelo
                config_options = self._extract_config_options(node)
        
        return PydanticModelInfo(
            name=class_node.name,
            file_path=str(file_path),
            line_number=class_node.lineno,
            fields=fields,
            validators=validators,
            config_options=config_options,
            methods=methods,
            inheritance=inheritance,
            decorators=decorators
        )

    def _extract_field_detailed(self, node: ast.AnnAssign) -> Optional[Dict[str, Any]]:
        """Extracción detallada de información de campo"""
        if not node.target or not isinstance(node.target, ast.Name):
            return None
            
        field_name = node.target.id
        field_type = ast.unparse(node.annotation) if node.annotation else 'Any'
        
        field_info = {
            'name': field_name,
            'type': field_type,
            'default': None,
            'field_constraints': {},
            'is_optional': 'Optional' in field_type or 'Union' in field_type,
            'is_list': 'List' in field_type or 'Sequence' in field_type,
            'line_number': node.lineno
        }
        
        # Analizar valor por defecto y Field()
        if node.value:
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'Field':
                field_info['field_constraints'] = self._extract_field_constraints(node.value)
                field_info['has_field_info'] = True
            else:
                field_info['default'] = ast.unparse(node.value)
                field_info['has_field_info'] = False
        
        return field_info

    def _extract_field_constraints(self, field_call: ast.Call) -> Dict[str, Any]:
        """Extrae constraints de Field()"""
        constraints = {}
        
        # Argumentos posicionales
        for i, arg in enumerate(field_call.args):
            constraints[f'default_{i}'] = ast.unparse(arg)
        
        # Argumentos nombrados
        for keyword in field_call.keywords:
            constraints[keyword.arg] = ast.unparse(keyword.value)
        
        return constraints

    def _extract_validator_fields(self, validator_node: ast.FunctionDef) -> List[str]:
        """Extrae campos que valida un validator"""
        fields = []
        
        for decorator in validator_node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == 'validator':
                for arg in decorator.args:
                    if isinstance(arg, ast.Constant):
                        fields.append(arg.value)
        
        return fields

    def _extract_config_options(self, config_node: ast.ClassDef) -> Dict[str, Any]:
        """Extrae opciones de configuración del modelo"""
        config = {}
        
        for node in config_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        config[target.id] = ast.unparse(node.value)
        
        return config

    def _analyze_fastapi_endpoints(self, files: List[Path]):
        """
        ╔══════════════════════════════════════════════════════════════════════╗
        ║                    ANÁLISIS ENDPOINTS FASTAPI                        ║
        ╚══════════════════════════════════════════════════════════════════════╝
        """
        api_files = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Detectar FastAPI
                if self._contains_fastapi(content):
                    api_files.append(file_path)
                    print(f"   🌐 FASTAPI DETECTADO: {file_path.name}")
                    
                    endpoints = self._extract_fastapi_endpoints(file_path, content)
                    self.api_endpoints.extend(endpoints)
                    
            except Exception as e:
                print(f"   ❌ ERROR procesando {file_path.name}: {e}")
        
        print(f"📊 TOTAL ENDPOINTS API: {len(self.api_endpoints)}")
        
        # Mostrar resumen de endpoints
        for endpoint in self.api_endpoints:
            print(f"   ├── {endpoint.method} {endpoint.path} -> {endpoint.function_name}()")
            if endpoint.request_model:
                print(f"   │   ├── Request: {endpoint.request_model}")
            if endpoint.response_model:
                print(f"   │   └── Response: {endpoint.response_model}")

    def _contains_fastapi(self, content: str) -> bool:
        """Detecta uso de FastAPI"""
        fastapi_indicators = [
            'from fastapi import',
            'import fastapi',
            'FastAPI(',
            '@app.',
            '@router.',
            'HTTPException',
            'APIRouter'
        ]
        return any(indicator in content for indicator in fastapi_indicators)

    def _extract_fastapi_endpoints(self, file_path: Path, content: str) -> List[APIEndpointInfo]:
        """Extrae endpoints de FastAPI"""
        endpoints = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    endpoint_info = self._analyze_fastapi_function(node, file_path)
                    if endpoint_info:
                        endpoints.append(endpoint_info)
                        
        except Exception as e:
            print(f"      ❌ Error extrayendo endpoints de {file_path.name}: {e}")
        
        return endpoints

    def _analyze_fastapi_function(self, func_node: ast.FunctionDef, file_path: Path) -> Optional[APIEndpointInfo]:
        """Analiza función de FastAPI para extraer información de endpoint"""
        
        for decorator in func_node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                method = decorator.func.attr.upper()
                
                if method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']:
                    # Extraer path
                    path = None
                    if decorator.args:
                        path = ast.unparse(decorator.args[0])
                    
                    # Extraer response_model de keywords
                    response_model = None
                    for keyword in decorator.keywords:
                        if keyword.arg == 'response_model':
                            response_model = ast.unparse(keyword.value)
                    
                    # Analizar parámetros de función
                    parameters = []
                    request_model = None
                    
                    for arg in func_node.args.args:
                        if arg.arg != 'self':
                            param_info = {
                                'name': arg.arg,
                                'type': ast.unparse(arg.annotation) if arg.annotation else 'Any',
                                'is_request_body': False
                            }
                            
                            # Verificar si es un request body (BaseModel)
                            if arg.annotation:
                                annotation_str = ast.unparse(arg.annotation)
                                if any(model.name in annotation_str for model in self.pydantic_models):
                                    param_info['is_request_body'] = True
                                    request_model = annotation_str
                            
                            parameters.append(param_info)
                    
                    return APIEndpointInfo(
                        method=method,
                        path=path or "/unknown",
                        function_name=func_node.name,
                        file_path=str(file_path),
                        line_number=func_node.lineno,
                        request_model=request_model,
                        response_model=response_model,
                        parameters=parameters,
                        security=[]  # TODO: extraer información de seguridad
                    )
        
        return None

    def _analyze_dependencies_and_integrations(self, files: List[Path]):
        """
        ╔══════════════════════════════════════════════════════════════════════╗
        ║                ANÁLISIS DEPENDENCIAS E INTEGRACIONES                 ║
        ╚══════════════════════════════════════════════════════════════════════╝
        """
        integrations = {}
        
        print("   🔗 Analizando integraciones y dependencias...")
        
        # Mapear relaciones entre modelos y endpoints
        model_usage = self._map_model_usage()
        integrations['model_usage'] = model_usage
        
        # Analizar patrones de validación
        validation_patterns = self._analyze_validation_patterns()
        integrations['validation_patterns'] = validation_patterns
        
        # Detectar sistemas externos
        external_integrations = self._detect_external_integrations(files)
        integrations['external_systems'] = external_integrations
        
        self.analysis_results['integrations'] = integrations
        
        print(f"      ├── Uso de modelos: {len(model_usage)} relaciones")
        print(f"      ├── Patrones de validación: {len(validation_patterns)} patrones")
        print(f"      └── Integraciones externas: {len(external_integrations)} sistemas")

    def _map_model_usage(self) -> Dict[str, Any]:
        """Mapea uso de modelos Pydantic en endpoints"""
        usage = {}
        
        for endpoint in self.api_endpoints:
            endpoint_key = f"{endpoint.method} {endpoint.path}"
            usage[endpoint_key] = {
                'request_model': endpoint.request_model,
                'response_model': endpoint.response_model,
                'file': endpoint.file_path,
                'function': endpoint.function_name
            }
        
        return usage

    def _analyze_validation_patterns(self) -> Dict[str, Any]:
        """Analiza patrones de validación"""
        patterns = {}
        
        # Analizar tipos de validators más comunes
        validator_types = {}
        field_constraints = {}
        
        for model in self.pydantic_models:
            for validator in model.validators:
                validator_name = validator.get('name', 'unknown')
                validator_types[validator_name] = validator_types.get(validator_name, 0) + 1
            
            for field in model.fields:
                constraints = field.get('field_constraints', {})
                for constraint_type in constraints.keys():
                    field_constraints[constraint_type] = field_constraints.get(constraint_type, 0) + 1
        
        patterns['validator_types'] = validator_types
        patterns['field_constraints'] = field_constraints
        
        return patterns

    def _detect_external_integrations(self, files: List[Path]) -> Dict[str, List[str]]:
        """Detecta integraciones con sistemas externos"""
        external_systems = {
            'databases': [],
            'apis': [],
            'message_queues': [],
            'cloud_services': [],
            'ai_models': []
        }
        
        # Patrones de detección
        patterns = {
            'databases': ['sqlalchemy', 'pymongo', 'redis', 'postgresql', 'mysql', 'sqlite'],
            'apis': ['requests', 'httpx', 'aiohttp', 'openai', 'anthropic'],
            'message_queues': ['celery', 'rabbitmq', 'kafka', 'redis'],
            'cloud_services': ['aws', 'gcp', 'azure', 'supabase'],
            'ai_models': ['openai', 'huggingface', 'transformers', 'langchain', 'anthropic']
        }
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    
                for category, keywords in patterns.items():
                    for keyword in keywords:
                        if keyword in content and keyword not in external_systems[category]:
                            external_systems[category].append(keyword)
                            
            except Exception:
                continue
        
        return external_systems

    def _generate_comprehensive_report(self) -> Dict[str, Any]:
        """
        ╔══════════════════════════════════════════════════════════════════════╗
        ║                      REPORTE COMPLETO GENERADO                       ║
        ╚══════════════════════════════════════════════════════════════════════╝
        """
        report = {
            'metadata': {
                'analysis_timestamp': datetime.now().isoformat(),
                'target_directory': str(self.target_dir),
                'analyzer_version': '2.0.0',
                'total_analysis_time': 'calculated_at_end'
            },
            'summary': {
                'total_pydantic_models': len(self.pydantic_models),
                'total_api_endpoints': len(self.api_endpoints),
                'models_by_complexity': self._categorize_models_by_complexity(),
                'endpoints_by_method': self._categorize_endpoints_by_method(),
                'validation_coverage': self._calculate_validation_coverage()
            },
            'pydantic_models': [
                {
                    'name': model.name,
                    'file_path': model.file_path,
                    'line_number': model.line_number,
                    'fields_count': len(model.fields),
                    'validators_count': len(model.validators),
                    'fields': model.fields,
                    'validators': model.validators,
                    'config_options': model.config_options,
                    'inheritance': model.inheritance
                }
                for model in self.pydantic_models
            ],
            'api_endpoints': [
                {
                    'method': endpoint.method,
                    'path': endpoint.path,
                    'function_name': endpoint.function_name,
                    'file_path': endpoint.file_path,
                    'line_number': endpoint.line_number,
                    'request_model': endpoint.request_model,
                    'response_model': endpoint.response_model,
                    'parameters_count': len(endpoint.parameters),
                    'parameters': endpoint.parameters
                }
                for endpoint in self.api_endpoints
            ],
            'analysis_insights': {
                'most_used_field_types': self._get_most_used_field_types(),
                'validation_patterns': self._get_validation_patterns(),
                'api_design_patterns': self._get_api_design_patterns(),
                'recommendations': self._generate_recommendations()
            },
            'integrations': self.analysis_results.get('integrations', {})
        }
        
        self.analysis_results = report
        return report

    def _categorize_models_by_complexity(self) -> Dict[str, int]:
        """Categoriza modelos por complejidad"""
        categories = {'simple': 0, 'medium': 0, 'complex': 0}
        
        for model in self.pydantic_models:
            field_count = len(model.fields)
            validator_count = len(model.validators)
            
            if field_count <= 3 and validator_count == 0:
                categories['simple'] += 1
            elif field_count <= 8 and validator_count <= 2:
                categories['medium'] += 1
            else:
                categories['complex'] += 1
        
        return categories

    def _categorize_endpoints_by_method(self) -> Dict[str, int]:
        """Categoriza endpoints por método HTTP"""
        methods = {}
        for endpoint in self.api_endpoints:
            methods[endpoint.method] = methods.get(endpoint.method, 0) + 1
        return methods

    def _calculate_validation_coverage(self) -> Dict[str, Any]:
        """Calcula cobertura de validación"""
        total_fields = sum(len(model.fields) for model in self.pydantic_models)
        validated_fields = sum(
            sum(1 for field in model.fields if field.get('field_constraints'))
            for model in self.pydantic_models
        )
        
        coverage_percentage = (validated_fields / total_fields * 100) if total_fields > 0 else 0
        
        return {
            'total_fields': total_fields,
            'validated_fields': validated_fields,
            'coverage_percentage': round(coverage_percentage, 2),
            'models_with_validators': len([m for m in self.pydantic_models if m.validators])
        }

    def _get_most_used_field_types(self) -> Dict[str, int]:
        """Obtiene tipos de campo más utilizados"""
        field_types = {}
        
        for model in self.pydantic_models:
            for field in model.fields:
                field_type = field.get('type', 'Unknown')
                # Simplificar tipos complejos
                simple_type = field_type.split('[')[0].split('.')[-1]
                field_types[simple_type] = field_types.get(simple_type, 0) + 1
        
        return dict(sorted(field_types.items(), key=lambda x: x[1], reverse=True)[:10])

    def _get_validation_patterns(self) -> Dict[str, Any]:
        """Obtiene patrones de validación"""
        return self.analysis_results.get('integrations', {}).get('validation_patterns', {})

    def _get_api_design_patterns(self) -> Dict[str, Any]:
        """Analiza patrones de diseño de API"""
        patterns = {
            'consistent_naming': self._check_consistent_naming(),
            'response_model_usage': len([e for e in self.api_endpoints if e.response_model]),
            'request_model_usage': len([e for e in self.api_endpoints if e.request_model]),
            'crud_endpoints': self._identify_crud_patterns()
        }
        return patterns

    def _check_consistent_naming(self) -> Dict[str, Any]:
        """Verifica consistencia en naming"""
        # Simplificado para el ejemplo
        return {
            'snake_case_endpoints': len([e for e in self.api_endpoints if '_' in e.function_name]),
            'camel_case_models': len([m for m in self.pydantic_models if m.name[0].isupper()])
        }

    def _identify_crud_patterns(self) -> Dict[str, int]:
        """Identifica patrones CRUD"""
        crud_patterns = {'create': 0, 'read': 0, 'update': 0, 'delete': 0}
        
        for endpoint in self.api_endpoints:
            method = endpoint.method.lower()
            path = endpoint.path.lower()
            
            if method == 'post':
                crud_patterns['create'] += 1
            elif method == 'get':
                crud_patterns['read'] += 1
            elif method in ['put', 'patch']:
                crud_patterns['update'] += 1
            elif method == 'delete':
                crud_patterns['delete'] += 1
        
        return crud_patterns

    def _generate_recommendations(self) -> List[str]:
        """Genera recomendaciones basadas en análisis"""
        recommendations = []
        
        # Recomendación de validación
        validation_coverage = self._calculate_validation_coverage()
        if validation_coverage['coverage_percentage'] < 50:
            recommendations.append(
                f"Baja cobertura de validación ({validation_coverage['coverage_percentage']:.1f}%). "
                "Considerar agregar más Field() constraints."
            )
        
        # Recomendación de modelos de respuesta
        endpoints_without_response_model = len([e for e in self.api_endpoints if not e.response_model])
        if endpoints_without_response_model > 0:
            recommendations.append(
                f"{endpoints_without_response_model} endpoints sin response_model. "
                "Considerar agregar response_model para mejor documentación."
            )
        
        # Recomendación de complejidad de modelos
        complex_models = len([m for m in self.pydantic_models if len(m.fields) > 10])
        if complex_models > 0:
            recommendations.append(
                f"{complex_models} modelos con más de 10 campos. "
                "Considerar dividir en modelos más pequeños."
            )
        
        return recommendations

    def generate_ascii_report(self) -> str:
        """
        ╔══════════════════════════════════════════════════════════════════════╗
        ║                    REPORTE ASCII ESPECIALIZADO                       ║
        ╚══════════════════════════════════════════════════════════════════════╝
        """
        if not self.analysis_results:
            return "⚠️ No hay resultados de análisis disponibles. Ejecute el análisis primero."
        
        summary = self.analysis_results.get('summary', {})
        
        ascii_report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                VIGOLEONROCKS PYDANTIC REVERSE ENGINEERING REPORT            ║
║                            ANÁLISIS COMPLETO                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 RESUMEN EJECUTIVO
════════════════════════════════════════════════════════════════════════════════
🧬 Modelos Pydantic Detectados: {summary.get('total_pydantic_models', 0)}
🌐 Endpoints FastAPI Detectados: {summary.get('total_api_endpoints', 0)}
✅ Cobertura de Validación: {summary.get('validation_coverage', {}).get('coverage_percentage', 0):.1f}%
📈 Complejidad Modelos:
   ├── Simples: {summary.get('models_by_complexity', {}).get('simple', 0)}
   ├── Medios: {summary.get('models_by_complexity', {}).get('medium', 0)}
   └── Complejos: {summary.get('models_by_complexity', {}).get('complex', 0)}

🌐 ENDPOINTS POR MÉTODO HTTP
════════════════════════════════════════════════════════════════════════════════"""
        
        # Agregar información de endpoints por método
        endpoints_by_method = summary.get('endpoints_by_method', {})
        for method, count in endpoints_by_method.items():
            ascii_report += f"\n{method:>6}: {count} endpoints"
        
        ascii_report += f"""

🧬 MODELOS PYDANTIC DETALLADOS
════════════════════════════════════════════════════════════════════════════════"""
        
        # Agregar detalles de modelos
        for model_info in self.analysis_results.get('pydantic_models', [])[:10]:  # Primeros 10
            ascii_report += f"""
📁 {model_info['name']} ({Path(model_info['file_path']).name})
   ├── Campos: {model_info['fields_count']}
   ├── Validators: {model_info['validators_count']}
   └── Línea: {model_info['line_number']}"""
        
        ascii_report += f"""

🌐 ENDPOINTS FASTAPI DETALLADOS
════════════════════════════════════════════════════════════════════════════════"""
        
        # Agregar detalles de endpoints
        for endpoint_info in self.analysis_results.get('api_endpoints', [])[:15]:  # Primeros 15
            ascii_report += f"""
🔗 {endpoint_info['method']} {endpoint_info['path']}
   ├── Función: {endpoint_info['function_name']}()
   ├── Archivo: {Path(endpoint_info['file_path']).name}"""
            if endpoint_info['request_model']:
                ascii_report += f"\n   ├── Request: {endpoint_info['request_model']}"
            if endpoint_info['response_model']:
                ascii_report += f"\n   └── Response: {endpoint_info['response_model']}"
            else:
                ascii_report += f"\n   └── Parámetros: {endpoint_info['parameters_count']}"
        
        # Agregar recomendaciones
        recommendations = self.analysis_results.get('analysis_insights', {}).get('recommendations', [])
        if recommendations:
            ascii_report += f"""

🎯 RECOMENDACIONES DE MEJORA
════════════════════════════════════════════════════════════════════════════════"""
            for i, rec in enumerate(recommendations, 1):
                ascii_report += f"\n{i:>2}. {rec}"
        
        ascii_report += f"""

╔══════════════════════════════════════════════════════════════════════════════╗
║                         ANÁLISIS COMPLETADO EXITOSAMENTE                     ║
║                    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        
        return ascii_report

    def save_results(self, base_filename: str = "vigoleonrocks_pydantic_analysis"):
        """Guarda resultados completos"""
        if not self.analysis_results:
            print("⚠️ No hay resultados para guardar. Ejecute el análisis primero.")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Guardar JSON detallado
        json_file = f"{base_filename}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
        
        # Guardar reporte ASCII
        ascii_file = f"{base_filename}_report_{timestamp}.txt"
        with open(ascii_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_ascii_report())
        
        print(f"💾 RESULTADOS GUARDADOS:")
        print(f"   ├── JSON detallado: {json_file}")
        print(f"   └── Reporte ASCII: {ascii_file}")


def main():
    """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                           PLAN DE EJECUCIÓN COMPLETO                         ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    
    print("""
🎯 PLAN DE INGENIERÍA INVERSA - COMPONENTES PYDANTIC VIGOLEONROCKS:

FASE 1: ESCANEO INTELIGENTE
├── Detección de archivos Python relevantes
├── Identificación de patrones Pydantic
├── Filtrado por importancia (APIs, modelos, schemas)
└── Preparación para análisis profundo

FASE 2: ANÁLISIS MODELOS PYDANTIC
├── Extracción de BaseModel classes
├── Análisis de Field definitions y constraints
├── Identificación de validators personalizados
├── Mapeo de configuraciones y opciones
└── Evaluación de complejidad y patrones

FASE 3: ANÁLISIS ENDPOINTS FASTAPI
├── Detección de decoradores @app.method
├── Extracción de rutas y parámetros
├── Identificación de request/response models
├── Análisis de patrones CRUD
└── Evaluación de consistencia de diseño

FASE 4: ANÁLISIS INTEGRACIONES
├── Mapeo uso de modelos en endpoints
├── Identificación de patrones de validación
├── Detección de integraciones externas
├── Análisis de dependencias
└── Evaluación de arquitectura general

FASE 5: REPORTE Y RECOMENDACIONES
├── Generación de métricas detalladas
├── Identificación de oportunidades de mejora
├── Recomendaciones de refactoring
├── Reporte ASCII visual
└── Exportación de resultados JSON

═══════════════════════════════════════════════════════════════════════════════════
    """)
    
    # Solicitar directorio objetivo
    target_dir = input("📁 Directorio objetivo (Enter para directorio actual): ").strip()
    if not target_dir:
        target_dir = "."
    
    if not Path(target_dir).exists():
        print(f"❌ ERROR: El directorio '{target_dir}' no existe.")
        return
    
    print(f"\n🚀 INICIANDO ANÁLISIS DE INGENIERÍA INVERSA EN: {Path(target_dir).resolve()}")
    print("=" * 88)
    
    try:
        # Crear analizador y ejecutar análisis
        analyzer = VigoleonrocksPydanticAnalyzer(target_dir)
        results = analyzer.execute_comprehensive_analysis()
        
        print("\n" + "=" * 88)
        print("📊 GENERANDO REPORTE FINAL...")
        
        # Mostrar reporte ASCII
        print(analyzer.generate_ascii_report())
        
        # Preguntar si guardar resultados
        save_results = input("\n💾 ¿Guardar resultados detallados? (y/N): ").strip().lower()
        if save_results in ['y', 'yes', 'sí', 's']:
            analyzer.save_results()
        
        print("\n🎉 ANÁLISIS DE INGENIERÍA INVERSA COMPLETADO EXITOSAMENTE!")
        print(f"📊 Total Modelos Pydantic: {len(analyzer.pydantic_models)}")
        print(f"🌐 Total Endpoints FastAPI: {len(analyzer.api_endpoints)}")
        
        return results
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Análisis interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO durante el análisis: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
