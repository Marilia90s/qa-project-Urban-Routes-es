from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import helpers


class UrbanRoutesPage:
    # 1. Rutas
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")

    CALL_TAXI_BUTTON = (
        By.XPATH,
        "//button[contains(@class, 'button') and "
        "(contains(., 'Pedir') or "
        "contains(., 'reservar') or "
        "contains(., 'Introducir'))]"
    )

    # 2. Tarifas
    COMFORT_TARIFF = (
        By.XPATH,
        "//div[contains(text(), 'Comfort')]"
    )

    COMFORT_TARIFF_CARD = (
        By.XPATH,
        "//div[contains(@class, 'tariff-card') or contains(@class, 'tariff-card')][.//div[contains(text(), 'Comfort')]]"
    )

    ACTIVE_TARIFF = (
        By.XPATH,
        "//div[(contains(@class, 'tariff-card') or contains(@class, 'tariff-card')) and contains(@class, 'active')]"
    )

    # 3. Teléfono
    PHONE_BUTTON = (
        By.XPATH,
        "//div[@class='np-text' and contains(text(), 'Número de teléfono')]"
    )

    PHONE_INPUT = (By.ID, "phone")

    NEXT_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Siguiente')]"
    )

    CONFIRM_CODE_INPUT = (By.ID, "code")

    CONFIRM_PHONE_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Confirmar')]"
    )

    # 4. Método de pago
    PAYMENT_METHOD_BUTTON = (
        By.XPATH,
        "//div[@class='pp-button filled']"
    )

    ADD_CARD_BUTTON = (
        By.XPATH,
        "//div[@class='pp-title' and text()='Agregar tarjeta']"
    )

    CARD_NUMBER_INPUT = (By.ID, "number")

    CARD_CODE_INPUT = (
        By.XPATH,
        "//input[@id='code' and @name='code']"
    )

    CONFIRM_CARD_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Agregar')]"
    )

    CLOSE_PAYMENT_MODAL_BUTTON = (
        By.XPATH,
        "//div[@class='payment-picker open']//button"
        "[@class='close-button section-close']"
    )

    PAYMENT_METHOD_VALUE = (
        By.XPATH,
        "//div[@class='pp-value-text']"
    )

    # 5. Comentarios
    COMMENT_FIELD = (By.ID, "comment")

    # 6. Opcionales
    BLANKET_SWITCH = (
        By.XPATH,
        "//div[contains(text(), 'Manta y pañuelos')]"
        "/following-sibling::div//span[@class='slider round']"
    )

    BLANKET_CHECKBOX = (
        By.XPATH,
        "//div[contains(text(), 'Manta y pañuelos')]"
        "/following-sibling::div//input"
    )

    ICE_CREAM_PLUS_BUTTON = (
        By.XPATH,
        "//div[contains(text(), 'Helado')]"
        "/following-sibling::div//div[@class='counter-plus']"
    )

    ICE_CREAM_COUNT = (
        By.XPATH,
        "//div[contains(text(), 'Helado')]"
        "/following-sibling::div//div[@class='counter-value']"
    )

    # 7. Buscar taxi
    ORDER_BUTTON = (
        By.XPATH,
        "//button[contains(@class, 'smart-button')]"
    )

    TAXI_SEARCH_MODAL = (
        By.XPATH,
        "//div[@class='order-body']"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 12)

    # ---------------------------------------------------------
    # RUTA
    # ---------------------------------------------------------

    def set_route(self, address_from, address_to):
        from_field = self.wait.until(
            EC.element_to_be_clickable(self.FROM_FIELD)
        )
        from_field.send_keys(address_from)

        to_field = self.wait.until(
            EC.element_to_be_clickable(self.TO_FIELD)
        )
        to_field.send_keys(address_to)

        self.wait.until(
            EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)
        ).click()

    def get_from(self):
        return self.wait.until(
            EC.presence_of_element_located(self.FROM_FIELD)
        ).get_attribute("value")

    def get_to(self):
        return self.wait.until(
            EC.presence_of_element_located(self.TO_FIELD)
        ).get_attribute("value")

    # ---------------------------------------------------------
    # TARIFA
    # ---------------------------------------------------------

    def select_comfort_tariff(self):
        comfort_card = self.wait.until(
            EC.presence_of_element_located(self.COMFORT_TARIFF_CARD)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comfort_card)

        comfort_text = self.wait.until(
            EC.element_to_be_clickable(self.COMFORT_TARIFF)
        )
        comfort_text.click()

    def get_active_tariff_name(self):
        element = self.wait.until(
            EC.presence_of_element_located(self.COMFORT_TARIFF)
        )
        return element.text.strip()

    # ---------------------------------------------------------
    # TELÉFONO
    # ---------------------------------------------------------

    def fill_phone_number(self, phone_number):
        self.wait.until(
            EC.element_to_be_clickable(self.PHONE_BUTTON)
        ).click()

        phone_input = self.wait.until(
            EC.element_to_be_clickable(self.PHONE_INPUT)
        )
        phone_input.send_keys(phone_number)

        self.wait.until(
            EC.element_to_be_clickable(self.NEXT_BUTTON)
        ).click()

        code = helpers.retrieve_phone_code(self.driver)

        self.wait.until(
            EC.element_to_be_clickable(self.CONFIRM_CODE_INPUT)
        ).send_keys(code)

        self.wait.until(
            EC.element_to_be_clickable(self.CONFIRM_PHONE_BUTTON)
        ).click()

    def get_phone(self):
        return self.wait.until(
            EC.presence_of_element_located(self.PHONE_INPUT)
        ).get_attribute("value")

    # ---------------------------------------------------------
    # TARJETA
    # ---------------------------------------------------------

    def add_credit_card(self, card_number, card_code):
        self.wait.until(
            EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(self.ADD_CARD_BUTTON)
        ).click()

        card_input = self.wait.until(
            EC.element_to_be_clickable(self.CARD_NUMBER_INPUT)
        )
        card_input.send_keys(card_number)
        card_input.send_keys(Keys.TAB)

        code_input = self.wait.until(
            EC.presence_of_element_located(self.CARD_CODE_INPUT)
        )
        code_input.send_keys(card_code)
        code_input.send_keys(Keys.TAB)

        self.wait.until(
            EC.element_to_be_clickable(self.CONFIRM_CARD_BUTTON)
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                self.CLOSE_PAYMENT_MODAL_BUTTON
            )
        ).click()

    def get_current_payment_method(self):
        return self.wait.until(
            EC.presence_of_element_located(
                self.PAYMENT_METHOD_VALUE
            )
        ).text

    # ---------------------------------------------------------
    # COMENTARIO
    # ---------------------------------------------------------

    def enter_message(self, message):
        self.wait.until(
            EC.element_to_be_clickable(self.COMMENT_FIELD)
        ).send_keys(message)

    def get_message(self):
        return self.wait.until(
            EC.presence_of_element_located(self.COMMENT_FIELD)
        ).get_attribute("value")

    # ---------------------------------------------------------
    # MANTA Y PAÑUELOS
    # ---------------------------------------------------------

    def order_blanket_and_tissues(self):
        switch = self.wait.until(
            EC.presence_of_element_located(self.BLANKET_SWITCH)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", switch)
        self.driver.execute_script("arguments[0].click();", switch)

    def is_blanket_selected(self):
        return self.wait.until(
            EC.presence_of_element_located(self.BLANKET_CHECKBOX)
        ).is_selected()

    # ---------------------------------------------------------
    # HELADO
    # ---------------------------------------------------------

    def order_ice_cream(self, count):
        plus = self.wait.until(
            EC.presence_of_element_located(self.ICE_CREAM_PLUS_BUTTON)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", plus)

        for _ in range(count):
            self.wait.until(
                EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON)
            ).click()

    def get_ice_cream_count(self):
        return int(
            self.wait.until(
                EC.presence_of_element_located(
                    self.ICE_CREAM_COUNT
                )
            ).text
        )

    # ---------------------------------------------------------
    # PEDIR TAXI
    # ---------------------------------------------------------

    def click_order_button(self):
        order = self.wait.until(
            EC.element_to_be_clickable(self.ORDER_BUTTON)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", order)
        order.click()

    def click_smart_button(self):
        self.click_order_button()

    def is_taxi_search_modal_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.TAXI_SEARCH_MODAL
            )
        ).is_displayed()