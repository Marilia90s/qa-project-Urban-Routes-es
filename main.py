from selenium import webdriver
import data
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get(data.URBAN_ROUTES_URL)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        # 1. Configurar la dirección de origen y destino
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)

    def test_select_comfort_tariff(self):
        # 2. Seleccionar la tarifa Comfort
        self.routes_page.select_comfort_tariff()

    def test_fill_phone_number(self):
        # 3. Rellenar el número de teléfono
        self.routes_page.fill_phone_number(data.PHONE_NUMBER)

    def test_add_credit_card(self):
        # 4. Agregar una tarjeta de crédito
        self.routes_page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)

    def test_write_message_for_driver(self):
        # 5. Escribir un mensaje para el conductor
        self.routes_page.enter_message(data.MESSAGE_FOR_DRIVER)
        assert self.routes_page.get_message() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_tissues(self):
        # 6. Pedir una manta y pañuelos
        self.routes_page.order_blanket_and_tissues()

    def test_order_ice_creams(self):
        # 7. Pedir 2 helados
        self.routes_page.order_ice_cream(2)

    def test_car_search_modal_appears(self):
        # 8. Confirmar pedido y verificar modal
        if hasattr(self.routes_page, 'click_smart_button'):
            self.routes_page.click_smart_button()
        elif hasattr(self.routes_page, 'click_order_button'):
            self.routes_page.click_order_button()
        elif hasattr(self.routes_page, 'click_reserve_button'):
            self.routes_page.click_reserve_button()
        else:

            self.routes_page.click_smart_button()

        assert self.routes_page.is_taxi_search_modal_displayed() is True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()