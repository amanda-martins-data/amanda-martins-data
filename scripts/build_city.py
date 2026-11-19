"""
build_city.py
--------------
Gera a cidade de contribuições animada do README do perfil
(assets/city-pt.svg e assets/city-en.svg), em vista isométrica.

O último ano vira um bairro: cada semana é um quarteirão de 3x3 lotes,
cada dia é um lote (os outros dois lotes do quarteirão são praças).
Dia com contribuição vira torre, mais alta quanto mais contribuições;
dia sem contribuição vira casa baixa ou árvore.

Animação em SVG puro (SMIL), que roda dentro da tag <img> do GitHub:
janelas acendendo e apagando, carros nas avenidas, antena piscando na
torre do dia mais ativo, estrelas e torres subindo ao carregar.

Uso:
    # no GitHub Actions (calendário oficial, via GraphQL)
    GITHUB_TOKEN=... python scripts/build_city.py --user amanda-martins-data

    # localmente, a partir de um JSON {"AAAA-MM-DD": contagem}
    python scripts/build_city.py --days-json dias.json
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

W, H = 860, 510
BLOCK_COLS = 9                 # quarteirões por linha (53 semanas -> 6 linhas)
STREET = 0.6                   # largura da rua, em lotes
TW = 29.0                      # largura do lote na tela
TH = TW * 0.46                 # altura do lote na tela (ângulo da câmera)
MAX_TOWER = 118                # altura da torre do dia mais ativo
PARK_CELLS = {(1, 1), (2, 0)}  # lotes de praça dentro do quarteirão 3x3

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace"
PINK, PINK_L, CREAM, PURPLE, VIOLET = "#ec4899", "#f9a8d4", "#fce7f3", "#a855f7", "#7c3aed"
WINDOW_COLORS = ["#ffd166", "#f9a8d4", "#fce7f3", "#c4b5fd"]

TEXT = {
    "pt": {
        "tag": "CONTRIBUTION.CITY",
        "sub": "> cada quarteirão é uma semana, cada lote um dia",
        "total": "{n} contribuições no último ano",
        "caption": "dados do GitHub, atualizados todo dia por um GitHub Action",
        "label": "Cidade animada das contribuições no GitHub: {n} no último ano",
    },
    "en": {
        "tag": "CONTRIBUTION.CITY",
        "sub": "> each block is a week, each lot a day",
        "total": "{n} contributions in the last year",
        "caption": "GitHub data, refreshed daily by a GitHub Action",
        "label": "Animated city of GitHub contributions: {n} in the last year",
    },
}

GRAPHQL = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


# --------------------------------------------------------------------------
# Dados
# --------------------------------------------------------------------------
def fetch_days(user: str, token: str) -> tuple[list[int], int]:
    """Contribuições por dia (calendário oficial do GitHub, ~53 semanas) e o total."""
    body = json.dumps({"query": GRAPHQL, "variables": {"login": user}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [d["contributionCount"] for w in cal["weeks"] for d in w["contributionDays"]]
    return days, cal["totalContributions"]


def days_from_json(raw: dict[str, int], today: date | None = None) -> tuple[list[int], int]:
    """Converte {data: contagem} na mesma janela do GitHub (domingo, 52 semanas atrás, até hoje)."""
    today = today or date.today()
    start = today - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    days = [0] * ((today - start).days + 1)
    for d, n in raw.items():
        dt = date.fromisoformat(d)
        if start <= dt <= today:
            days[(dt - start).days] += n
    return days, sum(days)


# --------------------------------------------------------------------------
# Geometria isométrica
# --------------------------------------------------------------------------
def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, font=SANS, size=12, weight=400, fill=CREAM, op=1.0, anchor="start", ls=0):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" fill-opacity="{op}" text-anchor="{anchor}" letter-spacing="{ls}">{esc(s)}</text>')


class Iso:
    def __init__(self, cols: float, rows: float):
        self.ox = W / 2 + (rows - cols) * TW / 4
        self.oy = 104

    def p(self, gx: float, gy: float, z: float = 0.0) -> tuple[float, float]:
        return self.ox + (gx - gy) * TW / 2, self.oy + (gx + gy) * TH / 2 - z


def pts(*ps) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)


def lot_xy(day_index: int) -> tuple[float, float]:
    """Posição (em lotes) do canto de trás do lote de um dia."""
    week, dow = divmod(day_index, 7)
    bx, by = week % BLOCK_COLS, week // BLOCK_COLS
    cells = [(cx, cy) for cy in range(3) for cx in range(3) if (cx, cy) not in PARK_CELLS]
    cx, cy = cells[dow]
    return bx * (3 + STREET) + cx, by * (3 + STREET) + cy


def park_xy(week: int):
    bx, by = week % BLOCK_COLS, week // BLOCK_COLS
    for cx, cy in PARK_CELLS:
        yield bx * (3 + STREET) + cx, by * (3 + STREET) + cy


def box(iso: Iso, gx, gy, h, m, top, left, right, stroke=None, sw=0.6):
    """Prisma sobre o lote (gx, gy), recuado m de cada lado; devolve o SVG e os vértices."""
    a, b = gx + m, gy + m
    c, d = gx + 1 - m, gy + 1 - m
    T0, R0, B0, L0 = iso.p(a, b), iso.p(c, b), iso.p(c, d), iso.p(a, d)
    T1, R1, B1, L1 = iso.p(a, b, h), iso.p(c, b, h), iso.p(c, d, h), iso.p(a, d, h)
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-opacity="0.8"' if stroke else ""
    svg = (f'<polygon points="{pts(L0, B0, B1, L1)}" fill="{left}"{st}/>'
           f'<polygon points="{pts(B0, R0, R1, B1)}" fill="{right}"{st}/>'
           f'<polygon points="{pts(T1, R1, B1, L1)}" fill="{top}"{st}/>')
    return svg, (L0, B0, R0, L1, B1, R1)


def face_windows(rng, p0, p1, h, lit=0.55, blink=0.3):
    """Janelas numa face vertical que vai de p0 a p1 (no chão), até a altura h."""
    out = []
    cols = 2
    for row_z in [z for z in frange(7, h - 4, 6.5)]:
        for k in range(cols):
            if rng.random() > lit:
                continue
            u0 = 0.2 + k * 0.38
            u1 = u0 + 0.22
            q0 = (p0[0] + (p1[0] - p0[0]) * u0, p0[1] + (p1[1] - p0[1]) * u0 - row_z)
            q1 = (p0[0] + (p1[0] - p0[0]) * u1, p0[1] + (p1[1] - p0[1]) * u1 - row_z)
            poly = pts(q0, q1, (q1[0], q1[1] - 3), (q0[0], q0[1] - 3))
            col = rng.choice(WINDOW_COLORS)
            if rng.random() < blink:
                dur = rng.uniform(3, 12)
                out.append(f'<polygon points="{poly}" fill="{col}" opacity="0.95">'
                           f'<animate attributeName="opacity" values="0.95;0.95;0.06;0.06;0.95" keyTimes="0;0.5;0.55;0.92;1" '
                           f'dur="{dur:.1f}s" begin="-{rng.uniform(0, dur):.1f}s" repeatCount="indefinite"/></polygon>')
            else:
                out.append(f'<polygon points="{poly}" fill="{col}" opacity="0.9"/>')
    return "".join(out)


def frange(a, b, step):
    while a < b:
        yield a
        a += step


# --------------------------------------------------------------------------
# Elementos
# --------------------------------------------------------------------------
def tower(iso, rng, gx, gy, count, peak, is_peak, order):
    h = 16 + (MAX_TOWER - 16) * math.sqrt(count / peak)
    svg, (L0, B0, R0, L1, B1, R1) = box(iso, gx, gy, h, 0.14, "#3b2a6b", "#1a1433", "#251a48", PURPLE)
    wins = face_windows(rng, L0, B0, h) + face_windows(rng, B0, R0, h)
    top_x, top_y = iso.p(gx + 0.5, gy + 0.5, h)
    roof = f'<circle cx="{top_x:.1f}" cy="{top_y:.1f}" r="1.6" fill="{PINK}" opacity="0.9"/>'
    antenna = ""
    if is_peak:
        antenna = (f'<line x1="{top_x:.1f}" y1="{top_y:.1f}" x2="{top_x:.1f}" y2="{top_y - 14:.1f}" stroke="{PINK_L}" stroke-width="1"/>'
                   f'<circle cx="{top_x:.1f}" cy="{top_y - 15:.1f}" r="2.2" fill="#ef4444">'
                   f'<animate attributeName="opacity" values="1;0.15;1" dur="1.4s" repeatCount="indefinite"/></circle>')
    base_y = B0[1]
    delay = 0.35 + 0.03 * order
    return (f'<g transform="translate(0 {base_y:.1f})"><g>'
            f'<animateTransform attributeName="transform" type="scale" values="1 0;1 0;1 1" '
            f'keyTimes="0;{delay / (delay + 0.8):.3f};1" dur="{delay + 0.8:.2f}s" fill="freeze"/>'
            f'<g transform="translate(0 {-base_y:.1f})">{svg}{wins}{roof}{antenna}</g></g></g>')


def house(iso, rng, gx, gy):
    h = rng.choice([5, 6, 7])
    svg, (L0, B0, R0, *_rest) = box(iso, gx, gy, h, 0.24, "#2a2150", "#151027", "#1d1638")
    if rng.random() < 0.35:   # uma luz acesa em algumas casas
        x, y = iso.p(gx + 0.62, gy + 0.76, 3)
        svg += f'<rect x="{x:.1f}" y="{y - 2:.1f}" width="2" height="2" fill="#ffd166" opacity="0.8"/>'
    return svg


def tree(iso, rng, gx, gy):
    out = []
    for _ in range(rng.choice([1, 2])):
        x, y = iso.p(gx + rng.uniform(0.3, 0.7), gy + rng.uniform(0.3, 0.7))
        r = rng.uniform(2.6, 3.6)
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - 3:.1f}" stroke="#3b2a5c" stroke-width="1"/>'
                   f'<circle cx="{x:.1f}" cy="{y - 3 - r:.1f}" r="{r:.1f}" fill="#134e4a" stroke="#2dd4bf" stroke-opacity="0.35" stroke-width="0.5"/>')
    return "".join(out)


def ground(iso, cols, rows):
    corners = [iso.p(0, 0), iso.p(cols, 0), iso.p(cols, rows), iso.p(0, rows)]
    out = [f'<polygon points="{pts(*corners)}" fill="#120c24" stroke="{PINK}" stroke-opacity="0.7" stroke-width="1.2"/>']
    # avenidas entre os quarteirões
    nb_rows = math.ceil(rows / (3 + STREET))
    for i in range(1, BLOCK_COLS):
        g = i * (3 + STREET) - STREET / 2
        a, b = iso.p(g, 0), iso.p(g, rows)
        out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{VIOLET}" stroke-opacity="0.55" stroke-width="0.8" stroke-dasharray="3 3"/>')
    for j in range(1, nb_rows):
        g = j * (3 + STREET) - STREET / 2
        a, b = iso.p(0, g), iso.p(cols, g)
        out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{VIOLET}" stroke-opacity="0.55" stroke-width="0.8" stroke-dasharray="3 3"/>')
    return "".join(out)


def lot_tiles(iso, n_days):
    out = []
    for i in range(n_days):
        gx, gy = lot_xy(i)
        out.append(f'<polygon points="{pts(iso.p(gx + 0.05, gy + 0.05), iso.p(gx + 0.95, gy + 0.05), iso.p(gx + 0.95, gy + 0.95), iso.p(gx + 0.05, gy + 0.95))}" fill="#1b1433"/>')
    return "".join(out)


def cars(iso, rng, cols, rows):
    out = []
    nb_rows = math.ceil(rows / (3 + STREET))
    lanes = ([("x", j * (3 + STREET) - STREET / 2) for j in range(1, nb_rows)] +
             [("y", i * (3 + STREET) - STREET / 2) for i in range(1, BLOCK_COLS)])
    for axis, g in rng.sample(lanes, min(7, len(lanes))):
        a, b = (iso.p(0, g), iso.p(cols, g)) if axis == "x" else (iso.p(g, 0), iso.p(g, rows))
        if rng.random() < 0.5:
            a, b = b, a
        dur = rng.uniform(9, 16)
        col = rng.choice(["#fde68a", PINK_L, "#67e8f9"])
        out.append(f'<circle r="1.8" fill="{col}"><animateMotion path="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" '
                   f'dur="{dur:.1f}s" begin="-{rng.uniform(0, dur):.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def stars(rng, iso, cols, rows):
    out = []
    top = iso.p(0, 0)[1]
    for _ in range(26):
        x = rng.uniform(30, W - 30)
        y = rng.uniform(64, top + 40)
        # só nos cantos do céu, longe do bairro
        if abs(x - iso.p(0, 0)[0]) < (y - 40) * 2.2:
            continue
        dur = rng.uniform(2.5, 7)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rng.choice([0.7, 0.9, 1.1])}" fill="{CREAM}">'
                   f'<animate attributeName="opacity" values="0.9;0.2;0.9" dur="{dur:.1f}s" begin="-{rng.uniform(0, dur):.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def render(lang: str, days: list[int], total: int) -> str:
    t = TEXT[lang]
    rng = random.Random(20260)          # determinístico: o SVG só muda quando os dados mudam
    weeks = math.ceil(len(days) / 7)
    cols = BLOCK_COLS * (3 + STREET) - STREET
    rows = math.ceil(weeks / BLOCK_COLS) * (3 + STREET) - STREET
    iso = Iso(cols, rows)
    peak = max(days) or 1
    peak_day = days.index(peak) if max(days) else -1

    # Pintor: do fundo (gx+gy pequeno) para a frente
    items = []
    for i, c in enumerate(days):
        gx, gy = lot_xy(i)
        items.append((gx + gy, gx, "day", i, c))
    for w in range(weeks):
        for gx, gy in park_xy(w):
            items.append((gx + gy, gx, "park", gx, gy))
    items.sort()

    objs = []
    order = 0
    for _, _, kind, a, b in items:
        if kind == "day":
            gx, gy = lot_xy(a)
            if b:
                objs.append(tower(iso, rng, gx, gy, b, peak, a == peak_day, order))
                order += 1
            elif rng.random() < 0.62:
                objs.append(house(iso, rng, gx, gy))
            else:
                objs.append(tree(iso, rng, gx, gy))
        else:
            objs.append(tree(iso, rng, a, b))

    total_txt = f"{total:,}".replace(",", "." if lang == "pt" else ",")
    return "".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{esc(t["label"].format(n=total_txt))}">',
        '<defs><linearGradient id="c-bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#0c0a09"/><stop offset="54%" stop-color="#1f1f3d"/><stop offset="100%" stop-color="#0c0a09"/></linearGradient>'
        f'<radialGradient id="c-glow" cx="50%" cy="60%" r="55%"><stop offset="0%" stop-color="{VIOLET}" stop-opacity="0.35"/>'
        f'<stop offset="100%" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="c-frame"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18"/></clipPath></defs>',
        '<g clip-path="url(#c-frame)">',
        f'<rect width="{W}" height="{H}" fill="url(#c-bg)"/><rect width="{W}" height="{H}" fill="url(#c-glow)"/>',
        stars(rng, iso, cols, rows),
        ground(iso, cols, rows),
        lot_tiles(iso, len(days)),
        cars(iso, rng, cols, rows),
        "".join(objs),
        f'<rect x="0" y="{H - 34}" width="{W}" height="34" fill="#07060d" fill-opacity="0.7"/>',
        text(32, H - 13, t["caption"], MONO, 11.5, 400, CREAM, 0.6),
        "</g>",
        text(32, 42, t["tag"], MONO, 13, 700, PINK, 1, ls=2),
        text(32 + len(t["tag"]) * 9.6 + 16, 42, t["sub"], MONO, 12, 400, CREAM, 0.7),
        text(W - 32, 42, t["total"].format(n=total_txt), MONO, 12.5, 700, PINK_L, 1, "end"),
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="{PINK}" stroke-opacity="0.55" stroke-width="1.5"/>',
        "</svg>\n",
    ])


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera a cidade de contribuições animada.")
    ap.add_argument("--user", default="amanda-martins-data")
    ap.add_argument("--days-json", help="JSON {data: contagem} para gerar sem acessar a API")
    ap.add_argument("--out", default=str(ASSETS))
    args = ap.parse_args()

    if args.days_json:
        days, total = days_from_json(json.loads(Path(args.days_json).read_text()))
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            print("GITHUB_TOKEN não definido; use --days-json para gerar localmente.", file=sys.stderr)
            return 1
        days, total = fetch_days(args.user, token)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for lang in TEXT:
        (out / f"city-{lang}.svg").write_text(render(lang, days, total), encoding="utf-8")
    active = sum(1 for d in days if d)
    print(f"{len(days)} dias, {active} com contribuição, {total} no total, pico de {max(days)} num dia")
    return 0


if __name__ == "__main__":
    sys.exit(main())
