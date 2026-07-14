from __future__ import annotations

from pathlib import Path

PATH = Path("scripts/python/verificar_artigo_integrado.py")


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    redundant = '''    (
        '"matriz analítica conceitual informada pela síntese da literatura",',
        '"Matriz de indicadores e fluxo para parametrização multicritério",',
        "padronização terminológica da matriz",
    ),
'''
    if redundant in text:
        text = text.replace(redundant, "", 1)

    old_start = "bloco_terminologia_antigo = '''for declaracao in ("
    new_start = "bloco_terminologia_antigo = r'''for declaracao in ("
    if old_start in text:
        text = text.replace(old_start, new_start, 1)

    old_new_start = "bloco_terminologia_novo = '''for declaracao in ("
    new_new_start = "bloco_terminologia_novo = r'''for declaracao in ("
    if old_new_start in text:
        text = text.replace(old_new_start, new_new_start, 1)

    if "padronização terminológica da matriz" in text:
        raise RuntimeError("Substituição redundante da matriz ainda presente.")
    for required in (new_start, new_new_start):
        if required not in text:
            raise RuntimeError(f"Bloco bruto ausente: {required}")

    PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
