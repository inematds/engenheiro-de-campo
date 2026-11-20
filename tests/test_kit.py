"""Testes do kit engenheiro-de-campo. Rodar da raiz do repo:
    python3 -m unittest discover -s tests -v
Só biblioteca padrão.
"""
import importlib.util
import io
import itertools
import json
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
KIT = RAIZ / "kit"


def carregar(caminho, nome):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tm = carregar(KIT / "1-teste-metade" / "teste_metade.py", "teste_metade")
ve = carregar(KIT / "4-escopo-1-pagina" / "validar_escopo.py", "validar_escopo")
ev = carregar(KIT / "5-eval" / "rodar_eval.py", "rodar_eval")


class TesteMetade(unittest.TestCase):
    def setUp(self):
        self.dados = tm.carregar()
        self.ordem = [p["metade"] for p in self.dados["perguntas"]]

    def respostas(self, construtor, confianca):
        return [construtor if m == "construtor" else confianca for m in self.ordem]

    def test_doze_perguntas_seis_por_metade_quatro_opcoes(self):
        self.assertEqual(len(self.dados["perguntas"]), 12)
        self.assertEqual(self.ordem.count("construtor"), 6)
        self.assertEqual(self.ordem.count("confianca"), 6)
        for p in self.dados["perguntas"]:
            self.assertEqual(len(p["opcoes"]), 4, p["id"])

    def test_construtor_fraco(self):
        r = tm.pontuar(self.dados, self.respostas(0, 3))
        self.assertEqual(r["pontos"], {"construtor": 0, "confianca": 18})
        self.assertEqual(r["mais_fraca"], "construtor")
        self.assertIn("CONSTRUTOR", r["plano"]["titulo"])

    def test_confianca_fraca(self):
        r = tm.pontuar(self.dados, self.respostas(3, 1))
        self.assertEqual(r["mais_fraca"], "confianca")

    def test_empate_dentro_da_margem(self):
        r = tm.pontuar(self.dados, self.respostas(2, 2))
        self.assertEqual(r["mais_fraca"], "empate")
        resp = self.respostas(2, 2)
        resp[self.ordem.index("construtor")] = 3  # diferença de 1 ponto ainda é empate
        self.assertEqual(tm.pontuar(self.dados, resp)["mais_fraca"], "empate")
        resp[self.ordem.index("construtor") + 1] = 3  # diferença de 2 já decide
        self.assertEqual(tm.pontuar(self.dados, resp)["mais_fraca"], "confianca")

    def test_todos_os_resultados_sao_alcancaveis(self):
        vistos = set()
        for c, p in itertools.product(range(19), repeat=2):
            resp = []
            restc, restp = c, p
            for m in self.ordem:
                if m == "construtor":
                    v = min(3, restc); restc -= v
                else:
                    v = min(3, restp); restp -= v
                resp.append(v)
            vistos.add(tm.pontuar(self.dados, resp)["mais_fraca"])
        self.assertEqual(vistos, set(self.dados["planos"]))

    def test_respostas_invalidas(self):
        with self.assertRaises(ValueError):
            tm.pontuar(self.dados, [1, 2])
        with self.assertRaises(ValueError):
            tm.pontuar(self.dados, [4] * 12)

    def test_cli_json(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cod = tm.main(["--respostas", ",".join(map(str, self.respostas(1, 3))), "--json"])
        self.assertEqual(cod, 0)
        self.assertEqual(json.loads(buf.getvalue())["mais_fraca"], "construtor")

    def test_pagina_usa_as_mesmas_perguntas(self):
        html = (KIT / "1-teste-metade" / "teste-metade.html").read_text(encoding="utf-8")
        m = re.search(r"const DADOS = (\{.*?\});\n", html, re.S)
        self.assertIsNotNone(m, "rode gerar_pagina.py")
        self.assertEqual(json.loads(m.group(1)), self.dados,
                         "teste-metade.html desatualizado: rode python3 kit/1-teste-metade/gerar_pagina.py")


class Escopo(unittest.TestCase):
    PASTA = KIT / "4-escopo-1-pagina"

    def test_exemplo_preenchido_passa(self):
        self.assertEqual(ve.validar((self.PASTA / "exemplo-preenchido.md").read_text(encoding="utf-8")), [])

    def test_exemplo_reprovado_e_modelo_vazio_falham(self):
        self.assertTrue(ve.validar((self.PASTA / "exemplo-reprovado.md").read_text(encoding="utf-8")))
        self.assertTrue(ve.validar((self.PASTA / "modelo.md").read_text(encoding="utf-8")))

    def base(self, numero="De 4 horas por dia para 1 hora por dia."):
        return ("## Problema (nas palavras do cliente)\n\"Perco a manhã separando e-mail.\"\n\n"
                f"## O número\n{numero}\n\n## Pronto quando\n- acerta 27 de 30 casos\n\n"
                "## Fora do escopo\n- WhatsApp\n")

    def test_sem_numero_reprova(self):
        erros = ve.validar(self.base("Melhorar muito o atendimento."))
        self.assertTrue(any("sem número" in e for e in erros), erros)

    def test_um_numero_so_reprova(self):
        erros = ve.validar(self.base("Chegar a 1 hora por dia."))
        self.assertTrue(any("partida e de chegada" in e for e in erros), erros)

    def test_escopo_minimo_valido(self):
        self.assertEqual(ve.validar(self.base()), [])

    def test_sem_aspas_reprova(self):
        erros = ve.validar(self.base().replace('"Perco a manhã separando e-mail."', "Perde tempo."))
        self.assertTrue(any("aspas" in e for e in erros), erros)

    def test_falta_secao(self):
        texto = self.base().split("## Fora do escopo")[0]
        self.assertTrue(any("Fora do escopo" in e for e in ve.validar(texto)))

    def test_titulos_em_ingles_e_espanhol(self):
        en = ("## Problem (in the client's words)\n\"We lose the morning sorting e-mail.\"\n\n"
              "## The number\nFrom 4 hours a day to 1 hour a day.\n\n## Done when\n- 27 of 30 cases\n\n"
              "## Out of scope\n- WhatsApp\n")
        es = ("## Problema (en palabras del cliente)\n\"Perdemos la mañana.\"\n\n"
              "## El número\nDe 4 horas al día a 1 hora al día.\n\n## Listo cuando\n- 27 de 30 casos\n\n"
              "## Fuera del alcance\n- WhatsApp\n")
        self.assertEqual(ve.validar(en), [])
        self.assertEqual(ve.validar(es), [])

    def test_cli_codigos_de_saida(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(self.base("sem meta"))
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(ve.main([f.name]), 1)
            self.assertEqual(ve.main([str(self.PASTA / "exemplo-preenchido.md")]), 0)
        self.assertEqual(ve.main(["/nao/existe.md"]), 2)


class Eval(unittest.TestCase):
    PASTA = KIT / "5-eval"

    def setUp(self):
        self.casos = ev.carregar_casos()
        self.novos = ev.carregar_casos(self.PASTA / "casos-novos.json")
        self.v1 = ev.carregar_automacao(self.PASTA / "automacao_v1.py")
        self.v2 = ev.carregar_automacao(self.PASTA / "automacao_v2.py")

    def test_casos_bem_formados(self):
        for dados in (self.casos, self.novos):
            ids = [c["id"] for c in dados["casos"]]
            self.assertEqual(len(ids), len(set(ids)))
            for c in dados["casos"]:
                self.assertIn(c["esperado"], dados["categorias"])
        self.assertEqual(len(self.casos["casos"]), 30)
        self.assertFalse({c["id"] for c in self.casos["casos"]} & {c["id"] for c in self.novos["casos"]})

    def test_notas_medidas_v1_e_v2(self):
        # números que o guia e o README citam: se mudar aqui, mude lá
        self.assertEqual(ev.avaliar(self.v1, self.casos)["acertos"], 18)
        self.assertEqual(ev.avaliar(self.v2, self.casos)["acertos"], 30)
        self.assertEqual(ev.avaliar(self.v2, self.novos)["acertos"], 4)

    def test_comparacao_v1_v2(self):
        c = ev.comparar(ev.avaliar(self.v1, self.casos), ev.avaliar(self.v2, self.casos))
        self.assertEqual(len(c["consertou"]), 12)
        self.assertEqual(c["quebrou"], [])

    def test_falhas_trazem_esperado_e_obtido(self):
        f = ev.avaliar(self.v1, self.casos)["falhas"]
        self.assertTrue(all({"entrada", "esperado", "obtido"} <= set(x) for x in f))

    def test_automacao_que_explode_conta_como_falha(self):
        def ruim(texto):
            raise ValueError("quebrou")
        r = ev.avaliar(ruim, self.casos)
        self.assertEqual(r["acertos"], 0)
        self.assertTrue(r["falhas"][0]["obtido"].startswith("ERRO"))

    def test_automacao_sem_classificar_e_erro(self):
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write("x = 1\n")
        with self.assertRaises(AttributeError):
            ev.carregar_automacao(f.name)

    def test_cli_minimo(self):
        cmd = [sys.executable, str(self.PASTA / "rodar_eval.py")]
        ok = subprocess.run(cmd + [str(self.PASTA / "automacao_v2.py"), "--minimo", "0.9"], capture_output=True)
        ruim = subprocess.run(cmd + [str(self.PASTA / "automacao_v1.py"), "--minimo", "0.9"], capture_output=True)
        self.assertEqual(ok.returncode, 0)
        self.assertEqual(ruim.returncode, 1)
        js = subprocess.run(cmd + ["--comparar", str(self.PASTA / "automacao_v1.py"),
                                   str(self.PASTA / "automacao_v2.py"), "--json"], capture_output=True, text=True)
        self.assertEqual(json.loads(js.stdout)["v1"]["acertos"], 18)

    def test_modelo_do_agente_nao_roda_sem_configurar(self):
        ag = ev.carregar_automacao(self.PASTA / "automacao_meu_agente.py")
        r = ev.avaliar(ag, self.casos)
        self.assertEqual(r["acertos"], 0)
        self.assertIn("RuntimeError", r["falhas"][0]["obtido"])


class SemNumerosProibidos(unittest.TestCase):
    """Política do kit: só número com fonte oficial registrada em fontes/ (lista do que é permitido)."""

    DINHEIRO_OK = {"$185K", "$300K", "US$ 185", "US$ 300"}   # fontes/vaga-openai.json
    PORCENTO_OK = {"90%"}                                     # nota mínima de exemplo do runner (LEIA.md)

    def textos(self):
        for p in RAIZ.rglob("*"):
            if p.suffix in {".md", ".html"} and ".git" not in p.parts and "tests" not in p.parts:
                txt = p.read_text(encoding="utf-8", errors="ignore")
                # CSS/JS e atributos style têm % de layout, não dado
                txt = re.sub(r"<style.*?</style>|<script.*?</script>|style=\"[^\"]*\"", "", txt, flags=re.S)
                yield p, txt

    def test_dinheiro_so_da_vaga_oficial(self):
        for arq, txt in self.textos():
            for m in re.findall(r"US\$ ?\d+|\$\d+K?", txt):
                self.assertIn(m, self.DINHEIRO_OK, f"{arq.relative_to(RAIZ)}: valor sem fonte {m}")

    def test_sem_porcentagem_em_texto(self):
        for arq, txt in self.textos():
            for m in re.findall(r"\d+(?:[.,]\d+)?\s?%", txt):
                self.assertIn(m, self.PORCENTO_OK, f"{arq.relative_to(RAIZ)}: porcentagem sem fonte {m}")

    def test_faixa_bate_com_a_fonte(self):
        fonte = json.loads((RAIZ / "fontes" / "vaga-openai.json").read_text(encoding="utf-8"))
        self.assertTrue(fonte["conferido"])
        guia = (RAIZ / "guia" / "index.html").read_text(encoding="utf-8")
        self.assertIn(fonte["faixa_salarial_texto_literal"], guia)


if __name__ == "__main__":
    unittest.main()
