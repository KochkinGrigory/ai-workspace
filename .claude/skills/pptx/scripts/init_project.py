#!/usr/bin/env python3
"""
Инициализация проекта презентации.

Создаёт структуру папок и копирует шаблон presentation.md.

Использование:
    python init_project.py <название-проекта>
    python init_project.py marketing-strategy
    python init_project.py "Годовой отчёт 2024"
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Пути
SKILL_DIR = Path(__file__).parent.parent
PROJECTS_DIR = SKILL_DIR / "projects"
TEMPLATE_FILE = SKILL_DIR / "templates" / "presentation-template.md"


def slugify(text: str) -> str:
    """Преобразует текст в slug для имени папки."""
    # Заменяем пробелы на дефисы
    text = text.strip().lower().replace(" ", "-")
    # Оставляем только буквы, цифры и дефисы
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    text = "".join(c for c in text if c in allowed)
    # Убираем множественные дефисы
    while "--" in text:
        text = text.replace("--", "-")
    return text.strip("-")


def create_project(name: str) -> Path:
    """Создаёт структуру проекта презентации."""

    # Формируем имя папки
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(name)
    folder_name = f"{date_prefix}_{slug}"

    project_dir = PROJECTS_DIR / folder_name

    # Проверяем что папка не существует
    if project_dir.exists():
        print(f"Ошибка: Папка уже существует: {project_dir}")
        sys.exit(1)

    # Создаём структуру
    (project_dir / "assets").mkdir(parents=True)
    (project_dir / "slides").mkdir(parents=True)
    (project_dir / "output").mkdir(parents=True)

    # Копируем шаблон
    if TEMPLATE_FILE.exists():
        dest = project_dir / "presentation.md"
        shutil.copy(TEMPLATE_FILE, dest)

        # Заменяем плейсхолдер названия
        content = dest.read_text(encoding="utf-8")
        content = content.replace("[Название презентации]", name)
        content = content.replace("[дата]", datetime.now().strftime("%Y-%m-%d"))
        dest.write_text(content, encoding="utf-8")
    else:
        # Создаём минимальный файл если шаблона нет
        (project_dir / "presentation.md").write_text(
            f"# {name}\n\n> Проект создан: {datetime.now().strftime('%Y-%m-%d')}\n",
            encoding="utf-8"
        )

    return project_dir


def main():
    if len(sys.argv) < 2:
        print("Использование: python init_project.py <название-проекта>")
        print("Пример: python init_project.py marketing-strategy")
        sys.exit(1)

    name = " ".join(sys.argv[1:])

    project_dir = create_project(name)

    print(f"✅ Проект создан: {project_dir}")
    print()
    print("Структура:")
    print(f"  {project_dir}/")
    print("  ├── presentation.md    # Описание и структура")
    print("  ├── assets/            # Фоны, персонажи, логотипы")
    print("  ├── slides/            # Готовые визуалы слайдов")
    print("  └── output/            # Финальный .pptx")
    print()
    print("Следующие шаги:")
    print(f"  1. Отредактируй {project_dir}/presentation.md")
    print("  2. Сгенерируй фон и персонажей (nano-banana)")
    print("  3. Создай визуалы слайдов (edit.py)")
    print("  4. Собери презентацию (html2pptx)")


if __name__ == "__main__":
    main()
