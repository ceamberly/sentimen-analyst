import streamlit as st

st.set_page_config(
    page_title="Sentiment Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sentiment Analyst")

st.markdown(
    "Platform Scraping dan Analisis Sentimen Komentar"
)

st.divider()

st.subheader("🎯 Selamat Datang")

st.write("""
Sentiment Analyst merupakan platform untuk mengambil,
mengolah, dan menganalisis sentimen komentar dari media sosial.

Masukkan URL konten untuk memulai proses analisis.
""")

st.info("Platform sedang dalam tahap pengembangan.")

st.caption("Sentiment Analyst | Powered by Python & Streamlit")