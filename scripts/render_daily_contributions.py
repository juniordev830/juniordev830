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
    days = data["days"]
    counts = data["counts"]
    maximum = max(1, *counts)
    bg, panel, border = "#10181d", "#192329", "#354148"
    text, secondary, green = "#edf2f3", "#aebbc1", "#79be92"
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="940" height="470" '
        'viewBox="0 0 940 470" role="img" aria-label="Contribuições diárias no GitHub">',
        '<rect width="940" height="470" rx="18" fill="' + bg + '"/>',
        '<rect x="1" y="1" width="938" height="468" rx="17" fill="none" stroke="' + border + '"/>',
        '<text x="30" y="44" font-family="Arial, sans-serif" font-size="23" '
        'font-weight="700" fill="' + text + '">Contribuições diárias</text>',
        '<text x="30" y="67" font-family="Arial, sans-serif" font-size="13" '
        'fill="' + secondary + '">Últimos 14 dias · dados do GitHub</text>',
    ]

    cards = [
        ("Hoje", data["today"]),
        ("Ontem", data["yesterday"]),
        ("Últimos 7 dias", data["week_total"]),
        ("Últimos 12 meses", data["year_total"]),
    ]
    for i, (label, number) in enumerate(cards):
        x = 30 + i * 228
        parts.append(
            f'<rect x="{x}" y="87" width="200" height="75" rx="12" '
            f'fill="{panel}" stroke="{border}"/>'
        )
        parts.append(
            f'<text x="{x+16}" y="111" font-family="Arial, sans-serif" '
            f'font-size="13" fill="{secondary}">{label}</text>'
        )
        formatted_number = f"{number:,}".replace(",", ".")
        parts.append(
            f'<text x="{x+16}" y="143" font-family="Arial, sans-serif" '
            f'font-weight="700" font-size="27" '
            f'fill="{green if i == 0 else text}">{formatted_number}</text>'
        )

    chart_bottom, chart_top = 384, 210
    for fraction in (0, .5, 1):
        y = chart_bottom - fraction * (chart_bottom - chart_top)
        parts.append(
            f'<line x1="30" x2="908" y1="{y:.1f}" y2="{y:.1f}" '
            f'stroke="{border}" stroke-width="1" opacity=".7"/>'
        )
    for i, (day, count) in enumerate(zip(days, counts)):
        x = 40 + i * 62
        height = round(count / maximum * 134, 1)
        y = chart_bottom - height
        is_today = i == 13
        fill = "#8bce9e" if is_today else "#427d60"
        if height:
            parts.append(
                f'<rect x="{x}" y="{y:.1f}" width="36" height="{height:.1f}" '
                f'rx="5" fill="{fill}"/>'
            )
        parts.append(
            f'<text x="{x + 18}" y="{max(chart_top, y - 10):.1f}" '
            f'text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" '
            f'font-size="14" fill="{text}">{count}</text>'
        )
        parts.append(
            f'<text x="{x + 18}" y="404" text-anchor="middle" '
            f'font-family="Arial, sans-serif" font-size="12" '
            f'fill="{green if is_today else secondary}">{day:%d/%m}</text>'
        )
    avg = f'{data["week_average"]:.1f}'.replace(".", ",")
    updated = generated_at.astimezone(TZ).strftime("%d/%m/%Y")
    parts.extend([
        f'<text x="30" y="438" font-family="Arial, sans-serif" font-size="13" '
        f'fill="{secondary}">Média (7 dias): {avg} por dia</text>',
        f'<text x="908" y="438" text-anchor="end" font-family="Arial, sans-serif" '
        f'font-size="12" fill="{secondary}">Dados de {updated} (RN)</text>',
        '</svg>',
    ])
    return "\n".join(parts) + "\n"


def render_markdown(data: dict, generated_at: datetime) -> str:
    """Render numbers and expandable history without images or JavaScript."""
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
    panel = render_markdown(metrics(calendar, now.date()), now)
    original = README.read_text(encoding="utf-8")
    updated = update_readme(original, panel)
    if updated != original:
        README.write_text(updated, encoding="utf-8")
        print(f"Painel atualizado: {README}")
    else:
        print("Contagens e data não mudaram; README preservado")


if __name__ == "__main__":
    main()
