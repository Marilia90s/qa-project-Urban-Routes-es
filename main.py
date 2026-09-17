import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data


def retrieve_phone_code(driver) -> str:
    """Obtiene el código de confirmación del teléfono desde los logs de red (CDP)."""
    for _ in range(15):
        logs = driver.get_log("performance")

        for entry in logs:
            try:
                message = json.loads(entry["message"])["message"]

                if message["method"] != "Network.responseReceived":
                    continue

                params = message["params"]
                request_id = params["requestId"]

                try:
                    response = driver.execute_cdp_cmd(
                        "Network.getResponseBody",
                        {"requestId": request_id}
                    )
                except Exception:
                    continue

                body_text = response.get("body", "")

                if not body_text:
                    continue

                try:
                    body = json.loads(body_text)
                except json.JSONDecodeError:
                    continue

                if isinstance(body, dict) and "code" in body:
                    print("Código encontrado:", body["code"])
                    return str(body["code"])

            except Exception as error:
                print("Error procesando log:", error)

        time.sleep(1)

    raise Exception("No se encontró el código de confirmación del teléfono.")


class UrbanRoutesPage:

    # ==================================================
    # LOCALIZADORES
    # ==================================================

    # Ruta
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Pedir taxi
    order_taxi_button = (
        By.XPATH,
        '//button[contains(normalize-space(), "Pedir un taxi")]'
    )

    # Comfort
    comfort_text = (
        By.XPATH,
        '//div[contains(@class, "tcard-title") '
        'and normalize-space()="Comfort"]'
    )

    # Teléfono
    phone_button = (
        By.CLASS_NAME,
        'np-button'
    )

    phone_field = (
        By.ID,
        'phone'
    )

    next_button = (
        By.XPATH,
        '(//button[@class="button full"])[1]'
    )

    phone_code_field = (
        By.ID,
        'code'
    )

    confirm_phone_button = (
        By.XPATH,
        '//button[@class="button full" and text()="Confirmar"]'
    )

    # Tarjeta
    payment_method_button = (
        By.CLASS_NAME,
        'pp-text'
    )

    add_card_button = (
        By.CLASS_NAME,
        'pp-plus-container'
    )

    card_number_field = (
        By.ID,
        'number'
    )

    card_code_field = (
        By.XPATH,
        '//div[@class="card-code-input"]//input[@id="code"]'
    )

    link_card_button = (
        By.XPATH,
        '//button[text()="Agregar"]'
    )

    close_payment_modal_button = (
        By.XPATH,
        '//div[contains(@class, "payment-picker")]//button[contains(@class, "close-button")]'
    )

    # Mensaje al conductor
    message_field = (
        By.ID,
        'comment'
    )

    # Manta y pañuelos
    blanket_tissues_switch = (
        By.XPATH,
        '//span[@class="slider round"]'
    )

    # Helado
    ice_cream_plus_button = (
        By.XPATH,
        '//div[@class="r-counter-container"][1]'
        '//div[@class="counter-plus"]'
    )

    ice_cream_count = (
        By.XPATH,
        '//div[@class="r-counter-container"][1]'
        '//div[@class="counter-value"]'
    )

    # Botón final para pedir taxi
    smart_button = (
        By.CLASS_NAME,
        'smart-button'
    )

    # Modal de búsqueda
    taxi_search_modal = (
        By.CLASS_NAME,
        'order-body'
    )

    def __init__(self, driver):
        self.driver = driver

    # ==================================================
    # PASO 1 - CONFIGURAR RUTA
    # ==================================================

    def set_route(self, from_address, to_address):

        from_field = WebDriverWait(
            self.driver, 10
        ).until(
            EC.visibility_of_element_located(
                self.from_field
            )
        )

        from_field.clear()
        from_field.send_keys(from_address)

        to_field = WebDriverWait(
            self.driver, 10
        ).until(
            EC.visibility_of_element_located(
                self.to_field
            )
        )

        to_field.clear()
        to_field.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(
            *self.from_field
        ).get_property('value')

    def get_to(self):
        return self.driver.find_element(
            *self.to_field
        ).get_property('value')

    # ==================================================
    # PASO 2 - PEDIR TAXI
    # ==================================================

    def click_order_taxi_button(self):

        WebDriverWait(
            self.driver, 10
        ).until(
            EC.element_to_be_clickable(
                self.order_taxi_button
            )
        ).click()

    # ==================================================
    # PASO 3 - SELECCIONAR COMFORT
    # ==================================================

    def select_comfort_tariff(self):

        comfort = WebDriverWait(
            self.driver, 15
        ).until(
            EC.visibility_of_element_located(
                self.comfort_text
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            comfort
        )

        time.sleep(0.5)

        try:
            comfort.click()
        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                comfort
            )

    def is_comfort_selected(self):

        try:
            return self.driver.find_element(
                *self.comfort_text
            ).is_displayed()

        except Exception:
            return False

    # ==================================================
    # PASO 4 - TELÉFONO
    # ==================================================

    def fill_phone_number(self):
        wait = WebDriverWait(self.driver, 10)

        # 1. Abrir modal/campo de teléfono
        wait.until(
            EC.element_to_be_clickable(self.phone_button)
        ).click()

        # 2. Escribir número de teléfono
        phone_field = wait.until(
            EC.visibility_of_element_located(self.phone_field)
        )
        phone_field.clear()

        # Diagnóstico de formato de teléfono
        # print("PHONE:", repr(data.phone_number))
        phone_field.send_keys(data.phone_number)

        # Limpiar logs de red acumulados antes de la petición
        self.driver.get_log("performance")

        # 3. Avanzar para solicitar el código
        wait.until(
            EC.element_to_be_clickable(self.next_button)
        ).click()

        # 4. Obtener e ingresar el código de verificación
        code = retrieve_phone_code(self.driver)

        phone_code_field = wait.until(
            EC.visibility_of_element_located(self.phone_code_field)
        )
        phone_code_field.clear()
        phone_code_field.send_keys(code)

        # 5. Confirmar código
        wait.until(
            EC.element_to_be_clickable(self.confirm_phone_button)
        ).click()

    # ==================================================
    # PASO 5 - TARJETA
    # ==================================================

    def add_credit_card(self, card_number, card_code):
        # Abrir métodos de pago
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.payment_method_button)
        ).click()

        # Agregar tarjeta
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_card_button)
        ).click()

        # Número de tarjeta
        card_num_el = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.card_number_field)
        )
        card_num_el.send_keys(card_number)

        # CVV
        cvv = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.card_code_field)
        )
        cvv.send_keys(card_code)
        cvv.send_keys(Keys.TAB)

        # Guardar / vincular tarjeta
        link_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.link_card_button)
        )
        link_btn.click()

        # Cerrar modal de pago
        close_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.close_payment_modal_button)
        )
        self.driver.execute_script("arguments[0].click();", close_btn)

    # ==================================================
    # PASO 6 - MENSAJE AL CONDUCTOR
    # ==================================================

    def set_driver_message(self, message):

        field = WebDriverWait(
            self.driver, 10
        ).until(
            EC.visibility_of_element_located(
                self.message_field
            )
        )

        field.clear()
        field.send_keys(message)

    # ==================================================
    # PASO 7 - MANTA Y PAÑUELOS
    # ==================================================

    def select_blanket_and_tissues(self):
        WebDriverWait(
            self.driver, 10
        ).until(
            EC.element_to_be_clickable(
                self.blanket_tissues_switch
            )
        ).click()

    # ==================================================
    # PASO 8 - DOS HELADOS
    # ==================================================

    def add_ice_creams(self, count=2):

        for _ in range(count):

            plus_button = WebDriverWait(
                self.driver, 10
            ).until(
                EC.element_to_be_clickable(
                    self.ice_cream_plus_button
                )
            )

            plus_button.click()

    def get_ice_cream_count(self):

        return self.driver.find_element(
            *self.ice_cream_count
        ).text

    # ==================================================
    # PASO 9 - PEDIR TAXI
    # ==================================================

    def request_taxi(self):

        WebDriverWait(
            self.driver, 10
        ).until(
            EC.element_to_be_clickable(
                self.smart_button
            )
        ).click()

    # ==================================================
    # PASO 10 - COMPROBAR MODAL
    # ==================================================

    def is_taxi_modal_present(self):

        try:

            return WebDriverWait(
                self.driver, 15
            ).until(
                EC.visibility_of_element_located(
                    self.taxi_search_modal
                )
            ).is_displayed()

        except Exception:

            return False


class TestUrbanRoutes:

    # ==================================================
    # CONFIGURAR NAVEGADOR
    # ==================================================

    @classmethod
    def setup_class(cls):

        options = webdriver.ChromeOptions()

        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )

        cls.driver = webdriver.Chrome(
            options=options
        )

        cls.driver.maximize_window()

    # ==================================================
    # TEST COMPLETO
    # ==================================================

    def test_full_taxi_order_flow(self):

        # Abrir Urban Routes
        self.driver.get(
            data.urban_routes_url
        )

        routes_page = UrbanRoutesPage(
            self.driver
        )

        # ----------------------------------------------
        # 1. Configurar ruta
        # ----------------------------------------------

        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        assert routes_page.get_from() == \
            data.address_from

        assert routes_page.get_to() == \
            data.address_to

        # ----------------------------------------------
        # 2. Seleccionar Comfort
        # ----------------------------------------------

        routes_page.click_order_taxi_button()

        routes_page.select_comfort_tariff()

        assert routes_page.is_comfort_selected() is True

        # ----------------------------------------------
        # 3. Introducir teléfono
        # ----------------------------------------------

        routes_page.fill_phone_number()

        # ----------------------------------------------
        # 4. Agregar tarjeta
        # ----------------------------------------------

        routes_page.add_credit_card(
            data.card_number,
            data.card_code
        )

        # ----------------------------------------------
        # 5. Mensaje al conductor
        # ----------------------------------------------

        routes_page.set_driver_message(
            data.message_for_driver
        )

        # ----------------------------------------------
        # 6. Manta y pañuelos
        # ----------------------------------------------

        routes_page.select_blanket_and_tissues()

        # ----------------------------------------------
        # 7. Dos helados
        # ----------------------------------------------

        routes_page.add_ice_creams(2)

        assert routes_page.get_ice_cream_count() == "2"

        # ----------------------------------------------
        # 8. Pedir taxi
        # ----------------------------------------------

        routes_page.request_taxi()

        # ----------------------------------------------
        # 9. Comprobar modal
        # ----------------------------------------------

        assert routes_page.is_taxi_modal_present() is True

    # ==================================================
    # CERRAR NAVEGADOR
    # ==================================================

    @classmethod
    def teardown_class(cls):

        if cls.driver:
            cls.driver.quit()