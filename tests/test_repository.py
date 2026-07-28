import os
import pytest
import re

# Базовая директория репозитория
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ожидаемая структура папок верхнего уровня (проверено по актуальному состоянию репозитория)
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
    "Postrekvisity",  # Фактическое имя папки в репозитории
    "RPD",
    "SR",
    "docs",
    "team"
]

REQUIRED_ROOT_FILES = ["README.md", "LICENSE.md"]

REQUIRED_SECTIONS_IN_README = [
    "Цель дисциплины",
    "Модуль 1",
    "Модуль 8",
    "Компетенции",
    "Структура репозитория"
]

def test_repository_structure():
    """Проверяет наличие всех обязательных директорий верхнего уровня."""
    missing = [d for d in EXPECTED_DIRECTORIES if not os.path.isdir(os.path.join(REPO_ROOT, d))]
    assert not missing, f"❌ Отсутствуют обязательные директории: {', '.join(missing)}"

def test_required_root_files():
    """Проверяет наличие обязательных файлов в корне репозитория."""
    missing = [f for f in REQUIRED_ROOT_FILES if not os.path.isfile(os.path.join(REPO_ROOT, f))]
    assert not missing, f"❌ Отсутствуют обязательные файлы: {', '.join(missing)}"

def test_readme_content():
    """Проверяет наличие ключевых разделов в главном README.md."""
    readme_path = os.path.join(REPO_ROOT, "README.md")
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    missing_sections = [s for s in REQUIRED_SECTIONS_IN_README if s not in content]
    assert not missing_sections, f"❌ В README.md отсутствуют разделы: {', '.join(missing_sections)}"

def test_markdown_files_have_headings():
    """Проверяет, что все .md файлы содержат хотя бы один заголовок Markdown (# или ##)."""
    failed_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('__pycache__', '.git')]
        
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                has_heading = bool(re.search(r'^#{1,2}\s+.+', content, re.MULTILINE))
                if not has_heading:
                    failed_files.append(file_path)
    
    assert not failed_files, f"❌ Следующие .md файлы не содержат заголовков (# или ##):\n" + "\n".join(failed_files)

def test_no_spaces_in_filenames():
    """Проверяет, что имена файлов и папок не содержат пробелов (должен использоваться '_')."""
    failed_items = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for item in dirs + files:
            if " " in item:
                failed_items.append(os.path.join(root, item))
    
    assert not failed_items, f"❌ Найдены файлы/папки с пробелами в имени (замените пробелы на '_'):\n" + "\n".join(failed_items)
