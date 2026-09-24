import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import data
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    def setup_method(self):
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(data.URBAN_ROUTES_URL)
        self.routes_page = UrbanRoutesPage(self.driver)

    def teardown_method(self):
        self.driver.quit()


    def _set_route_and_select_comfort(self):
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.select_comfort_tariff()

    def test_set_route(self):
        # 1. Configurar la dirección de origen y destino
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.routes_page.get_from() == data.ADDRESS_FROM
        assert self.routes_page.get_to() == data.ADDRESS_TO

    def test_select_comfort_tariff(self):
        # 2. Seleccionar la tarifa Comfort
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.select_comfort_tariff()
        assert self.routes_page.get_active_tariff_name() == "Comfort"

    def test_fill_phone_number(self):
        # 3. Rellenar el número de teléfono
        self._set_route_and_select_comfort()
        self.routes_page.fill_phone_number(data.PHONE_NUMBER)
        assert self.routes_page.get_phone() == data.PHONE_NUMBER

    def test_add_credit_card(self):
        # 4. Agregar una tarjeta de crédito
        self._set_route_and_select_comfort()
        self.routes_page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.routes_page.get_current_payment_method() == "Tarjeta"

    def test_write_message_for_driver(self):
        # 5. Escribir un mensaje para el conductor
        self._set_route_and_select_comfort()
        self.routes_page.enter_message(data.MESSAGE_FOR_DRIVER)
        assert self.routes_page.get_message() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_tissues(self):
        # 6. Pedir una manta y pañuelos
        self._set_route_and_select_comfort()
        self.routes_page.order_blanket_and_tissues()
        assert self.routes_page.is_blanket_selected() is True

    def test_order_ice_creams(self):
        # 7. Pedir 2 helados
        self._set_route_and_select_comfort()
        self.routes_page.order_ice_cream(2)
        assert self.routes_page.get_ice_cream_count() == 2

    def test_car_search_modal_appears(self):
        # 8. Confirmar pedido y verificar modal
        self._set_route_and_select_comfort()
        self.routes_page.fill_phone_number(data.PHONE_NUMBER)
        self.routes_page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        self.routes_page.enter_message(data.MESSAGE_FOR_DRIVER)
        self.routes_page.order_blanket_and_tissues()
        self.routes_page.order_ice_cream(2)

        if hasattr(self.routes_page, 'click_smart_button'):
            self.routes_page.click_smart_button()
        elif hasattr(self.routes_page, 'click_order_button'):
            self.routes_page.click_order_button()
        elif hasattr(self.routes_page, 'click_reserve_button'):
            self.routes_page.click_reserve_button()
        else:
            self.routes_page.click_smart_button()

        assert self.routes_page.is_taxi_search_modal_displayed() is True