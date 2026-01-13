#!/usr/bin/env python3
"""
Конвертация PPTX в PDF с проверкой шрифтов.

Перед конвертацией проверяет, установлены ли все шрифты из презентации.
Если шрифт отсутствует - пытается установить из известных источников.

Использование:
    python pptx2pdf.py presentation.pptx
    python pptx2pdf.py presentation.pptx --output report.pdf
    python pptx2pdf.py presentation.pptx --check-only
"""

import argparse
import subprocess
import sys
import zipfile
import re
import os
import urllib.request
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

# Известные шрифты и их источники
FONT_SOURCES = {
    'arial': {
        'files': [
            ('arial.ttf', 'https://github.com/AntMargSan/arial-fonts/raw/master/arial.ttf'),
            ('arialbd.ttf', 'https://github.com/AntMargSan/arial-fonts/raw/master/arialbd.ttf'),
            ('ariali.ttf', 'https://github.com/AntMargSan/arial-fonts/raw/master/ariali.ttf'),
        ]
    },
    'times new roman': {
        'files': [
            ('times.ttf', 'https://github.com/AntMargSan/arial-fonts/raw/master/times.ttf'),
        ]
    },
    'manrope': {
        'package': 'fonts-manrope',  # apt package
        'files': []  # Устанавливается через apt
    },
    'liberation sans': {
        'package': 'fonts-liberation',
    },
    'liberation serif': {
        'package': 'fonts-liberation',
    },
    'dejavu sans': {
        'package': 'fonts-dejavu',
    },
}

# Альтернативы для шрифтов (если не удалось установить оригинал)
FONT_ALTERNATIVES = {
    'arial': 'Liberation Sans',
    'times new roman': 'Liberation Serif',
    'helvetica': 'Liberation Sans',
    'courier new': 'Liberation Mono',
}


def get_system_fonts() -> set:
    """Получить список установленных шрифтов в системе."""
    try:
        result = subprocess.run(
            ['fc-list', '--format', '%{family}\n'],
            capture_output=True, text=True, check=True
        )
        fonts = set()
        for line in result.stdout.strip().split('\n'):
            for font in line.split(','):
                fonts.add(font.strip().lower())
        return fonts
    except subprocess.CalledProcessError:
        return set()


def extract_fonts_from_pptx(pptx_path: str) -> set:
    """Извлечь список шрифтов из PPTX файла."""
    fonts = set()

    # Пробуем через python-pptx
    try:
        from pptx import Presentation
        from pptx.util import Pt

        prs = Presentation(pptx_path)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, 'text_frame'):
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            if run.font.name:
                                fonts.add(run.font.name.lower())
        return fonts
    except ImportError:
        pass

    # Fallback: парсим XML напрямую
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            for name in zf.namelist():
                if name.endswith('.xml'):
                    try:
                        content = zf.read(name).decode('utf-8')
                        # Ищем атрибуты typeface в XML
                        typeface_matches = re.findall(r'typeface="([^"]+)"', content, re.IGNORECASE)
                        for font in typeface_matches:
                            if font and not font.startswith('+'):
                                fonts.add(font.lower())
                    except:
                        pass
    except zipfile.BadZipFile:
        print(f"Ошибка: {pptx_path} не является валидным PPTX файлом")
        sys.exit(1)

    return fonts


def install_font(font_name: str) -> bool:
    """Попытаться установить шрифт."""
    font_lower = font_name.lower()

    if font_lower not in FONT_SOURCES:
        print(f"  [!] Неизвестный шрифт: {font_name}")
        if font_lower in FONT_ALTERNATIVES:
            alt = FONT_ALTERNATIVES[font_lower]
            print(f"      Альтернатива: {alt}")
        return False

    source = FONT_SOURCES[font_lower]

    # Попробуем установить через apt
    if 'package' in source:
        try:
            print(f"  [*] Устанавливаю пакет {source['package']}...")
            subprocess.run(
                ['apt-get', 'install', '-y', source['package']],
                capture_output=True, check=True
            )
            subprocess.run(['fc-cache', '-fv'], capture_output=True)
            print(f"  [+] Установлено через apt: {source['package']}")
            return True
        except subprocess.CalledProcessError:
            print(f"  [!] Не удалось установить через apt")

    # Попробуем скачать напрямую
    if 'files' in source and source['files']:
        font_dir = Path('/usr/share/fonts/truetype/custom')
        font_dir.mkdir(parents=True, exist_ok=True)

        success = True
        for filename, url in source['files']:
            dest = font_dir / filename
            if dest.exists():
                continue
            try:
                print(f"  [*] Скачиваю {filename}...")
                urllib.request.urlretrieve(url, dest)
            except Exception as e:
                print(f"  [!] Не удалось скачать {filename}: {e}")
                success = False

        if success:
            subprocess.run(['fc-cache', '-fv'], capture_output=True)
            print(f"  [+] Шрифт {font_name} установлен")
            return True

    return False


def check_and_install_fonts(fonts: set, auto_install: bool = True) -> tuple:
    """Проверить шрифты и установить отсутствующие."""
    system_fonts = get_system_fonts()

    missing = []
    installed = []

    for font in fonts:
        font_lower = font.lower()
        # Проверяем разные варианты имени
        found = any(
            font_lower in sf or sf in font_lower
            for sf in system_fonts
        )

        if not found:
            missing.append(font)

    if missing and auto_install:
        print(f"\nОтсутствующие шрифты: {', '.join(missing)}")
        print("Попытка установки...\n")

        for font in missing:
            if install_font(font):
                installed.append(font)

    return missing, installed


def convert_to_pdf(pptx_path: str, output_path: str = None) -> str:
    """Конвертировать PPTX в PDF через LibreOffice."""
    pptx_path = Path(pptx_path).resolve()

    if output_path:
        output_path = Path(output_path).resolve()
        output_dir = output_path.parent
        # LibreOffice не позволяет указать имя файла, только директорию
        # Поэтому конвертируем во временную папку и переименовываем
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = subprocess.run([
                'soffice', '--headless',
                '--convert-to', 'pdf',
                '--outdir', tmp_dir,
                str(pptx_path)
            ], capture_output=True, text=True)

            if result.returncode != 0:
                print(f"Ошибка конвертации: {result.stderr}")
                sys.exit(1)

            # Найдём созданный PDF и переименуем
            tmp_pdf = Path(tmp_dir) / (pptx_path.stem + '.pdf')
            if tmp_pdf.exists():
                import shutil
                shutil.move(str(tmp_pdf), str(output_path))
                return str(output_path)
    else:
        output_dir = pptx_path.parent
        output_path = output_dir / (pptx_path.stem + '.pdf')

        result = subprocess.run([
            'soffice', '--headless',
            '--convert-to', 'pdf',
            '--outdir', str(output_dir),
            str(pptx_path)
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Ошибка конвертации: {result.stderr}")
            sys.exit(1)

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Конвертация PPTX в PDF с проверкой шрифтов'
    )
    parser.add_argument('input', help='Путь к PPTX файлу')
    parser.add_argument('--output', '-o', help='Путь к выходному PDF файлу')
    parser.add_argument('--check-only', action='store_true',
                       help='Только проверить шрифты, не конвертировать')
    parser.add_argument('--no-install', action='store_true',
                       help='Не устанавливать отсутствующие шрифты')

    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Ошибка: файл не найден: {args.input}")
        sys.exit(1)

    # Извлекаем шрифты из презентации
    print(f"Анализ презентации: {args.input}")
    fonts = extract_fonts_from_pptx(args.input)

    if fonts:
        print(f"Используемые шрифты: {', '.join(sorted(fonts))}")
    else:
        print("Шрифты не обнаружены (возможно, используются системные)")

    # Проверяем и устанавливаем шрифты
    missing, installed = check_and_install_fonts(
        fonts,
        auto_install=not args.no_install
    )

    still_missing = set(missing) - set(installed)
    if still_missing:
        print(f"\n[!] Не удалось установить шрифты: {', '.join(still_missing)}")
        print("    PDF может отображаться с заменёнными шрифтами")

    if args.check_only:
        if still_missing:
            sys.exit(1)
        print("\nВсе шрифты доступны")
        sys.exit(0)

    # Конвертируем
    print(f"\nКонвертация в PDF...")
    output = convert_to_pdf(args.input, args.output)
    print(f"Готово: {output}")


if __name__ == '__main__':
    main()
