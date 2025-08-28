# Makefile para ejecutar pruebas con diferentes configuraciones

.PHONY: help install test test-parallel test-sequential test-fast test-auth test-cart test-navbar test-slow

# Ayuda
help:
	@echo "🚀 Comandos disponibles para pruebas:"
	@echo ""
	@echo "📦 Instalación:"
	@echo "  make install          - Instalar dependencias"
	@echo ""
	@echo "🧪 Ejecución de pruebas:"
	@echo "  make test             - Ejecutar todas las pruebas (auto-detect paralelo/secuencial)"
	@echo "  make test-parallel    - Ejecutar todas las pruebas en paralelo"
	@echo "  make test-sequential  - Ejecutar todas las pruebas secuencialmente"
	@echo "  make test-fast        - Ejecutar pruebas rápidas en paralelo (excluye 'slow')"
	@echo ""
	@echo "🎯 Pruebas específicas:"
	@echo "  make test-auth        - Solo pruebas de autenticación"
	@echo "  make test-cart        - Solo pruebas del carrito"
	@echo "  make test-navbar      - Solo pruebas del navbar"
	@echo "  make test-slow        - Solo pruebas marcadas como lentas"
	@echo ""
	@echo "⚡ Pruebas personalizadas:"
	@echo "  make test-custom TESTS=tests/auth/ WORKERS=4"
	@echo "  make test-custom TESTS=tests/cart/test_cart.py MARKERS='not slow'"

# Instalación
install:
	@echo "📦 Instalando dependencias..."
	@if command -v uv >/dev/null 2>&1; then \
		echo "Usando uv para instalar dependencias..."; \
		uv sync; \
	else \
		echo "Usando pip para instalar dependencias..."; \
		pip install -e .; \
	fi
	@echo "📦 Instalando navegadores de Playwright..."
	playwright install chromium

# Pruebas automáticas
test:
	@echo "🤖 Ejecutando pruebas (modo automático)..."
	python run_tests.py auto

# Pruebas paralelas
test-parallel:
	@echo "⚡ Ejecutando todas las pruebas en paralelo..."
	python run_tests.py parallel

# Pruebas secuenciales
test-sequential:
	@echo "🐌 Ejecutando todas las pruebas secuencialmente..."
	python run_tests.py sequential

# Pruebas rápidas (excluye slow)
test-fast:
	@echo "🚀 Ejecutando pruebas rápidas en paralelo..."
	python run_tests.py parallel auto tests/ "not slow"

# Pruebas específicas por categoría
test-auth:
	@echo "🔐 Ejecutando pruebas de autenticación..."
	python run_tests.py parallel auto tests/auth/

test-cart:
	@echo "🛒 Ejecutando pruebas del carrito..."
	python run_tests.py parallel auto tests/cart/

test-navbar:
	@echo "🧭 Ejecutando pruebas del navbar..."
	python run_tests.py parallel auto tests/navbar_horizontal/

test-slow:
	@echo "⏰ Ejecutando pruebas lentas..."
	python run_tests.py sequential tests/ "slow"

# Pruebas personalizadas
test-custom:
	@echo "🎯 Ejecutando pruebas personalizadas..."
	@if [ -z "$(TESTS)" ]; then \
		echo "❌ Error: Especifica TESTS=ruta/a/tests"; \
		exit 1; \
	fi
	@if [ -n "$(WORKERS)" ] && [ -n "$(MARKERS)" ]; then \
		python run_tests.py parallel $(WORKERS) $(TESTS) "$(MARKERS)"; \
	elif [ -n "$(WORKERS)" ]; then \
		python run_tests.py parallel $(WORKERS) $(TESTS); \
	elif [ -n "$(MARKERS)" ]; then \
		python run_tests.py parallel auto $(TESTS) "$(MARKERS)"; \
	else \
		python run_tests.py parallel auto $(TESTS); \
	fi

# Limpiar archivos temporales
clean:
	@echo "🧹 Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# Verificar configuración
check:
	@echo "🔍 Verificando configuración..."
	@echo "Python: $(shell python --version)"
	@echo "Pytest: $(shell python -m pytest --version | head -1)"
	@echo "Playwright: $(shell python -c 'import playwright; print(f\"Playwright {playwright.__version__}\")')"
	@echo "CPUs disponibles: $(shell python -c 'import multiprocessing; print(multiprocessing.cpu_count())')"
	@echo "Workers recomendados: $(shell python -c 'import multiprocessing; print(max(1, int(multiprocessing.cpu_count() * 0.75)))')"
