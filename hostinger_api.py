#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HOSTINGER API - VPS CREATION FOR SUPREMACY
==========================================
Script para crear VPS en Hostinger usando la API
"""

import requests
import json
import time

class HostingerVPSManager:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://developers.hostinger.com/api/vps/v1"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def get_vps_list(self):
        """Obtener lista de VPS existentes"""
        try:
            response = requests.get(f"{self.base_url}/virtual-machines", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo lista de VPS: {e}")
            return None
    
    def get_available_plans(self):
        """Obtener planes disponibles"""
        try:
            response = requests.get(f"{self.base_url}/plans", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo planes: {e}")
            return None
    
    def get_available_locations(self):
        """Obtener ubicaciones disponibles"""
        try:
            response = requests.get(f"{self.base_url}/locations", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo ubicaciones: {e}")
            return None
    
    def get_available_os(self):
        """Obtener sistemas operativos disponibles"""
        try:
            response = requests.get(f"{self.base_url}/os", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo sistemas operativos: {e}")
            return None
    
    def create_vps(self, name, plan_id, location_id, os_id, ssh_key_id=None):
        """Crear nuevo VPS"""
        data = {
            "name": name,
            "plan_id": plan_id,
            "location_id": location_id,
            "os_id": os_id
        }
        
        if ssh_key_id:
            data["ssh_key_id"] = ssh_key_id
        
        try:
            response = requests.post(f"{self.base_url}/virtual-machines", 
                                   headers=self.headers, 
                                   json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creando VPS: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Respuesta del servidor: {e.response.text}")
            return None
    
    def get_vps_status(self, vps_id):
        """Obtener estado de un VPS"""
        try:
            response = requests.get(f"{self.base_url}/virtual-machines/{vps_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo estado del VPS: {e}")
            return None

def main():
    """Función principal"""
    api_token = "yD8JTQQleIOgW2m38U4BtYQuuszQVDXcjixehGSJ77853215"
    
    print("🚀 HOSTINGER VPS MANAGER - SUPREMACÍA CUÁNTICA")
    print("="*60)
    
    manager = HostingerVPSManager(api_token)
    
    # 1. Obtener VPS existentes
    print("\n📋 VPS EXISTENTES:")
    vps_list = manager.get_vps_list()
    if vps_list:
        print(json.dumps(vps_list, indent=2))
    else:
        print("No se pudieron obtener los VPS existentes")
    
    # 2. Obtener planes disponibles
    print("\n💾 PLANES DISPONIBLES:")
    plans = manager.get_available_plans()
    if plans:
        print(json.dumps(plans, indent=2))
    else:
        print("No se pudieron obtener los planes")
    
    # 3. Obtener ubicaciones disponibles
    print("\n🌍 UBICACIONES DISPONIBLES:")
    locations = manager.get_available_locations()
    if locations:
        print(json.dumps(locations, indent=2))
    else:
        print("No se pudieron obtener las ubicaciones")
    
    # 4. Obtener sistemas operativos disponibles
    print("\n🐧 SISTEMAS OPERATIVOS DISPONIBLES:")
    os_list = manager.get_available_os()
    if os_list:
        print(json.dumps(os_list, indent=2))
    else:
        print("No se pudieron obtener los sistemas operativos")
    
    print("\n✅ INFORMACIÓN OBTENIDA EXITOSAMENTE")
    print("📋 Revisa la información arriba para crear el VPS")

if __name__ == "__main__":
    main()
