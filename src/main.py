import json
from data_loader import load_data
from schedule_generator import generate_schedule
from excel_exporter import export_to_excel
import os
import click

DATA_DIR = "data"
OUTPUT_DIR = "output"

@click.command()
def main():

    while True:
        action = click.prompt("Выберите действие (Генерировать расписание, Выход)",
                              type=str)
        action = action.lower()  
        if action == "генерировать расписание" :
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
        elif action == "выход":
            print("Выход из программы")
            break  
        else:
            print("Неизвестное действие")

if __name__ == "__main__":
    main()