# Методические указания по составлению контрольно-измерительных материалов (КИМ) с использованием учебно-методических ресурсов

## Назначение документа

Настоящие методические указания описывают способы использования учебно-методических ресурсов репозитория для создания и генерации контрольно-измерительных материалов по дисциплине «Управление проектами в сфере ИИ». Материал ориентирован на преподавателей, разрабатывающих новые варианты заданий, тестов, практических и лабораторных работ.

---

## Способы использования ресурсов

### 1. Ручное использование ресурсов

Ручной способ предполагает прямое использование готовых шаблонов, критериев и методических указаний для разработки КИМ «вручную», без применения автоматизированных инструментов.

#### 1.1. Адаптация существующих КИМ

**Порядок действий:**

1. Выберите КИМ из репозитория, наиболее близкий по тематике и типу задания.
2. Изучите комплект документов:
   - Подробное задание — поймите структуру и требования.
   - Шаблон для студента — оцените форму представления.
   - Варианты индивидуализации — изучите возможные модификации.
3. Модифицируйте содержание:
   - Смените кейс/предметную область.
   - Измените исходные данные.
   - Добавьте или исключите отдельные разделы в зависимости от уровня подготовки студентов.
   - Адаптируйте шкалы оценивания под свой курс.
4. Составьте новый комплект документов:
   - Новое задание (на основе подробного задания).
   - Новый шаблон для студента (при необходимости).
   - Обновлённые критерии оценивания.

**При ручной адаптации рекомендуется:**
- Сохранять общую структуру КИМ (тип, количество разделов, логику оценивания).
- Использовать профессиональную терминологию.
- Проверять соответствие таксономии Блума заявленному уровню сложности.
- Согласовывать изменения с рабочей программой дисциплины.

#### 1.2. Разработка новых вариантов заданий

1. На основе вариантов индивидуализации создайте новый набор вариантов.
2. Укажите для каждого варианта:
   - Тематику (отрасль, тип ИИ-решения).
   - Уровень сложности (базовый, средний, продвинутый).
   - Дополнительные условия (этический аспект, объяснимость модели, регуляторные требования).
3. Зафиксируйте правила распределения вариантов между студентами.

---

### 2. Автоматизированное использование ресурсов

Автоматизированный способ предполагает использование программных средств для генерации КИМ на основе структурированных данных и шаблонов из репозитория.

#### 2.1. Структура данных для автоматизации

Для автоматизированной генерации КИМ используется структурированное описание заданий в формате JSON или YAML. Пример структуры для тестового задания:

```json
{
  "kim_id": "KIM_1_Test",
  "module": 1,
  "title": "Основы проектного управления",
  "type": "test",
  "questions": [
    {
      "id": "q1",
      "type": "single_choice",
      "question": "Что является основным ограничением проекта?",
      "options": ["Сроки", "Бюджет", "Содержание", "Все перечисленные"],
      "correct_answer": 3
    }
  ],
  "variants": [
    {
      "id": "v1",
      "difficulty": "basic",
      "questions_count": 10
    }
  ]
}
```

#### 2.2. Скрипт для генерации КИМ

Ниже приведён пример скрипта на Python для генерации тестовых заданий из структурированных данных.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Генератор контрольно-измерительных материалов
Использование: python generate_kim.py --kim KIM_1_Test --variant basic
"""

import json
import argparse
import random
from datetime import datetime
from pathlib import Path


class KIMGenerator:
    """Генератор КИМ на основе JSON-описания"""

    def __init__(self, kim_file: str):
        """Загрузка описания КИМ из JSON-файла"""
        with open(kim_file, 'r', encoding='utf-8') as f:
            self.kim_data = json.load(f)

    def generate_test(self, variant_id: str) -> dict:
        """Генерация тестового задания"""
        variant = self._get_variant(variant_id)
        questions = self._select_questions(variant.get('questions_count', 10))

        return {
            "kim_id": self.kim_data['kim_id'],
            "title": self.kim_data['title'],
            "module": self.kim_data['module'],
            "variant": variant_id,
            "difficulty": variant.get('difficulty', 'standard'),
            "generated_at": datetime.now().isoformat(),
            "questions": questions
        }

    def _get_variant(self, variant_id: str) -> dict:
        """Получение варианта по ID"""
        for v in self.kim_data.get('variants', []):
            if v['id'] == variant_id:
                return v
        return {'id': variant_id, 'difficulty': 'standard', 'questions_count': 10}

    def _select_questions(self, count: int) -> list:
        """Выборка вопросов с учётом сложности"""
        all_questions = self.kim_data.get('questions', [])
        if len(all_questions) <= count:
            return all_questions
        return random.sample(all_questions, count)

    def export_to_markdown(self, test_data: dict) -> str:
        """Экспорт теста в формат Markdown"""
        lines = []
        lines.append(f"# {test_data['title']}")
        lines.append("")
        lines.append(f"**Вариант:** {test_data['variant']}")
        lines.append(f"**Сложность:** {test_data['difficulty']}")
        lines.append(f"**Дата генерации:** {test_data['generated_at']}")
        lines.append("")
        lines.append("---")
        lines.append("")

        for i, q in enumerate(test_data['questions'], 1):
            lines.append(f"## Вопрос {i}")
            lines.append("")
            lines.append(q['question'])
            lines.append("")
            if q['type'] == 'single_choice':
                for j, opt in enumerate(q.get('options', []), 1):
                    lines.append(f"{j}. {opt}")
            lines.append("")

        return "\n".join(lines)

    def export_to_lms_format(self, test_data: dict) -> dict:
        """Экспорт в формат для LMS Moodle (GIFT)"""
        gift_lines = []
        for q in test_data['questions']:
            if q['type'] == 'single_choice':
                question = q['question']
                options = q.get('options', [])
                correct = q.get('correct_answer', 0)
                gift_lines.append(f"::{question}:: {question} {{")
                for i, opt in enumerate(options):
                    if i == correct:
                        gift_lines.append(f"    ={opt}")
                    else:
                        gift_lines.append(f"    ~{opt}")
                gift_lines.append("}")
                gift_lines.append("")
        return {"gift_format": "\n".join(gift_lines)}


def main():
    parser = argparse.ArgumentParser(description='Генерация КИМ из JSON-описания')
    parser.add_argument('--kim', required=True, help='ID КИМ (например, KIM_1_Test)')
    parser.add_argument('--variant', default='basic', help='ID варианта')
    parser.add_argument('--output', '-o', help='Путь для сохранения результата')
    parser.add_argument('--format', choices=['md', 'gift'], default='md', help='Формат вывода')

    args = parser.parse_args()

    kim_file = Path(f"{args.kim}.json")
    if not kim_file.exists():
        print(f"Ошибка: файл {kim_file} не найден")
        return

    generator = KIMGenerator(kim_file)
    test_data = generator.generate_test(args.variant)

    if args.format == 'md':
        output = generator.export_to_markdown(test_data)
        ext = 'md'
    else:
        output = generator.export_to_lms_format(test_data)['gift_format']
        ext = 'txt'

    if args.output:
        output_file = args.output
    else:
        output_file = f"{args.kim}_{args.variant}.{ext}"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"✅ КИМ сгенерирован: {output_file}")


if __name__ == "__main__":
    main()
```

#### 2.3. Использование скрипта

```bash
# Генерация теста в формате Markdown
python generate_kim.py --kim KIM_1_Test --variant basic --format md

# Генерация теста в формате GIFT для импорта в Moodle
python generate_kim.py --kim KIM_1_Test --variant advanced --format gift

# Генерация с указанием выходного файла
python generate_kim.py --kim KIM_1_Test --variant basic -o test_v1.md
```

#### 2.4. Расширение функциональности

Для генерации других типов КИМ (лабораторных работ, практических заданий, эссе) структура данных может быть расширена:

```json
{
  "kim_id": "KIM_2_Lab",
  "type": "lab",
  "sections": [
    {
      "name": "Устав проекта",
      "fields": ["business_justification", "smart_goal", "kpi", "scope_in", "scope_out"]
    }
  ],
  "templates": {
    "basic": {"detail_level": "minimal"},
    "advanced": {"detail_level": "full", "extra_sections": ["ethics_checklist"]}
  }
}
```
