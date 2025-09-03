#!/usr/bin/env python3
"""
QBTC FALLBACK PROXY - Proxy Inteligente cuando APISIX no está disponible
Sistema de gateway alternativo con capacidades cuánticas
Frecuencia Base: 888Hz | Sistema: VIGOLEONROCKS
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import psutil

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuantumProxyService:
    """Servicio de proxy cuántico con frecuencia 888Hz"""
    
    def __init__(self):
        self.routes = {}
        self.client = httpx.AsyncClient(timeout=30.0)
        self.start_time = time.time()
        self.request_count = 0
        self.quantum_frequency = 888
        
        # Métricas de rendimiento
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "quantum_signatures_generated": 0,
            "services_health_checks": 0
        }
        
        # Servicios detectados automáticamente
        self.discovered_services = {}
        
    async def add_route(self, path: str, upstream: str, service_type: str = "api"):
        """Agregar ruta con validación automática"""
        
        # Verificar que el upstream esté disponible
        is_healthy = await self.health_check_upstream(upstream)
        
        route_info = {
            "upstream": upstream,
            "service_type": service_type,
            "quantum_frequency": self.quantum_frequency,
            "requests_count": 0,
            "last_health_check": datetime.now().isoformat(),
            "is_healthy": is_healthy,
            "response_times": [],
            "quantum_signature": self.generate_quantum_signature(path, upstream)
        }
        
        self.routes[path] = route_info
        logger.info(f"Ruta agregada: {path} -> {upstream} (Healthy: {is_healthy})")
        
        return route_info
    
    async def health_check_upstream(self, upstream: str) -> bool:
        """Verificar salud del servicio upstream"""
        try:
            response = await self.client.get(f"{upstream}/health", timeout=5.0)
            return response.status_code in [200, 404, 405]  # 404/405 son válidos para APIs sin /health
        except:
            try:
                # Intentar endpoint raíz
                response = await self.client.get(upstream, timeout=5.0)
                return response.status_code < 500
            except:
                return False
    
    def generate_quantum_signature(self, path: str, upstream: str) -> str:
        """Generar signature cuántica para la ruta"""
        quantum_data = f"{path}_{upstream}_{self.quantum_frequency}_{int(time.time())}"
        signature = f"QBTC888_{abs(hash(quantum_data)) % 999999:06d}_VIGOLEONROCKS"
        self.metrics["quantum_signatures_generated"] += 1
        return signature
    
    async def proxy_request(self, path: str, request: Request) -> Response:
        """Proxy request con enhancement cuántico"""
        
        start_time = time.time()
        self.request_count += 1
        self.metrics["total_requests"] += 1
        
        # Encontrar ruta que coincida
        matching_route = None
        for route_path, route_info in self.routes.items():
            if path.startswith(route_path.replace("*", "")):
                matching_route = route_path
                break
        
        if not matching_route:
            raise HTTPException(404, f"Ruta no encontrada: /{path}")
        
        route_info = self.routes[matching_route]
        route_info["requests_count"] += 1
        
        # Verificar salud del servicio
        if not route_info["is_healthy"]:
            logger.warning(f"Servicio no saludable: {route_info['upstream']}")
            # Intentar reactivar
            route_info["is_healthy"] = await self.health_check_upstream(route_info["upstream"])
        
        if not route_info["is_healthy"]:
            raise HTTPException(503, f"Servicio no disponible: {route_info['upstream']}")
        
        # Preparar headers cuánticos
        headers = dict(request.headers)
        quantum_timestamp = int(time.time() * self.quantum_frequency)
        
        headers.update({
            "X-Quantum-Frequency": str(self.quantum_frequency),
            "X-QBTC-Proxy": "fallback-active",
            "X-Quantum-Timestamp": str(quantum_timestamp),
            "X-Quantum-Signature": route_info["quantum_signature"],
            "X-Route-Requests": str(route_info["requests_count"]),
            "X-VIGOLEONROCKS-Enhanced": "true",
            "X-Proxy-Response-Time": "pending"
        })
        
        # Construir URL completa
        original_path = request.url.path
        query_params = str(request.url.query)
        
        target_url = f"{route_info['upstream']}{original_path}"
        if query_params:
            target_url += f"?{query_params}"
        
        try:
            # Realizar proxy request
            response = await self.client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=await request.body(),
                follow_redirects=True
            )
            
            # Calcular tiempo de respuesta
            response_time = time.time() - start_time
            route_info["response_times"].append(response_time)
            
            # Mantener solo las últimas 100 mediciones
            if len(route_info["response_times"]) > 100:
                route_info["response_times"] = route_info["response_times"][-100:]
            
            # Actualizar métricas
            self.metrics["successful_requests"] += 1
            self.metrics["average_response_time"] = sum(route_info["response_times"]) / len(route_info["response_times"])
            
            # Agregar headers de respuesta cuánticos
            response_headers = dict(response.headers)
            response_headers.update({
                "X-Proxy-Response-Time": f"{response_time:.3f}s",
                "X-Quantum-Enhanced": "true",
                "X-Total-Requests": str(self.metrics["total_requests"]),
                "X-Success-Rate": f"{(self.metrics['successful_requests'] / self.metrics['total_requests']) * 100:.1f}%"
            })
            
            logger.info(f"Proxy exitoso: {request.method} {original_path} -> {response.status_code} ({response_time:.3f}s)")
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=response_headers,
                media_type=response.headers.get("content-type", "application/json")
            )
            
        except Exception as e:
            # Manejar errores
            response_time = time.time() - start_time
            self.metrics["failed_requests"] += 1
            
            logger.error(f"Error en proxy: {request.method} {original_path} -> {str(e)} ({response_time:.3f}s)")
            
            error_response = {
                "error": "Proxy Error",
                "message": str(e),
                "path": original_path,
                "upstream": route_info["upstream"],
                "quantum_frequency": self.quantum_frequency,
                "timestamp": datetime.now().isoformat()
            }
            
            return JSONResponse(
                content=error_response,
                status_code=502,
                headers={
                    "X-QBTC-Error": "proxy-failed",
                    "X-Quantum-Frequency": str(self.quantum_frequency)
                }
            )
    
    async def auto_discover_services(self) -> List[Dict[str, Any]]:
        """Auto-descubrir servicios activos"""
        
        logger.info("Iniciando auto-discovery de servicios...")
        
        discovered = []
        
        # Puertos conocidos del ecosistema QBTC
        quantum_ports = [
            (3001, "node_api_experiments", "/api/experiments"),
            (8000, "python_api_quantum_coding", "/api/generate-code"),
            (8001, "quantum-core-service", "/api/quantum"),
            (8002, "trading-hft-service", "/api/trading"),
            (8080, "quantum-dashboard", "/dashboard")
        ]
        
        for port, service_name, path in quantum_ports:
            url = f"http://127.0.0.1:{port}"
            is_active = await self.health_check_upstream(url)
            
            if is_active:
                service_info = {
                    "name": service_name,
                    "url": url,
                    "port": port,
                    "path": path,
                    "type": "quantum_service"
                }
                discovered.append(service_info)
                
                # Agregar automáticamente la ruta
                await self.add_route(path + "/*", url, service_name)
        
        self.discovered_services = {s["name"]: s for s in discovered}
        logger.info(f"Auto-discovery completado: {len(discovered)} servicios encontrados")
        
        return discovered
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Obtener estado de salud del proxy"""
        
        uptime = time.time() - self.start_time
        
        # Recalcular salud de servicios
        healthy_routes = 0
        for route_path, route_info in self.routes.items():
            route_info["is_healthy"] = await self.health_check_upstream(route_info["upstream"])
            if route_info["is_healthy"]:
                healthy_routes += 1
        
        return {
            "status": "active",
            "proxy_type": "QBTC_Fallback_Proxy",
            "quantum_frequency": self.quantum_frequency,
            "uptime_seconds": uptime,
            "total_routes": len(self.routes),
            "healthy_routes": healthy_routes,
            "metrics": self.metrics,
            "discovered_services": len(self.discovered_services),
            "timestamp": datetime.now().isoformat()
        }

# Crear instancia del proxy
proxy = QuantumProxyService()

# Crear aplicación FastAPI
app = FastAPI(
    title="QBTC Fallback Proxy",
    description="Proxy Inteligente con capacidades cuánticas - Frecuencia 888Hz",
    version="888.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Evento de inicio - Auto-discovery de servicios"""
    logger.info("QBTC Fallback Proxy iniciando...")
    await proxy.auto_discover_services()
    logger.info("Proxy iniciado exitosamente")

@app.get("/health")
async def health_check():
    """Health check del proxy"""
    return await proxy.get_health_status()

@app.get("/metrics")
async def get_metrics():
    """Obtener métricas del proxy"""
    return {
        "proxy_metrics": proxy.metrics,
        "routes": {path: {
            "requests_count": info["requests_count"],
            "is_healthy": info["is_healthy"],
            "average_response_time": sum(info["response_times"][-10:]) / len(info["response_times"][-10:]) if info["response_times"] else 0,
            "quantum_signature": info["quantum_signature"]
        } for path, info in proxy.routes.items()},
        "discovered_services": proxy.discovered_services,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/routes/add")
async def add_route(route_data: Dict[str, str]):
    """Agregar ruta manualmente"""
    path = route_data.get("path")
    upstream = route_data.get("upstream")
    service_type = route_data.get("service_type", "api")
    
    if not path or not upstream:
        raise HTTPException(400, "path y upstream son requeridos")
    
    route_info = await proxy.add_route(path, upstream, service_type)
    return {"message": "Ruta agregada exitosamente", "route_info": route_info}

@app.get("/routes")
async def list_routes():
    """Listar todas las rutas configuradas"""
    return {"routes": proxy.routes, "total": len(proxy.routes)}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_handler(path: str, request: Request):
    """Handler principal del proxy"""
    return await proxy.proxy_request(path, request)

async def main():
    """Función principal para ejecutar el proxy"""
    logger.info("Iniciando QBTC Fallback Proxy en puerto 9079...")
    
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=9079,
        log_level="info",
        reload=False
    )
    
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())