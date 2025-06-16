import sys
import json
import argparse
from src.data_loader import load_data
from src.schedule_generator import generate_schedule
from src.excel_exporter import export_to_excel
import os

DATA_DIR = "data"
OUTPUT_DIR = "output"

def main():
    parser = argparse.ArgumentParser(description="School schedule generator.")
    parser.add_argument("action", choices=["generate"], help="Action to perform: generate")

    args = parser.parse_args()

    if args.action == "generate":
        teachers, classes = load_data()
        if teachers and classes:
            try:
                schedule, teacher_lessons = generate_schedule(teachers, classes)
                os.makedirs(OUTPUT_DIR, exist_ok=True)

                with open(f"{OUTPUT_DIR}/schedule.json", 'w', encoding='utf-8') as f:
                    json.dump(schedule, f, indent=4, ensure_ascii=False)
                print(f"Расписание сохранено в {OUTPUT_DIR}/schedule.json")

                with open(f"{OUTPUT_DIR}/teacher_schedule.json", 'w', encoding='utf-8') as f:
                    json.dump(teacher_lessons, f, indent=4, ensure_ascii=False)
                print(f"Расписание учителей сохранено в {OUTPUT_DIR}/teacher_schedule.json")

                export_to_excel(schedule, f"{OUTPUT_DIR}/schedule.xlsx")
                print(f"Расписание экспортировано в {OUTPUT_DIR}/schedule.xlsx")

            except Exception as e:
                print(f"Произошла ошибка: {e}")

        else:
            print("Не удалось загрузить данные")

if __name__ == "__main__":
    main()