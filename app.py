import streamlit as st
import pandas as pd

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
    "search_config": None,
    "analysis_projects": [],
    "analysis_results": None,
    "active_analysis_config": None,
    "preprocessing_results": None,
    "preprocessing_config": None,
    "labeling_results": None,
    "labeling_saved": False,
    "labeling_version": 0,

    # Default preferences
    "default_platform": "YouTube",
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
        "overview": "Dashboard",
        "new_analysis": "Analisis Baru",
        "preprocessing": "Prapemrosesan Data",
        "labeling": "Pelabelan Sentimen",
        "explorer": "Penjelajah Sentimen",
        "history": "Riwayat Analisis",
        "settings": "Pengaturan",
        "workspace": "WORKSPACE",
        "platform_options": "PILIHAN PLATFORM",
        "active": "Aktif",
        "coming_soon": "Segera hadir",
        "language": "Bahasa / Language",
        "indonesian": "Indonesia",
        "english": "Inggris",

        "dashboard_desc": "Pantau dan kelola proyek analisis media sosial.",
        "total_projects": "Total Proyek",
        "available_platforms": "Platform Tersedia",
        "current_status": "Status Saat Ini",
        "ready": "Siap",
        "recent_projects": "Proyek Terbaru",
        "no_projects": "Belum Ada Proyek",
        "no_projects_desc": "Proyek analisismu akan muncul di sini.",

        "project": "Proyek",
        "keyword": "Kata Kunci",
        "platforms": "Platform",
        "project_config": "Konfigurasi Proyek",
        "project_name": "Nama Proyek",
        "project_placeholder": "Contoh: Opini masyarakat tentang harga BBM",
        "select_platforms": "Pilih Platform",
        "select_platform_desc": "Pilih satu atau beberapa platform media sosial.",
        "available_platforms_label": "Platform yang Tersedia",
        "select_platform_placeholder": "Pilih platform media sosial...",
        "search_config": "Konfigurasi Pencarian",
        "search_keyword": "Kata Kunci Pencarian",
        "keyword_placeholder": "Contoh: karhutla",
        "max_contents": "Maksimal Konten",
        "max_comments": "Maksimal Komentar per Konten",
        "comment_limit": "Batas komentar berlaku untuk setiap video secara terpisah.",
        "preferences": "Preferensi Analisis",
        "content_language": "Bahasa Konten",
        "search_button": "Cari Media Sosial →",

        "enter_project": "Masukkan nama proyek terlebih dahulu.",
        "select_platform_warning": "Pilih minimal satu platform.",
        "enter_keyword": "Masukkan kata kunci pencarian.",
        "youtube_only": "Saat ini konektor aktif adalah YouTube. Silakan pilih YouTube.",
        "searching": "Sedang mencari video YouTube dan mengumpulkan komentar...",
        "search_success": "Pengumpulan data YouTube berhasil!",
        "search_failed": "Gagal mengumpulkan data YouTube. Periksa API atau koneksi internet.",
        "unsupported": "Platform berikut belum terintegrasi:",
        "config_preview": "Ringkasan Konfigurasi",
        "save_config": "Simpan Konfigurasi Proyek",
        "duplicate_project": "Nama proyek tersebut sudah digunakan.",
        "config_saved": "Konfigurasi proyek berhasil disimpan!",
        "max_contents_metric": "Maksimal Konten",
        "comments_per_content": "Komentar per Konten",
        "youtube_notice": "Saat ini YouTube merupakan platform pertama yang sudah terintegrasi.",

        "search_results": "Hasil Pencarian",
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

        "preprocessing_desc": "Bersihkan dan siapkan komentar untuk analisis sentimen.",
        "no_dataset": "Belum ada dataset. Silakan kumpulkan data terlebih dahulu.",
        "go_new_analysis": "Buka Analisis Baru dan lakukan pencarian YouTube.",
        "no_comments_preprocessing": "Tidak ada komentar untuk diproses.",
        "raw_dataset": "Dataset Mentah",
        "available_columns": "Kolom Tersedia",
        "preview_raw": "Pratinjau Komentar Mentah",
        "preprocessing_config": "Konfigurasi Prapemrosesan",
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
        "export_dataset": "Ekspor Dataset",
        "download_processed": "Unduh Dataset Hasil Prapemrosesan (CSV)",

        "labeling_desc": "Klasifikasikan dan periksa sentimen komentar.",
        "automatic_labeling": "Pelabelan Sentimen Otomatis",
        "automatic_description": "Sistem akan mengelompokkan komentar ke dalam tiga kategori sentimen.",
        "positive": "Positif",
        "negative": "Negatif",
        "neutral": "Netral",
        "positive_opinion": "Opini positif",
        "negative_opinion": "Opini negatif",
        "neutral_opinion": "Opini netral",
        "automatic_note": "Label otomatis merupakan prediksi awal berdasarkan kamus sentimen sederhana. Periksa hasilnya sebelum digunakan untuk pelatihan model.",
        "generate_labels": "Buat Label Sentimen →",
        "analyzing_sentiment": "Sedang menganalisis sentimen komentar...",
        "labeling_success": "Pelabelan sentimen otomatis berhasil!",
        "labeling_failed": "Pelabelan sentimen gagal.",
        "sentiment_results": "Hasil Sentimen",
        "total_comments": "Total Komentar",
        "sentiment_distribution": "Distribusi Sentimen",
        "label_summary": "Ringkasan Label",
        "manual_review": "Pemeriksaan Label Manual",
        "manual_review_note": "Ubah label melalui pilihan pada kolom Label Akhir. Kolom lainnya hanya dapat dibaca.",
        "final_label": "Label Akhir",
        "automatic_label": "Label Otomatis",
        "confidence": "Tingkat Keyakinan",
        "save_labels": "Simpan Label yang Diperiksa",
        "labels_saved": "Label hasil pemeriksaan tersimpan dalam sesi saat ini.",
        "ready_next": "Dataset siap digunakan untuk tahap berikutnya.",
        "changed_labels": "Label yang diubah secara manual",
        "export_labeled": "Ekspor Dataset Berlabel",
        "download_labeled": "Unduh Dataset Berlabel (CSV)",
        "labeled_note": "Dataset berisi komentar asli, prediksi otomatis, dan label hasil pemeriksaan.",

        "explorer_desc": "Jelajahi opini audiens yang telah diklasifikasikan.",
        "sentiment_overview": "Ringkasan Sentimen",
        "classified_comments": "Komentar yang Diklasifikasikan",
        "no_sentiment": "Belum Ada Data Sentimen",
        "no_sentiment_desc": "Selesaikan pengumpulan data, prapemrosesan, dan pelabelan untuk melihat hasil sentimen.",
        "complete_labeling": "Selesaikan Pelabelan Sentimen untuk menampilkan hasil.",

        "history_desc": "Lihat kembali proyek analisis sebelumnya.",
        "max_contents_history": "Maksimal konten",
        "no_history": "Belum Ada Riwayat Analisis",
        "history_note": "Riwayat proyek masih tersimpan dalam sesi aplikasi dan akan hilang ketika sesi berakhir.",

        "settings_desc": "Kelola preferensi, data, dan informasi aplikasi.",
        "general_preferences": "Preferensi Analisis",
        "analysis_language": "Bahasa Konten Default",
        "default_platform": "Platform Utama",
        "default_max_contents": "Batas Video Default",
        "default_max_comments": "Batas Komentar Default",
        "save_preferences": "Simpan Preferensi",
        "preferences_saved": "Preferensi berhasil disimpan dan akan digunakan pada Analisis Baru.",
        "preferences_note": "Pengaturan tersimpan selama sesi aplikasi berjalan.",
        "platform_information": "Status Platform",
        "platform_note": "Platform lain akan diintegrasikan secara bertahap.",
        "data_export": "Data & Ekspor",
        "data_description": "Ringkasan data yang tersedia dalam sesi aplikasi saat ini.",
        "raw_data_count": "Komentar Mentah",
        "processed_data_count": "Komentar Hasil Preprocessing",
        "labeled_data_count": "Komentar Berlabel",
        "data_source": "Sumber Data",
        "data_source_note": "Data dikumpulkan dari YouTube. Teks komentar asli tetap disimpan dan tidak diterjemahkan oleh aplikasi.",
        "export_status": "Format ekspor yang tersedia saat ini adalah CSV.",
        "about": "Tentang Aplikasi",
        "about_description": "Sentiment Analyst adalah aplikasi untuk mengumpulkan komentar media sosial, melakukan prapemrosesan teks, dan mengelompokkan sentimen.",
        "current_features": "Fitur Saat Ini",
        "feature_collection": "Pengumpulan video dan komentar YouTube",
        "feature_preprocessing": "Prapemrosesan teks menggunakan Sastrawi",
        "feature_labeling": "Pelabelan sentimen berbasis leksikon",
        "feature_review": "Pemeriksaan dan koreksi label secara manual",
        "interface_languages": "Bahasa Antarmuka",
        "sentiment_categories": "Kategori Sentimen",
        "version": "SENTIMENT ANALYST · KECERDASAN MEDIA SOSIAL",
        "no_processed_data": "Belum ada dataset hasil prapemrosesan.",
        "complete_preprocessing": "Selesaikan Prapemrosesan Data sebelum melakukan pelabelan."
    },

    "en": {
        "overview": "Dashboard",
        "new_analysis": "New Analysis",
        "preprocessing": "Data Preprocessing",
        "labeling": "Sentiment Labeling",
        "explorer": "Sentiment Explorer",
        "history": "Analysis History",
        "settings": "Settings",
        "workspace": "WORKSPACE",
        "platform_options": "PLATFORM OPTIONS",
        "active": "Active",
        "coming_soon": "Coming soon",
        "language": "Language / Bahasa",
        "indonesian": "Indonesian",
        "english": "English",

        "dashboard_desc": "Monitor and manage your social media analysis projects.",
        "total_projects": "Total Projects",
        "available_platforms": "Available Platforms",
        "current_status": "Current Status",
        "ready": "Ready",
        "recent_projects": "Recent Projects",
        "no_projects": "No Projects Yet",
        "no_projects_desc": "Your analysis projects will appear here.",

        "project": "Project",
        "keyword": "Keyword",
        "platforms": "Platforms",
        "project_config": "Project Configuration",
        "project_name": "Project Name",
        "project_placeholder": "Example: Public opinion about fuel prices",
        "select_platforms": "Select Platforms",
        "select_platform_desc": "Choose one or more social media platforms.",
        "available_platforms_label": "Available Platforms",
        "select_platform_placeholder": "Select social media platforms...",
        "search_config": "Search Configuration",
        "search_keyword": "Search Keyword",
        "keyword_placeholder": "Example: forest fires",
        "max_contents": "Maximum Content Results",
        "max_comments": "Maximum Comments Per Content",
        "comment_limit": "Comment limits apply separately to each video.",
        "preferences": "Analysis Preferences",
        "content_language": "Content Language",
        "search_button": "Search Social Media →",

        "enter_project": "Please enter a project name.",
        "select_platform_warning": "Please select at least one platform.",
        "enter_keyword": "Please enter a search keyword.",
        "youtube_only": "Currently, YouTube is the active connector. Please select YouTube.",
        "searching": "Searching YouTube videos and collecting comments...",
        "search_success": "YouTube data collection completed!",
        "search_failed": "Failed to collect YouTube data. Check your API configuration or connection.",
        "unsupported": "These platforms are not integrated yet:",
        "config_preview": "Configuration Preview",
        "save_config": "Save Project Configuration",
        "duplicate_project": "A project with this name already exists.",
        "config_saved": "Project configuration saved!",
        "max_contents_metric": "Maximum Contents",
        "comments_per_content": "Comments Per Content",
        "youtube_notice": "Currently, YouTube is the first integrated platform.",

        "search_results": "Search Results",
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

        "preprocessing_desc": "Clean and prepare comments for sentiment analysis.",
        "no_dataset": "No dataset available. Please collect data first.",
        "go_new_analysis": "Go to New Analysis and perform a YouTube search.",
        "no_comments_preprocessing": "No comments available for preprocessing.",
        "raw_dataset": "Raw Dataset",
        "available_columns": "Available Columns",
        "preview_raw": "Preview Raw Comments",
        "preprocessing_config": "Preprocessing Configuration",
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
        "export_dataset": "Export Dataset",
        "download_processed": "Download Processed Dataset (CSV)",

        "labeling_desc": "Classify and review the sentiment of comments.",
        "automatic_labeling": "Automatic Sentiment Labeling",
        "automatic_description": "The system will classify comments into three sentiment categories.",
        "positive": "Positive",
        "negative": "Negative",
        "neutral": "Neutral",
        "positive_opinion": "Positive opinions",
        "negative_opinion": "Negative opinions",
        "neutral_opinion": "Neutral opinions",
        "automatic_note": "Automatic labels are initial predictions based on a simple sentiment dictionary. Review results before model training.",
        "generate_labels": "Generate Sentiment Labels →",
        "analyzing_sentiment": "Analyzing comment sentiment...",
        "labeling_success": "Automatic sentiment labeling completed!",
        "labeling_failed": "Sentiment labeling failed.",
        "sentiment_results": "Sentiment Results",
        "total_comments": "Total Comments",
        "sentiment_distribution": "Sentiment Distribution",
        "label_summary": "Label Summary",
        "manual_review": "Manual Label Review",
        "manual_review_note": "Change the label using the dropdown in the Final Label column. Other columns are read-only.",
        "final_label": "Final Label",
        "automatic_label": "Automatic Label",
        "confidence": "Confidence",
        "save_labels": "Save Reviewed Labels",
        "labels_saved": "Reviewed labels saved in the current session.",
        "ready_next": "Your dataset is ready for the next stage.",
        "changed_labels": "Manually changed labels",
        "export_labeled": "Export Labeled Dataset",
        "download_labeled": "Download Labeled Dataset (CSV)",
        "labeled_note": "The dataset contains original comments, automatic predictions, and reviewed labels.",

        "explorer_desc": "Explore classified audience opinions.",
        "sentiment_overview": "Sentiment Overview",
        "classified_comments": "Classified Comments",
        "no_sentiment": "No Sentiment Data Available",
        "no_sentiment_desc": "Complete data collection, preprocessing, and labeling to explore sentiment results.",
        "complete_labeling": "Complete Sentiment Labeling to display results.",

        "history_desc": "Review your previous analysis projects.",
        "max_contents_history": "Maximum contents",
        "no_history": "No Analysis History",
        "history_note": "Project history is stored in the current application session and will reset when the session ends.",

        "settings_desc": "Manage your preferences, data, and application information.",
        "general_preferences": "Analysis Preferences",
        "analysis_language": "Default Content Language",
        "default_platform": "Default Platform",
        "default_max_contents": "Default Video Limit",
        "default_max_comments": "Default Comment Limit",
        "save_preferences": "Save Preferences",
        "preferences_saved": "Preferences saved and will be used in New Analysis.",
        "preferences_note": "Settings are stored during the current application session.",
        "platform_information": "Platform Status",
        "platform_note": "Other platforms will be integrated progressively.",
        "data_export": "Data & Export",
        "data_description": "Overview of data available in the current application session.",
        "raw_data_count": "Raw Comments",
        "processed_data_count": "Preprocessed Comments",
        "labeled_data_count": "Labeled Comments",
        "data_source": "Data Source",
        "data_source_note": "Data is collected from YouTube. Original comment text is preserved and is not translated by the application.",
        "export_status": "CSV is currently the available export format.",
        "about": "About",
        "about_description": "Sentiment Analyst is an application for collecting social media comments, preprocessing text, and classifying sentiment.",
        "current_features": "Current Features",
        "feature_collection": "YouTube video and comment collection",
        "feature_preprocessing": "Text preprocessing using Sastrawi",
        "feature_labeling": "Lexicon-based sentiment labeling",
        "feature_review": "Manual label review and correction",
        "interface_languages": "Interface Languages",
        "sentiment_categories": "Sentiment Categories",
        "version": "SENTIMENT ANALYST · SOCIAL INTELLIGENCE",
        "no_processed_data": "No processed dataset available.",
        "complete_preprocessing": "Complete Data Preprocessing before performing sentiment labeling."
    }
}


def t(key):
    language = st.session_state.language
    return TEXT.get(language, TEXT["id"]).get(key, key)


# =====================================
# MENU
# =====================================

MENU_KEYS = {
    "Overview": "overview",
    "New Analysis": "new_analysis",
    "Data Preprocessing": "preprocessing",
    "Sentiment Labeling": "labeling",
    "Sentiment Explorer": "explorer",
    "History": "history",
    "Settings": "settings"
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
# HELPER FUNCTIONS
# =====================================

def get_raw_comments():
    result = st.session_state.analysis_results

    if result is None:
        return pd.DataFrame()

    return pd.DataFrame(result.get("comments", []))


def prepare_export_dataframe(dataframe):
    export_df = dataframe.copy()

    for column in ["tokens", "filtered_tokens"]:
        if column in export_df.columns:
            export_df[column] = export_df[column].apply(
                lambda value: " ".join(value)
                if isinstance(value, list)
                else str(value)
            )

    return export_df


def show_page_header(section, title, description):
    st.markdown(f"""
    <div class="eyebrow">{section}</div>
    <div class="page-title">{title}</div>
    <div class="page-description">{description}</div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


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
            "🇮🇩 " + t("indonesian")
            if value == "id"
            else "🇬🇧 " + t("english")
        ),
        key="language"
    )

    st.divider()

    menu = st.radio(
        "WORKSPACE",
        options=list(MENU_KEYS.keys()),
        key="menu"
    )

    st.divider()

    st.caption(t("platform_options"))

    for platform_name in PLATFORMS:

        platform_status = (
            t("active") if platform_name == "YouTube"
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

    # Only YouTube is currently integrated.
    col2.metric(t("available_platforms"), 1)

    col3.metric(t("current_status"), t("ready"))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### {t('recent_projects')}")

    if st.session_state.analysis_projects:

        for project in reversed(st.session_state.analysis_projects[-5:]):

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
# NEW ANALYSIS
# =====================================

elif menu == "New Analysis":

    show_page_header(
        "WORKSPACE / PROJECT",
        t("new_analysis"),
        t("dashboard_desc")
    )

    with st.container(border=True):

        st.markdown(f"### {t('project_config')}")

        project_name = st.text_input(
            t("project_name"),
            placeholder=t("project_placeholder")
        )

        st.divider()

        st.markdown(f"### {t('select_platforms')}")
        st.caption(t("select_platform_desc"))

        default_platform = st.session_state.default_platform

        selected_platforms = st.multiselect(
            t("available_platforms_label"),
            options=PLATFORMS,
            default=[default_platform],
            placeholder=t("select_platform_placeholder")
        )

        st.divider()

        st.markdown(f"### {t('search_config')}")

        keyword = st.text_input(
            t("search_keyword"),
            placeholder=t("keyword_placeholder")
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
            )
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

                st.session_state.search_config = config

                st.session_state.analysis_results = None
                st.session_state.active_analysis_config = None
                st.session_state.preprocessing_results = None
                st.session_state.preprocessing_config = None
                st.session_state.labeling_results = None
                st.session_state.labeling_saved = False

                try:

                    with st.spinner(t("searching")):

                        result = search_youtube(
                            keyword=config["keyword"],
                            max_contents=config["max_contents"],
                            max_comments=config["max_comments"],
                            language=config["language"]
                        )

                    st.session_state.analysis_results = result
                    st.session_state.active_analysis_config = config

                    st.success(t("search_success"))

                    unsupported = [
                        platform for platform in selected_platforms
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

    # CONFIGURATION PREVIEW

    if st.session_state.search_config:

        config = st.session_state.search_config

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"### {t('config_preview')}")

        with st.container(border=True):

            st.write(f"**{t('project_name')}:** {config['name']}")
            st.write(f"**{t('keyword')}:** {config['keyword']}")
            st.write(
                f"**{t('platforms')}:** "
                + ", ".join(config["platforms"])
            )

            col1, col2 = st.columns(2)

            col1.metric(
                t("max_contents_metric"),
                config["max_contents"]
            )

            col2.metric(
                t("comments_per_content"),
                config["max_comments"]
            )

            st.caption(
                f"{t('content_language')}: {config['language']}"
            )

            st.info(t("youtube_notice"))

            if st.button(
                t("save_config"),
                type="primary",
                use_container_width=True
            ):

                existing = [
                    project["name"]
                    for project in st.session_state.analysis_projects
                ]

                if config["name"] in existing:
                    st.warning(t("duplicate_project"))

                else:
                    st.session_state.analysis_projects.append(config)
                    st.success(t("config_saved"))
                    st.session_state.search_config = None

    # SEARCH RESULTS

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

        videos = result.get("contents", [])
        comments = result.get("comments", [])
        errors = result.get("errors", [])

        col1, col2, col3 = st.columns(3)

        col1.metric(t("videos_found"), len(videos))
        col2.metric(t("comments_collected"), len(comments))
        col3.metric(t("collection_errors"), len(errors))

        st.markdown(f"### {t('youtube_videos')}")

        if videos:

            videos_df = pd.DataFrame(videos)

            video_columns = [
                "title", "author", "published_at", "content_url"
            ]

            available = [
                column for column in video_columns
                if column in videos_df.columns
            ]

            st.dataframe(
                videos_df[available],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info(t("no_videos"))

        st.markdown(f"### {t('collected_comments')}")

        if comments:

            comments_df = pd.DataFrame(comments)

            comment_columns = [
                "platform",
                "content_title",
                "author",
                "text",
                "published_at",
                "like_count"
            ]

            available = [
                column for column in comment_columns
                if column in comments_df.columns
            ]

            st.dataframe(
                comments_df[available],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info(t("no_comments"))

        if errors:

            with st.expander(t("view_errors")):

                for item in errors:
                    st.warning(
                        f"{item.get('content_title', t('unknown_video'))} "
                        f"— {item.get('error', t('unknown_error'))}"
                    )


# =====================================
# DATA PREPROCESSING
# =====================================

elif menu == "Data Preprocessing":

    show_page_header(
        "WORKSPACE / NLP",
        t("preprocessing"),
        t("preprocessing_desc")
    )

    if st.session_state.analysis_results is None:

        st.warning(t("no_dataset"))
        st.info(t("go_new_analysis"))

    else:

        raw_df = get_raw_comments()

        if raw_df.empty:

            st.warning(t("no_comments_preprocessing"))

        else:

            st.markdown(f"### {t('raw_dataset')}")

            col1, col2 = st.columns(2)

            col1.metric(t("comments_collected"), len(raw_df))
            col2.metric(t("available_columns"), len(raw_df.columns))

            with st.expander(t("preview_raw")):

                st.dataframe(
                    raw_df,
                    use_container_width=True,
                    hide_index=True
                )

            st.markdown(f"### {t('preprocessing_config')}")

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

                    st.session_state.preprocessing_results = processed_df
                    st.session_state.preprocessing_config = (
                        st.session_state.active_analysis_config
                    )

                    st.session_state.labeling_results = None
                    st.session_state.labeling_saved = False

                    st.success(t("preprocessing_success"))

                except Exception as error:

                    st.error(t("preprocessing_failed"))
                    st.exception(error)

            if st.session_state.preprocessing_results is not None:

                processed_df = st.session_state.preprocessing_results

                st.markdown(f"## {t('preprocessing_results')}")

                original_count = len(raw_df)
                processed_count = len(processed_df)
                removed_count = original_count - processed_count

                col1, col2, col3 = st.columns(3)

                col1.metric(t("original_comments"), original_count)
                col2.metric(t("processed_comments"), processed_count)
                col3.metric(t("removed_comments"), removed_count)

                st.markdown(f"### {t('before_after')}")

                comparison_columns = [
                    "text", "cleaned_text", "stemmed_text"
                ]

                available = [
                    column for column in comparison_columns
                    if column in processed_df.columns
                ]

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

                export_df = prepare_export_dataframe(processed_df)

                csv_data = export_df.to_csv(
                    index=False
                ).encode("utf-8-sig")

                st.download_button(
                    label=t("download_processed"),
                    data=csv_data,
                    file_name="sentiment_processed_dataset.csv",
                    mime="text/csv",
                    type="primary",
                    use_container_width=True
                )


# =====================================
# SENTIMENT LABELING
# =====================================

elif menu == "Sentiment Labeling":

    show_page_header(
        "WORKSPACE / NLP",
        t("labeling"),
        t("labeling_desc")
    )

    if st.session_state.preprocessing_results is None:

        st.warning(t("no_processed_data"))
        st.info(t("complete_preprocessing"))

    elif st.session_state.preprocessing_results.empty:

        st.warning(t("no_processed_data"))

    else:

        processed_df = st.session_state.preprocessing_results

        st.markdown(f"### {t('automatic_labeling')}")

        with st.container(border=True):

            st.write(t("automatic_description"))

            col1, col2, col3 = st.columns(3)

            col1.markdown(f"🟢 **{t('positive')}**")
            col1.caption(t("positive_opinion"))

            col2.markdown(f"🔴 **{t('negative')}**")
            col2.caption(t("negative_opinion"))

            col3.markdown(f"⚪ **{t('neutral')}**")
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

                with st.spinner(t("analyzing_sentiment")):

                    labeled_df = label_dataset(processed_df)

                st.session_state.labeling_results = labeled_df
                st.session_state.labeling_version += 1
                st.session_state.labeling_saved = False

                if "sentiment_label_editor" in st.session_state:
                    del st.session_state["sentiment_label_editor"]

                st.success(t("labeling_success"))

            except Exception as error:

                st.error(t("labeling_failed"))
                st.exception(error)

        if st.session_state.labeling_results is not None:

            labeled_df = st.session_state.labeling_results.copy()

            st.markdown(f"## {t('sentiment_results')}")

            total = len(labeled_df)

            positive_count = (
                labeled_df["label"] == "Positive"
            ).sum()

            negative_count = (
                labeled_df["label"] == "Negative"
            ).sum()

            neutral_count = (
                labeled_df["label"] == "Neutral"
            ).sum()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(t("total_comments"), total)
            col2.metric(t("positive"), positive_count)
            col3.metric(t("negative"), negative_count)
            col4.metric(t("neutral"), neutral_count)

            st.markdown(f"### {t('sentiment_distribution')}")

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

                st.markdown(f"#### {t('label_summary')}")
                st.write(f"🟢 {t('positive')}: **{positive_count}**")
                st.write(f"🔴 {t('negative')}: **{negative_count}**")
                st.write(f"⚪ {t('neutral')}: **{neutral_count}**")

            st.markdown(f"### {t('manual_review')}")
            st.caption(t("manual_review_note"))

            edited_df = st.data_editor(
                labeled_df,
                column_config={
                    "label": st.column_config.SelectboxColumn(
                        t("final_label"),
                        options=[
                            "Positive",
                            "Negative",
                            "Neutral"
                        ],
                        format_func=lambda value: {
                            "Positive": t("positive"),
                            "Negative": t("negative"),
                            "Neutral": t("neutral")
                        }.get(value, value),
                        required=True
                    ),
                    "auto_label": st.column_config.TextColumn(
                        t("automatic_label")
                    ),
                    "confidence": st.column_config.TextColumn(
                        t("confidence")
                    )
                },
                disabled=[
                    column for column in labeled_df.columns
                    if column != "label"
                ],
                use_container_width=True,
                hide_index=True,
                height=450,
                key="sentiment_label_editor"
            )

            edited_df = edited_df.copy()

            edited_df["label_source"] = edited_df.apply(
                lambda row: (
                    "Manual"
                    if row["label"] != row["auto_label"]
                    else "Automatic"
                ),
                axis=1
            )

            st.session_state.labeling_results = edited_df

            changed_count = (
                edited_df["label"] != edited_df["auto_label"]
            ).sum()

            st.caption(
                f"{t('changed_labels')}: {changed_count}"
            )

            if st.button(
                t("save_labels"),
                type="primary",
                use_container_width=True
            ):

                st.session_state.labeling_saved = True
                st.success(t("labels_saved"))

            if st.session_state.labeling_saved:
                st.success(t("ready_next"))

            st.markdown(f"### {t('export_labeled')}")

            export_df = prepare_export_dataframe(
                st.session_state.labeling_results
            )

            csv_data = export_df.to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                label=t("download_labeled"),
                data=csv_data,
                file_name="sentiment_labeled_dataset.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )

            st.caption(t("labeled_note"))


# =====================================
# SENTIMENT EXPLORER
# =====================================

elif menu == "Sentiment Explorer":

    show_page_header(
        "WORKSPACE / NLP",
        t("explorer"),
        t("explorer_desc")
    )

    if st.session_state.labeling_results is not None:

        labeled_df = st.session_state.labeling_results.copy()

        positive_count = (
            labeled_df["label"] == "Positive"
        ).sum()

        negative_count = (
            labeled_df["label"] == "Negative"
        ).sum()

        neutral_count = (
            labeled_df["label"] == "Neutral"
        ).sum()

        st.markdown(f"### {t('sentiment_overview')}")

        col1, col2, col3 = st.columns(3)

        col1.metric(t("positive"), positive_count)
        col2.metric(t("negative"), negative_count)
        col3.metric(t("neutral"), neutral_count)

        chart_df = pd.DataFrame({
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

        st.bar_chart(chart_df.set_index("Sentiment"))

        st.markdown(f"### {t('classified_comments')}")

        display_columns = [
            column for column in [
                "author",
                "text",
                "label",
                "confidence"
            ]
            if column in labeled_df.columns
        ]

        st.dataframe(
            labeled_df[display_columns],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.markdown(f"""
        <div style="text-align:center;padding:35px 20px;
                    border:1px solid var(--border-color);
                    border-radius:15px;">
            <div style="font-size:34px;color:#7665f5;">◈</div>
            <div style="font-size:18px;font-weight:700;margin-top:12px;">
                {t('no_sentiment')}
            </div>
            <div style="font-size:13px;opacity:.65;margin-top:7px;">
                {t('no_sentiment_desc')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info(t("complete_labeling"))


# =====================================
# HISTORY
# =====================================

elif menu == "History":

    show_page_header(
        "WORKSPACE / ARCHIVE",
        t("history"),
        t("history_desc")
    )

    if st.session_state.analysis_projects:

        for project in reversed(st.session_state.analysis_projects):

            with st.container(border=True):

                st.markdown(f"**{project['name']}**")

                st.caption(
                    f"{t('keyword')}: {project['keyword']}"
                )

                st.write(
                    f"{t('platforms')}: "
                    + ", ".join(project["platforms"])
                )

                st.write(
                    f"{t('max_contents_history')}: "
                    f"{project['max_contents']}"
                )

    else:

        st.info(t("no_history"))

    st.caption(t("history_note"))


# =====================================
# SETTINGS
# =====================================

elif menu == "Settings":

    show_page_header(
        "WORKSPACE / PREFERENCES",
        t("settings"),
        t("settings_desc")
    )

    tab_preferences, tab_data, tab_platforms, tab_about = st.tabs([
        t("general_preferences"),
        t("data_export"),
        t("platform_information"),
        t("about")
    ])

    # ---------------------------------
    # TAB 1: ANALYSIS PREFERENCES
    # ---------------------------------

    with tab_preferences:

        st.markdown(f"### {t('general_preferences')}")

        st.caption(t("preferences_note"))

        with st.container(border=True):

            st.selectbox(
                t("default_platform"),
                options=["YouTube"],
                index=0,
                key="settings_platform"
            )

            st.selectbox(
                t("analysis_language"),
                options=CONTENT_LANGUAGES,
                index=CONTENT_LANGUAGES.index(
                    st.session_state.default_content_language
                ),
                key="settings_content_language"
            )

            st.divider()

            st.markdown(f"**{t('default_max_contents')}**")

            st.select_slider(
                t("max_contents"),
                options=CONTENT_LIMITS,
                value=st.session_state.default_max_contents,
                key="settings_max_contents"
            )

            st.markdown(f"**{t('default_max_comments')}**")

            st.select_slider(
                t("max_comments"),
                options=COMMENT_LIMITS,
                value=st.session_state.default_max_comments,
                key="settings_max_comments"
            )

            st.divider()

            if st.button(
                t("save_preferences"),
                type="primary",
                use_container_width=True
            ):

                st.session_state.default_platform = (
                    st.session_state.settings_platform
                )

                st.session_state.default_content_language = (
                    st.session_state.settings_content_language
                )

                st.session_state.default_max_contents = (
                    st.session_state.settings_max_contents
                )

                st.session_state.default_max_comments = (
                    st.session_state.settings_max_comments
                )

                st.success(t("preferences_saved"))

    # ---------------------------------
    # TAB 2: DATA & EXPORT
    # ---------------------------------

    with tab_data:

        st.markdown(f"### {t('data_export')}")
        st.caption(t("data_description"))

        raw_df = get_raw_comments()

        raw_count = len(raw_df)

        processed_df = st.session_state.preprocessing_results

        processed_count = (
            len(processed_df)
            if processed_df is not None
            else 0
        )

        labeled_df = st.session_state.labeling_results

        labeled_count = (
            len(labeled_df)
            if labeled_df is not None
            else 0
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            t("raw_data_count"),
            raw_count
        )

        col2.metric(
            t("processed_data_count"),
            processed_count
        )

        col3.metric(
            t("labeled_data_count"),
            labeled_count
        )

        st.divider()

        st.markdown(f"**{t('data_source')}**")
        st.write("◈ YouTube")

        st.caption(t("data_source_note"))

        st.info(t("export_status"))

    # ---------------------------------
    # TAB 3: PLATFORM STATUS
    # ---------------------------------

    with tab_platforms:

        st.markdown(f"### {t('platform_information')}")

        for platform_name in PLATFORMS:

            is_active = platform_name == "YouTube"

            status = (
                t("active")
                if is_active
                else t("coming_soon")
            )

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                col1.markdown(f"**◈ {platform_name}**")

                if is_active:
                    col2.success(status)
                else:
                    col2.caption(status)

        st.caption(t("platform_note"))

    # ---------------------------------
    # TAB 4: ABOUT
    # ---------------------------------

    with tab_about:

        st.markdown(f"### {t('about')}")

        st.write(t("about_description"))

        st.divider()

        st.markdown(f"**{t('current_features')}**")

        st.markdown(f"""
        - {t('feature_collection')}
        - {t('feature_preprocessing')}
        - {t('feature_labeling')}
        - {t('feature_review')}
        """)

        st.divider()

        st.markdown(f"**{t('interface_languages')}**")
        st.write("🇮🇩 Bahasa Indonesia")
        st.write("🇬🇧 English")

        st.divider()

        st.markdown(f"**{t('sentiment_categories')}**")
        st.write(f"🟢 {t('positive')}")
        st.write(f"🔴 {t('negative')}")
        st.write(f"⚪ {t('neutral')}")

        st.divider()

        st.caption("Sentiment Analyst · Version 1.0")