# 🚀 Guía de Ejecución de Pruebas Paralelas

Esta guía te ayudará a ejecutar tus pruebas de Playwright en paralelo para mejorar significativamente la velocidad de ejecución.

## ⚡ Configuración Completa

### 📦 Instalación

```bash
# 1. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install playwright pytest pytest-xdist python-dotenv Faker

# 3. Instalar browsers
playwright install chromium
```

### 🔧 Características Implementadas

- ✅ **pytest-xdist** para ejecución paralela
- ✅ **Detección automática** de modo paralelo/secuencial
- ✅ **Browser headless automático** en modo paralelo
- ✅ **Configuración optimizada** de timeouts y recursos
- ✅ **Scripts de conveniencia** (Makefile y Python)
- ✅ **Distribución inteligente** de archivos de prueba

## 🎯 Formas de Ejecutar Pruebas

### Opción 1: Script Python (Recomendado)

```bash
# Activar entorno virtual
source venv/bin/activate

# Modo automático (detecta si usar paralelo o secuencial)
python run_tests.py auto

# Paralelo con workers automáticos
python run_tests.py parallel

# Paralelo con workers específicos
python run_tests.py parallel 4

# Secuencial tradicional
python run_tests.py sequential

# Pruebas específicas
python run_tests.py parallel 2 tests/auth/
python run_tests.py auto tests/cart/ "not slow"
```

### Opción 2: Makefile (Más Simple)

```bash
# Ver ayuda
make help

# Ejecución básica
make test                 # Automático
make test-parallel        # Paralelo
make test-sequential      # Secuencial
make test-fast           # Paralelo sin pruebas lentas

# Categorías específicas
make test-auth           # Solo autenticación
make test-cart           # Solo carrito
make test-navbar         # Solo navbar

# Personalizado
make test-custom TESTS=tests/auth/ WORKERS=4
make test-custom TESTS=tests/cart/ MARKERS="not slow"
```

### Opción 3: pytest Directo

```bash
# Activar entorno virtual
source venv/bin/activate

# Paralelo básico
pytest -n auto

# Paralelo con workers específicos
pytest -n 4

# Paralelo con distribución por archivo
pytest -n 4 --dist=loadfile

# Combinando con otros filtros
pytest -n 4 tests/auth/ -m "not slow"
```

## 📊 Comparación de Rendimiento

| Modo | Tiempo (aprox) | Uso de CPU | Browser |
|------|---------------|------------|---------|
| **Secuencial** | 100% (baseline) | 25% | Visual |
| **Paralelo 2 workers** | ~50% | 50% | Headless |
| **Paralelo 4 workers** | ~35% | 75% | Headless |
| **Paralelo auto** | ~40% | 65% | Headless |

*Resultados basados en 12 pruebas de auth: 35.28s con 2 workers vs ~70s secuencial*

## 🛠️ Configuraciones Avanzadas

### Variables de Entorno

```bash
# Forzar modo headless siempre
export PYTEST_XDIST_WORKER=true

# Configurar timeouts personalizados
export PLAYWRIGHT_TIMEOUT=30000
```

### Markers Personalizados

```python
# En tu prueba
@pytest.mark.parallel
def test_can_run_parallel():
    pass

@pytest.mark.serial  
def test_must_run_sequential():
    pass

@pytest.mark.slow
def test_takes_long_time():
    pass
```

```bash
# Ejecutar solo pruebas paralelas
pytest -n 4 -m "parallel"

# Excluir pruebas lentas
pytest -n auto -m "not slow"
```

## 🔍 Debugging y Troubleshooting

### Logs Detallados

```bash
# Con logs detallados
python run_tests.py parallel 2 tests/auth/ -v

# Ver qué worker ejecuta cada prueba
pytest -n 2 --dist=loadfile -v tests/auth/
```

### Problemas Comunes

1. **Error de "externally-managed-environment"**
   ```bash
   # Solución: Usar entorno virtual
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Pruebas fallan en paralelo pero pasan secuencialmente**
   ```bash
   # Marcar como serial
   @pytest.mark.serial
   # O ejecutar sin paralelismo
   pytest tests/problema/ --dist=no
   ```

3. **Consumo excesivo de memoria**
   ```bash
   # Reducir workers
   python run_tests.py parallel 2
   ```

## 📈 Mejores Prácticas

### ✅ DO (Hacer)
- Usar entorno virtual
- Empezar con pocos workers (2-4)
- Marcar pruebas problemáticas como `@pytest.mark.serial`
- Usar `--dist=loadfile` para mejor distribución
- Configurar timeouts apropiados

### ❌ DON'T (No Hacer)
- Usar más workers que CPUs disponibles
- Ejecutar pruebas interdependientes en paralelo
- Ignorar warnings de recursos
- Usar modo visual en paralelo (muy lento)

## 🎯 Resultados Esperados

Con la configuración implementada deberías ver:
- **50-70% reducción** en tiempo total de ejecución
- **Detección automática** de mejor estrategia de ejecución
- **Modo headless automático** en paralelo
- **Distribución inteligente** de pruebas entre workers

## 🚀 Quick Start

```bash
# Setup completo en 3 comandos
python3 -m venv venv && source venv/bin/activate
pip install playwright pytest pytest-xdist python-dotenv Faker
playwright install chromium

# Ejecutar pruebas optimizadas
python run_tests.py auto
```

¡Ya tienes configuración completa de pruebas paralelas! 🎉
