"""Checa integridade cruzada do painel antes de publicar na main.

Não consulta API, não cria métricas e não altera arquivos.
"""
from __future__ import annotations

import json
import os
import re
from datetime import date, timedelta
from pathlib import Path
from xml.etree import ElementTree


def verify(readme: str, feed: dict, daily_svg: str, portfolio_svg: str, report: str) -> None:
    """Falha se calendário, SVG e métricas invisíveis divergem."""
    if feed.get("source") != "github-contributions-graphql":
        raise ValueError("Fonte de contribuições não é a API oficial")
    observed = feed.get("last_14_days")
    if not isinstance(observed, list) or len(observed) != 14:
        raise ValueError("O feed precisa conter exatamente 14 dias")

    days, counts = [], []
    for item in observed:
        if not isinstance(item, dict):
            raise ValueError("Dia inválido no feed")
        day = date.fromisoformat(item["date"])
        count = item["contributions"]
        if type(count) is not int or count < 0:
            raise ValueError("Contribuição inválida no feed")
        days.append(day)
        counts.append(count)
    if any(right - left != timedelta(days=1) for left, right in zip(days, days[1:])):
        raise ValueError("Calendário tem dias duplicados ou ausentes")
    if feed.get("calendar_date") != days[-1].isoformat():
        raise ValueError("Data do calendário diverge do último dia")

    expected = (counts[-1], counts[-2], sum(counts[-7:]), feed.get("last_12_months"))
    if type(expected[3]) is not int or expected[3] < 0:
        raise ValueError("Total anual inválido")
    if any(feed.get(key) != count for key, count in zip(
        ("today", "yesterday", "last_7_days"), expected[:3]
    )):
        raise ValueError("Indicadores do JSON não correspondem aos dias")

    strong = "".join(f"<strong>{number:,}</strong>".replace(",", ".") for number in expected)
    if f"<!-- CONTRIBUTIONS:METRICS {strong} -->" not in readme:
        raise ValueError("README contém métricas diferentes do JSON")

    root = ElementTree.fromstring(daily_svg)
    bars = [(node.get("data-date"), int(node.get("data-count")))
            for node in root.iter()
            if node.get("data-date") is not None and node.get("data-count") is not None]
    if bars != [(day.isoformat(), count) for day, count in zip(days, counts)]:
        raise ValueError("Barras do SVG não correspondem ao JSON")
    if "assets/contribuicoes-diarias.svg" not in readme:
        raise ValueError("README não aponta para o SVG de contribuições")

    ElementTree.fromstring(portfolio_svg)
    if "assets/portfolio-andamento.svg" not in readme:
        raise ValueError("README não aponta para o SVG do portfólio")
    if not re.search(r"<!-- PORTFOLIO-SNAPSHOT:v[34]:[^>]+ -->", report):
        raise ValueError("Relatório do portfólio não tem referência de auditoria")
    if not re.search(r"\*\*Projetos catalogados:\*\* \d+", report):
        raise ValueError("Relatório do portfólio não contém inventário")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    feed = json.loads((root / "assets/contribuicoes-diarias.json").read_text(encoding="utf-8"))
    svg = (root / "assets/contribuicoes-diarias.svg").read_text(encoding="utf-8")
    portfolio = (root / "assets/portfolio-andamento.svg").read_text(encoding="utf-8")
    report = (root / "docs/ANDAMENTO_DOS_PROJETOS.md").read_text(encoding="utf-8")
    verify(readme, feed, svg, portfolio, report)

    message = (
        f"Integridade verificada: dia {feed['calendar_date']}, "
        f"{feed['today']} hoje, {feed['last_7_days']} em 7 dias, "
        f"{feed['last_12_months']} no calendário. "
        "SVG, JSON e README consistentes."
    )
    print(message)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as output:
            output.write("### Painéis do perfil — verificação\n\n")
            output.write(message + "\n\n")
            output.write("O agendamento GitHub é best-effort; sucesso não significa consulta exata de 5 em 5 minutos.\n")


if __name__ == "__main__":
    main()
