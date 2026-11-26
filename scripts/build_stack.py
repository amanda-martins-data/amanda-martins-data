"""Gera assets/stack-pt.svg e assets/stack-en.svg.

Duas partes: o que é usado no trabalho (em produção) e o que foi praticado
só nos projetos do portfólio. O estilo segue os outros cartões do README.
"""
from pathlib import Path
from xml.sax.saxutils import escape

MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

TEXTOS = {
    "pt": {
        "sub": "&gt; o que uso no trabalho e o que pratiquei no portfólio",
        "prod": ("EM PRODUÇÃO", "uso no trabalho"),
        "port": ("NO PORTFÓLIO", "projetos próprios com dados públicos"),
        "linhas_prod": [
            ("Linguagens e dados", ["Python", "SQL", "PostgreSQL", "DuckDB"]),
            ("Azure", ["ADLS Gen2", "Container Apps", "Key Vault", "Entra ID"]),
            ("Entrega e testes", ["Docker", "GitHub Actions", "Azure DevOps", "pytest"]),
            ("APIs, BI e IA", ["FastAPI", "APIs REST", "Power BI", "LLMs (Claude)"]),
        ],
        "linhas_port": [
            ("Processamento e modelagem", ["PySpark", "Databricks", "Delta Lake", "dbt", "Snowflake"]),
            ("Orquestração e governança", ["Airflow", "Great Expectations", "Unity Catalog"]),
            ("Nuvem e infraestrutura", ["AWS (S3, Lambda, RDS)", "Terraform"]),
        ],
    },
    "en": {
        "sub": "&gt; what I use at work and what I practiced in the portfolio",
        "prod": ("IN PRODUCTION", "used at work"),
        "port": ("PORTFOLIO", "personal projects on public data"),
        "linhas_prod": [
            ("Languages and data", ["Python", "SQL", "PostgreSQL", "DuckDB"]),
            ("Azure", ["ADLS Gen2", "Container Apps", "Key Vault", "Entra ID"]),
            ("Delivery and tests", ["Docker", "GitHub Actions", "Azure DevOps", "pytest"]),
            ("APIs, BI and AI", ["FastAPI", "REST APIs", "Power BI", "LLMs (Claude)"]),
        ],
        "linhas_port": [
            ("Processing and modeling", ["PySpark", "Databricks", "Delta Lake", "dbt", "Snowflake"]),
            ("Orchestration and governance", ["Airflow", "Great Expectations", "Unity Catalog"]),
            ("Cloud and infrastructure", ["AWS (S3, Lambda, RDS)", "Terraform"]),
        ],
    },
}

ROSA = {"fill": "#ec4899", "fill_op": "0.10", "stroke": "#f9a8d4", "dash": ""}
VIOLETA = {"fill": "#7c3aed", "fill_op": "0.08", "stroke": "#c4b5fd", "dash": ' stroke-dasharray="4 3"'}


def texto(x, y, s, fonte, tam, peso, cor, op="1", esp="0"):
    return (f'<text x="{x}" y="{y}" font-family="{fonte}" font-size="{tam}" font-weight="{peso}" '
            f'fill="{cor}" fill-opacity="{op}" text-anchor="start" letter-spacing="{esp}">{s}</text>')


def chips(y, itens, estilo):
    out, x = [], 290
    for item in itens:
        w = round(7.45 * len(item) + 22)
        out.append(f'<rect x="{x}" y="{y - 17}" width="{w}" height="24" rx="12" fill="{estilo["fill"]}" '
                   f'fill-opacity="{estilo["fill_op"]}" stroke="{estilo["stroke"]}" stroke-opacity="0.6"{estilo["dash"]}/>')
        out.append(texto(x + 11, y - 0.5, escape(item), MONO, 12, 400, "#fce7f3"))
        x += w + 8
    assert x <= 836, f"linha larga demais: {itens}"
    return out


def svg(t):
    y, corpo = 96, []
    for titulo, sub, linhas, estilo, cor in [
        (*t["prod"], t["linhas_prod"], ROSA, "#ec4899"),
        (*t["port"], t["linhas_port"], VIOLETA, "#a78bfa"),
    ]:
        corpo.append(texto(32, y, titulo, MONO, 12, 700, cor, esp="2"))
        corpo.append(texto(32 + len(titulo) * 9.6 + 14, y, f"· {sub}", MONO, 12, 400, "#fce7f3", op="0.6"))
        y += 36
        for rotulo, itens in linhas:
            corpo.append(texto(32, y, rotulo, SANS, 13, 600, "#f9a8d4"))
            corpo += chips(y, itens, estilo)
            y += 40
        y += 14
    h = y - 14
    cab = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{h}" viewBox="0 0 860 {h}" role="img" aria-label="stack">
<defs>
<linearGradient id="stack-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0c0a09"/><stop offset="54%" stop-color="#1f1f3d"/><stop offset="100%" stop-color="#0c0a09"/></linearGradient>
<radialGradient id="stack-o1" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ec4899" stop-opacity="0.55"/><stop offset="60%" stop-color="#ec4899" stop-opacity="0.12"/><stop offset="100%" stop-color="#ec4899" stop-opacity="0"/></radialGradient>
<radialGradient id="stack-o2" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#7c3aed" stop-opacity="0.5"/><stop offset="60%" stop-color="#7c3aed" stop-opacity="0.1"/><stop offset="100%" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>
<linearGradient id="stack-line" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ec4899"/><stop offset="100%" stop-color="#a855f7"/></linearGradient>
<clipPath id="stack-clip"><rect x="1" y="1" width="858" height="{h - 2}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#stack-clip)">
<rect width="860" height="{h}" fill="url(#stack-bg)"/>
<circle cx="103.2" cy="26.4" r="237.6" fill="url(#stack-o1)"/>
<circle cx="791.2" cy="{h - 13}" r="211.2" fill="url(#stack-o2)"/>
</g>
<rect x="1" y="1" width="858" height="{h - 2}" rx="18" fill="none" stroke="#ec4899" stroke-opacity="0.55" stroke-width="1.5"/>
{texto(32, 44, "STACK.SCAN", MONO, 13, 700, "#ec4899", esp="2")}
{texto(150, 44, t["sub"], MONO, 12, 400, "#fce7f3", op="0.6")}
<line x1="32" y1="60" x2="828" y2="60" stroke="url(#stack-line)" stroke-opacity="0.7"/>
'''
    return cab + "\n".join(corpo) + "\n</svg>\n"


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent.parent
    for lang, t in TEXTOS.items():
        (raiz / "assets" / f"stack-{lang}.svg").write_text(svg(t), encoding="utf-8")
