# Crawler de Bibliografia em PDF

Busca e baixa automaticamente livros em PDF a partir de uma lista de referências bibliográficas usando Playwright + Bing.

## Funcionalidades

- Busca no Bing com stealth anti-bot (playwright-stealth)
- Validação de PDFs: descarta arquivos com menos de 50 páginas
- Tenta múltiplos links por livro até encontrar um válido
- Fallback de query: busca com prefixo `livro` e depois `pdf`
- Retry automático dos livros que falharam
- Pula livros já baixados com sucesso
- Relatório final de sucessos e falhas

## Requisitos

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)

## Instalação

```bash
uv sync
uv run playwright install chromium
```

## Uso

Edite a lista `LISTA_LIVROS` em `main.py` e execute:

```bash
uv run python main.py
```

Os PDFs são salvos na pasta `bibliografia_pdf/`.
