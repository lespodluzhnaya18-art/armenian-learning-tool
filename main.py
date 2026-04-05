import streamlit as st
import json
import os
import random

DB_FILE = "words.json"

def load_words():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_words(words):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="Armenian Trainer", page_icon="🇦🇲")
st.title("🇦🇲 Мой армянский словарь")
st.info("Учусь по системе Дария Степаняна")

words_data = load_words()

# Добавление слов
st.sidebar.header("📝 Новое слово")
new_arm = st.sidebar.text_input("Слово (основа)", placeholder="Напр: Hayr")
new_art = st.sidebar.text_input("Артикль (-ն или -ը)", placeholder="Напр: -ը")
new_rus = st.sidebar.text_input("Перевод на русский")

if st.sidebar.button("Добавить в базу"):
    if new_arm and new_rus:
        full_arm = f"{new_arm}{new_art}" if new_art else new_arm
        words_data[full_arm] = new_rus
        save_words(words_data)
        st.sidebar.success(f"Добавлено: {full_arm}")
        st.rerun()

# Вкладки
tab1, tab2 = st.tabs(["🎯 Тренировка", "📚 Весь список"])

with tab1:
    if not words_data:
        st.write("Словарь пока пуст. Добавь слова в меню слева!")
    else:
        if 'q_word' not in st.session_state:
            st.session_state.q_word = random.choice(list(words_data.keys()))
        
        q = st.session_state.q_word
        st.subheader(f"Как переводится: **{q}**?")
        user_ans = st.text_input("Твой ответ:", key="user_input")
        
        if st.button("Проверить"):
            if user_ans.lower().strip() == words_data[q].lower().strip():
                st.success("Правильно! Джан! ✨")
                st.session_state.q_word = random.choice(list(words_data.keys()))
                st.button("Дальше")
            else:
                st.error(f"Не совсем. Правильно: {words_data[q]}")

with tab2:
    st.write("Твои накопленные знания:")
    for a, r in words_data.items():
        st.write(f"🔹 **{a}** — {r}")
