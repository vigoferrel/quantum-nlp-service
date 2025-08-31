"""
Cliente de Supabase para almacenamiento transparente de evaluaciones
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logging.warning("Supabase no está instalado. Usando almacenamiento local.")
    Client = None

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Cliente para interactuar con Supabase"""

    def __init__(self):
        self.client = None
        self._init_supabase()

    def _init_supabase(self):
        """Inicializa el cliente de Supabase si está disponible"""
        if not SUPABASE_AVAILABLE:
            logger.info("Supabase no disponible, usando almacenamiento local")
            return

        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            logger.warning("Credenciales de Supabase no encontradas")
            return

        try:
            self.client = create_client(url, key)
            logger.info("Cliente de Supabase inicializado")
        except Exception as e:
            logger.error(f"Error inicializando Supabase: {e}")
            self.client = None

    async def store_evaluation(self, evaluation_data: Dict[str, Any]) -> bool:
        """Almacena una evaluación completa"""
        try:
            if self.client:
                result = self.client.table("organic_evaluations").insert(evaluation_data).execute()
                return bool(result.data)
            else:
                # Almacenamiento local como fallback
                filename = f"local_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w') as f:
                    json.dump(evaluation_data, f, indent=2, default=str)
                logger.info(f"Evaluación almacenada localmente: {filename}")
                return True

        except Exception as e:
            logger.error(f"Error almacenando evaluación: {e}")
            return False

    async def store_metric(self, evaluation_id: str, metric_name: str, value: Any) -> bool:
        """Almacena una métrica individual"""
        try:
            metric_data = {
                "evaluation_id": evaluation_id,
                "metric_name": metric_name,
                "value": json.dumps(value, default=str),
                "timestamp": datetime.now().isoformat()
            }

            if self.client:
                result = self.client.table("real_time_metrics").insert(metric_data).execute()
                return bool(result.data)
            else:
                # Almacenamiento local
                filename = f"metric_{evaluation_id}_{metric_name}.json"
                with open(filename, 'w') as f:
                    json.dump(metric_data, f, indent=2, default=str)
                return True

        except Exception as e:
            logger.error(f"Error almacenando métrica: {e}")
            return False

    async def get_evaluation(self, evaluation_id: str) -> Optional[Dict[str, Any]]:
        """Recupera una evaluación por ID"""
        try:
            if self.client:
                result = self.client.table("organic_evaluations").select("*").eq("evaluation_id", evaluation_id).execute()
                return result.data[0] if result.data else None
            else:
                # Buscar localmente
                import glob
                files = glob.glob(f"local_evaluation_*{evaluation_id}*.json")
                if files:
                    with open(files[0], 'r') as f:
                        return json.load(f)
                return None

        except Exception as e:
            logger.error(f"Error recuperando evaluación: {e}")
            return None

    async def get_all_evaluations(self) -> List[Dict[str, Any]]:
        """Recupera todas las evaluaciones"""
        try:
            if self.client:
                result = self.client.table("organic_evaluations").select("*").execute()
                return result.data or []
            else:
                # Buscar localmente
                import glob
                evaluations = []
                files = glob.glob("local_evaluation_*.json")
                for file in files:
                    try:
                        with open(file, 'r') as f:
                            evaluations.append(json.load(f))
                    except:
                        continue
                return evaluations

        except Exception as e:
            logger.error(f"Error recuperando evaluaciones: {e}")
            return []

# Instancia global del cliente
supabase_client = SupabaseClient()

# Funciones auxiliares asíncronas
async def store_evaluation_async(evaluation_data: Dict[str, Any]) -> bool:
    """Almacena evaluación de forma asíncrona"""
    return await supabase_client.store_evaluation(evaluation_data)

async def store_metric_async(evaluation_id: str, metric_name: str, value: Any) -> bool:
    """Almacena métrica de forma asíncrona"""
    return await supabase_client.store_metric(evaluation_id, metric_name, value)

async def get_evaluation_async(evaluation_id: str) -> Optional[Dict[str, Any]]:
    """Recupera evaluación de forma asíncrona"""
    return await supabase_client.get_evaluation(evaluation_id)

async def get_all_evaluations_async() -> List[Dict[str, Any]]:
    """Recupera todas las evaluaciones de forma asíncrona"""
    return await supabase_client.get_all_evaluations()

# Funciones síncronas para compatibilidad
def store_evaluation_sync(evaluation_data: Dict[str, Any]) -> bool:
    """Almacena evaluación de forma síncrona"""
    return asyncio.run(store_evaluation_async(evaluation_data))

def store_metric_sync(evaluation_id: str, metric_name: str, value: Any) -> bool:
    """Almacena métrica de forma síncrona"""
    return asyncio.run(store_metric_async(evaluation_id, metric_name, value))
