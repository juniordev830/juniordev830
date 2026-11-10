"""Atualiza o painel nativo do README com o calendário oficial de contribuições.

Uso:
    GITHUB_TOKEN=... python scripts/render_daily_contributions.py

Dados vêm da GraphQL API do GitHub; nenhum valor diário é inventado.
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

LOGIN = "juniordev830"
README = Path("README.md")
CHART = Path("assets/contribuicoes-diarias.svg")
START = "<!-- CONTRIBUTIONS:START -->"
END = "<!-- CONTRIBUTIONS:END -->"
TZ = ZoneInfo("America/Fortaleza")
QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date contributionCount }
        }
      }
    }
  }
}
"""


def fetch_calendar(token: str) -> dict:
    if not token:
        raise ValueError("GITHUB_TOKEN não configurado")
    payload = json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode("utf-8")
    req = Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "juniordev830-contributions-dashboard",
        },
        method="POST",
    )
    with urlopen(req, timeout=25) as response:
        result = json.load(response)
    if result.get("errors"):
        raise ValueError("GitHub GraphQL: " + str(result["errors"])[:350])
    try:
        return result["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    except (KeyError, TypeError) as exc:
        raise ValueError("Calendário de contribuições não disponível") from exc


def metrics(calendar: dict, today: date) -> dict:
    total = calendar["totalContributions"]
    if type(total) is not int or total < 0:
        raise ValueError("Total anual inválido")

    observed: dict[date, int] = {}
    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            when = date.fromisoformat(day["date"])
            count = day["contributionCount"]
            if type(count) is not int or count < 0:
                raise ValueError("Quantidade diária inválida")
            if when in observed:
                raise ValueError("Data repetida no calendário")
            observed[when] = count

    days = [today - timedelta(days=offset) for offset in range(13, -1, -1)]
    if any(day not in observed for day in days):
        raise ValueError("GitHub não forneceu os 14 dias esperados; gráfico não atualizado")
    counts = [observed[day] for day in days]
    week_total = sum(counts[-7:])
    return {
        "days": days,
        "counts": counts,
        "today": counts[-1],
        "yesterday": counts[-2],
        "week_total": week_total,
        "year_total": total,
        "week_average": week_total / 7,
    }


def render_svg(data: dict, generated_at: datetime) -> str:
    """Render a script-free chart styled to match the interactive dashboard."""
    from html import escape

    counts, days = data["counts"], data["days"]
    maximum = max(100, *counts)
    step = 10 ** (len(str(maximum)) - 1)
    ceiling = ((maximum + step - 1) // step) * step
    left, right, top, bottom = 66, 908, 102, 300
    height = bottom - top
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="940" height="390" viewBox="0 0 940 390" role="img" aria-labelledby="title desc">',
        '<title id="title">Contribuições — últimos 14 dias</title>',
        '<desc id="desc">Barras com contagens reais do GitHub. A linha pontilhada marca a meta de 100 contribuições por dia.</desc>',
        '<defs><linearGradient id="blue" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#4d95ff"/><stop offset="1" stop-color="#275cc1"/></linearGradient><linearGradient id="teal" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#42d7bc"/><stop offset="1" stop-color="#209780"/></linearGradient></defs>',
        '<rect x="1" y="1" width="938" height="388" rx="18" fill="#0f192b" stroke="#25344c"/>',
        '<g font-family="Arial, Helvetica, sans-serif">',
        '<text x="28" y="36" fill="#edf2fa" font-size="19" font-weight="700">Ritmo de contribuições</text>',
        f'<text x="28" y="59" fill="#91a1ba" font-size="12">Últimos 14 dias · {days[0]:%d/%m} a {days[-1]:%d/%m/%Y}</text>',
        '<rect x="752" y="23" width="160" height="29" rx="14" fill="#132d30" stroke="#20574c"/>',
        '<circle cx="769" cy="37" r="3" fill="#40d7b1"/><text x="782" y="41" fill="#71dfc5" font-size="11">Dados reais do GitHub</text>',
        '<rect x="28" y="78" width="7" height="7" rx="2" fill="#4d95ff"/><text x="41" y="85" fill="#91a1ba" font-size="11">Contribuições</text>',
        '<line x1="145" x2="162" y1="82" y2="82" stroke="#e6b64c" stroke-dasharray="4 3"/><text x="168" y="85" fill="#91a1ba" font-size="11">Meta diária: 100</text>',
    ]
    for fraction in (0, .25, .5, .75, 1):
        y = bottom - fraction * height
        parts.append(f'<line x1="{left}" x2="{right}" y1="{y:.2f}" y2="{y:.2f}" stroke="#2a3850" stroke-dasharray="3 5" opacity=".7"/>')
        parts.append(f'<text x="52" y="{y+4:.2f}" text-anchor="end" fill="#7e90ab" font-size="11">{ceiling*fraction:g}</text>')
    goal_y = bottom - 100 / ceiling * height
    parts.append(f'<line x1="{left}" x2="{right}" y1="{goal_y:.2f}" y2="{goal_y:.2f}" stroke="#e6b64c" stroke-dasharray="5 5" opacity=".8"/>')
    slot = (right - left) / len(counts)
    for i, (day, count) in enumerate(zip(days, counts)):
        x = left + slot * i + slot / 2
        bar_height = count / ceiling * height
        y = bottom - bar_height
        fill = 'teal' if i == len(counts) - 1 else 'blue'
        parts.append(f'<g data-date="{day.isoformat()}" data-count="{count}"><title>{day:%d/%m/%Y}: {count} contribuições</title>')
        if count:
            parts.append(f'<rect x="{x-17:.2f}" y="{y:.2f}" width="34" height="{bar_height:.2f}" rx="4" fill="url(#{fill})"/>')
        parts.append(f'<text x="{x:.2f}" y="{y-9:.2f}" text-anchor="middle" fill="#dce8fb" font-size="11" font-weight="700">{count}</text>')
        parts.append(f'<text x="{x:.2f}" y="323" text-anchor="middle" fill="{"#60d9bd" if fill == "teal" else "#91a1ba"}" font-size="10">{day:%d/%m}</text></g>')
    average = f'{data["week_average"]:.1f}'.replace('.', ',')
    updated = generated_at.astimezone(TZ).strftime('%d/%m/%Y')
    parts.extend([
        '<line x1="28" x2="912" y1="343" y2="343" stroke="#25344c"/>',
        f'<text x="28" y="369" fill="#91a1ba" font-size="12">Média (7 dias): {average} por dia</text>',
        f'<text x="912" y="369" text-anchor="end" fill="#91a1ba" font-size="11">Dados de {escape(updated)} (RN)</text>',
        '</g></svg>',
    ])
    return '\n'.join(parts) + '\n'


def render_chart(data: dict) -> str:
    """Version the image by its data so changed counts get a new cache URL."""
    from hashlib import sha256

    version = sha256(json.dumps({"days": [d.isoformat() for d in data["days"]],
                                 "counts": data["counts"],
                                 "week_average": data["week_average"]}, sort_keys=True).encode()).hexdigest()[:12]
    return '\n'.join([
        '<p align="center">',
        '<a href="https://joao-github-dashboard.joaosilva42333.chatgpt.site">',
        f'<img src="https://raw.githubusercontent.com/{LOGIN}/{LOGIN}/main/assets/contribuicoes-diarias.svg?v={version}" width="940" alt="Contribuições dos últimos 14 dias: barras azuis, destaque verde no dia mais recente e meta diária de 100."/>',
        '</a>',
        '</p>',
    ])


def render_markdown(data: dict, generated_at: datetime) -> str:
    """Render native numbers, a styled vector chart and expandable history."""
    labels = ("Hoje", "Ontem", "Últimos 7 dias", "Últimos 12 meses")
    numbers = (data["today"], data["yesterday"], data["week_total"], data["year_total"])
    headers = "".join(f"<th>{label}</th>" for label in labels)
    cells = "".join(
        f'<td align="center"><strong>{number:,}</strong></td>'.replace(",", ".")
        for number in numbers
    )
    average = f'{data["week_average"]:.1f}'.replace(".", ",")
    day = generated_at.astimezone(TZ).strftime("%d/%m/%Y")
    parts = [
        '<table align="center">',
        f"<thead><tr>{headers}</tr></thead>",
        f"<tbody><tr>{cells}</tr></tbody>",
        "</table>",
        "",
        f'<p align="center">Média dos últimos 7 dias: <strong>{average}</strong> contribuições por dia.</p>',
        "",
        render_chart(data),
        "",
        "<details>",
        "<summary>Ver contribuições por dia — últimos 14 dias</summary>",
        "",
        "| Data (RN) | Contribuições |",
        "| :--- | ---: |",
    ]
    for when, count in reversed(list(zip(data["days"], data["counts"]))):
        parts.append(f"| {when:%d/%m/%Y} | {count:,} |".replace(",", "."))
    parts.extend([
        "",
        "</details>",
        "",
        f'<p align="center"><sub>Dados de {day}. Consulta programada a cada 5 minutos, '
        'sujeita a atrasos do GitHub. As novas contagens aparecem ao recarregar o perfil. '
        '<a href="https://github.com/juniordev830/juniordev830/actions/workflows/contribuicoes-diarias.yml">'
        'Ver última execução</a>.</sub></p>',
    ])
    return "\n".join(parts)


def update_readme(document: str, panel: str) -> str:
    """Replace exactly one marked block, preserving the rest of the profile."""
    if document.count(START) != 1 or document.count(END) != 1:
        raise ValueError("README deve conter exatamente um par de marcadores do painel")
    start = document.index(START) + len(START)
    end = document.index(END)
    if end < start:
        raise ValueError("Marcadores do painel estão fora de ordem")
    return document[:start] + "\n\n" + panel + "\n\n" + document[end:]


def main() -> None:
    calendar = fetch_calendar(os.environ.get("GITHUB_TOKEN", ""))
    now = datetime.now(TZ)
    data = metrics(calendar, now.date())
    panel = render_markdown(data, now)
    chart = render_svg(data, now)
    original = README.read_text(encoding="utf-8")
    updated = update_readme(original, panel)
    if not CHART.exists() or CHART.read_text(encoding="utf-8") != chart:
        CHART.parent.mkdir(parents=True, exist_ok=True)
        CHART.write_text(chart, encoding="utf-8")
    if updated != original:
        README.write_text(updated, encoding="utf-8")
        print(f"Painel atualizado: {README}")
    else:
        print("Contagens e data não mudaram; README preservado")


if __name__ == "__main__":
    main()
