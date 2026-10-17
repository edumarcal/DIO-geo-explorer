import subprocess
import sys

from geo_explorer.services import (
    gerar_certificado,
    gerar_desafio,
    gerar_trilha,
    listar_trilhas,
)


def test_listar_trilhas_contem_python():
    tecnologias = listar_trilhas()
    assert "python" in tecnologias
    assert "javascript" in tecnologias


def test_gerar_trilha_python():
    trilha = gerar_trilha("Python")
    assert trilha["nome"] == "Python para Iniciantes"
    assert "Fundamentos de Python e variáveis" in trilha["modulos"]


def test_gerar_desafio_python_intermediario():
    desafio = gerar_desafio("Python", "intermediario")
    assert desafio["titulo"] == "Gerenciador de tarefas"
    assert "lista" in desafio["descricao"].lower()


def test_gerar_certificado_valido():
    certificado = gerar_certificado("Maria", "Python", "Python para Iniciantes")
    assert certificado["status"] == "Concluída"
    assert certificado["nome"] == "Maria"
    assert "Geo Explorer" in certificado["assinatura"]


def test_cli_trilha_command():
    result = subprocess.run(
        [sys.executable, "-m", "geo_explorer.cli", "trilha", "--tecnologia", "Python"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 0
    assert "Tecnologia: Python" in result.stdout
    assert "Python para Iniciantes" in result.stdout


def test_cli_desafio_command():
    result = subprocess.run(
        [sys.executable, "-m", "geo_explorer.cli", "desafio", "--tecnologia", "Python", "--nivel", "iniciante"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 0
    assert "Calculadora de média" in result.stdout
