import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import (
    TIMEOUT,
    esperar_elemento_clickeable,
    esperar_elemento_visible,
    hacer_login,
    login_y_esperar_inventario,
    obtener_cantidad_carrito,
    obtener_nombre_y_precio,
    obtener_productos,
)

logger = logging.getLogger(__name__)


def test_login_exitoso(driver):
    hacer_login(driver)

    # Espera explícita a que cargue el inventario
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/inventory.html"))
    assert "/inventory.html" in driver.current_url

    # Título de la pestaña y encabezado de la página
    assert driver.title == "Swag Labs"
    titulo = esperar_elemento_visible(driver, (By.CLASS_NAME, "title")).text
    assert titulo == "Products", f"Se esperaba 'Products' y apareció '{titulo}'"


def test_catalogo_de_productos(driver):
    login_y_esperar_inventario(driver)

    titulo = esperar_elemento_visible(driver, (By.CLASS_NAME, "title")).text
    assert titulo == "Products"

    productos = obtener_productos(driver)
    assert len(productos) > 0, "No hay productos visibles en el catálogo"
    logger.info("Productos encontrados: %s", len(productos))

    # Elementos importantes de la interfaz
    menu = driver.find_element(By.ID, "react-burger-menu-btn")
    filtro = driver.find_element(By.CLASS_NAME, "product_sort_container")
    assert menu.is_displayed(), "El menú no se muestra"
    assert filtro.is_displayed(), "El filtro de orden no se muestra"

    nombre, precio = obtener_nombre_y_precio(productos[0])
    logger.info("Primer producto: %s - %s", nombre, precio)
    print(f"Primer producto: {nombre} - {precio}")
    assert nombre != ""
    assert precio.startswith("$")


def test_agregar_producto_al_carrito(driver):
    login_y_esperar_inventario(driver)

    primer_producto = obtener_productos(driver)[0]
    nombre, _ = obtener_nombre_y_precio(primer_producto)

    boton_agregar = primer_producto.find_element(By.TAG_NAME, "button")
    assert boton_agregar.text == "Add to cart"
    boton_agregar.click()
    logger.info("Producto agregado: %s", nombre)

    # El contador del carrito tiene que pasar a 1
    WebDriverWait(driver, TIMEOUT).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1")
    )
    assert obtener_cantidad_carrito(driver) == 1

    # Entrar al carrito y revisar que esté el producto
    esperar_elemento_clickeable(driver, (By.CLASS_NAME, "shopping_cart_link")).click()
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/cart.html"))

    items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items) == 1, f"Se esperaba 1 producto en el carrito y hay {len(items)}"
    nombre_en_carrito = items[0].find_element(By.CLASS_NAME, "inventory_item_name").text
    assert nombre_en_carrito == nombre
