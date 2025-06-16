#!/bin/bash

# Переходим в директорию src
cd src

# Функция для генерации расписания
generate() {
  python main.py generate --teachers_file ../data/teachers.json --classes_file ../data/classes.json
}

# Функция для экспорта расписания в Excel
export() {
  python main.py export --schedule_file ../output/schedule.json --excel_file ../output/schedule.xlsx
}

# Обрабатываем аргументы командной строки
case "$1" in
  "generate")
    generate
    ;;
  "export")
    export
    ;;
  *)
    echo "Использование: ./run.sh [generate|export]"
    exit 1
    ;;
esac

# Возвращаемся в корневую директорию
cd ..