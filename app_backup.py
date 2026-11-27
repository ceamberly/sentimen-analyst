
import io
import html
import re

import streamlit as st
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    LongTable,
    TableStyle
)
from reportlab.lib.units import mm

from src.scraper import search_youtube
from src.preprocessing import preprocess_comments
from src.labeling import label_dataset


# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Sentiment Analyst",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================
# SESSION STATE
# =====================================

DEFAULT_STATES = {
    "menu": "Overview",
    "language": "id",
    "analysis_projects": [],
    "analysis_results": None,
    "active_analysis_config": None,
    "preprocessing_results": None,
    "labeling_results": None,
    "labeling_saved": False,
    "default_content_language": "Indonesian",
    "default_max_contents": 50,
    "default_max_comments": 100
}

for key, value in DEFAULT_STATES.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================
# TRANSLATION
# =====================================

TEXT = {
    "id": {
        "overview": "Overview",
        "new_analysis": "New Analyst",
        "workspace": "WORKSPACE",
        "language": "Bahasa / Language",
        "dashboard_desc": "Pantau dan kelola proyek analisis media sosial.",
        "total_projects": "Total Proyek",
        "available_platforms": "Platform Tersedia",
        "current_status": "Status Saat Ini",
        "ready": "Siap",
        "recent_projects": "Proyek Terbaru",
        "no_projects": "Belum Ada Proyek",
        "no_projects_desc": "Proyek analisismu akan muncul di sini.",
        "project_config": "Konfigurasi Proyek",
        "project_name": "Nama Proyek",
        "project_placeholder": "Contoh: Opini masyarakat tentang harga BBM",
        "select_platforms": "Pilih Platform",
        "select_platform_desc": "Pilih satu atau beberapa platform media sosial.",
        "available_platforms": "Platform yang Tersedia",
        "search_config": "Konfigurasi Pencarian",
        "search_keyword": "Kata Kunci Pencarian",
        "keyword_placeholder": "Contoh: karhutla",
        "max_contents": "Maksimal Video",
        "max_comments": "Maksimal Komentar per Video",
        "comment_limit": "Batas komentar berlaku untuk setiap video secara terpisah.",
        "preferences": "Preferensi Analisis",
        "content_language": "Bahasa Konten",
        "search_button": "Mulai Analisis →",
        "enter_project": "Masukkan nama proyek terlebih dahulu.",
        "select_platform_warning": "Pilih minimal satu platform.",
        "enter_keyword": "Masukkan kata kunci pencarian.",
        "youtube_only": "Saat ini konektor aktif adalah YouTube. Silakan pilih YouTube.",
        "searching": "Sedang mencari video YouTube dan mengumpulkan komentar...",
        "search_success": "Pengumpulan data YouTube berhasil!",
        "search_failed": "Gagal mengumpulkan data YouTube. Periksa API atau koneksi internet.",
        "unsupported": "Platform berikut belum terintegrasi:",
        "youtube_notice": "Saat ini YouTube merupakan platform pertama yang sudah terintegrasi.",
        "search_results": "Hasil Scraping",
        "videos_found": "Video Ditemukan",
        "comments_collected": "Komentar Dikumpulkan",
        "collection_errors": "Kesalahan Pengumpulan",
        "youtube_videos": "Video YouTube",
        "no_videos": "Tidak ada video yang ditemukan.",
        "collected_comments": "Komentar yang Dikumpulkan",
        "no_comments": "Tidak ada komentar yang berhasil dikumpulkan.",
        "view_errors": "Lihat Kesalahan Pengumpulan",
        "unknown_video": "Video Tidak Diketahui",
        "unknown_error": "Kesalahan Tidak Diketahui",
        "raw_dataset": "Dataset Mentah",
        "preprocessing": "Prapemrosesan Data",
        "preprocessing_desc": "Bersihkan dan siapkan komentar untuk analisis sentimen.",
        "no_dataset": "Belum ada dataset. Silakan kumpulkan data terlebih dahulu.",
        "no_comments_preprocessing": "Tidak ada komentar untuk diproses.",
        "process_description": "Tahapan pemrosesan yang akan dilakukan:",
        "remove_empty": "Menghapus komentar kosong.",
        "remove_duplicate": "Menghapus komentar duplikat.",
        "lowercase": "Mengubah teks menjadi huruf kecil.",
        "remove_symbols": "Menghapus URL, mention, angka, dan simbol.",
        "tokenize": "Memecah kalimat menjadi kata-kata.",
        "stopwords": "Menghapus kata umum (stopword) Bahasa Indonesia.",
        "stemming": "Melakukan stemming Bahasa Indonesia menggunakan Sastrawi.",
        "negation_note": "Kata negasi seperti tidak, bukan, dan belum tetap dipertahankan.",
        "run_preprocessing": "Jalankan Prapemrosesan →",
        "processing": "Sedang membersihkan dan memproses komentar...",
        "preprocessing_success": "Prapemrosesan data berhasil!",
        "preprocessing_failed": "Prapemrosesan gagal.",
        "preprocessing_results": "Hasil Prapemrosesan",
        "original_comments": "Komentar Awal",
        "processed_comments": "Komentar Diproses",
        "removed_comments": "Komentar Dihapus",
        "before_after": "Sebelum dan Sesudah Prapemrosesan",
        "processed_dataset": "Dataset Hasil Prapemrosesan",
        "labeling": "Pelabelan Sentimen",
        "labeling_desc": "Klasifikasikan dan periksa sentimen komentar.",
        "automatic_labeling": "Pelabelan Sentimen Otomatis",
        "automatic_description": "Sistem akan mengelompokkan komentar ke dalam tiga kategori sentimen.",
        "positive": "Positif",
        "negative": "Negatif",
        "neutral": "Netral",
        "positive_opinion": "Opini positif",
        "negative_opinion": "Opini negatif",
        "neutral_opinion": "Opini netral",
        "automatic_note": "Label otomatis merupakan prediksi awal berdasarkan kamus sentimen sederhana. Periksa hasilnya sebelum digunakan.",
        "generate_labels": "Buat Label Sentimen →",
        "analyzing_sentiment": "Sedang menganalisis sentimen komentar...",
        "labeling_success": "Pelabelan sentimen otomatis berhasil!",
        "labeling_failed": "Pelabelan sentimen gagal.",
        "sentiment_results": "Hasil Analisis Sentimen",
        "total_comments": "Total Komentar",
        "sentiment_distribution": "Distribusi Sentimen",
        "label_summary": "Ringkasan Sentimen",
        "manual_review": "Pemeriksaan Label Manual",
        "manual_review_note": "Ubah label melalui pilihan pada kolom Label Akhir.",
        "final_label": "Label Akhir",
        "automatic_label": "Label Otomatis",
        "confidence": "Tingkat Keyakinan",
        "save_labels": "Simpan Label yang Diperiksa",
        "labels_saved": "Label hasil pemeriksaan tersimpan.",
        "ready_next": "Dataset siap digunakan.",
        "changed_labels": "Label yang diubah secara manual",
        "export_labeled": "Download Hasil Analisis",
        "labeled_note": "Dataset berisi komentar asli, prediksi otomatis, dan label hasil pemeriksaan.",
        "export_dataset": "Download Dataset",
        "download_raw": "Download Hasil Scraping",
        "download_processed": "Download Hasil Preprocessing",
        "download_labeled": "Download Hasil Labeling",
        "download_format": "Pilih Format Download",
        "export_success": "Dataset siap diunduh.",
        "project": "Proyek",
        "keyword": "Kata Kunci",
        "platforms": "Platform",
        "no_history": "Belum Ada Proyek",
        "version": "SENTIMENT ANALYST · SOCIAL INTELLIGENCE",
        "active": "Aktif",
        "coming_soon": "Segera hadir",
        "indonesian": "Indonesia",
        "english": "Inggris",
        "all_languages": "Semua Bahasa",
        "total_columns": "Total Kolom",
        "preview_dataset": "Preview Dataset",
        "sentiment_percentage": "Persentase Sentimen",
        "no_download_data": "Tidak ada data untuk diunduh.",
        "rows_available": "baris data tersedia untuk diunduh.",
        "pdf_failed": "Gagal membuat PDF:",
        "pdf_unavailable": "PDF tidak tersedia.",
        "label_missing": "Kolom label tidak ditemukan pada hasil labeling.",
        "empty_preprocessing": "Hasil prapemrosesan kosong.",
        "empty_labeling": "Tidak ada data untuk dilakukan pelabelan."
    },

    "en": {
        "overview": "Overview",
        "new_analysis": "New Analyst",
        "workspace": "WORKSPACE",
        "language": "Language / Bahasa",
        "dashboard_desc": "Monitor and manage your social media analysis projects.",
        "total_projects": "Total Projects",
        "available_platforms": "Available Platforms",
        "current_status": "Current Status",
        "ready": "Ready",
        "recent_projects": "Recent Projects",
        "no_projects": "No Projects Yet",
        "no_projects_desc": "Your analysis projects will appear here.",
        "project_config": "Project Configuration",
        "project_name": "Project Name",
        "project_placeholder": "Example: Public opinion about fuel prices",
        "select_platforms": "Select Platforms",
        "select_platform_desc": "Choose one or more social media platforms.",
        "available_platforms": "Available Platforms",
        "search_config": "Search Configuration",
        "search_keyword": "Search Keyword",
        "keyword_placeholder": "Example: forest fires",
        "max_contents": "Maximum Videos",
        "max_comments": "Maximum Comments Per Video",
        "comment_limit": "Comment limits apply separately to each video.",
        "preferences": "Analysis Preferences",
        "content_language": "Content Language",
        "search_button": "Start Analysis →",
        "enter_project": "Please enter a project name.",
        "select_platform_warning": "Please select at least one platform.",
        "enter_keyword": "Please enter a search keyword.",
        "youtube_only": "Currently, YouTube is the active connector. Please select YouTube.",
        "searching": "Searching YouTube videos and collecting comments...",
        "search_success": "YouTube data collection completed!",
        "search_failed": "Failed to collect YouTube data. Check your API configuration or connection.",
        "unsupported": "These platforms are not integrated yet:",
        "youtube_notice": "Currently, YouTube is the first integrated platform.",
        "search_results": "Scraping Results",
        "videos_found": "Videos Found",
        "comments_collected": "Comments Collected",
        "collection_errors": "Collection Errors",
        "youtube_videos": "YouTube Videos",
        "no_videos": "No videos were found.",
        "collected_comments": "Collected Comments",
        "no_comments": "No comments were collected.",
        "view_errors": "View Collection Errors",
        "unknown_video": "Unknown Video",
        "unknown_error": "Unknown Error",
        "raw_dataset": "Raw Dataset",
        "preprocessing": "Data Preprocessing",
        "preprocessing_desc": "Clean and prepare comments for sentiment analysis.",
        "no_dataset": "No dataset available. Please collect data first.",
        "no_comments_preprocessing": "No comments available for preprocessing.",
        "process_description": "The following processes will be performed:",
        "remove_empty": "Remove empty comments.",
        "remove_duplicate": "Remove duplicate comments.",
        "lowercase": "Convert text to lowercase.",
        "remove_symbols": "Remove URLs, mentions, numbers, and symbols.",
        "tokenize": "Split sentences into individual words.",
        "stopwords": "Remove Indonesian stopwords.",
        "stemming": "Apply Indonesian stemming using Sastrawi.",
        "negation_note": "Negation words such as tidak, bukan, and belum are preserved.",
        "run_preprocessing": "Run Preprocessing →",
        "processing": "Cleaning and processing comments...",
        "preprocessing_success": "Data preprocessing completed successfully!",
        "preprocessing_failed": "Preprocessing failed.",
        "preprocessing_results": "Preprocessing Results",
        "original_comments": "Original Comments",
        "processed_comments": "Processed Comments",
        "removed_comments": "Removed Comments",
        "before_after": "Before & After Preprocessing",
        "processed_dataset": "Processed Dataset",
        "labeling": "Sentiment Labeling",
        "labeling_desc": "Classify and review comment sentiment.",
        "automatic_labeling": "Automatic Sentiment Labeling",
        "automatic_description": "The system will classify comments into three sentiment categories.",
        "positive": "Positive",
        "negative": "Negative",
        "neutral": "Neutral",
        "positive_opinion": "Positive opinions",
        "negative_opinion": "Negative opinions",
        "neutral_opinion": "Neutral opinions",
        "automatic_note": "Automatic labels are initial predictions based on a simple sentiment dictionary. Review the results before use.",
        "generate_labels": "Generate Sentiment Labels →",
        "analyzing_sentiment": "Analyzing comment sentiment...",
        "labeling_success": "Automatic sentiment labeling completed!",
        "labeling_failed": "Sentiment labeling failed.",
        "sentiment_results": "Sentiment Analysis Results",
        "total_comments": "Total Comments",
        "sentiment_distribution": "Sentiment Distribution",
        "label_summary": "Sentiment Summary",
        "manual_review": "Manual Label Review",
        "manual_review_note": "Change the label using the dropdown in the Final Label column.",
        "final_label": "Final Label",
        "automatic_label": "Automatic Label",
        "confidence": "Confidence",
        "save_labels": "Save Reviewed Labels",
        "labels_saved": "Reviewed labels saved.",
        "ready_next": "Dataset is ready.",
        "changed_labels": "Manually changed labels",
        "export_labeled": "Download Analysis Results",
        "labeled_note": "The dataset contains original comments, automatic predictions, and reviewed labels.",
        "export_dataset": "Download Dataset",
        "download_raw": "Download Scraping Results",
        "download_processed": "Download Preprocessing Results",
        "download_labeled": "Download Labeling Results",
        "download_format": "Choose Download Format",
        "export_success": "Dataset is ready to download.",
        "project": "Project",
        "keyword": "Keyword",
        "platforms": "Platforms",
        "no_history": "No Projects Yet",
        "version": "SENTIMENT ANALYST · SOCIAL INTELLIGENCE",
        "active": "Active",
        "coming_soon": "Coming soon",
        "indonesian": "Indonesian",
        "english": "English",
        "all_languages": "All Languages",
        "total_columns": "Total Columns",
        "preview_dataset": "Dataset Preview",
        "sentiment_percentage": "Sentiment Percentage",
        "no_download_data": "No data available for download.",
        "rows_available": "rows available for download.",
        "pdf_failed": "Failed to create PDF:",
        "pdf_unavailable": "PDF is unavailable.",
        "label_missing": "The label column was not found in the labeling results.",
        "empty_preprocessing": "The preprocessing result is empty.",
        "empty_labeling": "There is no data available for labeling."
    }
}


def t(key):
    language = st.session_state.get("language", "id")
    return TEXT.get(language, TEXT["id"]).get(key, key)


# =====================================
# CONSTANTS
# =====================================

MENU_OPTIONS = {
    "Overview": "overview",
    "New Analyst": "new_analysis"
}

PLATFORMS = [
    "YouTube",
    "TikTok",
    "Instagram",
    "Facebook",
    "X (Twitter)",
    "Reddit",
    "Threads"
]

CONTENT_LANGUAGES = [
    "Indonesian",
    "English",
    "All Languages"
]

CONTENT_LIMITS = [10, 20, 50, 100, 200, 500]
COMMENT_LIMITS = [20, 50, 100, 250, 500, 1000]


# =====================================
# DATA HELPER FUNCTIONS
# =====================================

def get_raw_comments():
    result = st.session_state.get("analysis_results")

    if not isinstance(result, dict):
        return pd.DataFrame()

    comments = result.get("comments", [])

    if not isinstance(comments, (list, tuple)):
        return pd.DataFrame()

    return pd.DataFrame(comments)


def get_result_list(result, key):
    """Mengambil list dari hasil scraping dengan aman."""
    if not isinstance(result, dict):
        return []

    value = result.get(key, [])

    if isinstance(value, (list, tuple)):
        return list(value)

    return []


def prepare_export_dataframe(dataframe):
    export_df = dataframe.copy()

    def safe_value(value):
        if value is None:
            return ""

        if isinstance(value, (list, tuple, set)):
            return ", ".join(str(item) for item in value)

        if isinstance(value, dict):
            return str(value)

        try:
            if pd.isna(value):
                return ""
        except (TypeError, ValueError):
            pass

        return str(value)

    for column in export_df.columns:
        export_df[column] = export_df[column].apply(safe_value)

    return export_df


def show_page_header(section, title, description):
    st.markdown(
        f"""
        <div class="eyebrow">{section}</div>
        <div class="page-title">{title}</div>
        <div class="page-description">{description}</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)


def reset_analysis_state():
    """Membersihkan hasil analisis sebelumnya."""
    st.session_state.analysis_results = None
    st.session_state.active_analysis_config = None
    st.session_state.preprocessing_results = None
    st.session_state.labeling_results = None
    st.session_state.labeling_saved = False

    for key in [
        "sentiment_label_editor",
        "project_name_input",
        "search_keyword_input"
    ]:
        if key in st.session_state:
            del st.session_state[key]


# =====================================
# EXPORT FUNCTIONS
# =====================================

def create_pdf(dataframe, title):
    output = io.BytesIO()

    page_width, _ = landscape(A4)

    document = SimpleDocTemplate(
        output,
        pagesize=landscape(A4),
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=16,
        leading=20,
        spaceAfter=5
    )

    cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["BodyText"],
        fontSize=7,
        leading=9,
        wordWrap="CJK",
        splitLongWords=True
    )

    header_style = ParagraphStyle(
        "TableHeader",
        parent=cell_style,
        textColor=colors.white,
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=9
    )

    elements = [
        Paragraph(html.escape(str(title)), title_style),
        Paragraph(
            f"Total data: {len(dataframe)}",
            styles["Normal"]
        ),
        Spacer(1, 10)
    ]

    if not dataframe.empty and len(dataframe.columns) > 0:

        table_data = []

        header = [
            Paragraph(
                html.escape(str(column)),
                header_style
            )
            for column in dataframe.columns
        ]

        table_data.append(header)

        for _, row in dataframe.iterrows():
            table_row = []

            for value in row:
                text_value = str(value)

                text_value = re.sub(
                    r"[\x00-\x08\x0b\x0c\x0e-\x1f]",
                    "",
                    text_value
                )

                text_value = html.escape(text_value)
                text_value = text_value.replace("\n", "<br/>")

                table_row.append(
                    Paragraph(text_value, cell_style)
                )

            table_data.append(table_row)

        columns = list(dataframe.columns)

        available_width = page_width - (20 * mm)

        long_text_columns = [
            "text",
            "comment",
            "cleaned_text",
            "stemmed_text",
            "content",
            "title"
        ]

        weights = []

        for column in columns:
            if str(column).lower() in long_text_columns:
                weights.append(3)
            else:
                weights.append(1)

        total_weight = sum(weights)

        column_widths = [
            available_width * weight / total_weight
            for weight in weights
        ]

        table = LongTable(
            table_data,
            colWidths=column_widths,
            repeatRows=1,
            hAlign="LEFT"
        )

        table.setStyle(TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#7665f5")
            ),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.35,
                colors.HexColor("#cccccc")
            ),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.HexColor("#f5f5fa")
                ]
            )
        ]))

        elements.append(table)

    document.build(elements)

    output.seek(0)
    return output.getvalue()


def show_download_options(dataframe, filename, title, label):

    if dataframe is None or dataframe.empty:
        st.info(t("no_download_data"))
        return

    export_df = prepare_export_dataframe(dataframe)

    st.markdown(f"**{label}**")

    st.caption(
        f"{len(export_df)} {t('rows_available')}"
    )

    csv_data = export_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    pdf_data = None

    try:
        pdf_data = create_pdf(export_df, title)

    except Exception as error:
        st.error(f"{t('pdf_failed')} {error}")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name=f"{filename}.csv",
            mime="text/csv",
            use_container_width=True,
            key=f"{filename}_csv"
        )

    with col2:
        if pdf_data is not None:
            st.download_button(
                label="📕 Download PDF",
                data=pdf_data,
                file_name=f"{filename}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key=f"{filename}_pdf"
            )
        else:
            st.warning(t("pdf_unavailable"))


# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --accent: #7665f5;
    --accent-hover: #6553e8;
}

.stApp {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

[data-testid="stSidebar"] {
    border-right: 1px solid var(--border-color);
}

.brand {
    padding: 12px 0 22px 0;
}

.brand-icon {
    color: var(--accent);
    font-size: 32px;
    font-weight: bold;
}

.brand-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 19px;
    font-weight: 700;
}

.brand-subtitle {
    font-size: 10px;
    letter-spacing: 2px;
    opacity: 0.65;
}

.eyebrow {
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.page-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 700;
    margin-top: 6px;
}

.page-description {
    font-size: 14px;
    opacity: 0.65;
    margin-top: 5px;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button[kind="primary"] {
    background: var(--accent);
    border-color: var(--accent);
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    background: var(--accent-hover);
    border-color: var(--accent-hover);
}

div[data-testid="stMetric"] {
    background: var(--secondary-background-color);
    border: 1px solid var(--border-color);
    padding: 17px;
    border-radius: 13px;
}

div[data-testid="stTabs"] button {
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-icon">◈</div>
        <div class="brand-title">Sentiment Analyst</div>
        <div class="brand-subtitle">SOCIAL INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.selectbox(
        t("language"),
        options=["id", "en"],
        format_func=lambda value: (
            "🇮🇩 " + TEXT["id"]["indonesian"]
            if value == "id"
            else "🇬🇧 " + TEXT["en"]["english"]
        ),
        key="language"
    )

    st.divider()

    menu = st.radio(
        t("workspace"),
        options=list(MENU_OPTIONS.keys()),
        format_func=lambda value: t(MENU_OPTIONS[value]),
        key="menu"
    )

    st.divider()

    st.caption("PLATFORM OPTIONS")

    for platform_name in PLATFORMS:

        platform_status = (
            t("active")
            if platform_name == "YouTube"
            else t("coming_soon")
        )

        st.markdown(
            f"""
            <div style="font-size:13px;margin-bottom:9px;">
                <span style="color:#7665f5;">●</span>
                {platform_name}
                <span style="opacity:.5;font-size:10px;">
                    ({platform_status})
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()
    st.caption(t("version"))


# =====================================
# OVERVIEW
# =====================================

if menu == "Overview":

    show_page_header(
        "WORKSPACE",
        t("overview"),
        t("dashboard_desc")
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        t("total_projects"),
        len(st.session_state.analysis_projects)
    )

    col2.metric(
        t("available_platforms"),
        1
    )

    col3.metric(
        t("current_status"),
        t("ready")
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### {t('recent_projects')}")

    if st.session_state.analysis_projects:

        for project in reversed(
            st.session_state.analysis_projects[-5:]
        ):

            with st.container(border=True):

                st.markdown(f"**{project['name']}**")

                st.caption(
                    f"{t('keyword')}: {project['keyword']}"
                )

                st.write(
                    f"{t('platforms')}: "
                    + ", ".join(project["platforms"])
                )

    else:

        with st.container(border=True):

            st.markdown(f"""
            <div style="text-align:center;padding:35px 10px;">
                <div style="font-size:30px;color:#7665f5;">◈</div>
                <div style="font-size:17px;font-weight:700;margin-top:10px;">
                    {t('no_projects')}
                </div>
                <div style="font-size:13px;opacity:.6;margin-top:6px;">
                    {t('no_projects_desc')}
                </div>
            </div>
            """, unsafe_allow_html=True)


# =====================================
# NEW ANALYST
# =====================================

elif menu == "New Analyst":

    show_page_header(
        "WORKSPACE / ANALYSIS",
        t("new_analysis"),
        t("dashboard_desc")
    )

    # ---------------------------------
    # PROJECT CONFIGURATION
    # ---------------------------------

    with st.container(border=True):

        st.markdown(f"### {t('project_config')}")

        project_name = st.text_input(
            t("project_name"),
            placeholder=t("project_placeholder"),
            key="project_name_input"
        )

        st.divider()

        st.markdown(f"### {t('select_platforms')}")
        st.caption(t("select_platform_desc"))

        selected_platforms = st.multiselect(
            t("available_platforms"),
            options=PLATFORMS,
            default=["YouTube"],
            key="selected_platforms"
        )

        st.divider()

        st.markdown(f"### {t('search_config')}")

        keyword = st.text_input(
            t("search_keyword"),
            placeholder=t("keyword_placeholder"),
            key="search_keyword_input"
        )

        col1, col2 = st.columns(2)

        with col1:
            max_contents = st.select_slider(
                t("max_contents"),
                options=CONTENT_LIMITS,
                value=st.session_state.default_max_contents
            )

        with col2:
            max_comments = st.select_slider(
                t("max_comments"),
                options=COMMENT_LIMITS,
                value=st.session_state.default_max_comments
            )

        st.caption(t("comment_limit"))

        st.divider()

        st.markdown(f"### {t('preferences')}")

        analysis_language = st.selectbox(
            t("content_language"),
            CONTENT_LANGUAGES,
            index=CONTENT_LANGUAGES.index(
                st.session_state.default_content_language
            ),
            format_func=lambda value: {
                "Indonesian": (
                    "Indonesia"
                    if st.session_state.language == "id"
                    else "Indonesian"
                ),
                "English": (
                    "Inggris"
                    if st.session_state.language == "id"
                    else "English"
                ),
                "All Languages": (
                    "Semua Bahasa"
                    if st.session_state.language == "id"
                    else "All Languages"
                )
            }[value]
        )

        start_search = st.button(
            t("search_button"),
            type="primary",
            use_container_width=True
        )

        if start_search:

            if not project_name.strip():
                st.warning(t("enter_project"))

            elif not selected_platforms:
                st.warning(t("select_platform_warning"))

            elif not keyword.strip():
                st.warning(t("enter_keyword"))

            elif "YouTube" not in selected_platforms:
                st.warning(t("youtube_only"))

            else:

                config = {
                    "name": project_name.strip(),
                    "platforms": selected_platforms,
                    "keyword": keyword.strip(),
                    "max_contents": max_contents,
                    "max_comments": max_comments,
                    "language": analysis_language
                }

                reset_analysis_state()

                try:

                    with st.spinner(t("searching")):

                        result = search_youtube(
                            keyword=config["keyword"],
                            max_contents=config["max_contents"],
                            max_comments=config["max_comments"],
                            language=config["language"]
                        )

                    if not isinstance(result, dict):
                        raise ValueError(
                            "Hasil scraping tidak memiliki format dictionary."
                        )

                    st.session_state.analysis_results = result
                    st.session_state.active_analysis_config = config

                    existing_projects = (
                        st.session_state.analysis_projects
                    )

                    project_exists = any(
                        project["name"] == config["name"]
                        and project["keyword"] == config["keyword"]
                        for project in existing_projects
                    )

                    if not project_exists:
                        st.session_state.analysis_projects.append({
                            "name": config["name"],
                            "keyword": config["keyword"],
                            "platforms": config["platforms"]
                        })

                    st.success(t("search_success"))

                    unsupported = [
                        platform
                        for platform in selected_platforms
                        if platform != "YouTube"
                    ]

                    if unsupported:
                        st.warning(
                            t("unsupported") + " "
                            + ", ".join(unsupported)
                        )

                except Exception as error:

                    st.error(t("search_failed"))
                    st.exception(error)

    # ---------------------------------
    # SEARCH RESULTS
    # ---------------------------------

    if (
        st.session_state.analysis_results is not None
        and st.session_state.active_analysis_config is not None
    ):

        result = st.session_state.analysis_results
        active_config = st.session_state.active_analysis_config

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"## {t('search_results')}")

        st.caption(
            f"{t('project')}: {active_config['name']} | "
            f"{t('keyword')}: {active_config['keyword']}"
        )

        videos = get_result_list(result, "contents")
        comments = get_result_list(result, "comments")
        errors = get_result_list(result, "errors")

        col1, col2, col3 = st.columns(3)

        col1.metric(t("videos_found"), len(videos))
        col2.metric(t("comments_collected"), len(comments))
        col3.metric(t("collection_errors"), len(errors))

        # ---------------------------------
        # VIDEO TABLE
        # ---------------------------------

        st.markdown(f"### {t('youtube_videos')}")

        if videos:

            videos_df = pd.DataFrame(videos)

            video_columns = [
                "title",
                "author",
                "published_at",
                "content_url"
            ]

            available = [
                column
                for column in video_columns
                if column in videos_df.columns
            ]

            st.dataframe(
                videos_df[available] if available else videos_df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info(t("no_videos"))

        # ---------------------------------
        # RAW COMMENTS
        # ---------------------------------

        st.markdown(f"### {t('collected_comments')}")

        raw_df = get_raw_comments()

        if not raw_df.empty:

            st.dataframe(
                raw_df,
                use_container_width=True,
                hide_index=True
            )

            st.markdown(f"### {t('export_dataset')}")

            show_download_options(
                raw_df,
                "sentiment_raw_dataset",
                "Sentiment Analyst - Raw Dataset",
                t("download_raw")
            )

        else:
            st.info(t("no_comments"))

        # ---------------------------------
        # COLLECTION ERRORS
        # ---------------------------------

        if errors:

            with st.expander(t("view_errors")):

                for item in errors:

                    if isinstance(item, dict):
                        error_title = item.get(
                            "content_title",
                            t("unknown_video")
                        )

                        error_message = item.get(
                            "error",
                            t("unknown_error")
                        )
                    else:
                        error_title = t("unknown_video")
                        error_message = str(item)

                    st.warning(
                        f"{error_title} — {error_message}"
                    )

        # ---------------------------------
        # DATA PREPROCESSING
        # ---------------------------------

        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()

        show_page_header(
            "WORKSPACE / NLP",
            t("preprocessing"),
            t("preprocessing_desc")
        )

        if raw_df.empty:

            st.warning(t("no_comments_preprocessing"))

        else:

            st.markdown(f"### {t('raw_dataset')}")

            col1, col2 = st.columns(2)

            col1.metric(
                t("comments_collected"),
                len(raw_df)
            )

            col2.metric(
                t("total_columns"),
                len(raw_df.columns)
            )

            with st.expander(t("preview_dataset")):

                st.dataframe(
                    raw_df,
                    use_container_width=True,
                    hide_index=True
                )

            with st.container(border=True):

                st.write(t("process_description"))

                st.markdown(f"""
                - {t('remove_empty')}
                - {t('remove_duplicate')}
                - {t('lowercase')}
                - {t('remove_symbols')}
                - {t('tokenize')}
                - {t('stopwords')}
                - {t('stemming')}
                """)

                st.caption(t("negation_note"))

                run_preprocessing = st.button(
                    t("run_preprocessing"),
                    type="primary",
                    use_container_width=True
                )

            if run_preprocessing:

                try:

                    with st.spinner(t("processing")):

                        processed_df = preprocess_comments(raw_df)

                    if not isinstance(processed_df, pd.DataFrame):
                        raise ValueError(
                            "Fungsi preprocessing harus mengembalikan DataFrame."
                        )

                    if processed_df.empty:
                        st.session_state.preprocessing_results = None
                        st.session_state.labeling_results = None
                        st.session_state.labeling_saved = False
                        st.warning(t("empty_preprocessing"))

                    else:
                        st.session_state.preprocessing_results = (
                            processed_df.copy()
                        )

                        st.session_state.labeling_results = None
                        st.session_state.labeling_saved = False

                        if "sentiment_label_editor" in st.session_state:
                            del st.session_state[
                                "sentiment_label_editor"
                            ]

                        st.success(t("preprocessing_success"))

                except Exception as error:

                    st.error(t("preprocessing_failed"))
                    st.exception(error)

            # ---------------------------------
            # PREPROCESSING RESULTS
            # ---------------------------------

            if st.session_state.preprocessing_results is not None:

                processed_df = (
                    st.session_state.preprocessing_results.copy()
                )

                st.markdown(f"## {t('preprocessing_results')}")

                original_count = len(raw_df)
                processed_count = len(processed_df)
                removed_count = max(
                    original_count - processed_count,
                    0
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    t("original_comments"),
                    original_count
                )

                col2.metric(
                    t("processed_comments"),
                    processed_count
                )

                col3.metric(
                    t("removed_comments"),
                    removed_count
                )

                st.markdown(f"### {t('before_after')}")

                comparison_columns = [
                    "text",
                    "cleaned_text",
                    "stemmed_text"
                ]

                available = [
                    column
                    for column in comparison_columns
                    if column in processed_df.columns
                ]

                if available:

                    st.dataframe(
                        processed_df[available],
                        use_container_width=True,
                        hide_index=True
                    )

                st.markdown(f"### {t('processed_dataset')}")

                st.dataframe(
                    processed_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown(f"### {t('export_dataset')}")

                show_download_options(
                    processed_df,
                    "sentiment_processed_dataset",
                    "Sentiment Analyst - Processed Dataset",
                    t("download_processed")
                )

                # ---------------------------------
                # SENTIMENT LABELING
                # ---------------------------------

                st.markdown("<br>", unsafe_allow_html=True)
                st.divider()

                show_page_header(
                    "WORKSPACE / NLP",
                    t("labeling"),
                    t("labeling_desc")
                )

                with st.container(border=True):

                    st.markdown(
                        f"### {t('automatic_labeling')}"
                    )

                    st.write(t("automatic_description"))

                    col1, col2, col3 = st.columns(3)

                    col1.markdown(
                        f"🟢 **{t('positive')}**"
                    )
                    col1.caption(t("positive_opinion"))

                    col2.markdown(
                        f"🔴 **{t('negative')}**"
                    )
                    col2.caption(t("negative_opinion"))

                    col3.markdown(
                        f"⚪ **{t('neutral')}**"
                    )
                    col3.caption(t("neutral_opinion"))

                    st.divider()

                    st.caption(t("automatic_note"))

                    run_labeling = st.button(
                        t("generate_labels"),
                        type="primary",
                        use_container_width=True
                    )

                if run_labeling:

                    try:

                        if processed_df.empty:
                            raise ValueError(
                                t("empty_labeling")
                            )

                        with st.spinner(t("analyzing_sentiment")):

                            labeled_df = label_dataset(
                                processed_df.copy()
                            )

                        if not isinstance(labeled_df, pd.DataFrame):
                            raise ValueError(
                                "Fungsi label_dataset harus mengembalikan DataFrame."
                            )

                        if labeled_df.empty:
                            raise ValueError(
                                t("empty_labeling")
                            )

                        if "label" not in labeled_df.columns:
                            raise ValueError(
                                t("label_missing")
                            )

                        st.session_state.labeling_results = (
                            labeled_df.copy()
                        )

                        st.session_state.labeling_saved = False

                        if "sentiment_label_editor" in st.session_state:
                            del st.session_state[
                                "sentiment_label_editor"
                            ]

                        st.success(t("labeling_success"))

                    except Exception as error:

                        st.error(t("labeling_failed"))
                        st.exception(error)

                # ---------------------------------
                # SENTIMENT RESULTS
                # ---------------------------------

                if st.session_state.labeling_results is not None:

                    labeled_df = (
                        st.session_state.labeling_results.copy()
                    )

                    st.markdown(
                        f"## {t('sentiment_results')}"
                    )

                    if "label" not in labeled_df.columns:

                        st.error(t("label_missing"))

                    else:

                        # Normalisasi label agar perhitungan konsisten.
                        normalized_labels = (
                            labeled_df["label"]
                            .astype(str)
                            .str.strip()
                            .str.title()
                        )

                        total = len(labeled_df)

                        positive_count = (
                            normalized_labels == "Positive"
                        ).sum()

                        negative_count = (
                            normalized_labels == "Negative"
                        ).sum()

                        neutral_count = (
                            normalized_labels == "Neutral"
                        ).sum()

                        # TOTAL AND COUNTS

                        col1, col2, col3, col4 = st.columns(4)

                        col1.metric(
                            t("total_comments"),
                            total
                        )

                        col2.metric(
                            t("positive"),
                            positive_count
                        )

                        col3.metric(
                            t("negative"),
                            negative_count
                        )

                        col4.metric(
                            t("neutral"),
                            neutral_count
                        )

                        # SENTIMENT PERCENTAGES

                        if total > 0:

                            positive_percentage = (
                                positive_count / total * 100
                            )

                            negative_percentage = (
                                negative_count / total * 100
                            )

                            neutral_percentage = (
                                neutral_count / total * 100
                            )

                            st.markdown(
                                f"### {t('sentiment_percentage')}"
                            )

                            pct1, pct2, pct3 = st.columns(3)

                            pct1.metric(
                                t("positive"),
                                f"{positive_percentage:.1f}%"
                            )

                            pct2.metric(
                                t("negative"),
                                f"{negative_percentage:.1f}%"
                            )

                            pct3.metric(
                                t("neutral"),
                                f"{neutral_percentage:.1f}%"
                            )

                            percentage_df = pd.DataFrame({
                                "Sentiment": [
                                    t("positive"),
                                    t("negative"),
                                    t("neutral")
                                ],
                                "Percentage": [
                                    positive_percentage,
                                    negative_percentage,
                                    neutral_percentage
                                ]
                            })

                            st.bar_chart(
                                percentage_df.set_index("Sentiment")
                            )

                        # SENTIMENT DISTRIBUTION

                        st.markdown(
                            f"### {t('sentiment_distribution')}"
                        )

                        distribution_df = pd.DataFrame({
                            "Sentiment": [
                                t("positive"),
                                t("negative"),
                                t("neutral")
                            ],
                            "Total": [
                                positive_count,
                                negative_count,
                                neutral_count
                            ]
                        })

                        chart_col, info_col = st.columns([2, 1])

                        with chart_col:

                            st.bar_chart(
                                distribution_df.set_index("Sentiment")
                            )

                        with info_col:

                            st.markdown(
                                f"#### {t('label_summary')}"
                            )

                            st.write(
                                f"🟢 {t('positive')}: "
                                f"**{positive_count}**"
                            )

                            st.write(
                                f"🔴 {t('negative')}: "
                                f"**{negative_count}**"
                            )

                            st.write(
                                f"⚪ {t('neutral')}: "
                                f"**{neutral_count}**"
                            )

                        # ---------------------------------
                        # MANUAL REVIEW
                        # ---------------------------------

                        st.markdown(
                            f"### {t('manual_review')}"
                        )

                        st.caption(
                            t("manual_review_note")
                        )

                        # Pastikan kolom label menggunakan format konsisten.
                        labeled_df["label"] = (
                            labeled_df["label"]
                            .astype(str)
                            .str.strip()
                            .str.title()
                        )

                        valid_labels = [
                            "Positive",
                            "Negative",
                            "Neutral"
                        ]

                        # Jika ada label yang tidak dikenal,
                        # jadikan Neutral agar editor tetap valid.
                        labeled_df["label"] = (
                            labeled_df["label"].where(
                                labeled_df["label"].isin(valid_labels),
                                "Neutral"
                            )
                        )

                        column_config = {
                            "label": st.column_config.SelectboxColumn(
                                t("final_label"),
                                options=valid_labels,
                                format_func=lambda value: {
                                    "Positive": t("positive"),
                                    "Negative": t("negative"),
                                    "Neutral": t("neutral")
                                }.get(value, value),
                                required=True
                            )
                        }

                        if "auto_label" in labeled_df.columns:

                            column_config["auto_label"] = (
                                st.column_config.TextColumn(
                                    t("automatic_label")
                                )
                            )

                        if "confidence" in labeled_df.columns:

                            column_config["confidence"] = (
                                st.column_config.TextColumn(
                                    t("confidence")
                                )
                            )

                        edited_df = st.data_editor(
                            labeled_df,
                            column_config=column_config,
                            disabled=[
                                column
                                for column in labeled_df.columns
                                if column != "label"
                            ],
                            use_container_width=True,
                            hide_index=True,
                            height=450,
                            key="sentiment_label_editor"
                        )

                        edited_df = edited_df.copy()

                        # ---------------------------------
                        # MANUAL LABEL TRACKING
                        # ---------------------------------

                        if "auto_label" in edited_df.columns:

                            edited_df["label_source"] = edited_df.apply(
                                lambda row: (
                                    "Manual"
                                    if str(row["label"]).strip().title()
                                    != str(row["auto_label"]).strip().title()
                                    else "Automatic"
                                ),
                                axis=1
                            )

                            changed_count = (
                                edited_df["label_source"] == "Manual"
                            ).sum()

                            st.caption(
                                f"{t('changed_labels')}: "
                                f"{changed_count}"
                            )

                        else:
                            changed_count = 0

                        # Simpan perubahan editor ke session state.
                        previous_df = st.session_state.labeling_results

                        labels_changed = False

                        if (
                            isinstance(previous_df, pd.DataFrame)
                            and "label" in previous_df.columns
                            and len(previous_df) == len(edited_df)
                        ):
                            labels_changed = not (
                                previous_df["label"]
                                .astype(str)
                                .reset_index(drop=True)
                                .equals(
                                    edited_df["label"]
                                    .astype(str)
                                    .reset_index(drop=True)
                                )
                            )

                        st.session_state.labeling_results = (
                            edited_df.copy()
                        )

                        if labels_changed:
                            st.session_state.labeling_saved = False

                        # ---------------------------------
                        # SAVE REVIEWED LABELS
                        # ---------------------------------

                        if st.button(
                            t("save_labels"),
                            type="primary",
                            use_container_width=True
                        ):

                            st.session_state.labeling_results = (
                                edited_df.copy()
                            )

                            st.session_state.labeling_saved = True

                            st.success(t("labels_saved"))

                        if st.session_state.labeling_saved:
                            st.success(t("ready_next"))

                        # ---------------------------------
                        # DOWNLOAD LABELED DATA
                        # ---------------------------------

                        st.markdown(
                            "<br>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"### {t('export_labeled')}"
                        )

                        show_download_options(
                            st.session_state.labeling_results,
                            "sentiment_labeled_dataset",
                            "Sentiment Analyst - Labeled Dataset",
                            t("download_labeled")
                        )

                        st.caption(t("labeled_note"))