# Pre-entrega Automation Testing - SauceDemo

Proyecto de automatización web sobre [SauceDemo](https://www.saucedemo.com/), hecho para la pre-entrega del curso de Automation Testing con Selenium y Python.

## Objetivo

Se automatizan tres flujos básicos del sitio y se valida que funcionen bien:

1. **Login:** ingresar con `standard_user` / `secret_sauce` y comprobar que se llega a `/inventory.html` con el encabezado `Products`.
2. **Catálogo:** verificar el título, que haya productos visibles, que estén el menú y el filtro, y obtener nombre y precio del primer producto.
3. **Carrito:** agregar el primer producto, comprobar que el contador pase a 1 y que el producto aparezca dentro del carrito.

Cada test abre su propio navegador y hace su propio login, así que son independientes entre sí.

## Tecnologías

- Python 3
- Selenium WebDriver
- Pytest (con pytest-html para el reporte)
- Git y GitHub

## Estructura

```text
├── tests/
│   ├── conftest.py          # fixture del driver y capturas en fallos
│   └── test_saucedemo.py    # los 3 tests
├── utils/
│   └── helpers.py           # login, esperas y funciones auxiliares
├── reports/                 # reporte HTML, log y capturas
├── pytest.ini
├── requirements.txt
└── README.md
```

## Instalación

Hace falta tener Python y Google Chrome instalados.

```bash
git clone https://github.com/tomndc/pre-entrega-automation-testing-tomas-manduca.git
cd pre-entrega-automation-testing-tomas-manduca

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

## Ejecución

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html
```

Para correr sin abrir la ventana del navegador:

```bash
# Mac / Linux
HEADLESS=1 pytest tests/test_saucedemo.py -v --html=reports/reporte.html
```

## Reportes y evidencias

- **Reporte HTML:** `reports/reporte.html`
- **Log de ejecución:** `reports/ejecucion.log`
- **Capturas de pantalla:** si un test falla, se guarda una captura en `reports/screenshots/` y también queda adjunta en el reporte HTML.
