"""Reel 3: ¿Cuántos ladrillos necesitás para un muro?  (misma cuenta que la calculadora de la app)

La app calcula: superficie = largo × alto − aberturas; ladrillos = ⌈superficie × u/m² × (1 + desperdicio/100)⌉
con 16 u/m² (referencia ladrillo hueco 12×18×33) y 5 % de desperdicio por defecto.
Ejemplo del video: 5 × 2,5 = 12,5 m²; − 1,5 m² de ventana = 11 m²; 11 × 16 × 1,05 = 184,8 → 185 u.
"""
import math

from gfx import *  # noqa: F401,F403
from scenes2 import Scene, pulse_of, BW, BH

# muro de 5 m x 2,5 m a 120 px por metro
WX, WY, WW, WH = 290, 640, 600, 300
WIN_X, WIN_Y, WIN_W, WIN_H = WX + 390, WY + 80, 150, 144   # ventana 1,25 x 1,2 m = 1,5 m²
CX, CY = WX + WW // 2, WY + WH // 2
CARD_CX = WX + 190   # tarjeta de superficie, a la izquierda de la ventana


def calc_total(l=5.0, h=2.5, ab=1.5, u=16, d=5):
    area = max(0.0, l * h - ab)
    return area, math.ceil(area * u * (1 + d / 100))


AREA_NETA, TOTAL_U = calc_total()
assert TOTAL_U == 185 and abs(AREA_NETA - 11.0) < 1e-9


def fnum(v, dec=1):
    s = f"{v:.{dec}f}".replace(".", ",")
    return s[:-2] if s.endswith(",0") else s


def draw_wall(a, t, t0=None, per_row=0.07):
    """Muro de ladrillos trabados. t0=None: ya construido."""
    for r in range(10):
        p = 1.0 if t0 is None else prog(t, t0 + r * per_row, 0.22)
        if p <= 0:
            continue
        y = WY + WH - (r + 1) * 30 - (1 - e_out(p)) * 26
        col = lerp_col(NAVY, BRICK, min(1.0, p * 3))
        off = 0 if r % 2 == 0 else -30
        for c in range(0, 11):
            x0, x1 = max(WX + c * 60 + off, WX), min(WX + c * 60 + off + 60, WX + WW)
            if x1 - x0 < 10:
                continue
            a.rect(x0 + 2, y + 2, x1 - x0 - 4, 26, fill=col, r=5)


def dim_lines(a, t, tb, tl, tlw=None, tlh=None):
    """Cotas del muro: línea inferior (largo) y lateral (alto), con sus etiquetas."""
    pb = e_out(prog(t, tb, 0.35))
    if pb > 0:
        y = WY + WH + 38
        a.rect(WX, y - 2, max(4, WW * pb), 4, fill=ORANGE, r=2)
        a.rect(WX - 2, y - 14, 4, 28, fill=ORANGE)
        if pb > 0.97:
            a.rect(WX + WW - 2, y - 14, 4, 28, fill=ORANGE)
    pl = e_out(prog(t, tl, 0.35))
    if pl > 0:
        x = WX - 38
        a.rect(x - 2, WY + WH - max(4, WH * pl), 4, max(4, WH * pl), fill=ORANGE, r=2)
        a.rect(x - 14, WY + WH - 2, 28, 4, fill=ORANGE)
        if pl > 0.97:
            a.rect(x - 14, WY - 2, 28, 4, fill=ORANGE)
    if tlw is not None:
        p = prog(t, tlw, 0.3)
        if p > 0:
            a.text(CX, WY + WH + 38 + 56 - (1 - e_out(p)) * -18, "5 m", "b", 42, lerp_col(NAVY, WHITE, min(1.0, p * 2.5)), anchor="ms")
    if tlh is not None:
        p = prog(t, tlh, 0.3)
        if p > 0:
            a.text(WX - 62, WY + WH // 2 + 14 + (1 - e_out(p)) * 18, "2,5 m", "b", 42, lerp_col(NAVY, WHITE, min(1.0, p * 2.5)), anchor="rs")


def wall_card_sprite():
    def d(sp):
        sp.rect(0, 12, 340, 120, fill=SHADOW, r=26)
        sp.rect(0, 0, 340, 120, fill=WHITE, r=26)
        sp.text(170, 36, "Superficie", "m", 28, SLATE, anchor="ms")
    return sprite("r3_wallcard", 340, 132, d)


def window_sprite():
    def d(sp):
        sp.rect(0, 0, WIN_W, WIN_H, fill=WHITE, r=8)
        sp.rect(9, 9, WIN_W - 18, WIN_H - 18, fill=(160, 205, 235), r=4)
        sp.rect(WIN_W / 2 - 3, 9, 6, WIN_H - 18, fill=WHITE)
        sp.rect(9, WIN_H / 2 - 3, WIN_W - 18, 6, fill=WHITE)
        sp.poly([(20, WIN_H - 18), (46, 18), (62, 18), (36, WIN_H - 18)], fill=(200, 228, 247))
    return sprite("r3_win", WIN_W, WIN_H, d)


def minus_tag_sprite():
    def d(sp):
        sp.rect(0, 6, 220, 62, fill=SHADOW, r=31)
        sp.rect(0, 0, 220, 62, fill=WHITE, r=31)
        sp.text(110, 44, "− 1,5 m²", "b", 34, ORANGE, anchor="ms")
    return sprite("r3_minus", 220, 74, d)


# =====================================================================  Hook
class R3Hook(Scene):
    COLS, ROWS = 5, 4

    def setup(self):
        n = self.COLS * self.ROWS
        step = min(0.06, max(0.03, (self.sd(0) - 0.35) / n))
        self.land = [self.ss(0) + 0.15 + i * step for i in range(n)]
        self.fall = 0.24
        self.t_q = self.at(0, 0.86)
        self.t_x = self.ss(1) + 0.28

    def draw(self, a, t, g):
        head_hook(a, t, self.spec)
        x0 = (W - (self.COLS * 154 - 8)) // 2
        for i in range(self.COLS * self.ROWS):
            r, c = divmod(i, self.COLS)
            ty = 1010 - r * 68
            p = prog(t, self.land[i] - self.fall, self.fall)
            if p <= 0:
                continue
            if p < 1:
                y = ty - 150 * (1 - e_in(p))
            else:
                q = t - self.land[i]
                y = ty - 8 * math.exp(-q * 13) * abs(math.sin(q * 22))
            col = lerp_col(NAVY, BRICK, min(1.0, p * 3))
            x = x0 + c * 154
            a.rect(x, y, BW, BH, fill=col, r=8)
            a.rect(x + 8, y + 7, BW - 16, 10, fill=lerp_col(col, WHITE, 0.2), r=5)
        # signo de pregunta que se vuelve una cruz roja ("a ojo" no)
        pq = prog(t, self.t_q, 0.3)
        if pq > 0:
            cx, cy, r = 905, 800, 58
            px = prog(t, self.t_x, 0.25)
            rr = r * e_back(pq)
            a.ellipse(cx - rr, cy - rr, 2 * rr, 2 * rr, fill=lerp_col(ORANGE, RED, px))
            if px < 1:
                a.text(cx, cy + 28, "?", "b", 84, lerp_col(WHITE, RED, px), anchor="ms")
            if px > 0:
                k = rr * 0.40 * px
                a.line([(cx - k, cy - k), (cx + k, cy + k)], WHITE, 11)
                a.line([(cx - k, cy + k), (cx + k, cy - k)], WHITE, 11)
        return shake_at(t, self.t_x, 6)

    def sfx(self):
        ev = [(0.12, "pop", 0.7)] + kin_sfx(self.spec["title"], 0.26, 0.09, 0.3)
        ev += [(tl, "tick", 0.35) for i, tl in enumerate(self.land) if i % 2 == 0]
        ev += [(self.t_q, "pop", 0.85), (self.t_x, "down", 0.8)]
        return ev


# =====================================================================  1 · medir
class R3Medir(Scene):
    def setup(self):
        self.t_wall = self.ss(0) + 0.05
        self.t_b = self.at(0, 0.38)
        self.t_l = self.at(0, 0.70)
        self.t_w = self.at(1, 0.30)
        self.t_h = self.at(1, 0.68)
        self.t_card = self.ss(2) + 0.12

    def draw(self, a, t, g):
        head_item(a, t, self.spec)
        draw_wall(a, t, self.t_wall)
        dim_lines(a, t, self.t_b, self.t_l, self.t_w, self.t_h)
        p = prog(t, self.t_card, 0.35)
        if p > 0:
            blit(a, wall_card_sprite(), CARD_CX, CY + 6, e_back(p), 0, min(1.0, p * 3))
            if p > 0.45:
                v = AREA_NETA_FULL * e_out(prog(t, self.t_card + 0.1, 0.5))
                a.text(CARD_CX, CY + 36, f"{fnum(v)} m²", "b", 62, NAVY, anchor="ms")
        return None

    def sfx(self):
        ev = [(0.22, "pop", 0.7)] + kin_sfx(self.spec["title"], 0.30, 0.07, 0.3)
        ev += [(self.t_wall + i * 0.07, "tick", 0.3) for i in range(10)]
        ev += [(self.t_b, "whoosh", 0.3), (self.t_l, "whoosh", 0.3),
               (self.t_w, "pop", 0.7), (self.t_h, "pop", 0.7), (self.t_card, "pop", 0.8)]
        ev += [(self.t_card + 0.1 + k * 0.1, "tick", 0.3) for k in range(5)]
        return ev


AREA_NETA_FULL = 5.0 * 2.5   # 12,5 m²


# =====================================================================  2 · aberturas
class R3Aberturas(Scene):
    def setup(self):
        self.t_win = self.at(0, 0.45)
        self.t_tag = self.at(1, 0.28)
        self.t_num = self.at(1, 0.74)

    def draw(self, a, t, g):
        head_item(a, t, self.spec)
        draw_wall(a, t, None)
        dim_lines(a, t, -9, -9, -9, -9)
        pw = prog(t, self.t_win, 0.35)
        if pw > 0:
            blit(a, window_sprite(), WIN_X + WIN_W / 2, WIN_Y + WIN_H / 2, e_back(pw), 0, min(1.0, pw * 3))
        pt = prog(t, self.t_tag, 0.32)
        if pt > 0:
            blit(a, minus_tag_sprite(), WIN_X + WIN_W / 2, WIN_Y - 36, e_back(pt), 0, min(1.0, pt * 3))
        blit(a, wall_card_sprite(), CARD_CX, CY + 6, 1.0, 0, 1.0)
        pn = e_out(prog(t, self.t_num, 0.4))
        a.text(CARD_CX, CY + 36 - 8 * pn, f"{fnum(AREA_NETA_FULL)} m²", "b", 62, lerp_col(NAVY, WHITE, min(1.0, pn * 1.6)), anchor="ms")
        if pn > 0:
            a.text(CARD_CX, CY + 36 + 8 * (1 - pn), f"{fnum(AREA_NETA)} m²", "b", 62, lerp_col(WHITE, ORANGE, min(1.0, pn * 1.6)), anchor="ms")
        pk = prog(t, self.t_num + 0.35, 0.3)
        if pk > 0:
            check_badge(a, CARD_CX + 170, CY - 56, 26, e_back(pk))
        return None

    def sfx(self):
        ev = [(0.22, "pop", 0.7)] + kin_sfx(self.spec["title"], 0.30, 0.07, 0.3)
        ev += [(self.t_win, "pop", 0.8), (self.t_tag, "pop", 0.7), (self.t_num, "whoosh", 0.4),
               (self.t_num + 0.35, "ding", 0.8)]
        return ev


# =====================================================================  3 · ladrillos + desperdicio
class R3Calc(Scene):
    ROWS = [("Superficie de muro", f"{fnum(AREA_NETA)} m²"), ("Unidades por m²", "16 u/m²"), ("Desperdicio", "5 %")]
    CY0 = 620

    def setup(self):
        self.t_card = self.ss(0) + 0.05
        self.tr = [self.at(0, 0.12), self.at(0, 0.40), self.at(0, 0.78)]
        self.t_res = self.ss(1) + 0.12
        self.d_res = 0.8

    @staticmethod
    def card_sprite():
        def d(sp):
            sp.rect(0, 12, 900, 440, fill=SHADOW, r=28)
            sp.rect(0, 0, 900, 440, fill=WHITE, r=28)
            sp.rect(0, 0, 900, 84, fill=NAVY_2, r=28)
            sp.rect(0, 50, 900, 34, fill=NAVY_2)
            sp.text(40, 57, "Calculadora · Ladrillos", "b", 38, WHITE)
            sp.rect(0, 322, 900, 118, fill=(253, 236, 222), r=28)
            sp.rect(0, 322, 900, 40, fill=(253, 236, 222))
        return sprite("r3_calc", 900, 452, d)

    def draw(self, a, t, g):
        head_item(a, t, self.spec)
        y0 = self.CY0
        p = prog(t, self.t_card, 0.4)
        blit(a, self.card_sprite(), 540, y0 + 226, e_back(p), 0, min(1.0, p * 3))
        for i, (lab, val) in enumerate(self.ROWS):
            pr = prog(t, self.tr[i], 0.3)
            if pr <= 0:
                continue
            off = (1 - e_out(pr)) * 110
            fa = min(1.0, pr * 2.5)
            y = y0 + 150 + i * 66
            a.text(90 + 40 + off, y, lab, "m", 38, lerp_col(WHITE, SLATE, fa))
            a.text(90 + 860 + off, y + 2, val, "b", 42, lerp_col(WHITE, NAVY, fa), anchor="rs")
            if i < 2:
                a.rect(90 + 30 + off, y + 20, 840, 2, fill=lerp_col(WHITE, CARD_SOFT, fa))
        pr = prog(t, self.t_res, self.d_res)
        if t >= self.t_res - 0.05:
            fa = min(1.0, prog(t, self.t_res - 0.05, 0.25) * 2)
            a.text(90 + 40, y0 + 322 + 74, "Ladrillos necesarios", "b", 36, lerp_col((253, 236, 222), NAVY, fa))
            v = int(round(TOTAL_U * e_out(pr)))
            a.text(90 + 860, y0 + 322 + 86, f"{v} u", "b", 82, lerp_col((253, 236, 222), ORANGE, fa), anchor="rs")
        pk = prog(t, self.t_res + self.d_res, 0.3)
        if pk > 0:
            check_badge(a, 585, y0 + 322 + 62, 28, e_back(pk))
        return None

    def sfx(self):
        ev = [(0.22, "pop", 0.7)] + kin_sfx(self.spec["title"], 0.30, 0.07, 0.3)
        ev.append((self.t_card, "pop", 0.8))
        ev += [(tr, "pop", 0.6) for tr in self.tr]
        ev += [(self.t_res + k * 0.07, "tick", 0.3) for k in range(10)]
        ev.append((self.t_res + self.d_res, "ding", 0.9))
        return ev


# =====================================================================  CTA
class R3Cta(Scene):
    TILES = [("Ladrillos", BRICK), ("Pintura", (88, 150, 220)), ("Hormigón", (150, 160, 178))]

    def setup(self):
        self.t_tile = [self.at(0, 0.34), self.at(0, 0.66), self.at(0, 0.86)]
        self.t_pill = self.ss(1) + 0.05
        self.t_link = self.ss(2) + 0.05

    @staticmethod
    def tile_sprite(name, col):
        def d(sp):
            sp.rect(0, 12, 285, 140, fill=SHADOW, r=26)
            sp.rect(0, 0, 285, 140, fill=WHITE, r=26)
            sp.rect(22, 42, 56, 56, fill=col, r=14)
            sp.text(92, 82, name, "b", 31, NAVY)
        return sprite(("r3tile", name), 285, 152, d)

    def draw(self, a, t, g):
        kinetic(a, M, 340, self.spec["title"], "b", 88, 900, 104, t, 0.28, step=0.09)
        for i, (name, col) in enumerate(self.TILES):
            p = prog(t, self.t_tile[i], 0.35)
            if p > 0:
                blit(a, self.tile_sprite(name, col), 90 + 142 + i * 307.5, 640 + 76, e_back(p), 0, min(1.0, p * 3))
        pf = prog(t, self.t_pill, 0.35)
        if pf > 0:
            sc = e_back(pf) * (1 + 0.04 * pulse_of(g) if pf >= 1 else 1)

            def d(sp):
                sp.pill(0, 0, 520, 100, "Empezá gratis", size=46)
            blit(a, sprite("gratis", 520, 100, d), 540, 935, sc, 0, min(1.0, pf * 3))
        if t >= self.t_link:
            fa = prog(t, self.t_link, 0.25)
            bob = 7 * abs(math.sin(g * 7))
            a.text(540, 1075, "Link en la bio", "b", 36, lerp_col(NAVY, WHITE, fa), anchor="ms")
            up_arrow(a, 540 - 185, 1062 - bob, 40, lerp_col(NAVY, ORANGE, fa))
            up_arrow(a, 540 + 185, 1062 - bob, 40, lerp_col(NAVY, ORANGE, fa))
        return None

    def sfx(self):
        ev = kin_sfx(self.spec["title"], 0.28, 0.09, 0.3)
        ev += [(tt, "pop", 0.8) for tt in self.t_tile] + [(self.t_pill, "ding", 0.8), (self.t_link, "pop", 0.7)]
        return ev


REELS3 = {
    "reel3_cuantos_ladrillos": [
        dict(scene=R3Hook, kind="hook", tag="CALCULADORA", tsize=96,
             title="¿Cuántos ladrillos [[necesitás]] para un muro?",
             vo="¿Cuántos ladrillos necesitás para un muro? ¡No lo calcules a ojo!"),
        dict(scene=R3Medir, chip="1", title="Medí el [[largo y el alto]]",
             vo="Primero, medí el largo y el alto. Cinco metros por dos y medio. ¡Son doce coma cinco metros cuadrados!"),
        dict(scene=R3Aberturas, chip="2", title="Restá las [[aberturas]]",
             vo="Después, restá las aberturas. Con una ventana de uno coma cinco metros cuadrados, te quedan once."),
        dict(scene=R3Calc, chip="3", title="Sumá el [[desperdicio]]",
             vo="Multiplicá por dieciséis ladrillos por metro cuadrado, y sumá cinco por ciento de desperdicio. ¡Son ciento ochenta y cinco ladrillos!"),
        dict(scene=R3Cta, kind="cta", title="Calculalo con [[ObraListo]]",
             vo="La calculadora de ObraListo hace esta cuenta por vos, y también calcula pintura y hormigón. ¡Empezá gratis! El link está en la bio."),
    ],
}
