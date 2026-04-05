import json
import random
import os

DB_FILE = "words.json"

def load_words():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_words(words):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=4)

def start_trainer():
    words = load_words()
    while True:
        print("\n--- 🇦🇲 Armenian Trainer ---")
        print("1. Добавить слово", "2. Тест", "3. Список", "4. Выход", sep="\n")
        choice = input("Выбор: ")
        if choice == '1':
            arm = input("Армянский: ")
            rus = input("Русский: ")
            words[arm] = rus
            save_words(words)
        elif choice == '2':
            items = list(words.items())
            if not items:
                print("Сначала добавь слова!")
                continue
            random.shuffle(items)
            for arm, rus in items:
                ans = input(f"Как переводится '{arm}'? ").lower()
                if ans == 'стоп': break
                if ans == rus.lower():
                    print("Да! ✅")
                else: print(f"Нет, это '{rus}' ❌")
        elif choice == '3':
            for a, r in words.items(): print(f"{a} — {r}")
        elif choice == '4': break

if __name__ == "__main__":
    start_trainer()
