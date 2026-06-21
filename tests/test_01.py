from src.transformations import normalize_company_name

def test_elimina_puntos():
    assert normalize_company_name("Fresh Fruits c.o") == "fresh fruits co"

def test_dos_variantes_dan_mismo_resultado():
    assert normalize_company_name("Fresh Fruits Co") == normalize_company_name("Fresh Fruits c.o")

def test_nombre_vacio():
    assert normalize_company_name("") == ""

def test_none_devuelve_vacio():
    assert normalize_company_name(None) == ""