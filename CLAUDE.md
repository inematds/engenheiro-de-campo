# CLAUDE.md — engenheiro-de-campo

Kit + guia do INEMA.CLUB sobre a profissão **engenheiro de campo de IA** (forward deployed engineer). Conteúdo aberto e gratuito.

## Regras do projeto

- Tudo roda local: Python só com biblioteca padrão, páginas HTML self-contained. Nada de API, modelo local ou dependência pesada.
- **Política de números:** só número com fonte oficial registrada em `fontes/` (URL + data). O único valor salarial é a faixa da vaga oficial da OpenAI em `fontes/vaga-openai.json`. Trechos da Anthropic: só os sem número. O teste `SemNumerosProibidos` (lista do que é permitido) trava isso.
- Sem crédito de terceiros: o kit não cita autores, canais ou comunidades.
- `kit/1-teste-metade/perguntas.json` é a fonte única: mudou, rode `gerar_pagina.py` (o teste confere).
- As notas do eval citadas no guia e no README (18/30, 30/30, 4/10) estão presas em `tests/test_kit.py`: mudou a automação ou os casos, atualize os três lugares.
- Guia: PT é a fonte; EN/ES são cópias traduzidas pelo `inema-traduz`. Nada técnico no guia; comandos ficam no README.
- Autor dos commits: `inematds <inematds@gmail.com>`.

## Testes

`python3 -m unittest discover -s tests -v`

## Self-learning

When I correct you, or you catch yourself making a mistake: before continuing, add the lesson as a one-line rule at the TOP of the Lessons section below, so it never happens again.

## Lessons

- (vazio)
