from __future__ import annotations

import json
import sys
from typing import Any

from .services import (
    gerar_certificado,
    gerar_desafio,
    gerar_trilha,
    listar_trilhas,
)


class GeoExplorerMCPServer:
    """Servidor MCP em stdin/stdout para expor as ferramentas do Geo Explorer."""

    def __init__(self) -> None:
        self.tools = {
            "listar_trilhas": {
                "name": "listar_trilhas",
                "description": "Lista as tecnologias disponíveis no banco fictício do Geo Explorer.",
                "inputSchema": {"type": "object", "properties": {}, "required": []},
                "handler": self.listar_trilhas,
            },
            "obter_trilha": {
                "name": "obter_trilha",
                "description": "Retorna a trilha detalhada para a tecnologia informada.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"tecnologia": {"type": "string", "description": "Tecnologia da trilha."}},
                    "required": ["tecnologia"],
                },
                "handler": self.obter_trilha,
            },
            "gerar_desafio": {
                "name": "gerar_desafio",
                "description": "Gera um desafio de código para uma tecnologia e nível informados.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "tecnologia": {"type": "string", "description": "Tecnologia do desafio."},
                        "nivel": {"type": "string", "description": "Nível do desafio: iniciante, intermediario ou avancado."},
                    },
                    "required": ["tecnologia", "nivel"],
                },
                "handler": self.gerar_desafio,
            },
            "gerar_certificado": {
                "name": "gerar_certificado",
                "description": "Cria um certificado fictício de conclusão da trilha.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "nome": {"type": "string", "description": "Nome da pessoa que concluiu a trilha."},
                        "tecnologia": {"type": "string", "description": "Tecnologia da trilha concluída."},
                        "trilha": {"type": "string", "description": "Nome da trilha concluída."},
                    },
                    "required": ["nome", "tecnologia", "trilha"],
                },
                "handler": self.gerar_certificado,
            },
        }

    def listar_trilhas(self, **_: Any) -> list[str]:
        return listar_trilhas()

    def obter_trilha(self, tecnologia: str, **_: Any) -> dict[str, Any]:
        return gerar_trilha(tecnologia)

    def gerar_desafio(self, tecnologia: str, nivel: str, **_: Any) -> dict[str, Any]:
        return gerar_desafio(tecnologia, nivel)

    def gerar_certificado(self, nome: str, tecnologia: str, trilha: str, **_: Any) -> dict[str, Any]:
        return gerar_certificado(nome, tecnologia, trilha)

    def _call_tool(self, name: str, arguments: dict[str, Any] | None) -> Any:
        tool = self.tools.get(name)
        if tool is None:
            raise ValueError(f"Ferramenta '{name}' não suportada.")
        args = arguments or {}
        return tool["handler"](**args)

    def process_message(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        if "tool" in payload and "arguments" in payload:
            result = self._call_tool(payload["tool"], payload["arguments"])
            return {"ok": True, "result": result}

        if "method" not in payload:
            raise ValueError("Mensagem inválida: método não informado.")

        method = payload["method"]
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": payload.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": "geo-explorer", "version": "0.1.0"},
                },
            }

        if method == "notifications/initialized":
            return None

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": payload.get("id"),
                "result": {
                    "tools": [
                        {
                            "name": item["name"],
                            "description": item["description"],
                            "inputSchema": item["inputSchema"],
                        }
                        for item in self.tools.values()
                    ]
                },
            }

        if method == "tools/call":
            params = payload.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})
            result = self._call_tool(name, arguments)
            return {
                "jsonrpc": "2.0",
                "id": payload.get("id"),
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
                    "structuredContent": result,
                    "isError": False,
                },
            }

        if method == "ping":
            return {"jsonrpc": "2.0", "id": payload.get("id"), "result": {}}

        raise ValueError(f"Método '{method}' não suportado.")

    def run_stdio(self) -> None:
        for raw_line in sys.stdin:
            line = raw_line.strip()
            if not line:
                continue
            payload = None
            try:
                payload = json.loads(line)
                response = self.process_message(payload)
                if response is not None:
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
            except Exception as exc:  # pragma: no cover - caminho de integração
                if isinstance(exc, json.JSONDecodeError):
                    continue
                message = {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(exc)}}
                json_id = None
                if isinstance(payload, dict):
                    json_id = payload.get("id")
                if json_id is not None:
                    message["id"] = json_id
                print(json.dumps(message, ensure_ascii=False))
                sys.stdout.flush()


if __name__ == "__main__":
    GeoExplorerMCPServer().run_stdio()
