from __future__ import annotations

from pathlib import Path

PATH = Path("scripts/python/verificar_artigo_integrado.py")


def remove_tuple_by_label(text: str, label: str) -> str:
    marker = repr(label) + ","
    marker_pos = text.find(marker)
    if marker_pos < 0:
        marker = f'"{label}",'
        marker_pos = text.find(marker)
    if marker_pos < 0:
        return text

    start = text.rfind("    (\n", 0, marker_pos)
    end = text.find("    ),\n", marker_pos)
    if start < 0 or end < 0:
        raise RuntimeError(f"Limites da tupla não localizados: {label}")
    return text[:start] + text[end + len("    ),\n") :]


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    for label in (
        "definição conjunta de AHP",
        "definição conjunta de TOPSIS",
        "definição conjunta de ANP",
        "padronização terminológica da matriz",
    ):
        text = remove_tuple_by_label(text, label)

    old_start = "bloco_terminologia_antigo = '''for declaracao in ("
    new_start = "bloco_terminologia_antigo = r'''for declaracao in ("
    if old_start in text:
        text = text.replace(old_start, new_start, 1)

    old_new_start = "bloco_terminologia_novo = '''for declaracao in ("
    new_new_start = "bloco_terminologia_novo = r'''for declaracao in ("
    if old_new_start in text:
        text = text.replace(old_new_start, new_new_start, 1)

    for label in (
        "definição conjunta de AHP",
        "definição conjunta de TOPSIS",
        "definição conjunta de ANP",
        "padronização terminológica da matriz",
    ):
        if label in text:
            raise RuntimeError(f"Controle redundante ainda presente: {label}")

    for required in (new_start, new_new_start, "padronização terminológica consolidada"):
        if required not in text:
            raise RuntimeError(f"Controle consolidado ausente: {required}")

    PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
