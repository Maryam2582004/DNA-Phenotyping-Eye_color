import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

# تحميل الداتا
url = "https://raw.githubusercontent.com/divyita/DNA-Phenotyping-Eye_color/main/synthetic_eye_color_dataset.csv"
df = pd.read_csv(url)

st.title("👁️ DNA Eye Color Prediction (Blended)")

# خريطة ألوان نصية -> RGB
color_map = {
    "blue": (47, 111, 219),   # أزرق
    "brown": (107, 62, 33),   # بني
    "green": (30, 154, 95),   # أخضر
    "hazel": (154, 111, 42),  # عسلي
    "gray": (126, 135, 144)   # رمادي
}

def blend_colors(results):
    """مزج الألوان حسب الاحتمالات"""
    rgb = np.zeros(3)
    for color, prob in results.items():
        if color.lower() in color_map:
            rgb += np.array(color_map[color.lower()]) * prob
    rgb = rgb / 100  # لأن الاحتمالات بالـ %
    return tuple(rgb.astype(int))

if st.button("🔮 Generate Eye"):
    # --- احتمالات عشوائية (مكان الموديل) ---
    colors = list(color_map.keys())
    probs = np.random.dirichlet(np.ones(len(colors)), size=1)[0] * 100
    results = {c: p for c, p in zip(colors, probs)}
    st.subheader("Probabilities")
    st.write(results)

    # --- تحديد اللون النهائي ---
    blended_rgb = blend_colors(results)
    hex_color = '#%02x%02x%02x' % blended_rgb
    st.write(f"Final Blended Color: {hex_color}")

    # --- رسم عين طبيعية أكتر ---
    fig, ax = plt.subplots(figsize=(4,2.5))

    # sclera (بياض العين)
    sclera = Ellipse((0.5, 0.5), 1.0, 0.6, color="white", ec="black", lw=1.5)
    ax.add_patch(sclera)

    # iris (قزحية العين) بلون مدمج
    iris = Circle((0.5, 0.5), 0.18, facecolor=hex_color, edgecolor="black", lw=0.8)
    ax.add_patch(iris)

    # خطوط شعاعية للقزحية (عشان شكل طبيعي أكتر)
    num_spokes = 40
    for i in range(num_spokes):
        angle = 2 * np.pi * i / num_spokes
        r1, r2 = 0.05, 0.18
        x1 = 0.5 + r1 * np.cos(angle)
        y1 = 0.5 + r1 * np.sin(angle)
        x2 = 0.5 + r2 * np.cos(angle)
        y2 = 0.5 + r2 * np.sin(angle)
        ax.plot([x1, x2], [y1, y2], color=hex_color, lw=0.5, alpha=0.2)

    # pupil (بؤبؤ العين)
    pupil = Circle((0.5, 0.5), 0.07, color="black")
    ax.add_patch(pupil)

    # highlight (لمعة العين)
    highlight = Circle((0.56, 0.58), 0.03, color="white", alpha=0.8)
    ax.add_patch(highlight)

    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig)
