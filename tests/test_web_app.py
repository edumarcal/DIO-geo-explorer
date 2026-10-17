from geo_explorer.web_app import build_dashboard_html


def test_dashboard_html_contains_expected_sections():
    html = build_dashboard_html("python", "iniciante", "Maria")
    assert "Geo Explorer" in html
    assert "Python para Iniciantes" in html
    assert "Calculadora de média" in html
    assert "Certificado Geo Explorer" in html
    assert "Maria" in html
