import json
import sys

DATA_DIR = "data"

def load_data():
    try:
        with open(f"{DATA_DIR}/teachers.json", 'r', encoding='utf-8') as f:
            teachers = json.load(f)
        with open(f"{DATA_DIR}/classes.json", 'r', encoding='utf-8') as f:
            classes = json.load(f)
        return teachers, classes
    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Ошибка: Некорректный JSON: {e}")
        sys.exit(1)