from dotenv import load_dotenv
import pytest
from playwright.sync_api import sync_playwright
import os
from utils.config import DEFAULT_TIMEOUT, DEFAULT_NAVIGATION_TIMEOUT, DEFAULT_VIEWPORT_WIDTH, DEFAULT_VIEWPORT_HEIGHT, IS_HEADLESS


load_dotenv()

@pytest.fixture(scope="session")
def browser_context_args():
    """Argumentos para el contexto del browser, optimizados para paralelismo"""
    return {
        "viewport": {"width": DEFAULT_VIEWPORT_WIDTH, "height": DEFAULT_VIEWPORT_HEIGHT},
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Argumentos para el lanzamiento del browser, optimizados para paralelismo"""
    # Detectar si estamos en ejecución paralela
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")
    is_parallel = worker_id is not None
    
    return {
        "headless": is_parallel or IS_HEADLESS,  # Usar config, pero forzar headless en paralelo
        "args": [
            "--disable-dev-shm-usage",
            "--disable-extensions", 
            "--disable-gpu",
            "--no-sandbox",
            "--disable-setuid-sandbox"
        ] if is_parallel else []
    }

@pytest.fixture(scope="function")
def browser():
    """Browser fixture optimizado para ejecución paralela"""
    with sync_playwright() as p:
        # Obtener argumentos del browser
        # Usar headless de config, pero forzar headless en paralelo
        is_parallel = os.environ.get("PYTEST_XDIST_WORKER") is not None
        launch_args = {
            "headless": is_parallel or IS_HEADLESS,
            "args": [
                "--disable-dev-shm-usage",
                "--disable-extensions", 
                "--disable-gpu",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ] if is_parallel else []
        }
        
        browser = p.chromium.launch(**launch_args)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """Page fixture optimizado para paralelismo"""
    context = browser.new_context(
        viewport={"width": DEFAULT_VIEWPORT_WIDTH, "height": DEFAULT_VIEWPORT_HEIGHT},
        ignore_https_errors=True
    )
    page = context.new_page()
    
    # Configurar timeouts desde configuración centralizada
    page.set_default_timeout(DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(DEFAULT_NAVIGATION_TIMEOUT)
    
    yield page
    context.close()