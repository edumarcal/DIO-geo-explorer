from __future__ import annotations

import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .services import gerar_certificado, gerar_desafio, gerar_trilha, listar_trilhas


DEFAULT_TECHNOLOGY = "python"
DEFAULT_LEVEL = "iniciante"
DEFAULT_NAME = "Estudante"


def build_dashboard_html(tecnologia: str | None = None, nivel: str | None = None, nome: str | None = None) -> str:
    tecnologias = listar_trilhas()
    selected_tecnologia = (tecnologia or DEFAULT_TECHNOLOGY).strip().lower()
    if selected_tecnologia not in tecnologias:
        selected_tecnologia = tecnologias[0]

    selected_nivel = (nivel or DEFAULT_LEVEL).strip().lower()
    selected_name = (nome or DEFAULT_NAME).strip() or DEFAULT_NAME

    trilha = gerar_trilha(selected_tecnologia)
    desafio = gerar_desafio(selected_tecnologia, selected_nivel)
    certificado = gerar_certificado(selected_name, selected_tecnologia, trilha["nome"])

    options = "\n".join(
        f'<option value="{tecnologia}" {"selected" if tecnologia == selected_tecnologia else ""}>{html.escape(tecnologia.title())}</option>'
        for tecnologia in tecnologias
    )

    nivel_options = """
        <option value="iniciante" {selected}>Iniciante</option>
        <option value="intermediario" {selected}>Intermediário</option>
        <option value="avancado" {selected}>Avançado</option>
    """.replace("{selected}", "selected" if selected_nivel == "iniciante" else "")
    nivel_options = nivel_options.replace("{selected}", "selected" if selected_nivel == "intermediario" else "")
    nivel_options = nivel_options.replace("{selected}", "selected" if selected_nivel == "avancado" else "")

    return f"""<!doctype html>
<html lang=\"pt-BR\">
<head>
  <meta charset=\"utf-8\" />
  <title>Geo Explorer</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; background: #f5f7fb; color: #1e2430; }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 32px 20px 60px; }}
    .header {{ background: linear-gradient(135deg, #1f6feb, #4f8ef7); color: white; padding: 24px; border-radius: 18px; box-shadow: 0 10px 25px rgba(31,111,235,.18); }}
    .panel-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 24px; }}
    .panel {{ background: white; border-radius: 16px; padding: 20px; box-shadow: 0 8px 20px rgba(0,0,0,.05); }}
    .label {{ font-size: 13px; text-transform: uppercase; letter-spacing: .08em; color: #5d6b82; font-weight: 700; }}
    form {{ display: grid; gap: 16px; }}
    select, input {{ width: 100%; padding: 10px 12px; border: 1px solid #d6deeb; border-radius: 10px; font-size: 15px; }}
    button {{ background: #1f6feb; color: white; border: none; border-radius: 10px; padding: 12px 18px; font-size: 15px; cursor: pointer; }}
    h2, h3 {{ margin-top: 0; }}
    ul {{ margin: 10px 0 0 18px; padding: 0; }}
    li {{ margin-bottom: 8px; }}
    .badge {{ display: inline-block; background: #eaf2ff; color: #1d61d7; padding: 6px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; margin-bottom: 12px; }}
    .muted {{ color: #58657a; }}
    .certificate {{ border-left: 5px solid #1f6feb; padding-left: 14px; }}
  </style>
</head>
<body>
  <div class=\"container\">
    <div class=\"header\">
      <h1>Geo Explorer</h1>
      <div class=\"muted\">Explore trilhas, gere desafios e crie certificados fictícios.</div>
    </div>

    <div class=\"panel-grid\">
      <section class=\"panel\">
        <div class=\"badge\">Configuração</div>
        <form method=\"GET\">
          <div>
            <div class=\"label\">Tecnologia</div>
            <select name=\"tecnologia\">
              {options}
            </select>
          </div>
          <div>
            <div class=\"label\">Nível</div>
            <select name=\"nivel\">
              <option value=\"iniciante\" {'selected' if selected_nivel == 'iniciante' else ''}>Iniciante</option>
              <option value=\"intermediario\" {'selected' if selected_nivel == 'intermediario' else ''}>Intermediário</option>
              <option value=\"avancado\" {'selected' if selected_nivel == 'avancado' else ''}>Avançado</option>
            </select>
          </div>
          <div>
            <div class=\"label\">Nome do estudante</div>
            <input name=\"nome\" value=\"{html.escape(selected_name)}\" />
          </div>
          <button type=\"submit\">Atualizar visão</button>
        </form>
      </section>

      <section class=\"panel\">
        <div class=\"badge\">Trilha</div>
        <h2>{html.escape(trilha['nome'])}</h2>
        <p><strong>Tecnologia:</strong> {html.escape(trilha['tecnologia'])}</p>
        <p><strong>Duração:</strong> {html.escape(trilha['duracao'])}</p>
        <p><strong>Nível:</strong> {html.escape(trilha['nivel'])}</p>
        <p>{html.escape(trilha['descricao'])}</p>
        <h3>Módulos</h3>
        <ul>
          {''.join(f'<li>{html.escape(item)}</li>' for item in trilha['modulos'])}
        </ul>
      </section>

      <section class=\"panel\">
        <div class=\"badge\">Desafio</div>
        <h2>{html.escape(desafio['titulo'])}</h2>
        <p><strong>Nível:</strong> {html.escape(desafio['nivel'])}</p>
        <p>{html.escape(desafio['descricao'])}</p>
        <h3>Requisitos</h3>
        <ul>
          {''.join(f'<li>{html.escape(item)}</li>' for item in desafio['requisitos'])}
        </ul>
        <p><strong>Dica:</strong> {html.escape(desafio['dica'])}</p>
      </section>

      <section class=\"panel certificate\">
        <div class=\"badge\">Certificado</div>
        <h2>Certificado Geo Explorer</h2>
        <p><strong>Nome:</strong> {html.escape(certificado['nome'])}</p>
        <p><strong>Trilha:</strong> {html.escape(certificado['trilha'])}</p>
        <p><strong>Data:</strong> {html.escape(certificado['data'])}</p>
        <p><strong>Status:</strong> {html.escape(certificado['status'])}</p>
        <p>{html.escape(certificado['mensagem'])}</p>
      </section>
    </div>
  </div>
</body>
</html>
"""


class GeoExplorerHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        params = parse_qs(urlparse(self.path).query)
        tecnologia = params.get("tecnologia", [DEFAULT_TECHNOLOGY])[0]
        nivel = params.get("nivel", [DEFAULT_LEVEL])[0]
        nome = params.get("nome", [DEFAULT_NAME])[0]
        page = build_dashboard_html(tecnologia=tecnologia, nivel=nivel, nome=nome)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

    def log_message(self, format: str, *args) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), GeoExplorerHandler)
    print(f"Servidor Geo Explorer em http://{host}:{port}")
    server.serve_forever()
