"""Inventario verificavel do portfolio: evidencias tecnicas, nao percentual de conclusao."""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
from html import escape
import json
import os
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SVG = ROOT / "assets" / "portfolio-andamento.svg"
REPORT = ROOT / "docs" / "ANDAMENTO_DOS_PROJETOS.md"
START = "<!-- PORTFOLIO-STATUS:START -->"
END = "<!-- PORTFOLIO-STATUS:END -->"
OWNER = "juniordev830"
# Repositorios privados conhecidos, inacessiveis ao token do workflow.
KNOWN_RESTRICTED = ("codvision", "adc-de-fuc-ebd")
API = "https://api.github.com"
CODE_EXTS = (".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".cs", ".go", ".cpp",
             ".c", ".h", ".gd", ".rb", ".rs", ".php", ".html", ".css", ".sql",
             ".sh", ".ps1", ".kt", ".swift", ".vue", ".svelte")


def github_json(path: str, token: str):
    if not token:
        raise ValueError("GITHUB_TOKEN ausente: nao publicar indicadores sem verificacao")
    request = Request(API + path, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-profile-portfolio-audit",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urlopen(request, timeout=25) as response:
        return json.load(response)


def collect(token: str) -> list[dict]:
    projects = []
    for page in range(1, 11):
        items = github_json(f"/users/{OWNER}/repos?type=owner&per_page=100&page={page}", token)
        if not isinstance(items, list):
            raise ValueError("Listagem invalida do GitHub")
        for repo in items:
            name = repo["name"]
            branch = quote(repo.get("default_branch") or "main", safe="")
            tree = github_json(f"/repos/{OWNER}/{quote(name, safe='')}/git/trees/{branch}?recursive=1", token)
            if "tree" not in tree:
                raise ValueError(f"Arvore indisponivel em {name}")
            files = [entry["path"] for entry in tree["tree"] if entry.get("type") == "blob"]
            low = [path.lower() for path in files]
            docs = any(path in ("readme.md", "readme.rst", "readme.txt") for path in low)
            code = any(path.endswith(CODE_EXTS) and not path.startswith(
                ("node_modules/", "vendor/", "dist/", "build/", ".github/")) for path in low)
            tests = any(any(part in ("tests", "test", "__tests__", "spec", "specs") for part in path.split("/"))
                        or path.split("/")[-1].startswith(("test_", "spec_"))
                        or path.split("/")[-1].endswith((".test.ts", ".test.js", ".spec.ts", ".spec.js"))
                        for path in low)
            ci = any(path.startswith(".github/workflows/") and path.endswith((".yaml", ".yml"))
                     for path in low)
            projects.append({
                "name": name, "url": repo["html_url"],
                "pushed": (repo.get("pushed_at") or "")[:10],
                "pushed_iso": repo.get("pushed_at") or "",
                "docs": docs, "code": code, "tests": tests, "ci": ci,
                "archived": repo.get("archived", False),
                "partial": bool(tree.get("truncated", False)),
            })
        if len(items) < 100:
            break
    if not projects:
        raise ValueError("Nenhum repositorio recuperado; dados anteriores preservados")
    listed = {project["name"] for project in projects}
    for name in KNOWN_RESTRICTED:
        if name not in listed:
            projects.append({
                "name": name, "url": f"https://github.com/{OWNER}/{name}",
                "pushed": "", "pushed_iso": "", "docs": False, "code": False,
                "tests": False, "ci": False, "archived": False,
                "partial": True, "restricted": True,
            })
    return sorted(projects, key=lambda project: project["name"].casefold())


def stage(item: dict) -> str:
    if item.get("restricted"):
        return "Acesso restrito"
    if item["archived"]:
        return "Arquivado"
    if item["partial"]:
        return "Inspecao parcial"
    if item["tests"] and item["ci"]:
        return "Validacao automatizada"
    if item["tests"]:
        return "Com testes"
    if item["code"]:
        return "Implementacao"
    if item["docs"]:
        return "Estruturacao"
    return "Sem evidencias"


def summaries(projects: list[dict]) -> dict:
    return {
        "repos": len(projects),
        "scanned": sum(not p.get("restricted", False) for p in projects),
        "restricted": sum(p.get("restricted", False) for p in projects),
        "docs": sum(p["docs"] for p in projects),
        "code": sum(p["code"] for p in projects),
        "tests": sum(p["tests"] for p in projects),
        "ci": sum(p["ci"] for p in projects),
        "validated": sum(stage(p) == "Validacao automatizada" for p in projects),
        "with_tests": sum(stage(p) == "Com testes" for p in projects),
        "implementing": sum(stage(p) == "Implementacao" for p in projects),
        "structuring": sum(stage(p) in ("Estruturacao", "Sem evidencias", "Inspecao parcial")
                           for p in projects),
    }


def render_svg(projects: list[dict]) -> str:
    """Dashboard de portfolio. As barras medem evidencias, nunca conclusao.

    Os cinco indicadores sao extraidos da auditoria do GitHub. Um projeto
    com workflow e testes NAO e automaticamente considerado concluido.
    """
    from math import pi

    count = summaries(projects)
    width, height = 1120, 902
    output = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        'role="img" aria-label="Portfolio de projetos: inventario e sinais tecnicos auditados">',
        '<defs>',
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1724"/><stop offset="1" stop-color="#090e17"/></linearGradient>',
        '<linearGradient id="cyan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#087daf"/><stop offset="1" stop-color="#36c2e8"/></linearGradient>',
        '<linearGradient id="navy" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#142538"/><stop offset="1" stop-color="#101b29"/></linearGradient>',
        '<linearGradient id="green" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#128e83"/><stop offset="1" stop-color="#39c9a9"/></linearGradient>',
        '<linearGradient id="violet" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5b67ae"/><stop offset="1" stop-color="#a48bdb"/></linearGradient>',
        '</defs>',
        f'<rect width="{width}" height="{height}" rx="20" fill="url(#bg)"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="19" fill="none" stroke="#294052"/>',
    ]
    def rect(x, y, w, h, fill="#121f2d", stroke="#2d4355", r=12):
        output.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')

    def text(x, y, msg, size=15, color="#dce8f1", weight=400, anchor=None):
        anchor_prop = f' text-anchor="{anchor}"' if anchor else ""
        output.append(
            f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,Helvetica,sans-serif" '
            f'font-size="{size}" font-weight="{weight}"{anchor_prop}>{escape(str(msg))}</text>'
        )

    def line(x1, y1, x2, y2, color="#294050", opacity="1"):
        output.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" opacity="{opacity}"/>')

    def bar(x, y, w, ratio, gradient="url(#cyan)", height=9):
        rect(x, y, w, height, "#243746", "#243746", height / 2)
        actual = max(0, min(1, ratio))
        if actual:
            rect(x, y, round(w * actual, 1), height, gradient, gradient, height / 2)

    def section(x, y, w, h, title, subtitle=""):
        rect(x, y, w, h, "url(#navy)")
        text(x + 20, y + 31, title, 19, "#f0f6fb", 700)
        if subtitle:
            text(x + 20, y + 52, subtitle, 12, "#98b1c2")
        line(x + 20, y + 65, x + w - 20, y + 65)

    # Identidade visual: linhas limpas e pouco brilho, no estilo do README.
    output.append('<g fill="none" stroke="#4cbce5" stroke-width="4" stroke-linejoin="round">')
    output.append('<path d="M34 40 L62 27 L90 40 L62 53 Z"/><path d="M34 53 L62 66 L90 53"/><path d="M34 66 L62 79 L90 66"/>')
    output.append('</g>')
    text(114, 52, "Portfólio de", 30, "#f2f6fa", 700)
    text(312, 52, "Projetos", 30, "#36b7df", 700)
    text(115, 77, "Andamento e saúde técnica do ecossistema de repositórios", 15, "#a4b9c9")
    rect(865, 27, 230, 38, "#102935", "#356078", 19)
    output.append('<circle cx="885" cy="46" r="6" fill="#36cfa8"/>')
    text(900, 51, "INVENTÁRIO AUDITADO", 12, "#d6eaf4", 700)

    # Indicadores verificaveis; as contagens refletem arquivos observados, não entregas finais.
    cards = [
        ("REPOSITÓRIOS", count["repos"], f"{count['restricted']} com acesso restrito", "#46bde7"),
        ("AUDITADOS", count["scanned"], "branches padrão", "#5fa8e7"),
        ("COM CÓDIGO", count["code"], "arquivos detectados", "#79bdd6"),
        ("COM TESTES", count["tests"], "estrutura detectada", "#a897e5"),
        ("COM PIPELINES", count["ci"], "workflows detectados", "#45c0a8"),
    ]
    for i, (label, value, caption, color) in enumerate(cards):
        x = 24 + i * 220
        rect(x, 106, 210, 107)
        rect(x + 14, 120, 45, 43, "#193046", "#264b63", 10)
        output.append(f'<circle cx="{x+36}" cy="141" r="9" fill="none" stroke="{color}" stroke-width="3"/>')
        text(x + 70, 130, label, 11, "#c1d2de", 700)
        text(x + 70, 164, value, 28, "#f2f6fb", 700)
        text(x + 16, 195, caption, 11, "#90a9ba")
        rect(x + 165, 185, 27, 3, color, color, 1)

    section(24, 232, 448, 317, "Distribuição técnica", "Fases identificadas por evidências dos arquivos")
    rows = [
        ("Testes + pipeline", count["validated"], "#36b8e5"),
        ("Testes, sem pipeline", count["with_tests"], "#a68be1"),
        ("Implementação", count["implementing"], "#48c3a9"),
        ("Estruturação / revisão", count["structuring"], "#f2ba5a"),
        ("Acesso restrito", count["restricted"], "#8495a7"),
    ]
    # Donut: grupos técnicos; não é um gráfico de progresso funcional.
    circumference = 2 * pi * 70
    output.append('<circle cx="154" cy="415" r="70" fill="none" stroke="#223749" stroke-width="25"/>')
    offset = 0.0
    for name, amount, color in rows:
        if amount:
            size = circumference * amount / max(1, count["repos"])
            output.append(
                f'<circle cx="154" cy="415" r="70" fill="none" stroke="{color}" stroke-width="25" '
                f'stroke-dasharray="{size:.2f} {circumference-size:.2f}" stroke-dashoffset="{-offset:.2f}" '
                'transform="rotate(-90 154 415)"/>'
            )
            offset += size
    text(154, 417, count["repos"], 32, "#f3f7fb", 700, "middle")
    text(154, 440, "projetos", 12, "#acbfcc", 400, "middle")
    for i, (name, amount, color) in enumerate(rows):
        y = 350 + i * 37
        output.append(f'<circle cx="270" cy="{y-5}" r="6" fill="{color}"/>')
        text(285, y, name, 12, "#dce6ee")
        text(447, y, amount, 14, "#f2f5f9", 700, "end")

    section(489, 232, 607, 317, "Projetos em foco", "Estágio técnico observado, sem percentuais de conclusão")
    featured = [
        "pixel-farm-seasons",
        "sentinel-atlas",
        "plataforma-de-recrutamento",
        "infrastructure-as-code-lab",
    ]
    by_name = {p["name"]: p for p in projects}
    for i, name in enumerate(featured):
        if name not in by_name:
            continue
        project = by_name[name]
        col = i % 2
        row = i // 2
        x = 508 + col * 288
        y = 315 + row * 110
        rect(x, y, 274, 96, "#122334", "#355067", 10)
        short_name = name if len(name) < 27 else name[:25] + ".."
        text(x + 14, y + 26, short_name, 13, "#f2f6fa", 700)
        desc = stage(project)
        if desc == "Validacao automatizada":
            desc = "Testes + CI"
        elif desc == "Implementacao":
            desc = "Código identificado"
        text(x + 14, y + 48, desc, 12, "#9dc6dc")
        signals = sum(bool(project.get(k)) for k in ("docs", "code", "tests", "ci"))
        text(x + 14, y + 77, f"{signals}/4 sinais técnicos", 11, "#95acbc")
        bar(x + 151, y + 67, 103, signals/4, "url(#cyan)" if i % 2 == 0 else "url(#violet)", 8)

    section(24, 567, 618, 232, "Fluxo de evolução", "Cada projeto pertence à fase mais avançada detectada")
    stage_cards = [
        ("ESTRUTURAÇÃO", count["structuring"], "#e4b566"),
        ("IMPLEMENTAÇÃO", count["implementing"], "#51afd5"),
        ("COM TESTES", count["with_tests"], "#a392d9"),
        ("TESTES + CI", count["validated"], "#45bf9f"),
    ]
    for i, (name, val, color) in enumerate(stage_cards):
        x = 43 + 148*i
        rect(x, 660, 135, 109, "#162a3c", "#335268", 9)
        text(x + 13, 687, name, 11, color, 700)
        text(x + 13, 734, val, 32, "#f2f8fb", 700)
        if i < len(stage_cards) - 1:
            text(x + 138, 726, "›", 24, "#6999b2", 700)
    text(45, 790, "Acesso restrito: " + str(count["restricted"]) + "  ·  Qualidade e cobertura exigem testes adicionais", 11, "#9fb2c2")

    section(658, 567, 438, 232, "Últimas movimentações", "Projetos ordenados pela última atualização")
    recent = sorted(
        [p for p in projects if not p.get("restricted")],
        key=lambda p: (p.get("pushed_iso") or p["pushed"], p["name"]),
        reverse=True,
    )[:4]
    for i, p in enumerate(recent):
        y = 660 + i * 33
        short = p["name"] if len(p["name"]) < 32 else p["name"][:30] + ".."
        text(676, y, short, 12, "#d9e7ef", 700)
        day = p["pushed"][8:10] + "/" + p["pushed"][5:7] if p["pushed"] else "—"
        text(1070, y, day, 12, "#81a6bc", 400, "end")
        if i < 3:
            line(677, y + 9, 1072, y + 9, "#284354")
    text(677, 787, "Datas de push não medem avanço funcional", 11, "#96aebd")

    rect(24, 815, 1072, 63, "#10202e", "#2b4759", 11)
    text(45, 840, f"71 projetos no inventário" if count["repos"] == 71 else f"{count['repos']} projetos no inventário", 16, "#eff5f9", 700)
    text(45, 863, "Relatório individual • métodos e limitações • links por repositório", 12, "#a8becc")
    text(1070, 852, "DADOS: GITHUB API", 12, "#73bedc", 700, "end")
    output.append("</svg>")
    return "\n".join(output) + "\n"


def render_report(projects: list[dict]) -> str:
    count = summaries(projects)
    lines = [
        "# Andamento dos projetos",
        "",
        "Inventario automatizado a partir da API do GitHub. **Fase nao equivale a percentual de conclusao**; analisa apenas evidencias de arquivos na branch padrao.",
        "",
        f"**Projetos catalogados:** {count['repos']} | Auditados: {count['scanned']} | Acesso restrito: {count['restricted']} | Com codigo: {count['code']} | Com testes: {count['tests']} | Com CI: {count['ci']} | Com README: {count['docs']}",
        "",
        "As marcacoes significam presenca de arquivos, nao garantem cobertura, testes aprovados ou qualidade. Uma arvore de arquivos truncada e marcada como inspecao parcial.",
        "",
        "| Repositorio | Fase tecnica | Codigo | Testes | CI | README | Ultimo push |",
        "| :-- | :-- | :--: | :--: | :--: | :--: | :-- |",
    ]
    for p in projects:
        checks = (["N/D"] * 4 if p.get("restricted") else
                  ["Sim" if p[x] else "—" for x in ("code", "tests", "ci", "docs")])
        name = p["name"].replace("|", r"\|")
        lines.append(f"| [{name}]({p['url']}) | {stage(p)} | {' | '.join(checks)} | {p['pushed'] or 'Indisponivel'} |")
    lines += [
        "",
        "## Metodologia",
        "",
        "- **Validacao automatizada:** arquivos de teste e workflow GitHub Actions identificados (execucao nao verificada).",
        "- **Com testes:** arquivos de teste encontrados; nenhum workflow detectado.",
        "- **Implementacao:** arquivos de codigo encontrados, sem evidencias de testes.",
        "- **Estruturacao:** README presente, sem codigo identificado.",
        "- **Inspecao parcial:** a API informou arvore truncada; indicadores podem estar incompletos.",
        "- **Acesso restrito:** repositorio privado conhecido, mas sem permissao do GITHUB_TOKEN. N/D nao significa ausencia.",
        "- **Ultimo push:** data da alteracao mais recente no repositorio; nao indica maturidade.",
        "- Um nome de arquivo de teste nao garante que ele seja executado ou aprovado.",
        "",
        "[Voltar ao perfil](../README.md)",
        "",
    ]
    return "\n".join(lines)


def replace_section(readme: str, block: str) -> str:
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("Marcadores unicos do portfolio nao encontrados")
    first = readme.index(START) + len(START)
    last = readme.index(END)
    if first > last:
        raise ValueError("Ordem incorreta de marcadores")
    return readme[:first] + "\n\n" + block + "\n\n" + readme[last:]


def snapshot_marker(now: datetime) -> str:
    """Janela UTC de seis horas para evitar auditorias a cada cinco minutos."""
    if now.tzinfo is None:
        raise ValueError("Horario do snapshot precisa de timezone")
    utc = now.astimezone(timezone.utc)
    window_hour = (utc.hour // 6) * 6
    return f"<!-- PORTFOLIO-SNAPSHOT:v4:{utc:%Y-%m-%d}T{window_hour:02d}Z -->"


def main():
    # O calendario recebe consultas frequentes; a varredura de dezenas de
    # repositorios e limitada a quatro janelas de auditoria por dia (UTC).
    freshness_marker = snapshot_marker(datetime.now(timezone.utc))
    force_refresh = os.environ.get("FORCE_PORTFOLIO_REFRESH", "").lower() in ("true", "1", "yes")
    if not force_refresh and REPORT.exists() and freshness_marker in REPORT.read_text(encoding="utf-8"):
        print("Portfolio ja auditado nesta janela UTC; snapshot preservado")
        return
    projects = collect(os.environ.get("GITHUB_TOKEN", ""))
    svg = render_svg(projects)
    report = freshness_marker + "\n" + render_report(projects)
    version = sha256(svg.encode("utf-8")).hexdigest()[:12]
    block = (
        '<div align="center">\n'
        '  <h2>Portfólio de Projetos</h2>\n'
        '  <p><sub>Visão executiva de estágio técnico, validação e últimas movimentações dos repositórios.</sub></p>\n'
        '  <a href="docs/ANDAMENTO_DOS_PROJETOS.md">\n'
        f'    <img src="https://raw.githubusercontent.com/{OWNER}/{OWNER}/main/assets/portfolio-andamento.svg?v={version}" width="100%" alt="Panorama tecnico de todos os repositorios"/>\n'
        '  </a>\n'
        '  <p><a href="docs/ANDAMENTO_DOS_PROJETOS.md"><strong>Consultar detalhes dos projetos</strong></a></p>\n'
        '</div>'
    )
    readme = README.read_text(encoding="utf-8")
    updated = replace_section(readme, block)
    for path, content in ((SVG, svg), (REPORT, report), (README, updated)):
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    print(f"Portfolio verificado: {len(projects)} repositorios")


if __name__ == "__main__":
    main()
