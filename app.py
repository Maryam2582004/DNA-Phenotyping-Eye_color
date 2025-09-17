# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import random

# ----------------------------
# تحميل الداتا من GitHub
url = "https://raw.githubusercontent.com/divyita/DNA-Phenotyping-Eye_color/main/synthetic_eye_color_dataset.csv"
df = pd.read_csv(url)
# ----------------------------

st.title("👁️ DNA Eye Color Demo — Eye Preview")

# خريطة ألوان نصية -> HEX لقزحية العين
color_map = {
    "blue": "#2F6FDB",
    "brown": "#6B3E21",
    "green": "#1E9A5F",
    "hazel": "#9A6F2A",
    "gray": "#7E8790"
}

st.write("اضغط Generate عشان نجيب عيّنة عشوائية من الداتا ونستعرض شكل العين.")

if st.button("Generate Random Prediction"):
    # اختيار صف عشوائي
    sample = df.sample(1).iloc[0]
    true_color = sample["eye_color"]  # اللون الحقيقي من الداتا (لو حابة تعرضي)
    
    # لو ما عندكيش موديل، نولّد احتمالات عشوائية (Dirichlet) للاستعراض
    colors = df["eye_color"].unique()
    probs = np.random.dirichlet(np.ones(len(colors)), size=1)[0]
    results = {c: p for c, p in zip(colors, probs)}
    predicted = max(results, key=results.get)
    pred_prob = results[predicted]

    st.subheader("Predicted Eye Color")
    st.markdown(f"**{predicted.capitalize()}** — {pred_prob*100:.2f}%")

    # عرض اللون الحقيقي لو موجود
    if "eye_color" in df.columns:
        st.write(f"Actual (ground truth): **{true_color}**")

    # ---------- رسم شكل العين (matplotlib) ----------
    iris_color = color_map.get(predicted.lower(), "#333333")
    fig, ax = plt.subplots(figsize=(4,2.5))

    # رسم الشكل الخارجي للعين (sclera) كـ ellipse أبيض
    sclera = Ellipse(xy=(0.5, 0.5), width=0.95, height=0.6, angle=0, facecolor="white", edgecolor="black", linewidth=1.2)
    ax.add_patch(sclera)

    # رسم القزحية (iris) كـ دائرة في منتصف العين
    iris = Circle((0.5, 0.5), 0.18, facecolor=iris_color, edgecolor="black", linewidth=0.8)
    ax.add_patch(iris)

    # رسم نمط بسيط للقزحية: شوية خطوط شعاعية (optional look)
    num_spokes = 18
    for i in range(num_spokes):
        angle = 2 * np.pi * i / num_spokes
        x_start = 0.5 + 0.02 * np.cos(angle)
        y_start = 0.5 + 0.02 * np.sin(angle)
        x_end = 0.5 + 0.18 * np.cos(angle)
        y_end = 0.5 + 0.18 * np.sin(angle)
        ax.plot([x_start, x_end], [y_start, y_end], color=iris_color, linewidth=0.8, alpha=0.25)

    # رسم البؤبؤ (pupil)
    pupil = Circle((0.5, 0.5), 0.07, facecolor="black")
    ax.add_patch(pupil)

    # إضافة بريق صغير (highlight)
    highlight = Circle((0.58, 0.62), 0.03, facecolor="white", edgecolor=None, alpha=0.9)
    ax.add_patch(highlight)
    highlight2 = Circle((0.52, 0.56), 0.007, facecolor="white", alpha=0.9)
    ax.add_patch(highlight2)

    # تهيئة الشكل وإخفاء المحاور
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig)

    # ---------- Chart للاحتمالات ----------
    st.subheader("Predicted Probabilities")
    prob_series = pd.Series(results).sort_values(ascending=False)
    st.bar_chart(prob_series)
    
    # عرض بيانات الـ sample (اختياري)
    with st.expander("Show sample DNA row"):
        st.write(sample)
