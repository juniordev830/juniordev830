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
                "pushed": "", "docs": False, "code": False,
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
    count = summaries(projects)
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1060" height="602" viewBox="0 0 1060 602" role="img" aria-label="Andamento tecnico dos projetos: documentacao, codigo, testes, pipelines e fases observadas">',
        '<rect width="1060" height="602" rx="18" fill="#0d141e"/>',
        '<rect x="1" y="1" width="1058" height="600" rx="17" fill="none" stroke="#303d49"/>',
    ]

    def rect(x, y, w, h, fill="#14212d", border="#344555", radius=10):
        lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{border}"/>')

    def txt(x, y, value, size=15, color="#e3ebf1", weight="400"):
        lines.append(f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(str(value))}</text>')

    txt(34, 47, "PORTFOLIO  /  ENGENHARIA DE SOFTWARE", 13, "#83b7d3", "700")
    txt(34, 91, "Andamento tecnico dos projetos", 31, "#f0f5fa", "700")
    txt(34, 119, "Evidencias observaveis nos repositorios  |  nao representam percentual concluido", 15, "#98aabd")

    cards = [("Com documentacao", count["docs"]), ("Com codigo", count["code"]),
             ("Com testes", count["tests"]), ("Com pipelines", count["ci"])]
    for i, (label, value) in enumerate(cards):
        x = 34 + i * 254
        rect(x, 150, 236, 92)
        txt(x + 18, 177, label, 14, "#9db1c3")
        txt(x + 18, 220, value, 33, "#e6f4ff", "700")
        txt(x + 188, 216, f"/ {count['scanned']}", 13, "#71899b")

    rect(34, 264, 616, 271)
    txt(55, 299, "FASES IDENTIFICADAS", 14, "#d7e6ef", "700")
    txt(55, 319, "Criterio: evidencias de codigo, testes e workflow", 12, "#91a6b8")
    rows = [
        ("Validacao automatizada", count["validated"], "#57b3da"),
        ("Testes sem pipeline", count["with_tests"], "#7ea6d3"),
        ("Implementacao", count["implementing"], "#8cb1ca"),
        ("Estruturacao / revisao", count["structuring"], "#8ca1b2"),
        ("Acesso restrito", count["restricted"], "#9e93af"),
    ]
    for i, (name, qty, color) in enumerate(rows):
        y = 347 + i * 39
        txt(55, y, name, 14)
        rect(290, y - 13, 268, 13, "#263342", "#263342", 5)
        if qty:
            rect(290, y - 13, max(4, round(268 * qty / max(1, count["repos"]))), 13, color, color, 5)
        txt(580, y, qty, 16, "#f0f5fa", "700")

    rect(668, 264, 358, 271)
    txt(688, 299, "ULTIMAS MOVIMENTACOES", 14, "#d7e6ef", "700")
    latest = sorted(projects, key=lambda project: (project["pushed"], project["name"]), reverse=True)[:6]
    for i, item in enumerate(latest):
        y = 331 + i * 33
        name = item["name"]
        if len(name) > 27:
            name = name[:25] + ".."
        txt(688, y, name, 13, "#e0edf7", "600")
        txt(950, y, item["pushed"][8:10] + "/" + item["pushed"][5:7] if item["pushed"] else "-", 12, "#8ca8bb")
        if i != 5:
            lines.append(f'<line x1="687" y1="{y+8}" x2="1004" y2="{y+8}" stroke="#2b3a48"/>')
    txt(34, 567, f"Catalogados: {count['repos']}  |  Auditados: {count['scanned']}  |  Restritos: {count['restricted']}", 14, "#b1c7d7")
    txt(34, 586, "Fonte: GitHub API  -  sinais tecnicos, nao medicao de entrega funcional", 12, "#748fa1")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


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


def main():
    # O calendario de contribuicoes atualiza com frequencia; a auditoria de
    # arvores de dezenas de repositorios executa apenas uma vez ao dia (UTC).
    snapshot_day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    freshness_marker = f"<!-- PORTFOLIO-SNAPSHOT:v2:{snapshot_day} -->"
    if REPORT.exists() and freshness_marker in REPORT.read_text(encoding="utf-8"):
        print("Portfolio ja auditado hoje; snapshot preservado")
        return
    projects = collect(os.environ.get("GITHUB_TOKEN", ""))
    svg = render_svg(projects)
    report = freshness_marker + "\n" + render_report(projects)
    version = sha256(svg.encode("utf-8")).hexdigest()[:12]
    block = (
        '<div align="center">\n'
        '  <h2>Andamento dos projetos</h2>\n'
        '  <p><sub>Visao tecnica de documentacao, codigo, testes e automacao — sem percentuais inventados.</sub></p>\n'
        '  <a href="docs/ANDAMENTO_DOS_PROJETOS.md">\n'
        f'    <img src="https://raw.githubusercontent.com/{OWNER}/{OWNER}/main/assets/portfolio-andamento.svg?v={version}" width="100%" alt="Panorama tecnico de todos os repositorios"/>\n'
        '  </a>\n'
        '  <p><a href="docs/ANDAMENTO_DOS_PROJETOS.md"><strong>Ver andamento individual de todos os projetos</strong></a></p>\n'
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
