import pytest
from src.transformations import get_address

class TestGetAddress:

    def test_ciudad_y_cp_completos(self):
        raw = '[{"city":"Munich","cp":"80331"}]'
        assert get_address(raw) == "Munich, 80331"

    def test_cp_como_entero(self):
        # cp puede venir como número en el JSON
        raw = '[{"city":"Berlin","cp":10115}]'
        assert get_address(raw) == "Berlin, 10115"

    def test_ciudad_ausente_usa_placeholder(self):
        raw = '[{"cp":"28001"}]'
        assert get_address(raw) == "Unknown, 28001"

    def test_cp_ausente_usa_placeholder(self):
        raw = '[{"city":"Madrid"}]'
        assert get_address(raw) == "Madrid, UNK00"

    def test_ambos_ausentes_doble_placeholder(self):
        raw = '[{}]'
        assert get_address(raw) == "Unknown, UNK00"

    def test_vacio_doble_placeholder(self):
        assert get_address("") == "Unknown, UNK00"

    def test_none_doble_placeholder(self):
        assert get_address(None) == "Unknown, UNK00"

    def test_json_malformado_doble_placeholder(self):
        assert get_address("esto no es json") == "Unknown, UNK00"

    def test_ciudad_con_espacios_se_limpia(self):
        raw = '[{"city":"  Paris  ","cp":"75001"}]'
        assert get_address(raw) == "Paris, 75001"

    def test_cp_string_vacio_usa_placeholder(self):
        # cp existe en el JSON pero es string vacío
        raw = '[{"city":"Lyon","cp":""}]'
        assert get_address(raw) == "Lyon, UNK00"