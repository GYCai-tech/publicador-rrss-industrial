import streamlit as st
from .openai_video_generator import configurar_openai
from src.db_config import get_programmed_posts, init_db


def init_states():
    """Inicializa todos los session_state necesarios para la aplicación."""
    # Asegurar que la base de datos esté inicializada antes de cualquier operación
    init_db()

    # Estados para la navegación y datos
    if 'page' not in st.session_state: st.session_state.page = 'Home'
    if 'selected_platforms' not in st.session_state: st.session_state.selected_platforms = []
    if 'results' not in st.session_state: st.session_state.results = {}
    if 'env_vars_checked' not in st.session_state: st.session_state.env_vars_checked = False
    if 'preview_video_path' not in st.session_state: st.session_state.preview_video_path = None
    if 'selected_pub_id' not in st.session_state: st.session_state.selected_pub_id = None
    if 'platforms_with_content' not in st.session_state: st.session_state.platforms_with_content = set()

    if "selected_event_id" not in st.session_state:
        st.session_state.selected_event_id = None
    if "programmed_posts_cache" not in st.session_state:
        st.session_state.programmed_posts_cache = get_programmed_posts()

    if 'force_page_rerun' not in st.session_state:
        st.session_state.force_page_rerun = False

    # Estado para el formulario de generación
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            "objetivo": "", "audiencia": "", "mensaje": "",
            "tono": "", "cta": "", "keywords": [], "logos": []
        }

    # Configuración de OpenAI
    if 'openai_configured' not in st.session_state:
        if configurar_openai():
            st.session_state.openai_configured = True
        else:
            st.session_state.openai_configured = False
            st.error("Error al configurar OpenAI. Revisa la OPENAI_API_KEY.")

    # Banner de versión industrial
    st.markdown("""
    <div style="position: fixed; top: 60px; right: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 8px 15px; border-radius: 8px; z-index: 999; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <span style="color: white; font-weight: bold; font-size: 14px;">🏭 VERSIÓN INDUSTRIAL</span>
    </div>
    """, unsafe_allow_html=True)

    # Estilos CSS para toda la app
    st.markdown("""
    <style>
    .theme-adaptable-container {
        background-color: var(--background-color); color: var(--text-color);
        padding: 15px; border-radius: 5px; border: 1px solid var(--border-color);
        margin-bottom: 15px;
    }
    [data-theme="light"] { --background-color: #FFFFFF; --text-color: #31333F; --border-color: #ddd; }
    [data-theme="dark"] { --background-color: #262730; --text-color: #FAFAFA; --border-color: #444; }
    .stTags div[data-baseweb="tag"] { background-color: var(--tag-background-color, #4A4A4A); color: var(--tag-text-color, white); }
    [data-theme="light"] .stTags div[data-baseweb="tag"] { --tag-background-color: #F0F2F6; --tag-text-color: #31333F; }
    [data-theme="dark"] .stTags div[data-baseweb="tag"] { --tag-background-color: #4A4A4A; --tag-text-color: #FFFFFF; }
    </style>
    <script>
    // Detección inicial al cargar
    updateTheme();
    
    // Observador para cambios futuros
    const observer = new MutationObserver(updateTheme);
    observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });
    </script>
    """, unsafe_allow_html=True)
