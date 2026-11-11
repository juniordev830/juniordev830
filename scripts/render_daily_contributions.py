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


def period_insights(data: dict) -> dict:
    """Summarize the observed window; never infer activity outside these 14 days."""
    counts, days = data['counts'], data['days']
    previous, recent = sum(counts[:7]), sum(counts[7:])
    cumulative, running = [], 0
    weekdays = [0] * 7
    for day, count in zip(days, counts):
        running += count
        cumulative.append(running)
        weekdays[day.weekday()] += count
    streak = 0
    for count in reversed(counts):
        if count == 0:
            break
        streak += 1
    peak_index = counts.index(max(counts))
    return {
        'total': running,
        'average': running / len(counts),
        'active_days': sum(n > 0 for n in counts),
        'streak': streak,
        'peak_count': counts[peak_index],
        'peak_day': days[peak_index],
        'week_delta_percent': (recent - previous) * 100 / previous if previous else None,
        'cumulative': cumulative,
        'weekdays': weekdays,
    }


def render_svg(data: dict, generated_at: datetime) -> str:
    """Render a restrained business report with a small, readable visual hierarchy."""
    from html import escape

    counts, days = data['counts'], data['days']
    insight = period_insights(data)
    previous, recent = sum(counts[:7]), sum(counts[7:])
    achieved = sum(n >= 100 for n in counts)
    fmt = lambda n: f'{n:,}'.replace(',', '.')
    ink, secondary = '#d8dde1', '#a2aab1'
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="1084" viewBox="0 0 1040 1084" role="img" aria-labelledby="title desc">',
        '<title id="title">Atividade de desenvolvimento — visão geral</title>',
        '<desc id="desc">Relatório de contribuições e projetos em destaque, com indicadores, histórico diário, acumulado, resumo e intensidade. Dados reais dos últimos 14 dias, meta de 100 por dia e sequência limitada à janela observada.</desc>',
        '<rect x="1" y="1" width="1038" height="1082" rx="16" fill="#1b2025" stroke="#343b42"/>',
        '<g font-family="Segoe UI, Arial, Helvetica, sans-serif">',
    ]

    def text(x,y,value,size=11,color=secondary,weight='400',anchor='start'):
        parts.append(f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')

    def line(x1,y1,x2,y2,color='#353d45',dash=None):
        extra=f' stroke-dasharray="{dash}"' if dash else ''
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}"{extra}/>')

    def rect(x,y,w,h,fill,radius=3,**attrs):
        extra=''.join(f' {k.replace("_","-")}="{v}"' for k,v in attrs.items())
        parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{radius}" fill="{fill}"{extra}/>')

    text(40,35,'VISÃO GERAL  /  GITHUB',10,secondary,'600')
    text(40,70,'Atividade de desenvolvimento',25,ink,'600')
    text(1000,35,'João Júnior · @juniordev830',11,secondary,anchor='end')
    text(1000,70,f'{days[0]:%d/%m} — {days[-1]:%d/%m/%Y}',11,secondary,anchor='end')
    line(40,91,1000,91)

    # Unboxed metrics replace colored cards and ornamental icons.
    cards=[('Hoje',fmt(data['today']),'Dia atual parcial'),
           ('Últimos 7 dias',fmt(recent),'Contribuições'),
           ('Últimos 12 meses',fmt(data['year_total']),'Total do calendário'),
           ('Meta diária',f"{data['today']}%",'Referência: 100/dia')]
    for i,(label,value,caption) in enumerate(cards):
        x=40+i*248
        if i:line(x-20,117,x-20,179,'#343b42')
        text(x,124,label,11)
        text(x,159,value,30,ink,'600')
        text(x,182,caption,10)
    line(40,204,1000,204)

    text(40,238,'Contribuições diárias',15,ink,'600')
    text(40,260,'Últimos 14 dias',10)
    text(1000,238,f'Média (7 dias): {data["week_average"]:.1f}'.replace('.',','),11,secondary,anchor='end')
    text(1000,260,'Linha tracejada · meta de 100/dia',10,secondary,anchor='end')
    left,right,top,bottom=78,1000,291,430
    maximum=max(100,*counts)
    step=10**(len(str(maximum))-1)
    ceiling=((maximum+step-1)//step)*step
    for fraction in (0,.5,1):
        y=bottom-fraction*(bottom-top)
        line(left,y,right,y,'#30383f')
        text(left-13,y+4,fmt(round(ceiling*fraction)),9,anchor='end')
    goal_y=bottom-100/ceiling*(bottom-top)
    line(left,goal_y,right,goal_y,'#65716f','4 6')
    slot=(right-left)/14
    peak_index=counts.index(max(counts))
    for i,(day,count) in enumerate(zip(days,counts)):
        x=left+(i+.5)*slot;h=count/ceiling*(bottom-top)
        parts.append(f'<g data-date="{day.isoformat()}" data-count="{count}"><title>{day:%d/%m/%Y}: {count} contribuições</title>')
        if count:
            rect(x-15,bottom-h,30,h,'#a3b9ac' if i==13 else '#8196a4',3,data_chart_bar='true',data_plot_top=top,data_plot_bottom=bottom)
        if i in (peak_index,13):text(x,bottom-h-10,count,10,ink,'600','middle')
        text(x,454,f'{day:%d/%m}',9,secondary,anchor='middle')
        parts.append('</g>')
    line(40,480,1000,480)

    text(40,514,'Evolução acumulada',15,ink,'600')
    period_average = f'{insight["average"]:.1f}'.replace('.', ',')
    text(40,536,f'Total: {fmt(insight["total"])} · média em 14 dias: {period_average}',10)
    left,right,top,bottom=82,621,563,658
    scale=max(1,insight['total'])
    for fraction in (0,1):
        y=bottom-fraction*(bottom-top);line(left,y,right,y,'#30383f')
        text(left-12,y+3,fmt(round(scale*fraction)),9,anchor='end')
    points=[(left+i*(right-left)/13,bottom-value/scale*(bottom-top)) for i,value in enumerate(insight['cumulative'])]
    coordinates=' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
    parts.append(f'<polyline points="{coordinates}" fill="none" stroke="#a6b7bd" stroke-width="2" stroke-linejoin="round"/>')
    for i,((x,y),value) in enumerate(zip(points,insight['cumulative'])):
        parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2" fill="#adbec3" data-cumulative="{value}"/>')
        if i in (0,6,13):text(x,681,f'{days[i]:%d/%m}',9,anchor='middle')
    line(655,506,655,684,'#343b42')
    text(687,514,'Resumo do período',15,ink,'600')
    delta=insight['week_delta_percent']
    delta_label=f'{delta:+.1f}%'.replace('.',',') if delta is not None else 'Sem base'
    summary=[('Melhor dia',f'{fmt(insight["peak_count"])} · {insight["peak_day"]:%d/%m}'),
             ('Dias ativos',f'{insight["active_days"]} de 14'),
             ('Sequência na janela',f'{insight["streak"]} dias'),
             ('Variação entre semanas',delta_label)]
    for i,(label,value) in enumerate(summary):
        y=551+i*36
        text(687,y,label,11)
        text(1000,y,value,12,ink,'600','end')
    line(40,704,1000,704)

    text(40,733,'Intensidade por dia',13,ink,'600')
    parts.append(f'<g data-summary-values="{recent},{previous}">')
    text(1000,733,f'7 dias recentes: {fmt(recent)} · anteriores: {fmt(previous)}',10,secondary,anchor='end')
    parts.append('</g>')
    colors=('#303b42','#43565d','#5d767b','#7c9896','#a5bfb1')
    heat_max=max(1,*counts)
    for i,(day,count) in enumerate(zip(days,counts)):
        x=40+i*69
        text(x+26,754,f'{day:%d/%m}',8,anchor='middle')
        level=0 if not count else min(4,1+int(count/heat_max*3))
        rect(x,763,53,28,colors[level],4,data_heat_date=day.isoformat(),data_heat_count=count)
        text(x+26.5,782,count,10,'#e1e7e7','500','middle')
    parts.append(f'<g data-summary-values="{achieved},{14-achieved}">')
    text(40,821,f'Meta cumprida: {achieved} de 14 dias · sequência limitada à janela exibida',9)
    parts.append('</g>')
    text(1000,821,f'{generated_at.astimezone(TZ):%d/%m/%Y} (RN) · consulta programada: 5 min',9,anchor='end')
    # Portfolio stays inside the same SVG surface as the live activity charts.
    # No image embedding or external fonts: GitHub's README image sanitizer can render it.
    line(40,852,1000,852)
    text(40,879,'PORTFÓLIO  /  GITHUB',10,secondary,'600')
    text(40,912,'Projetos em destaque',20,ink,'600')
    projects = [
        ('Plataforma de Recrutamento', ('Vagas, candidaturas e API REST', 'com autenticação.'), ('Node.js','Express','SQLite')),
        ('Atlas Sentinela', ('Monitoramento geoespacial', 'experimental e globo 3D.'), ('Python','FastAPI','3D')),
        ('Controle de Gastos', ('API para organizar receitas', 'e despesas familiares.'), ('C#','.NET','SQLite')),
    ]
    for i, (name, description, tags) in enumerate(projects):
        x = 40 + i * 328
        rect(x, 931, 304, 123, '#222d38', 10, stroke='#3c4b5a')
        text(x+16, 958, name, 15, '#a3cfff', '600')
        text(x+16, 983, description[0], 12, '#d2dbe5')
        text(x+16, 1000, description[1], 12, '#d2dbe5')
        tag_x = x+16
        for tag in tags:
            width = max(33, len(tag)*7+16)
            rect(tag_x, 1015, width, 23, '#304050', 5)
            text(tag_x+8, 1031, tag, 11, '#e3edfa', '600')
            tag_x += width+6
    parts.append('</g></svg>')
    return '\n'.join(parts)+'\n'


def render_chart(data: dict) -> str:
    """Version the image by its data so changed counts get a new cache URL."""
    from hashlib import sha256

    version = sha256(json.dumps({"design": "overview-v6-unified-portfolio", "year_total": data["year_total"], "days": [d.isoformat() for d in data["days"]],
                                 "counts": data["counts"],
                                 "week_average": data["week_average"]}, sort_keys=True).encode()).hexdigest()[:12]
    return '\n'.join([
        '<p align="center">',
        '<a href="https://joao-github-dashboard.joaosilva42333.chatgpt.site">',
        f'<img src="https://raw.githubusercontent.com/{LOGIN}/{LOGIN}/main/assets/contribuicoes-diarias.svg?v={version}" width="1040" alt="Painel unificado de contribuições, evolução diária, intensidade e projetos em destaque."/>',
        '</a>',
        '</p>',
    ])


def render_markdown(data: dict, generated_at: datetime) -> str:
    """Show the chart and history; retain raw metrics for the standalone dashboard."""
    numbers = (data["today"], data["yesterday"], data["week_total"], data["year_total"])
    # The HTML dashboard reads these four values from the raw README. An HTML
    # comment preserves that contract without duplicating the visible SVG KPIs.
    raw_metrics = "".join(
        f'<strong>{number:,}</strong>'.replace(",", ".")
        for number in numbers
    )
    day = generated_at.astimezone(TZ).strftime("%d/%m/%Y")
    parts = [
        f'<!-- CONTRIBUTIONS:METRICS {raw_metrics} -->',
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
    insights = period_insights(data)
    parts.extend([
        "", "</details>", "", "<details>",
        "<summary>Análise complementar — dias da semana e ranking</summary>", "",
        "| Dia da semana | Contribuições nos 14 dias |",
        "| :--- | ---: |",
    ])
    for label, value in zip(('Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'), insights['weekdays']):
        parts.append(f'| {label} | {value:,} |'.replace(',', '.'))
    parts.extend(["", "Cinco dias mais ativos na janela:", "", "| Posição | Data | Contribuições |", "| ---: | :--- | ---: |"])
    for rank, (when, value) in enumerate(sorted(zip(data['days'], data['counts']), key=lambda pair: (-pair[1], pair[0]))[:5], 1):
        parts.append(f'| {rank} | {when:%d/%m/%Y} | {value:,} |'.replace(',', '.'))
    parts.extend([
        "",
        "</details>",
        "",
        f'<p align="center"><sub>Dados de {day}. Consulta programada a cada 5 minutos, '
        'sujeita a atrasos do GitHub. As novas contagens aparecem ao recarregar o perfil. '
        '<a href="https://github.com/juniordev830/juniordev830/actions/workflows/contribuicoes-diarias.yml">'
        'Ver última execução</a>.</sub></p>',
    ])
    parts.extend([
        '',
        '<details>',
        '<summary>Links dos projetos em destaque</summary>',
        '',
        '<p align="center">',
        '<a href="https://github.com/juniordev830/plataforma-de-recrutamento">Plataforma de Recrutamento</a> · ',
        '<a href="https://github.com/juniordev830/sentinel-atlas">Atlas Sentinela</a> · ',
        '<a href="https://github.com/juniordev830/controle-gastos-residenciais">Controle de Gastos</a>',
        '</p>',
        '</details>',
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
