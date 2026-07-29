import pytest
import pandas as pd
from pathlib import Path

# Эталонные значения для проверки
EXPECTED_COLUMNS = ['Задача', 'Длительность', 'Предшественники', 
                    'ES', 'EF', 'LS', 'LF', 'Резерв']

EXPECTED_TASKS = ['Анализ требований', 'Проектирование', 'Разработка ML-модели', 
                  'Сбор данных', 'Обучение модели', 'Тестирование', 'Интеграция', 'Документация']

EXPECTED_CRITICAL_PATH = ['Анализ требований', 'Проектирование', 
                          'Разработка ML-модели', 'Обучение модели', 'Интеграция']

class TestNetworkPlanning:
    """Автотесты для лабораторной работы по сетевому планированию (Модуль 4)"""

    def test_file_exists(self):
        """Проверка 1: Файл с работой существует"""
        file_path = Path('submission/network_plan.xlsx')
        assert file_path.exists(), "❌ Файл network_plan.xlsx не найден в папке submission"

    def test_file_structure(self):
        """Проверка 2: Структура файла соответствует шаблону"""
        df = pd.read_excel('submission/network_plan.xlsx')
        for col in EXPECTED_COLUMNS:
            assert col in df.columns, f"❌ Отсутствует колонка '{col}'"

    def test_tasks_completeness(self):
        """Проверка 3: Все задачи из условия присутствуют"""
        df = pd.read_excel('submission/network_plan.xlsx')
        actual_tasks = df['Задача'].tolist()
        for task in EXPECTED_TASKS:
            assert task in actual_tasks, f"❌ Задача '{task}' не найдена"

    def test_critical_path_identification(self):
        """Проверка 4: Критический путь определен верно (резерв = 0)"""
        df = pd.read_excel('submission/network_plan.xlsx')
        critical_tasks = df[df['Резерв'] == 0]['Задача'].tolist()
        for task in EXPECTED_CRITICAL_PATH:
            assert task in critical_tasks, f"❌ Задача '{task}' должна быть на критическом пути (Резерв=0)"

    def test_slack_calculation(self):
        """Проверка 5: Резерв времени рассчитан верно (LS - ES) с погрешностью ≤ 0.1"""
        df = pd.read_excel('submission/network_plan.xlsx')
        for idx, row in df.iterrows():
            expected_slack = row['LS'] - row['ES']
            assert abs(row['Резерв'] - expected_slack) < 0.1, \
                f"❌ Неверный резерв для задачи '{row['Задача']}': ожидается {expected_slack:.1f}, получено {row['Резерв']:.1f}"

    def test_no_negative_slack(self):
        """Проверка 6: Резерв времени не может быть отрицательным"""
        df = pd.read_excel('submission/network_plan.xlsx')
        assert (df['Резерв'] >= -0.1).all(), "❌ Обнаружен отрицательный резерв времени"

    def test_duration_values(self):
        """Проверка 7: Длительность всех задач должна быть положительной"""
        df = pd.read_excel('submission/network_plan.xlsx')
        assert (df['Длительность'] > 0).all(), "❌ Длительность всех задач должна быть положительной"
