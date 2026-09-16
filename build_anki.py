#!/usr/bin/env python3
"""
Gera o Anki HTML de vocabulario a partir do arquivo Word "Vocabulario - Ingles.docx".

Uso:
    python build_anki.py

Sempre que o arquivo .docx for atualizado com novas palavras, basta rodar este
script novamente para regenerar o HTML com os cards atualizados.

Formato esperado da tabela no .docx (3 colunas):
    Termo | Definicao (PT) | Exemplo (EN)
"""
import json
import os
import zipfile
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCX_PATH = os.path.join(BASE_DIR, "Vocabulário - Inglês.docx")
HTML_PATH = os.path.join(BASE_DIR, "Anki - Vocabulário Inglês.html")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
TEMPLATE_PATH = os.path.join(BASE_DIR, "anki_template.html")

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


def extract_tables(docx_path):
    """Retorna uma lista de tabelas, cada uma como lista de linhas (linha = lista de celulas).

    O Word pode acabar com mais de uma tabela no mesmo documento (ex.: quando
    novas palavras sao coladas/adicionadas como uma tabela separada em vez de
    novas linhas na tabela original) - por isso lemos TODAS as tabelas do
    documento, nao so a primeira.
    """
    with zipfile.ZipFile(docx_path) as z:
        with z.open("word/document.xml") as f:
            root = ET.parse(f).getroot()

    body = root.find("w:body", NS)
    if body is None:
        raise SystemExit("Documento '%s' sem corpo valido." % docx_path)

    tables = body.findall("w:tbl", NS)
    if not tables:
        raise SystemExit("Nenhuma tabela encontrada em '%s'." % docx_path)

    all_tables = []
    for table in tables:
        rows = []
        for tr in table.findall("w:tr", NS):
            cells = []
            for tc in tr.findall("w:tc", NS):
                paragraphs = []
                for p in tc.findall(".//w:p", NS):
                    text = "".join(t.text or "" for t in p.findall(".//w:t", NS))
                    paragraphs.append(text)
                cells.append("\n".join(paragraphs).strip())
            rows.append(cells)
        all_tables.append(rows)
    return all_tables


def build_cards(all_tables):
    cards = []
    seen_terms = set()
    for rows in all_tables:
        if not rows:
            continue
        # Cada tabela pode ou nao ter sua propria linha de cabecalho
        # ("Termo | Definicao (PT) | Exemplo (EN)") - descartamos so se houver.
        data_rows = rows[1:] if rows[0][:1] and "termo" in rows[0][0].lower() else rows

        for row in data_rows:
            row = (row + ["", "", ""])[:3]
            term, definition, example = (c.strip() for c in row)
            if not term:
                continue
            key = term.lower()
            if key in seen_terms:
                continue
            seen_terms.add(key)
            cards.append({"term": term, "definition": definition, "example": example})
    return cards


def main():
    all_tables = extract_tables(DOCX_PATH)
    cards = build_cards(all_tables)
    if not cards:
        raise SystemExit("Nenhum card encontrado no documento.")

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    cards_json = json.dumps(cards, ensure_ascii=False, indent=2)
    output = template.replace("__CARDS_JSON__", cards_json)
    output = output.replace("__CARD_COUNT__", str(len(cards)))

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(output)

    # index.html eh uma copia identica, usada pelo GitHub Pages (URL limpa,
    # sem espacos/acentos no nome do arquivo).
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"OK: {len(cards)} cards gerados em '{HTML_PATH}' e '{INDEX_PATH}'")


if __name__ == "__main__":
    main()
