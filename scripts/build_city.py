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


# --------------------------------------------------------------------------
# Eventos do dia: clima sorteado pela data, mais Natal e Ano-Novo
# --------------------------------------------------------------------------
WEATHER = ["clear", "sun", "rain", "fog", "plane"]
EVENT_LABEL = {
    "pt": {"clear": "noite limpa", "sun": "pôr do sol", "rain": "chuva", "fog": "névoa",
           "plane": "tráfego aéreo", "christmas": "Feliz Natal", "newyear": "Feliz {year}"},
    "en": {"clear": "clear night", "sun": "sunset", "rain": "rain", "fog": "fog",
           "plane": "air traffic", "christmas": "Merry Christmas", "newyear": "Happy {year}"},
}


def today_sp() -> date:
    """Data de hoje em São Paulo (o Action roda de madrugada, em UTC)."""
    try:
        from zoneinfo import ZoneInfo
        from datetime import datetime
        return datetime.now(ZoneInfo("America/Sao_Paulo")).date()
    except Exception:
        return date.today()


def pick_event(day: date) -> str:
    """Natal de 20 a 26/12, Ano-Novo em 31/12 e 01/01; nos outros dias,
    um clima sorteado com a data como semente (o mesmo o dia inteiro)."""
    if day.month == 12 and 20 <= day.day <= 26:
        return "christmas"
    if (day.month == 12 and day.day == 31) or (day.month == 1 and day.day == 1):
        return "newyear"
    return random.Random(day.toordinal()).choice(WEATHER)


def falling_field(rng, n, w, h, draw, dur, sway=0):
    """Campo de partículas caindo sem emenda: duas cópias empilhadas que
    descem uma altura inteira e recomeçam. sway > 0 balança de lado."""
    items = "".join(draw(rng.uniform(0, w), rng.uniform(0, h)) for _ in range(n))
    inner = f'<g>{items}</g><g transform="translate(0 {-h})">{items}</g>'
    if sway:
        inner = (f'<g>{inner}<animateTransform attributeName="transform" type="translate" '
                 f'values="{-sway} 0;{sway} 0;{-sway} 0" dur="{dur / 2:.1f}s" repeatCount="indefinite"/></g>')
    return (f'<g>{inner}<animateTransform attributeName="transform" type="translate" values="0 0;0 {h}" '
            f'dur="{dur}s" repeatCount="indefinite"/></g>')


def ground_point(rng, iso, cols, rows):
    return iso.p(rng.uniform(0.5, cols - 0.5), rng.uniform(0.5, rows - 0.5))


GLOW_DEFS = ('<filter id="c-glow8" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="8"/></filter>'
             '<filter id="c-glow3" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3"/></filter>'
             '<filter id="c-blur" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>')


def moon(x, y):
    return (f'<g transform="translate({x} {y})"><circle r="30" fill="#fce7f3" opacity="0.22" filter="url(#c-glow8)"/>'
            '<circle r="17" fill="#fdf2f8"/><circle cx="-5" cy="-4" r="3.4" fill="#f5d0e6"/>'
            '<circle cx="6" cy="5" r="2.4" fill="#f5d0e6"/><circle cx="3" cy="-8" r="1.6" fill="#f5d0e6"/></g>')


def shooting_stars(rng):
    out = []
    for k in range(3):
        x, y = rng.uniform(120, 700), rng.uniform(70, 150)
        dur, begin = rng.uniform(7, 11), rng.uniform(0, 8)
        out.append(
            f'<g opacity="0"><line x1="0" y1="0" x2="-46" y2="-16" stroke="url(#c-tail)" stroke-width="1.8" stroke-linecap="round"/>'
            f'<circle r="1.6" fill="#ffffff"/>'
            f'<animateMotion path="M{x:.0f},{y:.0f} l130,45" keyPoints="0;0;1;1" keyTimes="0;0.85;0.93;1" calcMode="linear" '
            f'dur="{dur:.1f}s" begin="-{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.85;0.88;0.93;1" dur="{dur:.1f}s" '
            f'begin="-{begin:.1f}s" repeatCount="indefinite"/></g>')
    return ('<defs><linearGradient id="c-tail" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#ffffff"/>'
            '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>' + "".join(out))


def birds(rng):
    out = []
    for k in range(5):
        x0, y0 = 900 + k * 26, rng.uniform(95, 140)
        dur = 26
        out.append(
            f'<g><path d="M-6 0 Q-3 -4 0 0 Q3 -4 6 0" fill="none" stroke="#1f1147" stroke-width="1.5" stroke-linecap="round">'
            f'<animateTransform attributeName="transform" type="scale" values="1 1;1 -0.4;1 1" dur="{rng.uniform(0.5, 0.8):.2f}s" '
            f'repeatCount="indefinite"/></path>'
            f'<animateMotion path="M{x0:.0f},{y0:.0f} C600,{y0 - 30:.0f} 300,{y0 + 20:.0f} -80,{y0 - 10:.0f}" '
            f'dur="{dur}s" begin="-{k * 0.6:.1f}s" repeatCount="indefinite"/></g>')
    return "".join(out)


def sun_scene(rng):
    """Sol synthwave listrado com feixes de luz, céu de entardecer."""
    stripes = "".join(f'<rect x="-60" y="{y}" width="120" height="{h}" fill="#000"/>'
                      for y, h in [(6, 2), (14, 3), (23, 4), (33, 5)])
    beams = "".join(
        f'<polygon points="0,0 {-560 * math.cos(math.radians(a)):.0f},{560 * math.sin(math.radians(a)):.0f} '
        f'{-560 * math.cos(math.radians(a + 4)):.0f},{560 * math.sin(math.radians(a + 4)):.0f}" fill="#fde68a" fill-opacity="0.07"/>'
        for a in range(4, 70, 11))
    return ('<defs><linearGradient id="c-dusk" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#2a1250" stop-opacity="0.3"/><stop offset="0.35" stop-color="#be185d" stop-opacity="0.32"/>'
            '<stop offset="0.6" stop-color="#fb923c" stop-opacity="0.18"/><stop offset="1" stop-color="#fb923c" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="c-sunfill" cx="50%" cy="0%" r="100%"><stop offset="0" stop-color="#fde68a"/>'
            f'<stop offset="0.6" stop-color="#fb923c"/><stop offset="1" stop-color="{PINK}"/></radialGradient>'
            '<mask id="c-stripes"><rect x="-60" y="-60" width="120" height="120" fill="#fff"/>' + stripes + '</mask></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#c-dusk)"/>'
            f'<g transform="translate(720 150)"><g>{beams}<animateTransform attributeName="transform" type="rotate" '
            'values="-4;4;-4" dur="18s" repeatCount="indefinite"/></g>'
            '<circle r="70" fill="#fb923c" opacity="0.35" filter="url(#c-glow8)"/>'
            '<g mask="url(#c-stripes)"><circle r="44" fill="url(#c-sunfill)"/></g></g>')


def xmas_tree(rng, x, y):
    """Árvore de Natal com camadas sombreadas, neve, guirlandas de luzes em sequência,
    bolas, estrela com raios e presentes isométricos na base."""
    out = [f'<ellipse cx="{x:.0f}" cy="{y + 4:.0f}" rx="78" ry="30" fill="#fde68a" opacity="0.2" filter="url(#c-glow8)">'
           '<animate attributeName="opacity" values="0.14;0.26;0.14" dur="3s" repeatCount="indefinite"/></ellipse>',
           f'<circle cx="{x:.0f}" cy="{y - 60:.0f}" r="62" fill="#4ade80" opacity="0.08" filter="url(#c-glow8)"/>',
           f'<rect x="{x - 5:.0f}" y="{y - 16:.0f}" width="10" height="18" fill="#92400e"/>'
           f'<rect x="{x:.0f}" y="{y - 16:.0f}" width="5" height="18" fill="#451a03" opacity="0.6"/>']
    tiers = [(42, 12, 34), (35, 35, 32), (28, 57, 29), (20, 77, 26), (13, 95, 22)]
    colors = ["#ef4444", "#fde047", "#60a5fa", "#f472b6", "#c084fc", "#ffffff", "#4ade80"]
    bulb_i = 0
    for t, (wd, b, h) in enumerate(tiers):
        base, apex = y - b, y - b - h
        n = 6
        sc = "".join(f' Q{x - wd + (i + 0.5) * 2 * wd / n:.1f},{base + 6:.1f} {x - wd + (i + 1) * 2 * wd / n:.1f},{base:.1f}' for i in range(n))
        out.append(f'<path d="M{x - wd:.1f},{base:.1f}{sc} L{x:.1f},{apex:.1f} Z" fill="#15803d"/>')
        out.append(f'<path d="M{x:.1f},{apex:.1f} L{x + wd:.1f},{base:.1f}'
                   + "".join(f' Q{x + wd - (i + 0.5) * 2 * wd / n:.1f},{base + 6:.1f} {x + wd - (i + 1) * 2 * wd / n:.1f},{base:.1f}' for i in range(n // 2))
                   + ' Z" fill="#052e16" opacity="0.5"/>')
        out.append(f'<line x1="{x:.1f}" y1="{apex:.1f}" x2="{x - wd:.1f}" y2="{base:.1f}" stroke="#86efac" stroke-opacity="0.55" stroke-width="1"/>')
        out.append("".join(f'<ellipse cx="{x - wd + (i + 0.5) * 2 * wd / n:.1f}" cy="{base + 4.5:.1f}" rx="{wd / n * 0.7:.1f}" ry="1.6" '
                           f'fill="#ffffff" opacity="{0.9 if i < n / 2 else 0.55}"/>' for i in range(n)))
        # guirlanda diagonal com luzes em sequência
        p0 = (x - wd * 0.9, base - h * 0.08)
        p2 = (x + wd * 0.75, base - h * 0.55)
        p1 = ((p0[0] + p2[0]) / 2, (p0[1] + p2[1]) / 2 + 9)
        out.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} Q{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="none" '
                   'stroke="#fde68a" stroke-opacity="0.5" stroke-width="0.8"/>')
        k = max(4, int(wd / 5))
        for j in range(k):
            u = (j + 0.5) / k
            bx = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0]
            by = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]
            c = colors[bulb_i % len(colors)]
            begin = bulb_i * 0.11
            bulb_i += 1
            out.append(f'<g><circle cx="{bx:.1f}" cy="{by:.1f}" r="4" fill="{c}" opacity="0.35"/>'
                       f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="1.9" fill="{c}"/>'
                       f'<animate attributeName="opacity" values="0.25;1;0.25" dur="2.2s" begin="-{begin:.2f}s" repeatCount="indefinite"/></g>')
        # bolas
        for _ in range(2 if t < 4 else 0):
            v = rng.uniform(0.3, 0.6)
            half = wd * (1 - v) * 0.75
            ox, oy = x + rng.uniform(-half, half), base - h * v
            c = rng.choice(["#ef4444", "#f472b6", "#a855f7", "#fbbf24", "#38bdf8"])
            out.append(f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="3" fill="{c}"/>'
                       f'<circle cx="{ox - 1:.1f}" cy="{oy - 1:.1f}" r="0.9" fill="#ffffff" opacity="0.8"/>')
    # estrela com raios girando
    sy = y - 95 - 22 - 4
    pts = " ".join(f'{x + (9 if i % 2 == 0 else 4) * math.sin(math.radians(i * 36)):.1f},'
                   f'{sy - (9 if i % 2 == 0 else 4) * math.cos(math.radians(i * 36)):.1f}' for i in range(10))
    beams = "".join(f'<polygon points="0,0 {30 * math.cos(math.radians(a)):.1f},{30 * math.sin(math.radians(a)):.1f} '
                    f'{30 * math.cos(math.radians(a + 6)):.1f},{30 * math.sin(math.radians(a + 6)):.1f}"/>' for a in range(0, 360, 30))
    out.append(f'<g transform="translate({x:.0f} {sy:.0f})"><g fill="#fde68a" opacity="0.35">{beams}'
               '<animateTransform attributeName="transform" type="rotate" values="0;360" dur="14s" repeatCount="indefinite"/></g>'
               '<circle r="14" fill="#fde047" opacity="0.5" filter="url(#c-glow3)">'
               '<animate attributeName="opacity" values="0.3;0.8;0.3" dur="2s" repeatCount="indefinite"/></circle></g>'
               f'<polygon points="{pts}" fill="#fde047" stroke="#fef9c3" stroke-width="0.8"/>')
    # presentes isométricos
    def gift(gx, gy, s, h, top, left, right):
        t = s * 0.5
        rib = "#fde68a"
        return (f'<polygon points="{gx - s:.1f},{gy - h:.1f} {gx:.1f},{gy - h + t:.1f} {gx:.1f},{gy + t:.1f} {gx - s:.1f},{gy:.1f}" fill="{left}"/>'
                f'<polygon points="{gx + s:.1f},{gy - h:.1f} {gx:.1f},{gy - h + t:.1f} {gx:.1f},{gy + t:.1f} {gx + s:.1f},{gy:.1f}" fill="{right}"/>'
                f'<polygon points="{gx:.1f},{gy - h - t:.1f} {gx + s:.1f},{gy - h:.1f} {gx:.1f},{gy - h + t:.1f} {gx - s:.1f},{gy - h:.1f}" fill="{top}"/>'
                f'<line x1="{gx - s / 2:.1f}" y1="{gy - h + t / 2:.1f}" x2="{gx - s / 2:.1f}" y2="{gy + t / 2:.1f}" stroke="{rib}" stroke-width="1.4"/>'
                f'<line x1="{gx + s / 2:.1f}" y1="{gy - h + t / 2:.1f}" x2="{gx + s / 2:.1f}" y2="{gy + t / 2:.1f}" stroke="{rib}" stroke-width="1.4"/>'
                f'<line x1="{gx - s / 2:.1f}" y1="{gy - h - t / 2:.1f}" x2="{gx + s / 2:.1f}" y2="{gy - h + t / 2:.1f}" stroke="{rib}" stroke-width="1.4"/>'
                f'<line x1="{gx + s / 2:.1f}" y1="{gy - h - t / 2:.1f}" x2="{gx - s / 2:.1f}" y2="{gy - h + t / 2:.1f}" stroke="{rib}" stroke-width="1.4"/>'
                f'<circle cx="{gx - 2:.1f}" cy="{gy - h - 1.5:.1f}" r="1.8" fill="none" stroke="{rib}" stroke-width="1.2"/>'
                f'<circle cx="{gx + 2:.1f}" cy="{gy - h - 1.5:.1f}" r="1.8" fill="none" stroke="{rib}" stroke-width="1.2"/>')
    out.append(gift(x - 30, y + 2, 10, 11, "#f9a8d4", "#ec4899", "#9d174d")
               + gift(x + 30, y + 1, 9, 9, "#c4b5fd", "#8b5cf6", "#5b21b6")
               + gift(x + 13, y + 13, 7, 7, "#a5f3fc", "#22d3ee", "#0e7490")
               + gift(x - 14, y + 14, 8, 6, "#fde68a", "#f59e0b", "#92400e"))
    return "".join(out)


def event_back(event: str, rng: random.Random) -> str:
    """Camada atrás da cidade (céu)."""
    if event == "clear":
        return moon(735, 105) + shooting_stars(rng)
    if event == "sun":
        return sun_scene(rng) + birds(rng)
    if event == "rain":
        clouds = "".join(
            f'<ellipse cx="{rng.uniform(40, W - 40):.0f}" cy="{rng.uniform(40, 120):.0f}" rx="{rng.uniform(110, 190):.0f}" '
            f'ry="{rng.uniform(26, 40):.0f}" fill="#0b0716" fill-opacity="0.85" filter="url(#c-blur)">'
            f'<animateTransform attributeName="transform" type="translate" values="-30 0;30 0;-30 0" '
            f'dur="{rng.uniform(30, 45):.0f}s" repeatCount="indefinite"/></ellipse>' for _ in range(8))
        return clouds
    if event == "plane":
        far = ('<g><path d="M-6 0 L5 -0.6 L7 0 L5 0.6 Z M0 0 L-2 -3.5 L-0.5 -3.5 L2.5 0 Z M0 0 L-2 3.5 L-0.5 3.5 L2.5 0 Z" '
               'fill="#c4b5fd" opacity="0.6"/><circle cx="-2" cy="0" r="0.9" fill="#ffffff">'
               '<animate attributeName="opacity" values="1;0;0;1" dur="1.6s" repeatCount="indefinite"/></circle>'
               '<animateMotion path="M900,80 C620,95 300,70 -40,96" dur="26s" begin="-9s" repeatCount="indefinite" rotate="auto"/></g>')
        path = "M-60,170 C200,80 520,70 920,120"
        trail = (f'<path d="{path}" pathLength="1" fill="none" stroke="#e9d5ff" stroke-width="2.2" stroke-opacity="0.35" '
                 'stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1">'
                 '<animate attributeName="stroke-dashoffset" values="1;0;0" keyTimes="0;0.86;1" dur="15s" repeatCount="indefinite"/>'
                 '<animate attributeName="stroke-opacity" values="0.4;0.4;0" keyTimes="0;0.86;1" dur="15s" repeatCount="indefinite"/></path>')
        plane = ('<g><path d="M-16 0 L12 -1.5 L18 0 L12 1.5 Z M2 0 L-4 -10 L0 -10 L8 0 Z M2 0 L-4 10 L0 10 L8 0 Z '
                 'M-14 0 L-18 -5 L-16 -5 L-11 0 Z M-14 0 L-18 5 L-16 5 L-11 0 Z" fill="#f5f3ff"/>'
                 '<circle cx="-3" cy="-10" r="1.6" fill="#ef4444"><animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/></circle>'
                 '<circle cx="-3" cy="10" r="1.6" fill="#22c55e"><animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/></circle>'
                 '<circle cx="-17" cy="0" r="3" fill="#ffffff" filter="url(#c-glow3)"><animate attributeName="opacity" values="0;0;1;0;0" '
                 'keyTimes="0;0.7;0.75;0.8;1" dur="1.1s" repeatCount="indefinite"/></circle>'
                 f'<animateMotion path="{path}" keyPoints="0;1;1" keyTimes="0;0.86;1" calcMode="linear" dur="15s" '
                 'repeatCount="indefinite" rotate="auto"/></g>')
        return moon(120, 95) + far + trail + plane
    if event == "christmas":
        sleigh = ('<g fill="#1f1147"><path d="M0 0 h18 q4 0 4 -5 h3 q-1 9 -9 9 h-17 z"/>'
                  + "".join(f'<ellipse cx="{-14 - k * 13}" cy="-3" rx="5" ry="2.6"/><line x1="{-11 - k * 13}" y1="-4" x2="{-9 - k * 13}" '
                            f'y2="-9" stroke="#1f1147" stroke-width="1.2"/>' for k in range(3))
                  + '<line x1="-40" y1="-3" x2="0" y2="0" stroke="#1f1147" stroke-width="0.8"/>'
                  '<animateMotion path="M920,60 C800,140 640,60 520,120" dur="20s" begin="-6s" repeatCount="indefinite"/></g>')
        return moon(700, 100) + sleigh
    return ""


def event_front(event: str, rng: random.Random, iso: "Iso", cols: float, rows: float, year: int) -> str:
    """Camada na frente da cidade (chuva, névoa, neve, fogos, árvore)."""
    if event == "rain":
        far = falling_field(rng, 160, W, H, lambda x, y: f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - 2:.0f}" y2="{y + 8:.0f}" '
                            'stroke="#a78bfa" stroke-opacity="0.35" stroke-width="0.7"/>', 1.3)
        near = falling_field(rng, 70, W, H, lambda x, y: f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - 4:.0f}" y2="{y + 16:.0f}" '
                             'stroke="#ddd6fe" stroke-opacity="0.6" stroke-width="1.2"/>', 0.7)
        splashes = []
        for _ in range(45):
            x, y = ground_point(rng, iso, cols, rows)
            dur = rng.uniform(0.8, 1.4)
            begin = rng.uniform(0, dur)
            splashes.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="0" ry="0" fill="none" stroke="#c4b5fd" stroke-width="0.8">'
                            f'<animate attributeName="rx" values="0;5" dur="{dur:.2f}s" begin="-{begin:.2f}s" repeatCount="indefinite"/>'
                            f'<animate attributeName="ry" values="0;2.2" dur="{dur:.2f}s" begin="-{begin:.2f}s" repeatCount="indefinite"/>'
                            f'<animate attributeName="opacity" values="0.9;0" dur="{dur:.2f}s" begin="-{begin:.2f}s" repeatCount="indefinite"/></ellipse>')
        bx = rng.uniform(260, 600)
        bolt = (f'<g opacity="0"><polyline points="{bx:.0f},70 {bx - 18:.0f},120 {bx + 6:.0f},128 {bx - 14:.0f},185 {bx + 10:.0f},192 {bx - 6:.0f},250" '
                'fill="none" stroke="#f5f3ff" stroke-width="2.4" stroke-linejoin="round"/>'
                f'<polyline points="{bx:.0f},70 {bx - 18:.0f},120 {bx + 6:.0f},128 {bx - 14:.0f},185 {bx + 10:.0f},192 {bx - 6:.0f},250" '
                'fill="none" stroke="#c4b5fd" stroke-width="7" filter="url(#c-glow3)"/>'
                '<animate attributeName="opacity" values="0;0;1;0;0.8;0;0" keyTimes="0;0.8;0.805;0.82;0.835;0.85;1" dur="11s" repeatCount="indefinite"/></g>')
        flash = ('<rect width="100%" height="100%" fill="#ede9fe" opacity="0">'
                 '<animate attributeName="opacity" values="0;0;0.3;0;0.16;0;0" keyTimes="0;0.8;0.805;0.82;0.835;0.85;1" '
                 'dur="11s" repeatCount="indefinite"/></rect>')
        return (f'<rect width="{W}" height="{H}" fill="#05030b" fill-opacity="0.32"/>' + far + "".join(splashes)
                + near + bolt + flash)
    if event == "fog":
        lamps = []
        for _ in range(26):
            x, y = ground_point(rng, iso, cols, rows)
            lamps.append(f'<circle cx="{x:.0f}" cy="{y - 6:.0f}" r="9" fill="#fde68a" opacity="0.25" filter="url(#c-glow3)"/>'
                         f'<circle cx="{x:.0f}" cy="{y - 6:.0f}" r="1.3" fill="#fef3c7"/>')
        bands = []
        for k in range(7):
            y = 120 + k * 52 + rng.uniform(-12, 12)
            dur = rng.uniform(24, 40)
            bands.append(f'<ellipse cx="{W / 2:.0f}" cy="{y:.0f}" rx="{rng.uniform(320, 460):.0f}" ry="{rng.uniform(20, 32):.0f}" '
                         f'fill="#e9d5ff" fill-opacity="{rng.uniform(0.12, 0.2):.2f}" filter="url(#c-blur)">'
                         f'<animateTransform attributeName="transform" type="translate" values="{-110 if k % 2 else 110} 0;'
                         f'{110 if k % 2 else -110} 0;{-110 if k % 2 else 110} 0" dur="{dur:.0f}s" repeatCount="indefinite"/></ellipse>')
        texture = ('<filter id="c-mist" x="0" y="0" width="100%" height="100%">'
                   '<feTurbulence type="fractalNoise" baseFrequency="0.004 0.018" numOctaves="3" seed="7"/>'
                   '<feColorMatrix values="0 0 0 0 0.91  0 0 0 0 0.84  0 0 0 0 1  0 0 0 0.55 -0.12"/></filter>')
        return ('<defs>' + texture + '<linearGradient id="c-haze" x1="0" y1="0" x2="0" y2="1">'
                '<stop offset="0" stop-color="#e9d5ff" stop-opacity="0.05"/><stop offset="0.6" stop-color="#e9d5ff" stop-opacity="0.2"/>'
                '<stop offset="1" stop-color="#e9d5ff" stop-opacity="0.08"/></linearGradient></defs>'
                + "".join(lamps)
                + f'<rect width="{W}" height="{H}" fill="url(#c-haze)"/>'
                + f'<g><rect x="-200" y="0" width="{W + 400}" height="{H}" filter="url(#c-mist)" opacity="0.8"/>'
                  '<animateTransform attributeName="transform" type="translate" values="-120 0;120 0;-120 0" dur="50s" repeatCount="indefinite"/></g>'
                + "".join(bands))
    if event == "christmas":
        far = falling_field(rng, 110, W, H, lambda x, y: f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1" fill="#ffffff" fill-opacity="0.6"/>', 14, sway=6)
        near = falling_field(rng, 45, W, H, lambda x, y: f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.1" fill="#ffffff" fill-opacity="0.9"/>', 8, sway=12)
        x, y = iso.p(cols * 0.66, rows * 0.22)
        return far + xmas_tree(rng, x, y) + near
    if event == "newyear":
        colors = ["#f472b6", "#fde047", "#67e8f9", "#ffffff", "#c084fc", "#fb923c", "#4ade80"]
        out = []
        cycle = 6.0
        for k in range(9):
            cx, cy = rng.uniform(110, W - 110), rng.uniform(80, 210)
            gx, gy = cx + rng.uniform(-30, 30), 440
            col = colors[k % len(colors)]
            begin = rng.uniform(0, cycle)
            rise = 0.28
            n, r = rng.choice([(20, 46), (24, 56), (16, 38)])
            parts = []
            for i in range(n * 2):
                a = 2 * math.pi * i / n
                f = rng.uniform(0.45, 1.0)
                a += rng.uniform(-0.12, 0.12)
                dx, dy = r * f * math.cos(a), r * f * math.sin(a)
                parts.append(
                    f'<circle r="{rng.choice([1.4, 1.8, 2.2])}" fill="{col}">'
                    f'<animateMotion path="M0,0 Q{dx * 0.8:.1f},{dy * 0.8:.1f} {dx:.1f},{dy + 22:.1f}" keyPoints="0;0;1;1" '
                    f'keyTimes="0;{rise};0.85;1" calcMode="linear" dur="{cycle}s" begin="-{begin:.1f}s" repeatCount="indefinite"/></circle>')
            burst = (f'<g transform="translate({cx:.0f} {cy:.0f})"><g filter="url(#c-glow3)" opacity="0">{"".join(parts)}'
                     f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{rise};{rise + 0.02:.2f};0.55;0.85;1" '
                     f'dur="{cycle}s" begin="-{begin:.1f}s" repeatCount="indefinite"/></g>'
                     f'<g opacity="0">{"".join(parts)}'
                     f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{rise};{rise + 0.02:.2f};0.6;0.88;1" '
                     f'dur="{cycle}s" begin="-{begin:.1f}s" repeatCount="indefinite"/></g>'
                     f'<circle r="{r * 0.6:.0f}" fill="{col}" opacity="0" filter="url(#c-glow8)">'
                     f'<animate attributeName="opacity" values="0;0;0.45;0;0" keyTimes="0;{rise};{rise + 0.03:.2f};{rise + 0.2:.2f};1" '
                     f'dur="{cycle}s" begin="-{begin:.1f}s" repeatCount="indefinite"/></circle></g>')
            rocket = (f'<circle r="1.8" fill="#fef3c7" opacity="0">'
                      f'<animateMotion path="M{gx:.0f},{gy} Q{(gx + cx) / 2:.0f},{(gy + cy) / 2 + 40:.0f} {cx:.0f},{cy:.0f}" keyPoints="0;1;1" '
                      f'keyTimes="0;{rise};1" calcMode="linear" dur="{cycle}s" begin="-{begin:.1f}s" repeatCount="indefinite"/>'
                      f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{rise - 0.01:.2f};{rise};1" dur="{cycle}s" '
                      f'begin="-{begin:.1f}s" repeatCount="indefinite"/></circle>')
            out.append(rocket + burst)
        return "".join(out)
    return ""


def render(lang: str, days: list[int], total: int, event: str = "clear", day: date | None = None) -> str:
    day = day or today_sp()
    ev_rng = random.Random(day.toordinal() * 7 + 1)   # separado do layout da cidade
    year = day.year + 1 if day.month == 12 else day.year
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

    stars_svg = stars(rng, iso, cols, rows)   # mesma ordem de sorteios de antes: o bairro não muda
    total_txt = f"{total:,}".replace(",", "." if lang == "pt" else ",")
    return "".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{esc(t["label"].format(n=total_txt))}">',
        '<defs><linearGradient id="c-bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#0c0a09"/><stop offset="54%" stop-color="#1f1f3d"/><stop offset="100%" stop-color="#0c0a09"/></linearGradient>'
        f'<radialGradient id="c-glow" cx="50%" cy="60%" r="55%"><stop offset="0%" stop-color="{VIOLET}" stop-opacity="0.35"/>'
        f'<stop offset="100%" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="c-frame"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18"/></clipPath>' + GLOW_DEFS + '</defs>',
        '<g clip-path="url(#c-frame)">',
        f'<rect width="{W}" height="{H}" fill="url(#c-bg)"/><rect width="{W}" height="{H}" fill="url(#c-glow)"/>',
        stars_svg if event not in ("sun", "rain", "fog") else "",
        event_back(event, ev_rng),
        ground(iso, cols, rows),
        lot_tiles(iso, len(days)),
        cars(iso, rng, cols, rows),
        "".join(objs),
        event_front(event, ev_rng, iso, cols, rows, year),
        f'<rect x="0" y="{H - 34}" width="{W}" height="34" fill="#07060d" fill-opacity="0.7"/>',
        text(32, H - 13, t["caption"], MONO, 11.5, 400, CREAM, 0.6),
        text(W - 32, H - 13, EVENT_LABEL[lang][event].format(year=year),
             MONO, 11.5, 700, PINK_L if event in ("christmas", "newyear") else CREAM,
             1 if event in ("christmas", "newyear") else 0.75, "end"),
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
    ap.add_argument("--event", choices=WEATHER + ["christmas", "newyear"],
                    help="força um evento (para testes); sem isso, ele sai da data")
    ap.add_argument("--date", help="data AAAA-MM-DD usada para escolher o evento (padrão: hoje em São Paulo)")
    args = ap.parse_args()
    day = date.fromisoformat(args.date) if args.date else today_sp()
    event = args.event or pick_event(day)

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
        (out / f"city-{lang}.svg").write_text(render(lang, days, total, event, day), encoding="utf-8")
    active = sum(1 for d in days if d)
    print(f"{len(days)} dias, {active} com contribuição, {total} no total, pico de {max(days)} num dia; evento: {event} ({day})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
