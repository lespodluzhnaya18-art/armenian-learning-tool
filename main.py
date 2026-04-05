import streamlit as st
import json
import os
import random

# 1. Скрываем всё лишнее (логотипы, меню, подвалы)
st.set_page_config(
    page_title="Armenian Way", 
    page_icon="🇦🇲", 
    layout="centered",
    initial_sidebar_state="collapsed" # Сразу прячем боковую панель
)

hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# --- Дальше идет твой красивый Лендинг ---

st.markdown("<h1 style='text-align: center;'>🇦🇲 Armenian Way</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Твой системный путь к языку по Дарию Степаняну</p>", unsafe_allow_html=True)

DB_FILE = "words.json"
def load_words():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_words(words):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=4)

words = load_words()

# Центрируем основной контент
col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

with col2:
    tab1, tab2, tab3 = st.tabs(["🎯 Тренировка", "📝 Новое слово", "📚 Мой словарь"])

    with tab1:
        if not words:
            st.info("Твой словарь пока пуст. Загляни во вкладку 'Новое слово'.")
        else:
            if 'current_q' not in st.session_state:
                st.session_state.current_q = random.choice(list(words.keys()))
            
            q = st.session_state.current_q
            st.markdown(f"<h3 style='text-align: center;'>Как переводится: <b>{q}</b>?</h3>", unsafe_allow_html=True)
            ans = st.text_input("", placeholder="Твой ответ здесь...", key="test_input")
            
            if st.button("Проверить", use_container_width=True):
                if ans.lower().strip() == words[q].lower().strip():
                    st.success("Джан! Всё верно! ✨")
                    st.session_state.current_q = random.choice(list(words.keys()))
                    st.button("Следующее слово")
                else:
                    st.error(f"Почти! Правильный ответ: {words[q]}")

    with tab2:
        st.markdown("### Добавить в базу")
        word = st.text_input("Слово (основа)", placeholder="Напр: Tun")
        art = st.selectbox("Артикль", ["", "-ը", "-ն"])
        trans = st.text_input("Перевод на русский")
        if st.button("Сохранить", use_container_width=True):
            if word and trans:
                full = f"{word}{art}"
                words[full] = trans
                save_words(words)
                st.balloons() # Маленький праздник при сохранении!
                st.rerun()

    with tab3:
        st.markdown("### Твои накопленные слова")
        for a, r in words.items():
            st.markdown(f"📖 **{a}** — {r}")

st.markdown("<br><br><p style='text-align: center; font-size: 0.8em; color: lightgray;'>study track: Olesya x Stepanyan</p>", unsafe_allow_html=True)
