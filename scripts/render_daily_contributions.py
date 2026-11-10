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
    """Render a spacious, script-free analytics board for a GitHub README."""
    from html import escape
    from math import pi

    counts, days = data['counts'], data['days']
    insight = period_insights(data)
    previous, recent = sum(counts[:7]), sum(counts[7:])
    total = previous + recent
    achieved = sum(n >= 100 for n in counts)
    fmt = lambda n: f'{n:,}'.replace(',', '.')
    blue, mint, muted, white = '#79aaff', '#70dfbe', '#93a4bc', '#edf3ff'
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="1148" viewBox="0 0 1040 1148" role="img" aria-labelledby="title desc">',
        '<title id="title">Visão geral — seu código em movimento</title>',
        '<desc id="desc">Painel com dez indicadores, contribuições diárias, distribuição semanal, dias na meta, evolução acumulada, ranking, atividade por dia da semana e mapa de intensidade. Dados reais dos últimos 14 dias; sequência limitada à janela observada; meta diária de 100.</desc>',
        '<defs><linearGradient id="hero" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#172c42"/><stop offset="1" stop-color="#111c2b"/></linearGradient><linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#80afff"/><stop offset="1" stop-color="#466ed0"/></linearGradient><linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#68b8d4" stop-opacity=".3"/><stop offset="1" stop-color="#68b8d4" stop-opacity="0"/></linearGradient></defs>',
        '<rect x="1" y="1" width="1038" height="1146" rx="24" fill="#0b1019" stroke="#233044"/>',
        '<g font-family="Segoe UI, Arial, Helvetica, sans-serif">',
    ]

    def text(x,y,value,size=11,color=muted,weight='400',anchor='start'):
        parts.append(f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')

    def rect(x,y,w,h,fill='#111a27',radius=14,**attrs):
        extra=''.join(f' {k.replace("_","-")}="{v}"' for k,v in attrs.items())
        parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{radius}" fill="{fill}"{extra}/>')

    def panel(x,y,w,h,title,subtitle):
        rect(x,y,w,h,stroke='#233044',stroke_width='.8')
        text(x+20,y+29,title,16,white,'700')
        text(x+20,y+49,subtitle,10)

    def line(x1,y1,x2,y2,color='#253348',dash=None):
        extra=f' stroke-dasharray="{dash}"' if dash else ''
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}"{extra}/>')

    def donut(cx,cy,values,color,label,caption):
        parts.append(f'<g data-donut-values="{",".join(str(n) for n in values)}">')
        r=40; circumference=2*pi*r
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#29384d" stroke-width="10"/>')
        if sum(values):
            length=circumference*values[0]/sum(values)
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="10" stroke-linecap="butt" stroke-dasharray="{length:.4f} {circumference-length:.4f}" transform="rotate(-90 {cx} {cy})"/>')
        text(cx,cy+7,label,23,white,'700','middle')
        text(cx,cy+66,caption,10,muted,anchor='middle')
        parts.append('</g>')

    # Editorial header replaces the old ornamental sidebar.
    rect(32,27,132,25,'#172a34',12)
    parts.append('<circle cx="46" cy="39" r="3" fill="#70dfbe"/>')
    text(56,43,'VISÃO GERAL',9,mint,'700')
    text(1008,42,'@juniordev830',11,white,'600','end')
    text(32,94,'Seu código em movimento.',32,white,'700')
    text(32,120,'João Júnior  /  Engenharia de Software',12)
    text(1008,98,f'{days[0]:%d/%m} — {days[-1]:%d/%m/%Y}',12,white,'600','end')
    text(1008,120,'Últimos 14 dias · calendário oficial do GitHub',10,anchor='end')

    cards=[('CONTRIBUIÇÕES HOJE',fmt(data['today']),'Dia atual em andamento',blue),
           ('ÚLTIMOS 7 DIAS',fmt(recent),'Contribuições na semana',mint),
           ('ÚLTIMOS 12 MESES',fmt(data['year_total']),'Total do calendário','#b5a6ee'),
           ('META DIÁRIA',f"{data['today']}%",'Referência: 100 por dia','#e2c393')]
    for i,(label,value,caption,color) in enumerate(cards):
        x=32+i*248
        rect(x,148,232,112,'url(#hero)' if i==0 else '#131c29',16,stroke='#2b3c52',stroke_width='.8')
        text(x+18,174,label,9,muted,'600')
        text(x+18,216,value,36,color,'700')
        text(x+18,241,caption,10)
        rect(x+193,165,20,20,'none',5,stroke=color,stroke_opacity='.45')
        line(x+198,177,x+198,180,color);line(x+203,173,x+203,180,color);line(x+208,170,x+208,180,color)

    panel(32,280,650,270,'Ritmo diário','Contagens reais · valores por dia')
    panel(700,280,308,270,'Foco & constância','Participação semanal e meta de 100/dia')
    text(662,310,f'Média: {data["week_average"]:.1f}/dia'.replace('.',','),10,mint,'600','end')
    maximum=max(100,*counts)
    step=10**(len(str(maximum))-1)
    ceiling=((maximum+step-1)//step)*step
    left,right,top,bottom=78,662,357,497
    for fraction in (0,.5,1):
        y=bottom-fraction*(bottom-top)
        line(left,y,right,y,dash='2 5')
        text(left-10,y+3,fmt(round(ceiling*fraction)),9,anchor='end')
    goal_y=bottom-100/ceiling*(bottom-top)
    line(left,goal_y,right,goal_y,'#bca279','4 5')
    text(662,337,'— Meta: 100',9,'#d8bb8d',anchor='end')
    slot=(right-left)/14
    for i,(day,count) in enumerate(zip(days,counts)):
        x=left+(i+.5)*slot; h=count/ceiling*(bottom-top)
        parts.append(f'<g data-date="{day.isoformat()}" data-count="{count}"><title>{day:%d/%m/%Y}: {count} contribuições</title>')
        if count:
            rect(x-11,bottom-h,22,h,mint if i==13 else 'url(#bar)',4,data_chart_bar='true',data_plot_top=top,data_plot_bottom=bottom)
        text(x,bottom-h-7,count,9,white,'600','middle')
        text(x,520,f'{day:%d/%m}',8,mint if i==13 else muted,anchor='middle')
        parts.append('</g>')
    recent_pct=round(100*recent/total) if total else 0
    donut(777,391,[recent,previous],blue,f'{recent_pct}%','Semana recente')
    donut(931,391,[achieved,14-achieved],mint,f'{round(100*achieved/14)}%','Dias na meta')
    text(720,489,f'7 dias: {fmt(recent)}',10,blue,'600')
    text(720,514,f'Anterior: {fmt(previous)}',10)
    text(988,489,f'{achieved} de 14 dias',10,mint,'600','end')
    text(988,514,f'Abaixo: {14-achieved} dias',10,anchor='end')

    # The ten metrics remain available, now with a clearer visual hierarchy.
    delta=insight['week_delta_percent']
    details=[('TOTAL EM 14 DIAS',fmt(total),'Contribuições'),
             ('MÉDIA EM 14 DIAS',f'{insight["average"]:.1f}'.replace('.',','),'Por dia'),
             ('MELHOR DIA',fmt(insight['peak_count']),f'{insight["peak_day"]:%d/%m/%Y}'),
             ('DIAS ATIVOS',f'{insight["active_days"]}/14','Na janela observada'),
             ('SEQUÊNCIA ATUAL',f'{insight["streak"]} dias','Limitada aos 14 dias'),
             ('VARIAÇÃO SEMANAL',f'{delta:+.1f}%'.replace('.',',') if delta is not None else 'Sem base','Últimos 7 vs. anteriores')]
    for i,(label,value,caption) in enumerate(details):
        x=32+i*164
        rect(x,570,156,86,'#101925',12,stroke='#1e2e42',stroke_width='.8')
        text(x+13,591,label,8,muted,'600')
        text(x+13,620,value,25,white,'700')
        text(x+13,642,caption,8)

    panel(32,676,478,200,'Evolução acumulada','Soma progressiva das contribuições na janela')
    panel(526,676,482,200,'Dias de maior atividade','Top 5 dentro dos últimos 14 dias')
    left,right,top,bottom=78,490,743,829
    scale=max(1,total)
    for fraction in (0,.5,1):
        y=bottom-fraction*(bottom-top);line(left,y,right,y,dash='2 5')
        text(left-8,y+3,fmt(round(scale*fraction)),8,anchor='end')
    points=[(left+i*(right-left)/13,bottom-n/scale*(bottom-top)) for i,n in enumerate(insight['cumulative'])]
    coords=' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
    parts.append(f'<polygon points="{left},{bottom} {coords} {right},{bottom}" fill="url(#area)"/>')
    parts.append(f'<polyline points="{coords}" fill="none" stroke="#8bd2dc" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
    for i,((x,y),n) in enumerate(zip(points,insight['cumulative'])):
        parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.5" fill="#a5e6e5" data-cumulative="{n}"/>')
        if i in (0,6,13):text(x,853,f'{days[i]:%d/%m}',9,anchor='middle')
    ranking=sorted(zip(days,counts),key=lambda p:(-p[1],p[0]))[:5]
    rank_max=max(1,*(n for _,n in ranking))
    for i,(day,n) in enumerate(ranking):
        y=741+i*25
        text(548,y+11,f'{i+1:02}',9,'#62748f')
        text(574,y+11,f'{day:%d/%m}',10,white,'600')
        rect(620,y,315,13,'#233047',5)
        if n:rect(620,y,315*n/rank_max,13,'#7199d7',5)
        text(988,y+11,fmt(n),10,white,'600','end')

    panel(32,892,478,210,'Atividade por dia da semana','Soma das duas ocorrências de cada dia na janela')
    panel(526,892,482,210,'Mapa de intensidade','Cada célula mostra a data e a contagem observada')
    left,right,top,bottom=62,490,960,1060
    weekday_max=max(1,*insight['weekdays'])
    for fraction in (0,.5,1):line(left,bottom-fraction*(bottom-top),right,bottom-fraction*(bottom-top),dash='2 5')
    for i,(name,n) in enumerate(zip(('Seg','Ter','Qua','Qui','Sex','Sáb','Dom'),insight['weekdays'])):
        x=left+(i+.5)*(right-left)/7;h=n/weekday_max*(bottom-top)
        if n:rect(x-14,bottom-h,28,h,'#7d97d7',4,data_chart_bar='true',data_plot_top=top,data_plot_bottom=bottom)
        text(x,bottom-h-8,fmt(n),10,white,'600','middle')
        text(x,1084,name,10,anchor='middle')
    heat=('#263549','#385967','#468e90','#63b6a7','#9de0c3')
    heat_max=max(1,*counts)
    for i,(day,n) in enumerate(zip(days,counts)):
        row,col=divmod(i,7);x=548+col*62;y=958+row*65
        text(x+25,y-7,f'{day:%d/%m}',9,anchor='middle')
        level=0 if n==0 else min(4,1+int(n/heat_max*3))
        rect(x,y,50,42,heat[level],8,data_heat_date=day.isoformat(),data_heat_count=n)
        text(x+25,y+27,n,12,'#f0f9f6','600','middle')
    text(548,1086,'Menos',9)
    for i,color in enumerate(heat):rect(592+i*19,1076,13,13,color,3)
    text(701,1086,'Mais',9)
    line(32,1120,1008,1120)
    text(32,1138,f'Média (7 dias): {data["week_average"]:.1f}'.replace('.',','),9)
    text(1008,1138,f'{generated_at.astimezone(TZ):%d/%m/%Y} (RN) · dia atual parcial · consulta programada: 5 min',9,anchor='end')
    parts.append('</g></svg>')
    return '\n'.join(parts)+'\n'


def render_chart(data: dict) -> str:
    """Version the image by its data so changed counts get a new cache URL."""
    from hashlib import sha256

    version = sha256(json.dumps({"design": "overview-v4-modern", "year_total": data["year_total"], "days": [d.isoformat() for d in data["days"]],
                                 "counts": data["counts"],
                                 "week_average": data["week_average"]}, sort_keys=True).encode()).hexdigest()[:12]
    return '\n'.join([
        '<p align="center">',
        '<a href="https://joao-github-dashboard.joaosilva42333.chatgpt.site">',
        f'<img src="https://raw.githubusercontent.com/{LOGIN}/{LOGIN}/main/assets/contribuicoes-diarias.svg?v={version}" width="1040" alt="Painel completo GitHub: indicadores, comparação semanal, histórico, roscas, ranking, evolução acumulada, atividade por dia da semana e mapa de intensidade."/>',
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
