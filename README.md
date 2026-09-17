# QA Project: Urban Routes Automation

## Descripción del Proyecto
Este proyecto automatiza la prueba del flujo completo de solicitud de taxi en la aplicación web **Urban Routes**.

## Escenarios de Prueba Automatizados
1. Configuración de la ruta (origen y destino).
2. Selección de la tarifa **Comfort**.
3. Ingreso e interceptación del código de verificación de teléfono mediante CDP.
4. Vinculación de un método de pago (tarjeta de crédito).
5. Mensaje personalizado para el conductor.
6. Solicitud de accesorios (manta y pañuelos).
7. Pedido de elementos opcionales (dos helados).
8. Confirmación final de reserva y verificación de la aparición del modal de búsqueda de taxi.

## Tecnologías Utilizadas
* **Lenguaje:** Python 3.x
* **Framework de Pruebas:** Pytest
* **Herramienta de Automatización:** Selenium WebDriver
* **Patrón de Diseño:** Page Object Model (POM)
* **Captura de Logs:** Chrome DevTools Protocol (CDP)

## Requisitos Previos
* Python 3.x instalado.
* Google Chrome y ChromeDriver.

## Instrucciones de Ejecución
1. Instalar dependencias:
```bash
pip install pytest selenium
```
2. Ejecutar las pruebas:
```
pytest main.py
```