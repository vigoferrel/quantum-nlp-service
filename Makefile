SHELL := /bin/bash
.ONESHELL:

# Configuración de colores para output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
WHITE := \033[0;37m
NC := \033[0m # No Color

# Variables del proyecto
PROJECT_NAME := quantum-nlp-service
PYTHON_VERSION := 3.8
VENV_DIR := .venv
PID_DIR := run
LOG_DIR := logs
PORT := 5000
HOST := 0.0.0.0
SERVICE_NAME := vigoleonrocks

# Targets por defecto
.DEFAULT_GOAL := help
.PHONY: help setup install install-dev clean lint format type-check test test-coverage test-randomness start start-bg stop logs status health docker-build docker-up docker-down docker-logs monitoring-up monitoring-down security-scan deploy

## Ayuda y documentación
help: ## Mostrar esta ayuda
	@echo "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
	@echo "${CYAN}║                    VIGOLEONROCKS MAKEFILE                     ║${NC}"
	@echo "${CYAN}║                Quantum NLP Service v2.0.0                     ║${NC}"
	@echo "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
	@echo ""
	@echo "${WHITE}Comandos disponibles:${NC}"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "${GREEN}%-20s${NC} %s\n", $$1, $$2}'
	@echo ""
	@echo "${YELLOW}REGLAS OBLIGATORIAS:${NC}"
	@echo "  • Los servicios DEBEN ejecutarse en segundo plano"
	@echo "  • Los servicios DEBEN exponer métricas"
	@echo "  • PROHIBIDO usar Math.random (usar métricas del kernel)"
	@echo "  • Soporte multilingüe obligatorio"

## Setup y configuración
setup: ## Configurar entorno de desarrollo completo
	@echo "${BLUE}[SETUP]${NC} Configurando entorno de desarrollo..."
	@python$(PYTHON_VERSION) --version || (echo "${RED}Python $(PYTHON_VERSION)+ requerido${NC}" && exit 1)
	@python$(PYTHON_VERSION) -m venv $(VENV_DIR)
	@echo "${GREEN}[SETUP]${NC} Virtual environment creado"
	@source $(VENV_DIR)/bin/activate && pip install --upgrade pip wheel setuptools
	@echo "${GREEN}[SETUP]${NC} Herramientas base instaladas"
	@mkdir -p $(PID_DIR) $(LOG_DIR)
	@echo "${GREEN}[SETUP]${NC} Directorios creados: $(PID_DIR), $(LOG_DIR)"

install: ## Instalar dependencias de producción
	@echo "${BLUE}[INSTALL]${NC} Instalando dependencias..."
	@source $(VENV_DIR)/bin/activate && pip install -r requirements.txt
	@echo "${GREEN}[INSTALL]${NC} Dependencias instaladas"

install-dev: install ## Instalar dependencias de desarrollo
	@echo "${BLUE}[DEV-INSTALL]${NC} Instalando dependencias de desarrollo..."
	@source $(VENV_DIR)/bin/activate && pip install -r requirements-dev.txt
	@echo "${GREEN}[DEV-INSTALL]${NC} Dependencias de desarrollo instaladas"

clean: ## Limpiar archivos temporales y cache
	@echo "${YELLOW}[CLEAN]${NC} Limpiando archivos temporales..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/
	@echo "${GREEN}[CLEAN]${NC} Limpieza completada"

## Calidad de código
lint: ## Ejecutar linting con flake8
	@echo "${BLUE}[LINT]${NC} Ejecutando flake8..."
	@source $(VENV_DIR)/bin/activate && flake8 vigoleonrocks/ --max-line-length=88 --extend-ignore=E203,W503
	@echo "${GREEN}[LINT]${NC} Linting completado"

format: ## Formatear código con black
	@echo "${BLUE}[FORMAT]${NC} Formateando código con black..."
	@source $(VENV_DIR)/bin/activate && black vigoleonrocks/ --line-length=88
	@echo "${GREEN}[FORMAT]${NC} Formateo completado"

type-check: ## Verificar tipos con mypy
	@echo "${BLUE}[TYPECHECK]${NC} Verificando tipos..."
	@source $(VENV_DIR)/bin/activate && mypy vigoleonrocks/ --ignore-missing-imports
	@echo "${GREEN}[TYPECHECK]${NC} Verificación de tipos completada"

## Testing
test: ## Ejecutar tests unitarios
	@echo "${BLUE}[TEST]${NC} Ejecutando tests..."
	@source $(VENV_DIR)/bin/activate && python -m pytest tests/ -v
	@echo "${GREEN}[TEST]${NC} Tests completados"

test-coverage: ## Ejecutar tests con coverage
	@echo "${BLUE}[COVERAGE]${NC} Ejecutando tests con coverage..."
	@source $(VENV_DIR)/bin/activate && python -m pytest tests/ -v --cov=vigoleonrocks --cov-report=term-missing --cov-report=html
	@echo "${GREEN}[COVERAGE]${NC} Coverage generado en htmlcov/"

test-randomness: ## Verificar política de aleatoriedad (CRÍTICO)
	@echo "${BLUE}[RANDOMNESS-CHECK]${NC} Verificando política de aleatoriedad..."
	@echo "${YELLOW}[RANDOMNESS-CHECK]${NC} Buscando Math.random prohibido..."
	@if grep -r "Math\.random\|random\." --include="*.py" vigoleonrocks/; then \
		echo "${RED}[ERROR]${NC} Math.random o random. detectado - PROHIBIDO"; \
		echo "${RED}[ERROR]${NC} Use métricas del kernel para aleatoriedad"; \
		exit 1; \
	else \
		echo "${GREEN}[RANDOMNESS-CHECK]${NC} Política de aleatoriedad respetada"; \
	fi

## Servicios (SEGUNDO PLANO OBLIGATORIO con MÉTRICAS)
start: ## Iniciar servidor en primer plano (solo para desarrollo)
	@echo "${BLUE}[START]${NC} Iniciando servidor en primer plano..."
	@source $(VENV_DIR)/bin/activate && python -m vigoleonrocks.interfaces.rest_api --host $(HOST) --port $(PORT)

start-bg: ## Iniciar servidor en segundo plano con métricas (REQUERIDO)
	@echo "${BLUE}[START-BG]${NC} Iniciando servidor en segundo plano..."
	@mkdir -p $(PID_DIR) $(LOG_DIR)
	@source $(VENV_DIR)/bin/activate && \
	nohup python -m vigoleonrocks.interfaces.rest_api --host $(HOST) --port $(PORT) > $(LOG_DIR)/api.log 2>&1 & echo $$! > $(PID_DIR)/api.pid
	@sleep 2
	@if [ -f "$(PID_DIR)/api.pid" ] && kill -0 $$(cat $(PID_DIR)/api.pid) 2>/dev/null; then \
		echo "${GREEN}[START-BG]${NC} Servidor iniciado (PID: $$(cat $(PID_DIR)/api.pid))"; \
		echo "${GREEN}[START-BG]${NC} Métricas disponibles en http://$(HOST):$(PORT)/api/status"; \
	else \
		echo "${RED}[ERROR]${NC} Error al iniciar servidor"; \
		exit 1; \
	fi

stop: ## Detener servidor en segundo plano
	@echo "${YELLOW}[STOP]${NC} Deteniendo servidor..."
	@if [ -f "$(PID_DIR)/api.pid" ]; then \
		PID=$$(cat $(PID_DIR)/api.pid); \
		if kill -0 $$PID 2>/dev/null; then \
			kill $$PID; \
			rm -f $(PID_DIR)/api.pid; \
			echo "${GREEN}[STOP]${NC} Servidor detenido (PID: $$PID)"; \
		else \
			echo "${YELLOW}[STOP]${NC} Servidor no estaba ejecutándose"; \
			rm -f $(PID_DIR)/api.pid; \
		fi; \
	else \
		echo "${YELLOW}[STOP]${NC} No se encontró archivo PID"; \
	fi

logs: ## Mostrar logs del servidor en tiempo real
	@echo "${BLUE}[LOGS]${NC} Mostrando logs en tiempo real..."
	@if [ -f "$(LOG_DIR)/api.log" ]; then \
		tail -f $(LOG_DIR)/api.log; \
	else \
		echo "${RED}[ERROR]${NC} No se encontró archivo de logs"; \
	fi

status: ## Verificar estado del servidor y métricas
	@echo "${BLUE}[STATUS]${NC} Verificando estado del servidor..."
	@if [ -f "$(PID_DIR)/api.pid" ]; then \
		PID=$$(cat $(PID_DIR)/api.pid); \
		if kill -0 $$PID 2>/dev/null; then \
			echo "${GREEN}[STATUS]${NC} Servidor ejecutándose (PID: $$PID)"; \
			echo "${BLUE}[STATUS]${NC} Verificando métricas..."; \
			curl -s http://$(HOST):$(PORT)/api/status | head -10 || echo "${RED}[ERROR]${NC} No se pudo conectar a métricas"; \
		else \
			echo "${RED}[STATUS]${NC} Servidor no está ejecutándose"; \
		fi; \
	else \
		echo "${RED}[STATUS]${NC} No se encontró archivo PID"; \
	fi

health: ## Verificar salud completa del sistema
	@echo "${BLUE}[HEALTH]${NC} Verificando salud del sistema..."
	@echo "${BLUE}[HEALTH]${NC} 1. Verificando dependencias..."
	@python$(PYTHON_VERSION) --version
	@source $(VENV_DIR)/bin/activate && python -c "import vigoleonrocks; print('✓ VIGOLEONROCKS importado correctamente')" || echo "${RED}✗ Error importando VIGOLEONROCKS${NC}"
	@echo "${BLUE}[HEALTH]${NC} 2. Verificando configuración..."
	@source $(VENV_DIR)/bin/activate && python -c "from dotenv import load_dotenv; load_dotenv(); print('✓ Variables de entorno cargadas')" || echo "${YELLOW}⚠ .env no encontrado${NC}"
	@echo "${BLUE}[HEALTH]${NC} 3. Verificando métricas..."
	@curl -s http://$(HOST):$(PORT)/api/quantum-metrics > /dev/null && echo "✓ Métricas cuánticas disponibles" || echo "${YELLOW}⚠ Métricas no disponibles (servidor apagado?)${NC}"
	@echo "${GREEN}[HEALTH]${NC} Verificación completada"

## Docker
docker-build: ## Construir imagen Docker
	@echo "${BLUE}[DOCKER-BUILD]${NC} Construyendo imagen..."
	@docker build -t $(PROJECT_NAME):latest .
	@echo "${GREEN}[DOCKER-BUILD]${NC} Imagen construida: $(PROJECT_NAME):latest"

docker-up: ## Iniciar servicios con Docker Compose
	@echo "${BLUE}[DOCKER-UP]${NC} Iniciando servicios..."
	@docker compose up -d
	@echo "${GREEN}[DOCKER-UP]${NC} Servicios iniciados"
	@docker compose ps

docker-down: ## Detener servicios Docker Compose
	@echo "${YELLOW}[DOCKER-DOWN]${NC} Deteniendo servicios..."
	@docker compose down -v
	@echo "${GREEN}[DOCKER-DOWN]${NC} Servicios detenidos"

docker-logs: ## Mostrar logs de Docker Compose
	@echo "${BLUE}[DOCKER-LOGS]${NC} Mostrando logs..."
	@docker compose logs -f

## Monitoreo y Observabilidad
monitoring-up: ## Iniciar stack de monitoreo (Prometheus + Grafana)
	@echo "${BLUE}[MONITORING]${NC} Iniciando stack de monitoreo..."
	@if [ -f "docker-compose.monitoring.yml" ]; then \
		docker compose -f docker-compose.monitoring.yml up -d; \
		echo "${GREEN}[MONITORING]${NC} Stack de monitoreo iniciado"; \
		echo "${GREEN}[MONITORING]${NC} Grafana: http://localhost:3000"; \
		echo "${GREEN}[MONITORING]${NC} Prometheus: http://localhost:9090"; \
	else \
		echo "${YELLOW}[MONITORING]${NC} docker-compose.monitoring.yml no encontrado"; \
	fi

monitoring-down: ## Detener stack de monitoreo
	@echo "${YELLOW}[MONITORING]${NC} Deteniendo stack de monitoreo..."
	@if [ -f "docker-compose.monitoring.yml" ]; then \
		docker compose -f docker-compose.monitoring.yml down -v; \
		echo "${GREEN}[MONITORING]${NC} Stack de monitoreo detenido"; \
	else \
		echo "${YELLOW}[MONITORING]${NC} docker-compose.monitoring.yml no encontrado"; \
	fi

## Seguridad
security-scan: ## Ejecutar escaneo de seguridad
	@echo "${BLUE}[SECURITY]${NC} Ejecutando escaneo de seguridad..."
	@source $(VENV_DIR)/bin/activate && \
	pip install safety bandit && \
	safety check && \
	bandit -r vigoleonrocks/ -f json -o security-report.json
	@echo "${GREEN}[SECURITY]${NC} Escaneo completado - ver security-report.json"

## CI/CD
deploy: test-randomness lint type-check test ## Proceso de deployment completo
	@echo "${BLUE}[DEPLOY]${NC} Iniciando proceso de deployment..."
	@echo "${GREEN}[DEPLOY]${NC} ✓ Política de aleatoriedad verificada"
	@echo "${GREEN}[DEPLOY]${NC} ✓ Linting pasado"
	@echo "${GREEN}[DEPLOY]${NC} ✓ Verificación de tipos pasada"
	@echo "${GREEN}[DEPLOY]${NC} ✓ Tests pasados"
	@$(MAKE) docker-build
	@echo "${GREEN}[DEPLOY]${NC} Deployment completado"

## Comandos combinados
dev: install-dev format lint type-check test start-bg ## Configuración completa de desarrollo
	@echo "${GREEN}[DEV]${NC} Entorno de desarrollo listo"
	@echo "${GREEN}[DEV]${NC} Servidor ejecutándose en segundo plano"
	@echo "${GREEN}[DEV]${NC} Logs: make logs"
	@echo "${GREEN}[DEV]${NC} Estado: make status"

quality: format lint type-check test-randomness test-coverage ## Verificar calidad completa
	@echo "${GREEN}[QUALITY]${NC} Verificación de calidad completada"

all: setup install-dev quality docker-build ## Ejecutar todo el pipeline
	@echo "${GREEN}[ALL]${NC} Pipeline completo ejecutado"
