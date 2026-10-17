from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parent / "data" / "trilhas.json"


def load_trilhas() -> dict[str, Any]:
    with DATA_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def listar_tecnologias() -> list[str]:
    return sorted(item["tecnologia"].lower() for item in load_trilhas()["trilhas"])


def get_trilha(tecnologia: str) -> dict[str, Any]:
    target = tecnologia.strip().lower()
    for item in load_trilhas()["trilhas"]:
        if item["tecnologia"].lower() == target:
            return item
    raise ValueError(f"Tecnologia '{tecnologia}' não encontrada.")
