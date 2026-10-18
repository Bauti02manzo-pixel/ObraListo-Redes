"""Posts estáticos de la semana 2 (1080x1350) y carrusel 'cómo cobrar la mano de obra'."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from brand import *  # noqa

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
M = 90
SHADOW = (7, 30, 54)
GREEN = (46, 196, 120)
RED = (226, 69, 69)


def save(art, name):
    art.result().save(os.path.join(OUT, name), optimize=True)
    print("ok", name)


def money(v):
    return "$ " + f"{int(v):,}".replace(",", ".")


# ---------------------------------------------------------------- Post A: ajustar precios por %
a = Art(W, H, NAVY)
a.logo_row(M, 90)
bottom = a.rich(M, 290, "¿Subieron los [[materiales]]?", "b", 104, 900, WHITE, line_h=122)
a.rich(M, bottom + 20, "Ajustá todos los precios del presupuesto con un solo porcentaje.", "m", 44, 880, SOFT, line_h=64)
cy = 740
a.rect(M, cy + 12, 900, 330, fill=SHADOW, r=36)
a.rect(M, cy, 900, 330, fill=WHITE, r=36)
a.text(M + 44, cy + 78, "Ajustar todos los precios (%)", "b", 38, NAVY)
a.rect(M + 44, cy + 118, 330, 96, fill=WHITE, r=20, outline=SOFT, width=4)
a.text(M + 44 + 36, cy + 118 + 66, "10", "b", 46, NAVY)
a.rect(M + 44 + 330 + 30, cy + 118, 300, 96, fill=ORANGE, r=20)
a.text(M + 44 + 330 + 30 + 150, cy + 118 + 66, "% Aplicar", "b", 40, WHITE, anchor="ms")
a.text(M + 44, cy + 262, "Ej.: 10 sube un 10 %. Con -5 baja un 5 %.", "m", 32, SLATE)
a.text(M + 44, cy + 306, "Materiales, mano de obra y adicionales.", "m", 32, SLATE)
a.pill(M, 1130, 430, 100, "Empezá gratis", size=42)
a.text(M + 430 + 40, 1130 + 50 + 14, "Link en la bio", "m", 38, SOFT)
save(a, "w2_post_ajuste_precios.png")

# ---------------------------------------------------------------- Post B: gastado vs estimado
a = Art(W, H, NAVY)
a.logo_row(M, 90)
bottom = a.rich(M, 290, "¿Cuánto [[gastaste]] de lo que presupuestaste?", "b", 92, 900, WHITE, line_h=110)
obras = [("Casa Martínez", 372000, 600000), ("Local comercial", 448000, 400000)]
y = bottom + 50
for name, spent, est in obras:
    a.rect(M, y + 12, 900, 150, fill=SHADOW, r=30)
    a.rect(M, y, 900, 150, fill=WHITE, r=30)
    a.icon(M + 28, y + 34, 82, NAVY)
    a.text(M + 140, y + 62, name, "b", 40, NAVY)
    a.text(M + 140, y + 104, f"Gastado {money(spent)} de {money(est)}", "m", 28, SLATE)
    ratio = spent / est
    over = ratio > 1
    bx, by, bw = M + 140, y + 120, 560
    a.rect(bx, by, bw, 16, fill=SOFT, r=8)
    a.rect(bx, by, int(bw * min(ratio, 1.0)), 16, fill=RED if over else ORANGE, r=8)
    if over:
        a.text(M + 900 - 40, y + 62, f"Excedido {int(round((ratio - 1) * 100))}%", "b", 36, RED, anchor="rs")
    else:
        a.text(M + 900 - 40, y + 64, f"{int(round(ratio * 100))}%", "b", 46, NAVY, anchor="rs")
    y += 186
a.rich(M, y + 20, "Compará lo gastado con lo estimado.", "m", 42, 880, SOFT, line_h=60)
a.pill(M, 1170, 430, 100, "Empezá gratis", size=42)
a.text(M + 430 + 40, 1170 + 50 + 14, "Link en la bio", "m", 38, SOFT)
save(a, "w2_post_gastos.png")

# ---------------------------------------------------------------- Pregunta
a = Art(W, H, LIGHT)
a.logo_row(M, 90, dark=True)
bottom = a.rich(M, 270, "¿Cómo cobrás la [[mano de obra]]?", "b", 96, 900, NAVY, line_h=114)
opts = ["Por día (jornal)", "Por metro cuadrado", "Por obra completa", "Depende del trabajo"]
y = bottom + 50
for i, o in enumerate(opts):
    a.rect(M, y, 900, 104, fill=WHITE, r=52, outline=NAVY, width=3)
    a.ellipse(M + 20, y + 17, 70, 70, fill=NAVY)
    a.text(M + 55, y + 17 + 35 + 15, str(i + 1), "b", 40, WHITE, anchor="ms")
    a.text(M + 122, y + 52 + 15, o, "b", 44, NAVY)
    y += 128
a.text(M, y + 50, "Contanos en los comentarios.", "m", 40, SLATE)
save(a, "w2_post_pregunta.png")

# ---------------------------------------------------------------- Carrusel: cómo cobrar la mano de obra
slides = [
    ("1", "Por [[jornal]] (por día)",
     "Cobrás cada día trabajado. Sirve para arreglos y trabajos donde no se sabe cuánto va a llevar.",
     "Ojo: el cliente no sabe de antemano cuánto va a pagar en total."),
    ("2", "Por [[metro cuadrado]]",
     "Un precio por m² terminado. Es común en pisos, revoques y pintura, y es fácil de comparar.",
     "Ojo: aclará qué incluye el precio: preparación, materiales, limpieza."),
    ("3", "Por [[obra completa]]",
     "Un solo precio cerrado por todo el trabajo. El cliente sabe de entrada cuánto paga.",
     "Ojo: si calculaste mal, el riesgo es tuyo. Sumá desperdicio e imprevistos."),
]

a = Art(W, H, NAVY)
a.logo_row(M, 90)
a.pill(M, 330, 330, 84, "3 FORMAS", size=36)
a.rich(M, 470, "Cómo cobrar la [[mano de obra]]", "b", 100, 900, WHITE, line_h=118)
a.text(M, 1240, "Deslizá para verlas", "m", 42, SOFT)
ax = M + a.text_width("Deslizá para verlas", "m", 42) + 30
ay = 1240 - 15
a.d.line([(ax * 2, ay * 2), ((ax + 56) * 2, ay * 2)], fill=ORANGE, width=8)
a.d.line([((ax + 38) * 2, (ay - 18) * 2), ((ax + 56) * 2, ay * 2), ((ax + 38) * 2, (ay + 18) * 2)], fill=ORANGE, width=8, joint="curve")
save(a, "w2_carrusel_0_portada.png")

for num, title, desc, ojo in slides:
    a = Art(W, H, LIGHT)
    a.text(W - M, 140, f"{num}/3", "m", 40, SLATE, anchor="rs")
    a.text(M, 410, num, "b", 330, ORANGE)
    bottom = a.rich(M, 470, title, "b", 80, 900, NAVY, line_h=96)
    a.rich(M, bottom + 22, desc, "m", 42, 880, SLATE, line_h=60)
    a.rect(M, 900, 900, 196, fill=WHITE, r=30)
    a.rect(M, 900, 14, 196, fill=ORANGE, r=7)
    a.rich(M + 50, 936, ojo, "m", 36, 810, NAVY, line_h=52)
    a.logo_row(M, H - 170, icon_size=72, word_size=48, dark=True)
    save(a, f"w2_carrusel_{num}.png")

a = Art(W, H, NAVY)
a.logo_row(M, 90)
a.rich(M, 330, "Mostrá la [[mano de obra]] separada", "b", 100, 900, WHITE, line_h=118)
a.rich(M, 800, "En ObraListo, el presupuesto tiene un campo para los materiales y otro para la mano de obra.", "m", 44, 860, SOFT, line_h=64)
a.pill(M, 1090, 430, 100, "Empezá gratis", size=42)
a.text(M + 430 + 40, 1090 + 50 + 14, "Link en la bio", "m", 38, SOFT)
save(a, "w2_carrusel_4_cierre.png")
