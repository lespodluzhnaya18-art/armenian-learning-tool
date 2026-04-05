import streamlit as st
import json
import os
import random

# Настройка страницы (делаем широкий лендинг)
st.set_page_config(page_title="Armenian Way", page_icon="🇦🇲", layout="centered")

# --- Стилизация под Лендинг (немного магии CSS) ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    .hero-text {
        text-align: center;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("<div class='hero-text'><h1>🇦🇲 Armenian Way</h1><h3>Твой личный путь к армянскому языку</h3><p>Системное изучение по методике Дария Степаняна</p></div>", unsafe_allow_html=True)

# Логика работы со словарем (остается прежней)
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

# --- Контент лендинга ---
col1, col2, col3 = st.columns([1, 2, 1]) # Центрируем контент

with col2:
    tab1, tab2, tab3 = st.tabs(["🚀 Начать тест", "➕ Добавить слово", "📚 Мой словарь"])

    with tab1:
        if not words:
            st.info("Твой словарь пока пуст. Перейди во вкладку 'Добавить слово'.")
        else:
            if 'q' not in st.session_state:
                st.session_state.q = random.choice(list(words.keys()))
            
            q = st.session_state.q
            st.subheader(f"Как на русском: **{q}**?")
            ans = st.text_input("Введи перевод", key="input_text")
            
            if st.button("Проверить"):
                if ans.lower().strip() == words[q].lower().strip():
                    st.success("Джан! Правильно! 🎉")
                    st.session_state.q = random.choice(list(words.keys()))
                    st.button("Следующее слово")
                else:
                    st.error(f"Почти! Правильный ответ: {words[q]}")

    with tab2:
        st.write("### Наполни свою базу")
        new_arm = st.text_input("Слово (например, Girq)")
        new_art = st.selectbox("Артикль (если нужен)", ["", "-ը", "-ն"])
        new_rus = st.text_input("Перевод")
        if st.button("Сохранить в базу"):
            if new_arm and new_rus:
                full_word = f"{new_arm}{new_art}"
                words[full_word] = new_rus
                save_words(words)
                st.success(f"Слово '{full_word}' теперь в твоем списке!")
                st.rerun()

    with tab3:
        st.write("### Твои успехи")
        for a, r in words.items():
            st.markdown(f"📖 **{a}** — {r}")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Сделано с ❤️ для изучения армянского</p>", unsafe_allow_html=True)
