import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CARPETA_CAPTURAS = os.path.join("reports", "screenshots")


@pytest.fixture
def driver():
    """Abre un Chrome nuevo para cada test, así los tests no dependen entre sí."""
    opciones = Options()
    opciones.add_argument("--window-size=1280,800")
    opciones.add_argument("--incognito")
    # Para correr sin ventana: HEADLESS=1 pytest ...
    if os.environ.get("HEADLESS") == "1":
        opciones.add_argument("--headless=new")
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=opciones)
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test falla, guarda una captura y la agrega al reporte HTML."""
    outcome = yield
    reporte = outcome.get_result()

    if reporte.when == "call" and reporte.failed:
        driver = item.funcargs.get("driver")
        if driver is None:
            return

        os.makedirs(CARPETA_CAPTURAS, exist_ok=True)
        marca = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = os.path.join(CARPETA_CAPTURAS, f"{item.name}_{marca}.png")
        driver.save_screenshot(ruta)

        try:
            import pytest_html

            extras = getattr(reporte, "extras", [])
            extras.append(pytest_html.extras.image(driver.get_screenshot_as_base64()))
            reporte.extras = extras
        except ImportError:
            pass
