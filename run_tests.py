#!/usr/bin/env python3
"""
Script para ejecutar pruebas con diferentes configuraciones de paralelismo
"""
import os
import sys
import subprocess
import multiprocessing

def get_cpu_count():
    """Obtiene el número óptimo de workers basado en los CPUs disponibles"""
    cpu_count = multiprocessing.cpu_count()
    # Usar máximo 75% de los CPUs para evitar saturar el sistema
    optimal_workers = max(1, int(cpu_count * 0.75))
    return optimal_workers

def run_tests_parallel(workers=None, test_path="tests/", markers=None):
    """Ejecuta las pruebas en paralelo"""
    if workers is None:
        workers = get_cpu_count()
    
    cmd = [
        "python", "-m", "pytest",
        f"-n={workers}",  # Número de workers
        "--dist=loadfile",  # Distribuir archivos completos entre workers
        test_path
    ]
    
    if markers:
        cmd.extend(["-m", markers])
    
    print(f"🚀 Ejecutando pruebas en paralelo con {workers} workers...")
    print(f"📁 Ruta: {test_path}")
    if markers:
        print(f"🏷️  Markers: {markers}")
    print(f"💻 Comando: {' '.join(cmd)}")
    print("-" * 50)
    
    return subprocess.run(cmd)

def run_tests_sequential(test_path="tests/", markers=None):
    """Ejecuta las pruebas secuencialmente"""
    cmd = ["python", "-m", "pytest", test_path]
    
    if markers:
        cmd.extend(["-m", markers])
    
    print(f"🐌 Ejecutando pruebas secuencialmente...")
    print(f"📁 Ruta: {test_path}")
    if markers:
        print(f"🏷️  Markers: {markers}")
    print(f"💻 Comando: {' '.join(cmd)}")
    print("-" * 50)
    
    return subprocess.run(cmd)

def main():
    """Función principal con opciones de ejecución"""
    if len(sys.argv) < 2:
        print("📋 Opciones disponibles:")
        print("  python run_tests.py parallel [workers] [path] [markers]")
        print("  python run_tests.py sequential [path] [markers]")
        print("  python run_tests.py auto [path] [markers]")
        print("\n📖 Ejemplos:")
        print("  python run_tests.py parallel 4 tests/auth/")
        print("  python run_tests.py sequential tests/cart/")
        print("  python run_tests.py auto tests/ 'not slow'")
        print(f"\n💻 CPUs detectados: {multiprocessing.cpu_count()}")
        print(f"👥 Workers recomendados: {get_cpu_count()}")
        return
    
    mode = sys.argv[1].lower()
    test_path = sys.argv[3] if len(sys.argv) > 3 else "tests/"
    markers = sys.argv[4] if len(sys.argv) > 4 else None
    
    if mode == "parallel":
        workers = None
        if len(sys.argv) > 2 and sys.argv[2] != "auto":
            try:
                workers = int(sys.argv[2])
            except ValueError:
                workers = get_cpu_count()
        else:
            workers = get_cpu_count()
        result = run_tests_parallel(workers, test_path, markers)
    elif mode == "sequential":
        result = run_tests_sequential(test_path, markers)
    elif mode == "auto":
        # Decidir automáticamente basado en el número de archivos
        import glob
        test_files = glob.glob(f"{test_path}/**/test_*.py", recursive=True)
        if len(test_files) > 3:
            print("🤖 Auto-modo: Usando paralelo (muchos archivos detectados)")
            result = run_tests_parallel(None, test_path, markers)
        else:
            print("🤖 Auto-modo: Usando secuencial (pocos archivos detectados)")
            result = run_tests_sequential(test_path, markers)
    else:
        print(f"❌ Modo desconocido: {mode}")
        return
    
    return result.returncode

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code or 0)
