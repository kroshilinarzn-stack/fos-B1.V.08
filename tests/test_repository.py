import os
import pytest
import re

# Базовая директория репозитория (корень, откуда запускается pytest)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ожидаемая структура папок верхнего уровня (на основе анализа репозитория)
EXPECTED_DIRECTORIES = [
    "Exam",
    "M1-Projects_and_Management_Environment",
    "M2-Project_Scope_Management",
    "M3-Human_resources_management",
    "M4-Project_timeline_management",
    "M5-Project_cost_management",
    "M6-Project_quality_management",
    "M7-Project_risk",
    "M8-AI_Project_Management",
    "Methodical_guidelinesre",
    "Postrekvisity", # Фактическое имя папки в репозитории
    "RPD",
    "SR",
    "docs",
    "team"
]

# Обязательные файлы в корне
REQUIRED_ROOT_FILES = [
    "README.md",
    "LICENSE.md"
]

# Ключевые разделы, которые обязаны быть в главном README.md согласно ФОС
REQUIRED_SECTIONS_IN_README = [
    "Цель дисциплины",
    "Модуль 1",
    "Модуль 8",
    "Компетенции",
    "Структура репозитория"
]

def test_repository_structure():
    """Проверяет наличие всех обязательных директорий верхнего уровня."""
    for dir_name in EXPECTED_DIRECTORIES:
        dir_path = os.path.join(REPO_ROOT, dir_name)
        assert os.path.isdir(dir_path), f"❌ Отсутствует обязательная директория: {dir_name}"

def test_required_root_files():
    """Проверяет наличие обязательных файлов в корне репозитория."""
    for file_name in REQUIRED_ROOT_FILES:
        file_path = os.path.join(REPO_ROOT, file_name)
        assert os.path.isfile(file_path), f"❌ Отсутствует обязательный файл: {file_name}"

def test_readme_content():
    """Проверяет наличие ключевых разделов в главном README.md."""
    readme_path = os.path.join(REPO_ROOT, "README.md")
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for section in REQUIRED_SECTIONS_IN_README:
        assert section in content, f"❌ В README.md отсутствует ключевой раздел: '{section}'"

def test_markdown_files_have_headings():
    """Проверяет, что все .md файлы содержат хотя бы один заголовок Markdown (# или ##)."""
    for root, dirs, files in os.walk(REPO_ROOT):
        # Исключаем системные и служебные папки
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != '.git']
        
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Проверка на наличие заголовка первого или второго уровня
                has_heading = bool(re.search(r'^#{1,2}\s+.+', content, re.MULTILINE))
                assert has_heading, f"❌ Файл {file_path} не содержит заголовков Markdown"

def test_module_file_naming_conventions():
    """Проверяет, что файлы в модулях используют нижний регистр и snake_case (без пробелов)."""
    modules = [d for d in os.listdir(REPO_ROOT) if d.startswith("M")]
    for module in modules:
        module_path = os.path.join(REPO_ROOT, module)
        if os.path.isdir(module_path):
            for root, dirs, files in os.walk(module_path):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if file.endswith(".md"):
                        # Проверка на нижний регистр
                        assert file == file.lower(), f"❌ Файл '{file}' в модуле '{module}' должен быть в нижнем регистре"
                        # Проверка на отсутствие пробелов в имени файла
                        assert " " not in file, f"❌ Файл '{file}' содержит пробелы в имени. Используйте '_'."
