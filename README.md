# Vocabulário Inglês — Anki Flashcards

Flashcards estilo Anki para estudar vocabulário de inglês, gerados a partir de
uma tabela do Word (`Vocabulário - Inglês.docx`).

**Estudar online:** https://SEU-USUARIO.github.io/NOME-DO-REPO/

## Como funciona

- `Vocabulário - Inglês.docx` — fonte dos dados (tabela: Termo | Definição (PT) | Exemplo (EN)). Atualizada semanalmente com novas palavras.
- `build_anki.py` — lê o `.docx` e gera os arquivos HTML.
- `anki_template.html` — template/lógica do app de flashcards.
- `index.html` / `Anki - Vocabulário Inglês.html` — arquivo final, pronto para abrir no navegador (o `index.html` é o que o GitHub Pages serve).

## Atualizar o vocabulário

1. Edite a tabela em `Vocabulário - Inglês.docx` (adicione novas linhas: Termo, Definição, Exemplo).
2. Rode:

   ```bash
   python build_anki.py
   ```

3. Commit e push das mudanças (inclui `index.html` atualizado, que já fica disponível no link do GitHub Pages).

## Uso do app

- Clique no card (ou pressione `Espaço`) para virar e ver a definição/exemplo.
- `←` `→` navegam entre os cards.
- Após virar: `1` marca "preciso revisar", `2` marca "já sei" (progresso salvo no navegador).
- Filtro "Só revisar" mostra apenas as palavras marcadas para revisão.
