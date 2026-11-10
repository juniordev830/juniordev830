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
    """Render an accessible README dashboard with only observed calendar data."""
    from html import escape
    from math import pi

    counts, days = data["counts"], data["days"]
    previous, recent = sum(counts[:7]), sum(counts[7:])
    total = previous + recent
    achieved = sum(n >= 100 for n in counts)
    insights = period_insights(data)
    fmt = lambda n: f"{n:,}".replace(",", ".")
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="936" viewBox="0 0 1040 936" role="img" aria-labelledby="title desc">',
        '<title id="title">Visão geral — contribuições no GitHub</title>',
        '<desc id="desc">Indicadores, comparação entre semanas, histórico diário, distribuição das contribuições, ranking dos dias mais ativos, evolução acumulada, atividade por dia da semana e mapa de intensidade. Dados reais dos últimos 14 dias; meta diária de 100. A sequência informada é limitada à janela observada.</desc>',
        '<defs>',
    ]
    for name, a, b in [('blue','#182932','#121e26'),('purple','#172a29','#121f23'),('pink','#222735','#141f28'),('orange','#2a2b24','#191f22')]:
        parts.append(f'<linearGradient id="{name}" x1="0" x2="1" y1="0" y2="1"><stop stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
    parts += ['</defs>', '<rect x="1" y="1" width="1038" height="934" rx="22" fill="#0c1217" stroke="#293740"/>',
              '<path d="M22 1H46V935H22Q1 935 1 914V22Q1 1 22 1" fill="#10191f"/>',
              '<g font-family="Segoe UI, Arial, Helvetica, sans-serif">']

    def text(x, y, value, size=11, color='#91a4af', weight='400', anchor='start'):
        parts.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')

    def rect(x, y, w, h, fill, radius=8, **attrs):
        extra = ''.join(f' {k.replace("_", "-")}="{v}"' for k, v in attrs.items())
        parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{radius}" fill="{fill}"{extra}/>')

    def panel(x, y, w, h, title, subtitle=None):
        rect(x,y,w,h,'#141e25',12,stroke='#293b44',stroke_width='.8')
        text(x+14,y+22,title,12,'#dce7ed','700')
        if subtitle:
            text(x+14,y+39,subtitle,9)

    def donut(cx, cy, radius, values, colors, center, caption):
        parts.append(f'<g data-donut-values="{",".join(str(v) for v in values)}">')
        circumference = 2*pi*radius
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#263840" stroke-width="15"/>')
        amount = sum(values)
        offset = 0
        if amount:
            for value, color in zip(values, colors):
                length = circumference*value/amount
                if length:
                    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{color}" stroke-width="15" stroke-dasharray="{length:.4f} {circumference-length:.4f}" stroke-dashoffset="{-offset:.4f}" transform="rotate(-90 {cx} {cy})"/>')
                offset += length
        text(cx,cy+2,center,21,'#eef5f6','700','middle')
        text(cx,cy+19,caption,9,'#91a4af','400','middle')
        parts.append('</g>')

    # Decorative rail, intentionally without controls that cannot run in a README.
    parts.append('<path d="M12 32L23 21L34 28M14 18L23 28L34 15" fill="none" stroke="#82c5b6" stroke-width="3" stroke-linecap="round"/><path d="M12 32L23 21" stroke="#a5e2ce" stroke-width="3"/>')
    parts.append('<line x1="10" x2="36" y1="52" y2="52" stroke="#293a42"/>')
    for y in (97,169,241):
        rect(15,y,4,12,'#82c5b6',1);rect(22,y-7,4,19,'#54808a',1);rect(29,y-13,4,25,'#82c5b6',1)
    text(68,34,'VISÃO GERAL',19,'#e7f0f2','700')
    text(68,53,'JOÃO JÚNIOR  /  ENGENHARIA DE SOFTWARE',9,'#91a4af')
    text(1010,31,f'{days[0]:%d/%m} — {days[-1]:%d/%m/%Y}',11,'#bdcfd7','700','end')
    text(1010,49,'Últimos 14 dias · dados reais',9,'#91a4af','400','end')

    # Four KPIs use the same calendar source as the text table.
    cards = [('HOJE',fmt(data['today']),'Contribuições no dia','blue'),
             ('ÚLTIMOS 7 DIAS',fmt(recent),'Ritmo da semana','purple'),
             ('ÚLTIMOS 12 MESES',fmt(data['year_total']),'Total do calendário','pink'),
             ('META DIÁRIA',f"{data['today']}%",'Referência: 100 por dia','orange')]
    for i,(label,value,caption,color) in enumerate(cards):
        x=68+i*239
        rect(x,72,225,74,f'url(#{color})',10,stroke='#30424a',stroke_width='.8')
        accent = ('#8ec6db','#a0d7c3','#b9bedb','#d7c99e')[i]
        rect(x+13,72,32,2,accent,1)
        rect(x+13,91,32,32,'#334b54',8,fill_opacity='.45')
        parts.append(f'<path d="M{x+23} 113L{x+28} 106L{x+32} 109L{x+38} 100" stroke="#b7d6d8" stroke-width="2" fill="none" stroke-linecap="round"/>')
        text(x+57,91,label,8,'#9bb0bc','700')
        text(x+57,116,value,24,accent,'700')
        text(x+57,133,caption,8,'#a4b7c1')

    panel(68,162,449,180,'Comparação entre semanas','Mesma posição na semana · contagens por dia')
    panel(525,162,213,180,'Contribuições por semana')
    panel(750,162,260,358,'Top 5 dias mais ativos','Ranking dentro dos últimos 14 dias')
    panel(68,354,449,166,'Histórico de contribuições','Últimos 14 dias · valores absolutos')
    panel(525,354,213,166,'Consistência da meta')
    # Grouped bars compare consecutive non-overlapping seven-day windows.
    ceiling = max(1,*counts)
    plot_top, plot_bottom = 223,309
    for fraction in (0,.5,1):
        y=plot_bottom-fraction*(plot_bottom-plot_top)
        parts.append(f'<line x1="100" x2="502" y1="{y}" y2="{y}" stroke="#2a3942" stroke-dasharray="2 4"/>')
        text(94,y+3,round(ceiling*fraction),8,anchor='end')
    rect(82,210,5,5,'#466d84',2);text(91,215,'7 dias anteriores',8)
    rect(179,210,5,5,'#81c7b3',2);text(188,215,'Últimos 7 dias',8)
    for i in range(7):
        x=104+i*57
        for j,(count,color) in enumerate(((counts[i],'#466d84'),(counts[i+7],'#81c7b3'))):
            h=count/ceiling*(plot_bottom-plot_top)
            if count:
                rect(x+j*17,plot_bottom-h,15,h,color,1,data_chart_bar='true',data_plot_top=plot_top,data_plot_bottom=plot_bottom)
        text(x+16,326,f'{days[i+7]:%d/%m}',8,anchor='middle')
    recent_pct=round(100*recent/total) if total else 0
    donut(631,253,42,[recent,previous],['#81c7b3','#466d84'],f'{recent_pct}%','na semana atual')
    text(539,318,f'● Atual: {fmt(recent)}',8,'#91d8c3')
    text(725,330,f'Anterior: {fmt(previous)}',8,'#a9bdc8',anchor='end')

    # Daily history retains every observation, including zero-valued days.
    left,right,top,bottom=90,503,405,484
    for fraction in (0,.5,1):
        y=bottom-fraction*(bottom-top)
        parts.append(f'<line x1="{left}" x2="{right}" y1="{y}" y2="{y}" stroke="#2a3942" stroke-dasharray="2 4"/>')
    for i,(day,count) in enumerate(zip(days,counts)):
        x=left+(i+.5)*(right-left)/14
        h=count/ceiling*(bottom-top)
        parts.append(f'<g data-date="{day.isoformat()}" data-count="{count}"><title>{day:%d/%m/%Y}: {count} contribuições</title>')
        if count:
            rect(x-8,bottom-h,16,h,'#9cdec5' if i==13 else '#72a5bd',1,data_chart_bar='true',data_plot_top=top,data_plot_bottom=bottom)
        text(x,bottom-h-5,count,7,'#e0edf1','700','middle')
        text(x,503,f'{day:%d}',8,'#94adb9',anchor='middle')
        parts.append('</g>')
    achieved_pct=round(100*achieved/len(counts))
    donut(631,437,35,[achieved,len(counts)-achieved],['#72a5bd','#354f5b'],f'{achieved_pct}%','dos dias na meta')
    text(539,503,f'≥100: {achieved} dias',8,'#9fc9d8')
    text(725,503,f'<100: {len(counts)-achieved} dias',8,'#839ba8',anchor='end')
    # Sorted values are direct calendar observations, not repository estimates.
    ranking=sorted(zip(days,counts),key=lambda pair:(-pair[1],pair[0]))[:5]
    max_rank=max(1,*(n for _,n in ranking))
    for i,(day,count) in enumerate(ranking):
        y=231+i*55
        text(764,y+11,f'{day:%d/%m}',10,'#cbdce4','700')
        rect(809,y-3,183,23,'#25353d',3)
        if count:
            rect(809,y-3,max(1,183*count/max_rank),23,'#6e9fb4',3)
        text(985,y+12,fmt(count),10,'#ffffff','700','end')
    # Secondary metrics describe only the dates actually present in the source.
    delta = insights['week_delta_percent']
    delta_text = f'{delta:+.1f}%'.replace('.', ',') if delta is not None else 'Sem base'
    detail_cards = [
        ('TOTAL EM 14 DIAS', fmt(insights['total']), 'Contribuições na janela'),
        ('MÉDIA EM 14 DIAS', f'{insights["average"]:.1f}'.replace('.', ','), 'Contribuições por dia'),
        ('MELHOR DIA', fmt(insights['peak_count']), f'{insights["peak_day"]:%d/%m/%Y}'),
        ('DIAS ATIVOS', f'{insights["active_days"]}/14', 'Dias com contribuições'),
        ('SEQUÊNCIA ATUAL', f'{insights["streak"]} dias', 'Limitada à janela de 14 dias'),
        ('VARIAÇÃO SEMANAL', delta_text, 'Últimos 7 vs. 7 anteriores'),
    ]
    for i, (label, value, caption) in enumerate(detail_cards):
        x = 68 + i * 159
        rect(x, 536, 147, 79, '#121d24', 10, stroke='#263943', stroke_width='.8')
        rect(x, 547, 3, 20, '#76b5a6', 1)
        text(x+12, 554, label, 8, '#93abb7', '700')
        text(x+12, 582, value, 22, '#dcebee', '700')
        text(x+12, 602, caption, 7)

    panel(68,632,449,248,'Evolução acumulada','Soma progressiva das contribuições nos 14 dias')
    panel(525,632,213,248,'Por dia da semana','Soma das duas ocorrências na janela')
    panel(750,632,260,248,'Mapa de intensidade','Cada célula representa um dia real')
    # Area chart starts from an explicit zero baseline; its final value equals total.
    left, right, top, bottom = 111, 498, 695, 828
    scale = max(1, insights['total'])
    for fraction in (0,.5,1):
        y = bottom - fraction * (bottom-top)
        parts.append(f'<line x1="{left}" x2="{right}" y1="{y}" y2="{y}" stroke="#2a3942" stroke-dasharray="2 4"/>')
        text(left-8,y+3,fmt(round(scale*fraction)),8,anchor='end')
    points = [(left+i*(right-left)/13, bottom-value/scale*(bottom-top))
              for i,value in enumerate(insights['cumulative'])]
    polyline = ' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
    parts.append(f'<polygon points="{left},{bottom} {polyline} {right},{bottom}" fill="#4c8290" fill-opacity=".23"/>')
    parts.append(f'<polyline points="{polyline}" fill="none" stroke="#8ac6c5" stroke-width="3" stroke-linejoin="round"/>')
    for i, ((x,y),value) in enumerate(zip(points,insights['cumulative'])):
        parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.5" fill="#c5e9de" data-cumulative="{value}"/>')
        if i in (0,6,13):
            text(x,850,f'{days[i]:%d/%m}',8,anchor='middle')
    text(498,865,f'Total: {fmt(insights["total"])}',9,'#a1cfc9','700','end')

    # Weekday totals account for date rollover instead of assuming a starting weekday.
    weekday_names = ('Seg','Ter','Qua','Qui','Sex','Sáb','Dom')
    weekday_max = max(1,*insights['weekdays'])
    for i,(name,value) in enumerate(zip(weekday_names,insights['weekdays'])):
        y = 694 + i*24
        text(539,y+10,name,9,'#c7d7df')
        rect(568,y,113,13,'#263842',3)
        if value:
            rect(568,y,113*value/weekday_max,13,'#72a5bd',3)
        text(724,y+11,fmt(value),9,'#dcebee','700','end')

    heat_colors = ('#24343c','#345b5b','#4b8880','#76b4a2','#a9ddc7')
    max_count = max(1,*counts)
    for i,(day,count) in enumerate(zip(days,counts)):
        row,col = divmod(i,7)
        x,y = 764+col*33,710+row*61
        level = 0 if not count else min(4,1+int(count/max_count*3))
        text(x+14,y-8,f'{day:%d/%m}',7,anchor='middle')
        rect(x,y,28,34,heat_colors[level],5,data_heat_date=day.isoformat(),data_heat_count=count)
        text(x+14,y+21,count,8,'#ffffff','700','middle')
    text(764,834,'Menos',8)
    for i,color in enumerate(heat_colors):
        rect(803+i*17,824,12,12,color,2)
    text(997,834,'Mais',8,anchor='end')
    text(764,859,f'Meta atingida em {achieved} de 14 dias',9,'#a4c9d6')

    parts.append('<line x1="68" x2="1010" y1="895" y2="895" stroke="#273b44"/>')
    text(68,915,f'Média (7 dias): {data["week_average"]:.1f}'.replace('.',','),9)
    text(1010,915,f'Dados de {generated_at.astimezone(TZ):%d/%m/%Y} (RN) · dia atual parcial · meta: 100/dia',9,anchor='end')
    parts.append('</g></svg>')
    return '\n'.join(parts)+'\n'


def render_chart(data: dict) -> str:
    """Version the image by its data so changed counts get a new cache URL."""
    from hashlib import sha256

    version = sha256(json.dumps({"design": "overview-v3-matte", "year_total": data["year_total"], "days": [d.isoformat() for d in data["days"]],
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
