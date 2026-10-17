from __future__ import annotations

from datetime import datetime
from typing import Any

from .data_loader import get_trilha, listar_tecnologias


def listar_trilhas() -> list[str]:
    return listar_tecnologias()


def obter_trilha(tecnologia: str) -> dict[str, Any]:
    return get_trilha(tecnologia)


def gerar_trilha(tecnologia: str) -> dict[str, Any]:
    trilha = get_trilha(tecnologia)
    return {
        "tecnologia": trilha["tecnologia"],
        "nome": trilha["nome"],
        "descricao": trilha["descricao"],
        "duracao": trilha["duracao"],
        "nivel": trilha["nivel"],
        "modulos": trilha["modulos"],
        "objetivos": trilha["objetivos"],
    }


def gerar_desafio(tecnologia: str, nivel: str) -> dict[str, Any]:
    trilha = get_trilha(tecnologia)
    nivel_normalizado = nivel.strip().lower()
    desafios = trilha.get("desafios", {})
    desafio = desafios.get(nivel_normalizado)

    if desafio is None:
        raise ValueError(
            f"Nível '{nivel}' não encontrado para a tecnologia '{tecnologia}'. "
            f"Níveis disponíveis: {', '.join(desafios.keys())}."
        )

    return {
        "tecnologia": trilha["tecnologia"],
        "trilha": trilha["nome"],
        "nivel": nivel_normalizado,
        "titulo": desafio["titulo"],
        "descricao": desafio["descricao"],
        "requisitos": desafio["requisitos"],
        "dica": desafio["dica"],
    }


def gerar_certificado(nome: str, tecnologia: str, trilha: str) -> dict[str, Any]:
    if not nome or not nome.strip():
        raise ValueError("O nome da pessoa é obrigatório.")

    data_emissao = datetime.now().strftime("%d/%m/%Y")
    codigo = f"GE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return {
        "codigo": codigo,
        "nome": nome.strip(),
        "tecnologia": tecnologia.strip(),
        "trilha": trilha.strip(),
        "data": data_emissao,
        "status": "Concluída",
        "mensagem": (
            f"Parabéns, {nome.strip()}! Você concluiu com sucesso a trilha de "
            f"{tecnologia.strip()} em {data_emissao}."
        ),
        "assinatura": "Diretoria de Educação Geo Explorer",
    }


def formatar_trilha(trilha: dict[str, Any]) -> str:
    linha_1 = f"Tecnologia: {trilha['tecnologia']}"
    linha_2 = f"Trilha: {trilha['nome']}"
    linha_3 = f"Duração: {trilha['duracao']} | Nível: {trilha['nivel']}"
    linha_4 = f"Descrição: {trilha['descricao']}"
    itens_modulos = "\n".join(f"  - {modulo}" for modulo in trilha["modulos"])
    itens_objetivos = "\n".join(f"  - {objetivo}" for objetivo in trilha["objetivos"])
    return "\n".join(
        [
            linha_1,
            linha_2,
            linha_3,
            linha_4,
            "\nMódulos:",
            itens_modulos,
            "\nObjetivos:",
            itens_objetivos,
        ]
    )


def formatar_desafio(desafio: dict[str, Any]) -> str:
    requisitos = "\n".join(f"  - {item}" for item in desafio["requisitos"])
    return "\n".join(
        [
            f"Desafio: {desafio['titulo']}",
            f"Tecnologia: {desafio['tecnologia']}",
            f"Trilha: {desafio['trilha']}",
            f"Nível: {desafio['nivel']}",
            f"\nDescrição: {desafio['descricao']}",
            "\nRequisitos:",
            requisitos,
            f"\nDica: {desafio['dica']}",
        ]
    )


def formatar_certificado(certificado: dict[str, Any]) -> str:
    return "\n".join(
        [
            "====================================",
            "Certificado Geo Explorer",
            "====================================",
            f"Código: {certificado['codigo']}",
            f"Nome: {certificado['nome']}",
            f"Tecnologia: {certificado['tecnologia']}",
            f"Trilha: {certificado['trilha']}",
            f"Data de conclusão: {certificado['data']}",
            f"Status: {certificado['status']}",
            "",
            certificado["mensagem"],
            "",
            f"Assinatura: {certificado['assinatura']}",
            "====================================",
        ]
    )
