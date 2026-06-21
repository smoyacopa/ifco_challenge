import pytest
from src.transformations import get_full_name

class TestGetFullName:

    def test_nombre_y_apellido_completos(self):
        raw = '[{"contact_name":"Curtis","contact_surname":"Jackson"}]'
        assert get_full_name(raw) == "Curtis Jackson"

    def test_solo_nombre_sin_apellido(self):
        raw = '[{"contact_name":"Curtis"}]'
        assert get_full_name(raw) == "Curtis"

    def test_solo_apellido_sin_nombre(self):
        raw = '[{"contact_surname":"Jackson"}]'
        assert get_full_name(raw) == "Jackson"

    def test_vacio_devuelve_placeholder(self):
        assert get_full_name("") == "John Doe"

    def test_none_devuelve_placeholder(self):
        assert get_full_name(None) == "John Doe"

    def test_json_malformado_devuelve_placeholder(self):
        assert get_full_name("esto no es json") == "John Doe"

    def test_campos_vacios_devuelve_placeholder(self):
        # JSON válido pero con strings vacíos
        raw = '[{"contact_name":"","contact_surname":""}]'
        assert get_full_name(raw) == "John Doe"

    def test_espacios_en_nombre_se_limpian(self):
        raw = '[{"contact_name":"  Curtis  ","contact_surname":"  Jackson  "}]'
        assert get_full_name(raw) == "Curtis Jackson"