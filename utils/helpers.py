import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

URL_BASE = "https://www.saucedemo.com/"
USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDO = "secret_sauce"
TIMEOUT = 10


def esperar_elemento_visible(driver, locator, timeout=TIMEOUT):
    """Espera (explícita) a que el elemento sea visible y lo devuelve."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def esperar_elemento_clickeable(driver, locator, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


def hacer_login(driver, usuario=USUARIO_VALIDO, password=PASSWORD_VALIDO):
    """Abre SauceDemo e inicia sesión con las credenciales indicadas."""
    logger.info("Abriendo %s", URL_BASE)
    driver.get(URL_BASE)

    esperar_elemento_visible(driver, (By.ID, "user-name")).send_keys(usuario)
    driver.find_element(By.ID, "password").send_keys(password)
    logger.info("Haciendo login con el usuario '%s'", usuario)
    driver.find_element(By.ID, "login-button").click()


def login_y_esperar_inventario(driver):
    """Hace login y espera a estar en la página de inventario."""
    hacer_login(driver)
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/inventory.html"))


def obtener_productos(driver):
    """Devuelve la lista de productos visibles en el catálogo."""
    return driver.find_elements(By.CLASS_NAME, "inventory_item")


def obtener_nombre_y_precio(producto):
    """Recibe un elemento de producto y devuelve (nombre, precio)."""
    nombre = producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio = producto.find_element(By.CLASS_NAME, "inventory_item_price").text
    return nombre, precio


def obtener_cantidad_carrito(driver):
    """Devuelve el número que muestra el ícono del carrito (0 si no hay badge)."""
    badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    if not badges:
        return 0
    return int(badges[0].text)
