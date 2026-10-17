from __future__ import annotations

import argparse
import sys

from .services import (
    formatar_certificado,
    formatar_desafio,
    formatar_trilha,
    gerar_certificado,
    gerar_desafio,
    gerar_trilha,
    listar_trilhas,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Geo Explorer - trilhas, desafios e certificados.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    listar_parser = subparsers.add_parser("listar", help="Lista as tecnologias disponíveis.")
    listar_parser.set_defaults(func=listar_command)

    trilha_parser = subparsers.add_parser("trilha", help="Mostra a trilha de estudo por tecnologia.")
    trilha_parser.add_argument("--tecnologia", required=True, help="Tecnologia da trilha desejada.")
    trilha_parser.set_defaults(func=trilha_command)

    desafio_parser = subparsers.add_parser("desafio", help="Gera um desafio para uma tecnologia e nível.")
    desafio_parser.add_argument("--tecnologia", required=True, help="Tecnologia do desafio.")
    desafio_parser.add_argument("--nivel", required=True, help="Nível do desafio: iniciante, intermediario ou avancado.")
    desafio_parser.set_defaults(func=desafio_command)

    certificado_parser = subparsers.add_parser("certificado", help="Gera um certificado fictício de conclusão.")
    certificado_parser.add_argument("--nome", required=True, help="Nome da pessoa que concluiu a trilha.")
    certificado_parser.add_argument("--tecnologia", required=True, help="Tecnologia da trilha concluída.")
    certificado_parser.add_argument("--trilha", required=True, help="Nome da trilha concluída.")
    certificado_parser.set_defaults(func=certificado_command)

    return parser


def listar_command(args) -> int:
    tecnologias = listar_trilhas()
    print("Tecnologias disponíveis:")
    for tecnologia in tecnologias:
        print(f"- {tecnologia.title()}")
    return 0


def trilha_command(args) -> int:
    trilha = gerar_trilha(args.tecnologia)
    print(formatar_trilha(trilha))
    return 0


def desafio_command(args) -> int:
    desafio = gerar_desafio(args.tecnologia, args.nivel)
    print(formatar_desafio(desafio))
    return 0


def certificado_command(args) -> int:
    certificado = gerar_certificado(args.nome, args.tecnologia, args.trilha)
    print(formatar_certificado(certificado))
    return 0


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return args.func(args)
    except ValueError as exc:
        parser.exit(status=1, message=f"Erro: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
