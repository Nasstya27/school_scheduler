import json
import sys
import random

DATA_DIR = "data"
OUTPUT_DIR = "output"

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

def generate_schedule(teachers, classes, lessons_per_day=8, days_per_week=5):
    schedule = {}
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
    teacher_lessons = {} 
    lessons_not_placed = []
    max_subjects_per_day = 2

    # Инициализация расписания
    for class_data in classes:
        class_name = class_data['name']
        schedule[class_name] = {}
        for day in days:
            schedule[class_name][day] = [None] * lessons_per_day # None = в это время нет урока

    # Инициализация teacher_lessons 
    for teacher in teachers:
        teacher_name = teacher['name']
        teacher_lessons[teacher_name] = {}
        for day in days:
            teacher_lessons[teacher_name][day] = [None] * lessons_per_day

    # Создаем список уроков, которые нужно разместить
    lessons_to_place = []
    for class_data in classes:
        class_name =class_data['name']
        for subject, lessons_count in class_data['subjects'].items():
            for _ in range(lessons_count):
                lessons_to_place.append({'class': class_name, 'subject': subject})

    # Размещаем уроки последовательно
    for lesson_to_place in lessons_to_place:
        class_name = lesson_to_place['class']
        subject = lesson_to_place['subject']
        placed = False

        for day_index in range(days_per_week):
            day = days[day_index]

            # Считаем, сколько уроков уже есть в этот день
            lessons_today = 0
            for lesson in schedule[class_name][day]:
                if lesson:
                    lessons_today += 1

            # Считаем сколько раз этот предмет уже есть в этот день
            subject_count = 0
            for lesson in schedule[class_name][day]:
                if lesson and lesson['subject'] == subject:
                    subject_count += 1

            # Собираем список доступных слотов
            available_slots = []
            for lesson_num in range(lessons_per_day):
                if schedule[class_name][day][lesson_num] is None and subject_count < max_subjects_per_day:
                    teacher = find_best_available_teacher(teachers, subject, day, lesson_num, teacher_lessons, day)
                    if teacher:
                        teacher_name =teacher['name']
                        available_slots.append(lesson_num)

            # Если есть доступные слоты, выбираем случайный
            if available_slots:
                lesson_num = random.choice(available_slots)
                teacher = find_best_available_teacher(teachers, subject, day, lesson_num, teacher_lessons, day)
                teacher_name = teacher['name']
                schedule[class_name][day][lesson_num] = {
                    'subject': subject,
                    'teacher': teacher_name
                }
                # Обновляем teacher_lessons с информацией об уроке
                teacher_lessons[teacher_name][day][lesson_num] = {
                    'class': class_name,
                    'subject': subject
                }
                placed = True
                lessons_today += 1
                subject_count += 1

            if placed:
                break  # Переходим к следующему уроку, если разместили урок в этот день

        if not placed:
            lessons_not_placed.append(lesson_to_place)
            print(f"Предупреждение: Не удалось расставить урок {subject} для класса {class_name}")

    # Преобразуем расписание в нужный формат (только занятые слоты)
    formatted_schedule = {}
    for class_name, class_schedule in schedule.items():
        formatted_schedule[class_name] = {}
        for day in days:
            formatted_schedule[class_name][day] = []
            for lesson_num, lesson in enumerate(class_schedule[day]):
                if lesson:  # Добавляем урок только если он есть
                    formatted_schedule[class_name][day].append({
                        "time": lesson_num + 1,  # Добавляем номер урока
                        "subject": lesson['subject'],
                        "teacher": lesson['teacher']
                    })

    print("Неразмещенные уроки:", lessons_not_placed)
    return formatted_schedule, teacher_lessons  


def find_best_available_teacher(teachers, subject, day, lesson_num, teacher_lessons, day_for_check):
    # Находим лучшего доступного учителя (наименее занятого)
    available_teachers = []
    for teacher in teachers:
        if subject in teacher['subjects']:
            if teacher_lessons[teacher['name']][day][lesson_num] is None:
                available_teachers.append(teacher)

    if not available_teachers:
        return None

    # Находим учителя с наименьшим количеством уроков в этот день
    best_teacher = None
    min_lessons = float('inf') 
    for teacher in available_teachers:
        teacher_name = teacher['name']
        lessons_today = 0
        for lesson in teacher_lessons[teacher_name][day]:
            if lesson:
                lessons_today += 1
        if lessons_today < min_lessons:
            min_lessons = lessons_today
            best_teacher = teacher

    return best_teacher


def is_teacher_available(teacher, day, lesson_num):
    if 'unavailable_slots' in teacher:
        for slot in teacher['unavailable_slots']:
            if slot['day'] == day and slot['time'] == lesson_num + 1:
                return False

    return True
