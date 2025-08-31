#!/usr/bin/env python3
"""
🔔 SISTEMA DE NOTIFICACIONES VIGOLEONROCKS
Sistema de alertas y notificaciones en tiempo real
"""

import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

logger = logging.getLogger(__name__)

class NotificationSystem:
    """Sistema de notificaciones en tiempo real"""
    
    def __init__(self):
        self.notifications = []
        self.subscribers = {
            "email": [],
            "webhook": [],
            "console": True
        }
        self.alert_thresholds = {
            "high_error_rate": 0.1,  # 10% de errores
            "high_response_time": 10.0,  # 10 segundos
            "high_concurrent_users": 50,
            "new_user_connection": True,
            "system_issues": True
        }
        self.notification_history = []
        self.lock = threading.Lock()
        
        # Configuración de email (opcional)
        self.email_config = {
            "enabled": False,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "username": "",
            "password": "",
            "from_email": "vigoleonrocks@example.com"
        }
    
    def add_subscriber(self, subscriber_type: str, contact_info: str):
        """Agregar suscriptor para notificaciones"""
        with self.lock:
            if subscriber_type in self.subscribers:
                if contact_info not in self.subscribers[subscriber_type]:
                    self.subscribers[subscriber_type].append(contact_info)
                    logger.info(f"✅ Suscriptor agregado: {subscriber_type} - {contact_info}")
    
    def remove_subscriber(self, subscriber_type: str, contact_info: str):
        """Remover suscriptor"""
        with self.lock:
            if subscriber_type in self.subscribers:
                if contact_info in self.subscribers[subscriber_type]:
                    self.subscribers[subscriber_type].remove(contact_info)
                    logger.info(f"❌ Suscriptor removido: {subscriber_type} - {contact_info}")
    
    def send_notification(self, title: str, message: str, level: str = "INFO", 
                         notification_type: str = "system"):
        """Enviar notificación"""
        notification = {
            "id": len(self.notification_history) + 1,
            "title": title,
            "message": message,
            "level": level,
            "type": notification_type,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        
        with self.lock:
            self.notifications.append(notification)
            self.notification_history.append(notification)
            
            # Mantener solo las últimas 100 notificaciones
            if len(self.notifications) > 100:
                self.notifications.pop(0)
        
        # Enviar a todos los suscriptores
        self._dispatch_notification(notification)
        
        logger.info(f"🔔 Notificación enviada: {title} - {level}")
        return notification
    
    def _dispatch_notification(self, notification: Dict):
        """Despachar notificación a todos los suscriptores"""
        # Notificación por consola
        if self.subscribers["console"]:
            self._console_notification(notification)
        
        # Notificaciones por email
        if self.subscribers["email"] and self.email_config["enabled"]:
            self._email_notification(notification)
        
        # Webhooks
        if self.subscribers["webhook"]:
            self._webhook_notification(notification)
    
    def _console_notification(self, notification: Dict):
        """Notificación por consola"""
        level_icons = {
            "INFO": "ℹ️",
            "WARNING": "⚠️",
            "ERROR": "🚨",
            "SUCCESS": "✅"
        }
        
        icon = level_icons.get(notification["level"], "🔔")
        timestamp = datetime.fromisoformat(notification["timestamp"]).strftime("%H:%M:%S")
        
        print(f"\n{icon} [{timestamp}] {notification['title']}")
        print(f"   {notification['message']}")
        print(f"   Tipo: {notification['type']} | Nivel: {notification['level']}")
    
    def _email_notification(self, notification: Dict):
        """Enviar notificación por email"""
        try:
            if not self.email_config["enabled"]:
                return
            
            msg = MIMEMultipart()
            msg['From'] = self.email_config["from_email"]
            msg['Subject'] = f"🔔 Vigoleonrocks - {notification['title']}"
            
            body = f"""
            <html>
            <body>
                <h2>🔔 Notificación Vigoleonrocks</h2>
                <p><strong>Título:</strong> {notification['title']}</p>
                <p><strong>Mensaje:</strong> {notification['message']}</p>
                <p><strong>Nivel:</strong> {notification['level']}</p>
                <p><strong>Tipo:</strong> {notification['type']}</p>
                <p><strong>Timestamp:</strong> {notification['timestamp']}</p>
                <hr>
                <p><em>Sistema Vigoleonrocks - #1 Mundial</em></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"])
            server.starttls()
            server.login(self.email_config["username"], self.email_config["password"])
            
            for email in self.subscribers["email"]:
                msg['To'] = email
                server.send_message(msg)
            
            server.quit()
            
        except Exception as e:
            logger.error(f"Error enviando email: {e}")
    
    def _webhook_notification(self, notification: Dict):
        """Enviar notificación por webhook"""
        for webhook_url in self.subscribers["webhook"]:
            try:
                payload = {
                    "system": "vigoleonrocks",
                    "notification": notification,
                    "timestamp": datetime.now().isoformat()
                }
                
                response = requests.post(webhook_url, json=payload, timeout=5)
                if response.status_code != 200:
                    logger.warning(f"Webhook falló: {webhook_url} - {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Error enviando webhook: {e}")
    
    def check_system_alerts(self, system_stats: Dict):
        """Verificar alertas del sistema"""
        alerts = []
        
        # Alerta por alta tasa de errores
        if system_stats.get("total_requests", 0) > 0:
            error_rate = system_stats.get("failed_requests", 0) / system_stats.get("total_requests", 1)
            if error_rate > self.alert_thresholds["high_error_rate"]:
                alerts.append({
                    "title": "🚨 Alta Tasa de Errores",
                    "message": f"Tasa de errores: {error_rate:.2%} (umbral: {self.alert_thresholds['high_error_rate']:.2%})",
                    "level": "ERROR",
                    "type": "system_alert"
                })
        
        # Alerta por tiempo de respuesta alto
        avg_response_time = system_stats.get("avg_response_time", 0)
        if avg_response_time > self.alert_thresholds["high_response_time"]:
            alerts.append({
                "title": "⚠️ Tiempo de Respuesta Alto",
                "message": f"Tiempo promedio: {avg_response_time:.2f}s (umbral: {self.alert_thresholds['high_response_time']}s)",
                "level": "WARNING",
                "type": "system_alert"
            })
        
        # Alerta por muchos usuarios concurrentes
        current_users = system_stats.get("current_users", 0)
        if current_users > self.alert_thresholds["high_concurrent_users"]:
            alerts.append({
                "title": "👥 Muchos Usuarios Concurrentes",
                "message": f"Usuarios activos: {current_users} (umbral: {self.alert_thresholds['high_concurrent_users']})",
                "level": "INFO",
                "type": "system_alert"
            })
        
        return alerts
    
    def notify_new_connection(self, user_name: str, api_key: str, query_type: str, success: bool):
        """Notificar nueva conexión"""
        if not self.alert_thresholds["new_user_connection"]:
            return
        
        status = "✅" if success else "❌"
        level = "SUCCESS" if success else "WARNING"
        
        self.send_notification(
            title=f"{status} Nueva Conexión",
            message=f"Usuario: {user_name} | Tipo: {query_type} | API Key: {api_key[:10]}...",
            level=level,
            notification_type="connection"
        )
    
    def notify_system_status(self, status: str, details: str = ""):
        """Notificar cambio de estado del sistema"""
        if not self.alert_thresholds["system_issues"]:
            return
        
        level = "ERROR" if "error" in status.lower() else "INFO"
        
        self.send_notification(
            title=f"🖥️ Estado del Sistema: {status}",
            message=details or f"El sistema ha cambiado a estado: {status}",
            level=level,
            notification_type="system_status"
        )
    
    def get_notifications(self, limit: int = 50, unread_only: bool = False) -> List[Dict]:
        """Obtener notificaciones"""
        with self.lock:
            notifications = self.notifications.copy()
            
            if unread_only:
                notifications = [n for n in notifications if not n.get("read", False)]
            
            return notifications[-limit:]
    
    def mark_as_read(self, notification_id: int):
        """Marcar notificación como leída"""
        with self.lock:
            for notification in self.notifications:
                if notification["id"] == notification_id:
                    notification["read"] = True
                    break
    
    def mark_all_as_read(self):
        """Marcar todas las notificaciones como leídas"""
        with self.lock:
            for notification in self.notifications:
                notification["read"] = True
    
    def get_notification_stats(self) -> Dict:
        """Obtener estadísticas de notificaciones"""
        with self.lock:
            total = len(self.notification_history)
            unread = len([n for n in self.notifications if not n.get("read", False)])
            
            levels = {}
            for notification in self.notification_history:
                level = notification["level"]
                levels[level] = levels.get(level, 0) + 1
            
            return {
                "total_notifications": total,
                "unread_notifications": unread,
                "notifications_by_level": levels,
                "subscribers": {
                    "email": len(self.subscribers["email"]),
                    "webhook": len(self.subscribers["webhook"]),
                    "console": self.subscribers["console"]
                }
            }
    
    def configure_email(self, smtp_server: str, smtp_port: int, username: str, password: str, from_email: str):
        """Configurar notificaciones por email"""
        self.email_config.update({
            "enabled": True,
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "username": username,
            "password": password,
            "from_email": from_email
        })
        
        logger.info("✅ Configuración de email actualizada")
    
    def test_notification(self):
        """Enviar notificación de prueba"""
        return self.send_notification(
            title="🧪 Notificación de Prueba",
            message="Esta es una notificación de prueba del sistema Vigoleonrocks",
            level="INFO",
            notification_type="test"
        )

# Instancia global del sistema de notificaciones
notification_system = NotificationSystem()

def send_alert(title: str, message: str, level: str = "INFO"):
    """Función helper para enviar alertas"""
    return notification_system.send_notification(title, message, level)

if __name__ == "__main__":
    # Demo del sistema de notificaciones
    print("🔔 SISTEMA DE NOTIFICACIONES VIGOLEONROCKS")
    print("=" * 50)
    
    # Agregar suscriptores de prueba
    notification_system.add_subscriber("email", "test@example.com")
    notification_system.add_subscriber("webhook", "https://webhook.site/test")
    
    # Enviar notificaciones de prueba
    notification_system.send_notification(
        "🚀 Sistema Iniciado",
        "Vigoleonrocks está operativo y listo para conexiones",
        "SUCCESS"
    )
    
    notification_system.send_notification(
        "👤 Nueva Conexión",
        "Usuario kjacome24 se ha conectado al sistema",
        "INFO"
    )
    
    notification_system.send_notification(
        "⚠️ Alerta de Rendimiento",
        "Tiempo de respuesta ligeramente elevado",
        "WARNING"
    )
    
    # Mostrar estadísticas
    stats = notification_system.get_notification_stats()
    print(f"\n📊 Estadísticas:")
    print(f"  Total notificaciones: {stats['total_notifications']}")
    print(f"  No leídas: {stats['unread_notifications']}")
    print(f"  Por nivel: {stats['notifications_by_level']}")
    
    # Mostrar notificaciones recientes
    notifications = notification_system.get_notifications(5)
    print(f"\n🔔 Últimas 5 notificaciones:")
    for notif in notifications:
        timestamp = datetime.fromisoformat(notif["timestamp"]).strftime("%H:%M:%S")
        print(f"  [{timestamp}] {notif['title']} - {notif['level']}")
