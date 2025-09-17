import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

# ----------------------------
# تحميل الداتا من GitHub
url = "https://raw.githubusercontent.com/divyita/DNA-Phenotyping-Eye_color/main/synthetic_eye_color_dataset.csv"
df = pd.read_csv(url)
# ----------------------------

st.title("👁️ DNA Eye Color Demo — Blended Eye Preview")

# خريطة ألوان نصية -> RGB بدل HEX عشان نقدر نعمل مزج
color_map = {
    "blue": (47, 111, 219),
    "brown": (107, 62, 33),
    "green": (30, 154, 95),
    "hazel": (154, 111, 42),
    "gray": (126, 135, 144)
}

def blend_colors(results):
    """مزج الألوان حسب نسب الاحتمالات"""
    rgb = np.zeros(3)
    for color, prob in results.items():
        if color.lower() in color_map:
            rgb += np.array(color_map[color.lower()]) * prob
    rgb = rgb / 100  # تحويل النسب %
    return tuple(rgb.astype(int))

st.write("اضغط Generate عشان نجيب عيّنة عشوائية من الداتا ونستعرض شكل العين بلون ممزوج حسب الاحتمالات.")

if st.button("Generate Random Prediction"):
    # اختيار صف عشوائي
    sample = df.sample(1).iloc[0]
    true_color = sample["eye_color"]  
    
    # توليد احتمالات عشوائية (Dirichlet) للاستعراض
    colors = df["eye_color"].unique()
    probs = np.random.dirichlet(np.ones(len(colors)), size=1)[0] * 100
    results = {c: p for c, p in zip(colors, probs)}
    predicted = max(results, key=results.get)
    pred_prob = results[predicted]

    st.subheader("Predicted Eye Color")
    st.markdown(f"**{predicted.capitalize()}** — {pred_prob:.2f}%")

    # عرض اللون الحقيقي من الداتا
    if "eye_color" in df.columns:
        st.write(f"Actual (ground truth): **{true_color}**")

    # ---------- حساب اللون الممزوج ----------
    blended_rgb = blend_colors(results)
    iris_color = '#%02x%02x%02x' % blended_rgb

    # ---------- رسم شكل العين ----------
    fig, ax = plt.subplots(figsize=(4,2.5))

    # sclera (بياض العين)
    sclera = Ellipse((0.5, 0.5), 0.95, 0.6, color="white", ec="black", lw=1.2)
    ax.add_patch(sclera)

    # iris (قزحية العين) باللون الممزوج
    iris = Circle((0.5, 0.5), 0.18, facecolor=iris_color, edgecolor="black", linewidth=0.8)
    ax.add_patch(iris)

    # خطوط شعاعية خفيفة لإضافة واقعية
    num_spokes = 30
    for i in range(num_spokes):
        angle = 2 * np.pi * i / num_spokes
        x1 = 0.5 + 0.02 * np.cos(angle)
        y1 = 0.5 + 0.02 * np.sin(angle)
        x2 = 0.5 + 0.18 * np.cos(angle)
        y2 = 0.5 + 0.18 * np.sin(angle)
        ax.plot([x1, x2], [y1, y2], color=iris_color, linewidth=0.6, alpha=0.25)

    # pupil (بؤبؤ العين)
    pupil = Circle((0.5, 0.5), 0.07, color="black")
    ax.add_patch(pupil)

    # highlight (لمعة العين)
    highlight = Circle((0.58, 0.62), 0.03, color="white", alpha=0.9)
    ax.add_patch(highlight)
    highlight2 = Circle((0.52, 0.56), 0.007, color="white", alpha=0.9)
    ax.add_patch(highlight2)

    # إعداد الشكل
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig)

    # ---------- Chart للاحتمالات ----------
    st.subheader("Predicted Probabilities")
    prob_series = pd.Series(results).sort_values(ascending=False)
    st.bar_chart(prob_series)

    # عرض بيانات الـ sample
    with st.expander("Show sample DNA row"):
        st.write(sample)
