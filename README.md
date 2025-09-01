# VIGOLEONROCKS v2.0.0

Sistema de IA Humana Unificado - Arquitectura Modular

## Caracteristicas

- Respuestas humanas naturales
- Arquitectura modular reestructurada
- Testing automatizado completo
- Documentacion tecnica unificada
- Deployment simplificado con Docker

## Inicio Rapido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
python -m pytest tests/ -v

# Iniciar servidor
python -m vigoleonrocks.interfaces.rest_api
```

## Estructura del Proyecto

```
vigoleonrocks/
├── core/              # Configuracion central
├── services/          # Servicios de negocio
├── interfaces/        # APIs y interfaces
├── utils/            # Utilidades compartidas
└── tests/            # Testing automatizado
```

## Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=vigoleonrocks

# Tests especificos
pytest tests/unit/test_ai_service.py
```

## Documentacion

- [API Documentation](docs/api/)
- [Architecture Guide](docs/architecture/)
- [Development Setup](docs/development/)

## Deployment

```bash
# Con Docker Compose
docker-compose up -d

# Desarrollo local
python -m vigoleonrocks.interfaces.rest_api
```

## Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto esta bajo la Licencia MIT.
