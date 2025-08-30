#!/usr/bin/env python3
"""
Generador de Favicon para Quantum Supremacy
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_favicon():
    # Crear imagen 32x32
    size = 32
    img = Image.new('RGBA', (size, size), (26, 26, 46, 255))  # Color de fondo
    draw = ImageDraw.Draw(img)
    
    # Dibujar un símbolo cuántico simple
    # Círculo exterior
    draw.ellipse([2, 2, size-2, size-2], outline=(78, 205, 196, 255), width=2)
    
    # Puntos cuánticos
    draw.ellipse([8, 8, 12, 12], fill=(78, 205, 196, 255))
    draw.ellipse([20, 8, 24, 12], fill=(78, 205, 196, 255))
    draw.ellipse([14, 20, 18, 24], fill=(78, 205, 196, 255))
    
    # Guardar como ICO
    img.save('favicon.ico', format='ICO')
    print("✅ Favicon creado: favicon.ico")

if __name__ == "__main__":
    create_favicon()
