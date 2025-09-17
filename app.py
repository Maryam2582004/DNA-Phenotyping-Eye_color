import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# تحميل الـ dataset من GitHub
url = "https://raw.githubusercontent.com/divyita/DNA-Phenotyping-Eye_color/main/synthetic_eye_color_dataset.csv"
df = pd.read_csv(url)

st.title("👁️ DNA Eye Color Demo")

# اختيار record عشوائي من الـ dataset
random_row = df.sample(1).iloc[0]
eye_color = random_row["eye_color"]

st.subheader("Predicted Eye Color")

# خريطة تحويل الألوان النصية للـ RGB
color_map = {
    "blue": "#0000FF",
    "brown": "#8B4513",
    "green": "#008000",
    "hazel": "#8E7618",
    "gray": "#808080"
}

# رسم دائرة بلون العين
fig, ax = plt.subplots()
circle = plt.Circle((0.5, 0.5), 0.3, color=color_map.get(eye_color.lower(), "black"))
ax.add_artist(circle)
ax.set_aspect('equal')
ax.axis('off')
st.pyplot(fig)

st.markdown(f"<h3 style='color:{color_map.get(eye_color.lower(), 'black')}'>{eye_color.capitalize()}</h3>", unsafe_allow_html=True)

# توزيع باقي الألوان
color_counts = df["eye_color"].value_counts(normalize=True) * 100
st.subheader("Eye Color Distribution (%)")
st.bar_chart(color_counts)

# عرض بيانات الـ DNA للعينة المختارة
st.write("### Random DNA Sample Data")
st.write(random_row)
