import pytest
from src.transformations import normalize_company_name


class TestNormalizeCompanyName:

    def test_elimina_puntos(self):
        assert normalize_company_name("Fresh Fruits c.o") == "fresh fruits co"

    def test_elimina_mayusculas(self):
        assert normalize_company_name("ACME CORP") == "acme corp"

    def test_elimina_caracteres_especiales(self):
        assert normalize_company_name("Acme, Co.") == "acme co"

    def test_trim_espacios(self):
        assert normalize_company_name("  Acme Corp  ") == "acme corp"

    def test_string_vacio(self):
        assert normalize_company_name("") == ""

    def test_none_devuelve_vacio(self):
        assert normalize_company_name(None) == ""

    def test_fresh_fruits_variantes_dan_mismo_resultado(self):
        """Las dos variantes del nombre deben consolidarse en la misma clave."""
        v1 = normalize_company_name("Fresh Fruits Co")
        v2 = normalize_company_name("Fresh Fruits c.o")
        assert v1 == v2