"""Gera um painel SVG fosco usando o calendário oficial de contribuições.

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
OUTPUT = Path("assets/contribuicoes-diarias.svg")
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
        parts.append(
            f'<text x="{x+16}" y="143" font-family="Arial, sans-serif" '
            f'font-weight="700" font-size="27" '
            f'fill="{green if i == 0 else text}">{number:,}</text>'.replace(",", ".")
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
    updated = generated_at.astimezone(TZ).strftime("%d/%m/%Y às %H:%M")
    parts.extend([
        f'<text x="30" y="438" font-family="Arial, sans-serif" font-size="13" '
        f'fill="{secondary}">Média (7 dias): {avg} por dia</text>',
        f'<text x="908" y="438" text-anchor="end" font-family="Arial, sans-serif" '
        f'font-size="12" fill="{secondary}">Atualizado em {updated} (RN)</text>',
        '</svg>',
    ])
    return "\n".join(parts) + "\n"


def main() -> None:
    calendar = fetch_calendar(os.environ.get("GITHUB_TOKEN", ""))
    now = datetime.now(TZ)
    svg = render_svg(metrics(calendar, now.date()), now)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Painel atualizado: {OUTPUT}")


if __name__ == "__main__":
    main()
