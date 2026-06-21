import pytest
from src.transformations import calculate_net_value_eur, get_commission_rate

class TestCalculateNetValue:

    def test_sin_iva(self):
        # VAT=0: neto = bruto / 100
        assert calculate_net_value_eur(324222, 0) == 3242.22

    def test_con_iva_19(self):
        # 193498 / 1.19 / 100
        assert calculate_net_value_eur(193498, 19) == round(193498 / 1.19 / 100, 2)

    def test_con_iva_21(self):
        assert calculate_net_value_eur(345498, 21) == round(345498 / 1.21 / 100, 2)

    def test_con_iva_34(self):
        # El caso de la factura duplicada
        assert calculate_net_value_eur(345310, 34) == round(345310 / 1.34 / 100, 2)

    def test_gross_none_devuelve_cero(self):
        assert calculate_net_value_eur(None, 19) == 0.0

    def test_vat_none_devuelve_cero(self):
        assert calculate_net_value_eur(100000, None) == 0.0


class TestGetCommissionRate:

    def test_main_owner_6_pct(self):
        assert get_commission_rate(1) == 0.06

    def test_coowner1_2_5_pct(self):
        assert get_commission_rate(2) == 0.025

    def test_coowner2_0_95_pct(self):
        assert get_commission_rate(3) == 0.0095

    def test_resto_sin_comision(self):
        assert get_commission_rate(4) == 0.0
        assert get_commission_rate(5) == 0.0
        assert get_commission_rate(99) == 0.0

    def test_posicion_cero_sin_comision(self):
        # Defensivo: posición 0 no debería ocurrir pero no debe romper
        assert get_commission_rate(0) == 0.0