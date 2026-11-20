# Engenheiro de campo de IA: a nova profissão e o kit para se preparar

[![Engenheiro de campo: a nova profissão da IA](guia/assets/banner.jpg)](https://inematds.github.io/engenheiro-de-campo/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

**Engenheiro de campo de IA** (em inglês, *forward deployed engineer*, ou FDE) é o profissional que a empresa de IA manda para dentro do cliente: ele descobre o problema real, constrói a solução junto com a equipe, prova que funciona com um teste medido (eval) e faz as pessoas usarem. Este kit é uma formação grátis para se preparar: um teste para saber qual metade falta em você (a do construtor ou a da pessoa em quem o cliente confia), a trilha do que aprender, um cliente simulado para treinar a descoberta, o escopo de 1 página com conferidor, um eval que roda no seu computador, o roteiro do projeto-prova, o mapa das vagas e o treino da entrevista. Tudo roda local, sem API e sem instalar modelo.

## 📖 Guia de uso

Guia completo (o que é, o potencial, a formação passo a passo): **https://inematds.github.io/engenheiro-de-campo/guia/**

Teste no navegador, 3 minutos: **https://inematds.github.io/engenheiro-de-campo/kit/1-teste-metade/teste-metade.html**

## Comece pedindo para a sua IA

Abra o Claude Code ou o Codex numa pasta nova e cole:

```
Leia o kit "engenheiro de campo de IA" em https://github.com/inematds/engenheiro-de-campo (o README explica tudo).
Depois me ajude a me preparar para essa profissão, em português simples:
1. Faça comigo o teste "qual metade você tem", uma pergunta por vez, e me diga o resultado.
2. Monte um plano de 4 semanas focado na minha metade mais fraca, usando os passos do kit.
3. Comece pelo primeiro exercício do plano comigo.
Não instale nem mude nada no meu computador sem me mostrar antes e esperar eu dizer sim.
```

## Por que essa vaga existe

As empresas compram IA mais rápido do que conseguem fazê-la funcionar nos sistemas bagunçados delas. Em vez de entregar uma senha e desejar boa sorte, a empresa de IA manda um engenheiro sentar ao lado do cliente: ele não vende hora de trabalho nem software, entrega um resultado. O raro é quem tem **as duas metades**: o construtor e a pessoa em quem o cliente confia.

## Baseado em vagas oficiais (conferidas em 20/11/2026)

- **OpenAI**, vaga *Forward Deployed Engineer (FDE) - SF*: faixa publicada "$185K – $300K • Offers Equity". [Vaga](https://jobs.ashbyhq.com/openai/967f94aa-1706-4dba-ac89-bfbc2c38b688) · registro em [`fontes/vaga-openai.json`](fontes/vaga-openai.json).
- **Anthropic**, vagas *Forward Deployed Engineer* e *Staff Forward Deployed Engineer*: entregar "MCP servers, sub-agents, and agent skills", "identify and codify repeatable deployment patterns", chegar "with only a business problem and leave with a defensible technical strategy". [Vaga FDE](https://job-boards.greenhouse.io/anthropic/jobs/5391021008) · [vaga Staff](https://job-boards.greenhouse.io/anthropic/jobs/5449229008) · registro em [`fontes/vagas-anthropic.json`](fontes/vagas-anthropic.json).
- **Mercado, além da OpenAI:** as vagas oficiais de engenheiro de campo publicam de US$ 135 mil (Palantir) a US$ 415 mil (Cohere) por ano, com Anthropic, Harvey, Ramp, Databricks e Scale AI no meio. Há vagas abertas com o Brasil no endereço: Decagon (remota, pede português, espanhol e inglês), Cognition (presencial em São Paulo) e Databricks (FDE Brazil). A Salesforce diz, no próprio blog, que vai montar um time de 1.000 engenheiros de campo. Os 23 itens, com o texto exato, o link e o tipo de cada fonte (vaga oficial, blog oficial ou imprensa), estão em [`fontes/mercado.json`](fontes/mercado.json).

Vagas mudam: confira sempre a página oficial.

---

## O processo, do início ao fim

Quem faz: 🧠 sessão (você, com a IA ao lado) · ⚙️ script do kit · 🤖 `claude -p` (ou Codex) pela sua assinatura.

| # | Passo | Comando / arquivo | Quem |
|---|---|---|---|
| 1 | Descobrir qual metade você tem | `python3 kit/1-teste-metade/teste_metade.py` (ou a página `teste-metade.html`) | ⚙️ |
| 2 | Seguir a trilha, uma prática por item | [`kit/2-trilha/TRILHA.md`](kit/2-trilha/TRILHA.md) | 🧠 |
| 3 | Treinar a descoberta com o cliente simulado (4 setores) | colar um bloco de [`kit/3-cliente-simulado/PROMPTS.md`](kit/3-cliente-simulado/PROMPTS.md) na IA; conferir com o [checklist](kit/3-cliente-simulado/CHECKLIST-DESCOBERTA.md) | 🤖 + 🧠 |
| 4 | Escrever o escopo de 1 página e conferir | copiar [`modelo.md`](kit/4-escopo-1-pagina/modelo.md) → `python3 kit/4-escopo-1-pagina/validar_escopo.py meu-escopo.md` | 🧠 + ⚙️ |
| 5 | Rodar o eval de exemplo e depois o seu | `python3 kit/5-eval/rodar_eval.py --comparar kit/5-eval/automacao_v1.py kit/5-eval/automacao_v2.py` | ⚙️ |
| 6 | Projeto-prova com cliente real + estudo de caso | [`kit/6-projeto-prova/ROTEIRO.md`](kit/6-projeto-prova/ROTEIRO.md) + [`MODELO-ESTUDO-DE-CASO.md`](kit/6-projeto-prova/MODELO-ESTUDO-DE-CASO.md) | 🧠 |
| 7 | Procurar as vagas | [`kit/7-vagas/VAGAS.md`](kit/7-vagas/VAGAS.md) | 🧠 |
| 8 | Treinar a entrevista (caso, projeto, técnica, comportamental) | colar os prompts de [`kit/8-entrevista/ENTREVISTA.md`](kit/8-entrevista/ENTREVISTA.md) na IA | 🤖 + 🧠 |
| 9 | Entender a semana de trabalho | [`kit/9-semana/SEMANA.md`](kit/9-semana/SEMANA.md) | 🧠 |

---

## Instalação técnica

### Pré-requisitos

- Python 3.8 ou mais novo (só biblioteca padrão; nada para instalar com `pip`).
- Git, para baixar o kit. Nenhuma chave de API, nenhum modelo local.

```bash
git clone https://github.com/inematds/engenheiro-de-campo.git
cd engenheiro-de-campo
```

### Comandos

```bash
# 1. teste "qual metade você tem" (interativo, ou com o número da opção escolhida em cada uma das 12 perguntas)
python3 kit/1-teste-metade/teste_metade.py
python3 kit/1-teste-metade/teste_metade.py --respostas 3,3,2,3,2,3,1,1,2,0,1,2
#    regerar a página depois de mudar perguntas.json
python3 kit/1-teste-metade/gerar_pagina.py

# 4. conferir um escopo (0 = aprovado, 1 = reprovado)
python3 kit/4-escopo-1-pagina/validar_escopo.py kit/4-escopo-1-pagina/exemplo-preenchido.md
python3 kit/4-escopo-1-pagina/validar_escopo.py kit/4-escopo-1-pagina/exemplo-reprovado.md

# 5. eval: uma versão, comparar duas, casos novos, nota mínima
python3 kit/5-eval/rodar_eval.py kit/5-eval/automacao_v1.py
python3 kit/5-eval/rodar_eval.py --comparar kit/5-eval/automacao_v1.py kit/5-eval/automacao_v2.py
python3 kit/5-eval/rodar_eval.py --casos kit/5-eval/casos-novos.json kit/5-eval/automacao_v2.py
python3 kit/5-eval/rodar_eval.py kit/5-eval/automacao_v2.py --minimo 0.9
```

### O eval de exemplo, medido em 20/11/2026

| | `casos.json` (30) | `casos-novos.json` (10) |
|---|---|---|
| `automacao_v1.py` (palavra-chave simples) | 18/30 | 4/10 |
| `automacao_v2.py` (corrigida pelas falhas da v1) | 30/30 · 12 consertados, 0 quebrados | 4/10 |

A v2 decorou os casos que usamos para corrigi-la; nos casos novos ficou igual à v1. É a lição do kit: eval sério tem sempre um conjunto separado. Para avaliar o seu agente, copie [`automacao_meu_agente.py`](kit/5-eval/automacao_meu_agente.py) e leia [`kit/5-eval/LEIA.md`](kit/5-eval/LEIA.md).

O conferidor de escopo aceita os títulos das seções em português, inglês e espanhol (`Problema`/`Problem`, `O número`/`The number`/`El número`, `Pronto quando`/`Done when`/`Listo cuando`, `Fora do escopo`/`Out of scope`/`Fuera del alcance`).

### Arquivos

```
kit/1-teste-metade/     perguntas.json (fonte única), teste_metade.py, gerar_pagina.py, teste-metade.html
kit/2-trilha/           TRILHA.md
kit/3-cliente-simulado/ PROMPTS.md (4 setores), CHECKLIST-DESCOBERTA.md
kit/4-escopo-1-pagina/  modelo.md, exemplo-preenchido.md, exemplo-reprovado.md, validar_escopo.py
kit/5-eval/             casos.json, casos-novos.json, automacao_v1.py, automacao_v2.py, rodar_eval.py, automacao_meu_agente.py, LEIA.md
kit/6-projeto-prova/    ROTEIRO.md, MODELO-ESTUDO-DE-CASO.md
kit/7-vagas/            VAGAS.md
kit/8-entrevista/       ENTREVISTA.md
kit/9-semana/           SEMANA.md
fontes/                 vagas oficiais conferidas (URL, texto literal, data)
guia/                   página PT + en/ + es/
tests/                  testes automáticos
```

### Testes

```bash
python3 -m unittest discover -s tests -v
```

31 testes cobrem: o teste-metade (12 perguntas, 6 por metade, os 3 resultados alcançáveis, empate dentro da margem, respostas inválidas, a página com as mesmas perguntas do JSON), o conferidor de escopo (exemplo aprovado, exemplo e modelo reprovados, sem número, um número só, sem aspas, seção faltando, títulos em EN/ES, códigos de saída) e o eval (casos bem formados, as notas medidas 18/30, 30/30 e 4/10, a comparação 12 consertados e 0 quebrados, automação que explode conta como falha, código de saída do `--minimo`, o modelo do agente não roda sem configurar) e a política de números: só valores que estão no texto de uma vaga ou blog oficial registrado em `fontes/` (a faixa da OpenAI igual à registrada), a única porcentagem de imprensa sempre com a fonte (Fortune, com dados da Lightcast) ao lado, e os links da seção de mercado iguais nos três idiomas e todos registrados em `fontes/`.

## Licença

MIT. Conteúdo aberto e gratuito do [INEMA.CLUB](https://inema.club).
