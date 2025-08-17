#!/usr/bin/env python3
"""
Универсальный конвертер Markdown в различные форматы (HTML, PDF)
Поддерживает Mermaid диаграммы и подсветку синтаксиса кода
"""

import re
import sys
import base64
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from enum import Enum

# Установка зависимостей при необходимости
try:
    import requests
    import markdown
    from bs4 import BeautifulSoup
    from playwright.sync_api import sync_playwright
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import HtmlFormatter
    from pygments.styles import get_style_by_name, get_all_styles
except ImportError:
    print("Установка необходимых библиотек...")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "markdown",
            "beautifulsoup4",
            "playwright",
            "requests",
            "pygments",
        ]
    )
    import requests
    import markdown
    from bs4 import BeautifulSoup
    from playwright.sync_api import sync_playwright
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import HtmlFormatter
    from pygments.styles import get_style_by_name, get_all_styles


class OutputFormat(Enum):
    """Поддерживаемые форматы вывода"""

    HTML = "html"
    PDF = "pdf"


class Theme(Enum):
    """Доступные темы оформления"""

    DEFAULT = "default"
    DARK = "dark"
    GITHUB = "github"
    MINIMAL = "minimal"


class UniversalMarkdownConverter:
    """Универсальный конвертер Markdown в различные форматы"""

    # CSS темы оформления
    THEMES = {
        Theme.DEFAULT: """
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
            
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                line-height: 1.7;
                color: #2c3e50;
                background: white;
                padding: 40px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            h1 {
                color: #2c3e50;
                font-size: 2.5em;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #3498db;
                page-break-after: avoid;
            }
            
            h2 {
                color: #34495e;
                font-size: 2em;
                margin-top: 40px;
                margin-bottom: 20px;
                padding-bottom: 8px;
                border-bottom: 2px solid #ecf0f1;
                page-break-after: avoid;
            }
            
            h3 {
                color: #34495e;
                font-size: 1.5em;
                margin-top: 30px;
                margin-bottom: 15px;
                page-break-after: avoid;
            }
            
            p { margin-bottom: 15px; text-align: justify; }
            ul, ol { margin-bottom: 20px; padding-left: 30px; }
            li { margin-bottom: 8px; }
            
            code {
                background: #f8f9fa;
                padding: 2px 6px;
                border-radius: 4px;
                font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
                font-size: 0.9em;
                color: #e74c3c;
            }
            
            pre {
                background: #2c3e50;
                color: #ecf0f1;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                page-break-inside: avoid;
                font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
                font-size: 0.9em;
                line-height: 1.5;
            }
            
            pre code {
                background: none;
                color: #ecf0f1;
                padding: 0;
            }
            
            .highlight {
                border-radius: 8px;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
                page-break-inside: avoid;
            }
            
            .highlight pre {
                margin: 0 !important;
                padding: 20px;
                overflow-x: auto;
                font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
                font-size: 0.9em;
                line-height: 1.5;
                border: none !important;
                background: inherit;
            }
            
            blockquote {
                border-left: 4px solid #3498db;
                padding-left: 20px;
                margin: 20px 0;
                font-style: italic;
                color: #7f8c8d;
                background: #ecf0f1;
                padding: 15px 20px;
                border-radius: 0 8px 8px 0;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                page-break-inside: avoid;
            }
            
            th {
                background: #3498db;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }
            
            td {
                padding: 12px;
                border-bottom: 1px solid #ecf0f1;
            }
            
            tr:nth-child(even) { background: #f8f9fa; }
            
            strong { font-weight: 600; color: #2c3e50; }
            
            img {
                max-width: 100%;
                height: auto;
                display: block;
                margin: 20px auto;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .mermaid-diagram {
                text-align: center;
                margin: 20px 0;
            }
            
            .mermaid-diagram svg {
                max-width: 100%;
                height: auto;
            }
            
            @media print {
                body { padding: 20px; }
                h1, h2, h3, h4 { page-break-after: avoid; }
                pre, table, img, .highlight { page-break-inside: avoid; }
            }
        """,
        Theme.DARK: """
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
            
            body {
                font-family: 'Inter', sans-serif;
                line-height: 1.7;
                color: #e0e0e0;
                background: #1a1a1a;
                padding: 40px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            h1, h2, h3, h4 { color: #ffffff; }
            h1 { border-bottom-color: #4a9eff; }
            h2 { border-bottom-color: #333; }
            
            code { background: #2d2d2d; color: #f92672; }
            pre { background: #2d2d2d; color: #f8f8f2; }
            
            blockquote {
                background: #2d2d2d;
                border-left-color: #4a9eff;
                color: #b0b0b0;
            }
            
            table { background: #2d2d2d; }
            th { background: #4a9eff; }
            td { border-bottom-color: #333; }
            tr:nth-child(even) { background: #252525; }
            
            .mermaid-diagram {
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }
        """,
        Theme.GITHUB: """
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
                line-height: 1.5;
                color: #24292e;
                background: #ffffff;
                padding: 32px;
                max-width: 980px;
                margin: 0 auto;
            }
            
            h1 {
                padding-bottom: 0.3em;
                font-size: 2em;
                border-bottom: 1px solid #eaecef;
            }
            
            h2 {
                padding-bottom: 0.3em;
                font-size: 1.5em;
                border-bottom: 1px solid #eaecef;
            }
            
            code {
                padding: 0.2em 0.4em;
                margin: 0;
                font-size: 85%;
                background-color: rgba(27,31,35,0.05);
                border-radius: 3px;
            }
            
            pre {
                padding: 16px;
                overflow: auto;
                font-size: 85%;
                line-height: 1.45;
                background-color: #f6f8fa;
                border-radius: 6px;
            }
            
            blockquote {
                padding: 0 1em;
                color: #6a737d;
                border-left: 0.25em solid #dfe2e5;
            }
        """,
        Theme.MINIMAL: """
            body {
                font-family: Georgia, serif;
                line-height: 1.8;
                color: #333;
                background: #fff;
                padding: 2em;
                max-width: 700px;
                margin: 0 auto;
            }
            
            h1, h2, h3, h4 {
                font-family: Helvetica, Arial, sans-serif;
                margin-top: 2em;
            }
            
            h1 { font-size: 2em; }
            
            code {
                font-family: Consolas, Monaco, monospace;
                background: #f4f4f4;
                padding: 2px 4px;
            }
            
            pre {
                background: #f4f4f4;
                padding: 1em;
                overflow-x: auto;
            }
            
            blockquote {
                margin-left: 0;
                padding-left: 1em;
                border-left: 3px solid #ddd;
                color: #666;
            }
        """,
    }

    def __init__(
        self,
        input_file: str,
        output_format: OutputFormat = OutputFormat.HTML,
        output_file: Optional[str] = None,
        code_style: str = "monokai",
        theme: Theme = Theme.DEFAULT,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Инициализация конвертера

        Args:
            input_file: Путь к входному Markdown файлу
            output_format: Формат выходного файла
            output_file: Путь к выходному файлу (если не указан, генерируется автоматически)
            code_style: Стиль подсветки синтаксиса кода
            theme: Тема оформления документа
            config: Дополнительные настройки конвертера
        """
        self.input_file = Path(input_file)
        self.output_format = output_format
        self.output_file = (
            Path(output_file) if output_file else self._generate_output_filename()
        )
        self.code_style = code_style
        self.theme = theme
        self.config = config or {}

        # Настройки по умолчанию
        self.config.setdefault("embed_images", True)
        self.config.setdefault("standalone", True)
        self.config.setdefault("minify", False)
        self.config.setdefault("include_toc", False)

        # Временная директория для промежуточных файлов
        self.temp_dir = Path(tempfile.mkdtemp())
        self.mermaid_counter = 0

        # Создаём форматтер для подсветки кода
        self.code_formatter = HtmlFormatter(
            style=code_style,
            cssclass="highlight",
            nowrap=False,
            noclasses=False,
            nobackground=False,
            linenos=False,
        )

        # Расширения Markdown
        self.markdown_extensions = [
            "tables",
            "fenced_code",
            "nl2br",
            "sane_lists",
            "footnotes",
            "attr_list",
            "def_list",
            "abbr",
            "md_in_html",
        ]

        if self.config.get("include_toc"):
            self.markdown_extensions.append("toc")

    def _generate_output_filename(self) -> Path:
        """Генерирует имя выходного файла на основе формата"""
        extensions = {OutputFormat.HTML: ".html", OutputFormat.PDF: ".pdf"}
        return self.input_file.with_suffix(extensions[self.output_format])

    def escape_html(self, text: str) -> str:
        """Экранирует HTML символы"""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    def highlight_code_block(self, code: str, language: Optional[str] = None) -> str:
        """
        Подсвечивает блок кода используя Pygments

        Args:
            code: Код для подсветки
            language: Язык программирования

        Returns:
            HTML с подсвеченным кодом
        """
        try:
            if language:
                try:
                    lexer = get_lexer_by_name(language, stripall=True)
                except Exception:
                    lexer = guess_lexer(code)
            else:
                lexer = guess_lexer(code)

            return highlight(code, lexer, self.code_formatter)
        except Exception:
            return f'<pre class="highlight"><code>{self.escape_html(code)}</code></pre>'

    def process_code_blocks(self, content: str) -> str:
        """Обрабатывает все блоки кода в Markdown, добавляя подсветку синтаксиса"""
        # Сохраняем mermaid блоки
        mermaid_blocks = []
        mermaid_pattern = r"```mermaid\n(.*?)\n```"

        def save_mermaid(match):
            mermaid_blocks.append(match.group(0))
            return f"<<<MERMAID_BLOCK_{len(mermaid_blocks) - 1}>>>"

        content_with_placeholders = re.sub(
            mermaid_pattern, save_mermaid, content, flags=re.DOTALL
        )

        # Обрабатываем блоки кода с языком
        code_pattern = r"```(\w+)\n(.*?)\n```"

        def highlight_match(match):
            language = match.group(1)
            code = match.group(2)
            return self.highlight_code_block(code, language)

        content_highlighted = re.sub(
            code_pattern, highlight_match, content_with_placeholders, flags=re.DOTALL
        )

        # Обрабатываем блоки кода без языка
        generic_code_pattern = r"```\n(.*?)\n```"

        def highlight_generic(match):
            code = match.group(1)
            return self.highlight_code_block(code)

        content_highlighted = re.sub(
            generic_code_pattern,
            highlight_generic,
            content_highlighted,
            flags=re.DOTALL,
        )

        # Восстанавливаем mermaid блоки
        for i, block in enumerate(mermaid_blocks):
            content_highlighted = content_highlighted.replace(
                f"<<<MERMAID_BLOCK_{i}>>>", block
            )

        return content_highlighted

    def render_mermaid_online(self, diagram_code: str) -> Optional[str]:
        """Рендерит Mermaid диаграмму через онлайн сервис"""
        url = "https://kroki.io/mermaid/svg"
        encoded = base64.urlsafe_b64encode(diagram_code.encode("utf-8")).decode("ascii")

        try:
            response = requests.get(f"{url}/{encoded}")
            if response.status_code == 200:
                svg_file = self.temp_dir / f"mermaid_{self.mermaid_counter}.svg"
                svg_file.write_text(response.text, encoding="utf-8")
                self.mermaid_counter += 1
                return str(svg_file)
        except Exception as e:
            print(f"Ошибка при рендеринге диаграммы: {e}")
            return None

    def _render_md_html(self, p, html_file, png_file):
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file:///{html_file.absolute()}")
        page.wait_for_timeout(2000)

        element = page.locator(".mermaid")
        element.screenshot(path=str(png_file))
        browser.close()

    def render_mermaid_local(self, diagram_code: str) -> Optional[str]:
        """Рендерит Mermaid диаграмму локально через Playwright"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>mermaid.initialize({ startOnLoad: true });</script>
            <style>
                body { background: white; }
                .mermaid { text-align: center; }
            </style>
        </head>
        <body>
            <div class="mermaid">
            {diagram}
            </div>
        </body>
        </html>
        """

        html_file = self.temp_dir / f"mermaid_{self.mermaid_counter}.html"
        html_content = html_template.replace("{diagram}", diagram_code)
        html_file.write_text(html_content, encoding="utf-8")

        png_file = self.temp_dir / f"mermaid_{self.mermaid_counter}.png"

        try:
            with sync_playwright() as p:
                self._render_md_html(p, html_file, png_file)
            self.mermaid_counter += 1
            return str(png_file)
        except Exception as e:
            print(f"Ошибка при локальном рендеринге: {e}")
            return None

    def format_mermaid_for_html(self, diagram_path: str) -> str:
        """Форматирует Mermaid диаграмму для HTML"""
        if self.config.get("embed_images"):
            # Встраиваем SVG напрямую
            if diagram_path.endswith(".svg"):
                svg_content = Path(diagram_path).read_text(encoding="utf-8")
                return f'<div class="mermaid-diagram">{svg_content}</div>'
            else:
                # Для PNG используем base64
                with open(diagram_path, "rb") as img_file:
                    img_data = img_file.read()
                    img_base64 = base64.b64encode(img_data).decode("utf-8")
                    return f'<div class="mermaid-diagram"><img src="data:image/png;base64,{img_base64}" alt="Mermaid Diagram"/></div>'
        else:
            file_path = Path(diagram_path).absolute()
            return f'<div class="mermaid-diagram"><img src="file:///{file_path}" alt="Mermaid Diagram"/></div>'

    def process_markdown(self, content: str, use_online: bool = False) -> str:
        """Обрабатывает Markdown, заменяя Mermaid диаграммы и подсвечивая код"""
        # Подсвечиваем код
        content = self.process_code_blocks(content)

        # Обрабатываем mermaid диаграммы
        pattern = r"```mermaid\n(.*?)\n```"

        def replace_mermaid(match):
            diagram_code = match.group(1)

            if use_online:
                image_path = self.render_mermaid_online(diagram_code)
            else:
                image_path = self.render_mermaid_local(diagram_code)

            if image_path:
                return self.format_mermaid_for_html(image_path)
            else:
                return f"<pre><code>{diagram_code}</code></pre>"

        processed_content = re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)
        return processed_content

    def markdown_to_html(self, content: str) -> str:
        """Конвертирует обработанный Markdown в HTML"""
        return markdown.markdown(content, extensions=self.markdown_extensions)

    def create_html_document(self, body_content: str) -> str:
        """Создает полный HTML документ"""
        title = self.input_file.stem.replace("_", " ").title()
        theme_css = self.THEMES[self.theme]

        # Получаем дополнительный CSS, если тема не минимальная
        if self.theme != Theme.MINIMAL:
            theme_css = self.THEMES[Theme.DEFAULT] + "\n" + self.THEMES[self.theme]

        pygments_css = self.code_formatter.get_style_defs(".highlight")

        if self.config.get("standalone"):
            return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {theme_css}
        
        /* Pygments syntax highlighting */
        {pygments_css}
    </style>
</head>
<body>
    {body_content}
</body>
</html>"""
        else:
            return body_content

    def minify_html(self, html_content: str) -> str:
        """Минифицирует HTML"""
        import re

        # Убираем комментарии
        html_content = re.sub(r"<!--.*?-->", "", html_content, flags=re.DOTALL)
        # Убираем лишние пробелы между тегами
        html_content = re.sub(r">\s+<", "><", html_content)
        # Убираем лишние пробелы в начале строк
        html_content = re.sub(r"^\s+", "", html_content, flags=re.MULTILINE)

        return html_content.strip()

    def generate_html(self, use_online_mermaid: bool = False) -> str:
        """
        Генерирует HTML из Markdown
        Это центральный метод, используемый как для HTML, так и для PDF

        Returns:
            Готовый HTML документ
        """
        print(f"📄 Обработка {self.input_file}...")
        print(f"🎨 Стиль подсветки кода: {self.code_style}")
        print(f"🎨 Тема оформления: {self.theme.value}")

        # Читаем Markdown файл
        content = self.input_file.read_text(encoding="utf-8")

        # Обрабатываем код и Mermaid диаграммы
        print("🖌️ Подсветка синтаксиса кода...")
        print("🎨 Рендеринг Mermaid диаграмм...")
        processed_content = self.process_markdown(
            content, use_online=use_online_mermaid
        )

        # Конвертируем в HTML
        print("📝 Генерация HTML...")
        html_body = self.markdown_to_html(processed_content)

        # Создаем финальный HTML документ
        html_content = self.create_html_document(html_body)

        # Минифицируем если нужно
        if self.config.get("minify"):
            print("📦 Минификация HTML...")
            html_content = self.minify_html(html_content)

        return html_content

    def convert_to_html(self, use_online_mermaid: bool = False) -> None:
        """Конвертирует Markdown в HTML файл"""
        html_content = self.generate_html(use_online_mermaid)

        # Сохраняем результат
        self.output_file.write_text(html_content, encoding="utf-8")

        print(f"✅ HTML успешно создан: {self.output_file}")
        self._show_file_size()

    def _pdf_rendering(self, p, html_file):
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file:///{html_file.absolute()}")
        page.wait_for_timeout(2000)

        # Генерируем PDF
        page.pdf(
            path=str(self.output_file),
            format="A4",
            margin={
                "top": "20mm",
                "right": "20mm",
                "bottom": "20mm",
                "left": "20mm",
            },
            print_background=True,
        )

        browser.close()

    def convert_to_pdf(self, use_online_mermaid: bool = False) -> None:
        """Конвертирует Markdown в PDF через HTML"""
        # Сначала генерируем HTML
        html_content = self.generate_html(use_online_mermaid)

        # Сохраняем HTML во временный файл
        html_file = self.temp_dir / "temp.html"
        html_file.write_text(html_content, encoding="utf-8")

        print("📑 Генерация PDF...")

        try:
            with sync_playwright() as p:
                self._pdf_rendering(p, html_file)
            print(f"✅ PDF успешно создан: {self.output_file}")
            self._show_file_size()

        except Exception as e:
            print(f"❌ Ошибка при создании PDF: {e}")
            print("Попробуйте установить Chromium: playwright install chromium")

    def convert(self, use_online_mermaid: bool = False) -> None:
        """
        Универсальный метод конвертации
        Выбирает нужный конвертер на основе output_format
        """
        if self.output_format == OutputFormat.HTML:
            self.convert_to_html(use_online_mermaid)
        elif self.output_format == OutputFormat.PDF:
            self.convert_to_pdf(use_online_mermaid)
        else:
            raise ValueError(f"Неподдерживаемый формат: {self.output_format}")

        # Очищаем временные файлы
        self.cleanup()

    def cleanup(self) -> None:
        """Очищает временные файлы"""
        import shutil

        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def _show_file_size(self) -> None:
        """Показывает размер созданного файла"""
        file_size = self.output_file.stat().st_size
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{file_size / 1024:.2f} KB"
        print(f"📊 Размер файла: {size_str}")


def setup_playwright():
    """Установка Playwright и Chromium"""
    print("🔧 Настройка Playwright...")
    try:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"], check=True
        )
        print("✅ Playwright и Chromium установлены")
    except Exception as e:
        print(f"❌ Ошибка установки Playwright: {e}")


def list_available_styles():
    """Показывает доступные стили подсветки синтаксиса"""
    styles = list(get_all_styles())
    print("\n🎨 Доступные стили подсветки синтаксиса:")
    print("=" * 50)
    for i, style in enumerate(styles, 1):
        print(f"  {i:2}. {style}")
    print("=" * 50)
    print(f"Всего стилей: {len(styles)}\n")
    print("Популярные стили:")
    print("  • monokai - темная тема с яркими цветами")
    print("  • dracula - популярная темная тема")
    print("  • github - светлая тема в стиле GitHub")
    print("  • vs - светлая тема Visual Studio")
    return styles


def main():
    """Главная функция"""

    # Проверяем аргументы командной строки
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        print(
            """
╔════════════════════════════════════════════════════════════╗
║     Универсальный конвертер Markdown с Mermaid в PDF/HTML  ║
╚════════════════════════════════════════════════════════════╝

Использование:
    python universal_converter.py input.md [опции]

Параметры:
    input.md       - входной Markdown файл

Опции:
    --format FORMAT    - формат вывода: html (по умолчанию) или pdf
    --output FILE      - имя выходного файла (автоматически если не указано)
    --theme THEME      - тема оформления: default, dark, github, minimal
    --style STYLE      - стиль подсветки кода (по умолчанию: monokai)
    --online          - использовать онлайн сервис для Mermaid
    --minify          - минифицировать HTML
    --no-standalone   - генерировать только body HTML
    --no-embed        - не встраивать изображения в HTML
    --toc             - добавить оглавление
    --list-styles     - показать все доступные стили подсветки

Примеры:
    python universal_converter.py document.md
    python universal_converter.py document.md --format pdf
    python universal_converter.py document.md --format html --theme dark
    python universal_converter.py document.md --output report.pdf --format pdf
    python universal_converter.py document.md --style github --theme github
    python universal_converter.py --list-styles

Первый запуск:
    При первом запуске для PDF будет установлен Chromium (~130MB)
    Или используйте флаг --online для работы без Chromium
        """
        )
        sys.exit(1)

    # Проверка опции показа стилей
    if sys.argv[1] == "--list-styles":
        list_available_styles()
        sys.exit(0)

    # Парсинг аргументов
    input_file = sys.argv[1]
    output_file = None
    output_format = OutputFormat.HTML
    theme = Theme.DEFAULT
    code_style = "monokai"
    use_online = False
    config = {}

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg == "--format" and i + 1 < len(sys.argv):
            format_str = sys.argv[i + 1].lower()
            if format_str == "pdf":
                output_format = OutputFormat.PDF
            elif format_str == "html":
                output_format = OutputFormat.HTML
            else:
                print(f"⚠️ Неизвестный формат '{format_str}', используется HTML")
            i += 1

        elif arg == "--output" and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 1

        elif arg == "--theme" and i + 1 < len(sys.argv):
            theme_str = sys.argv[i + 1].lower()
            theme_map = {
                "default": Theme.DEFAULT,
                "dark": Theme.DARK,
                "github": Theme.GITHUB,
                "minimal": Theme.MINIMAL,
            }
            theme = theme_map.get(theme_str, Theme.DEFAULT)
            i += 1

        elif arg == "--style" and i + 1 < len(sys.argv):
            code_style = sys.argv[i + 1]
            i += 1

        elif arg == "--online":
            use_online = True

        elif arg == "--minify":
            config["minify"] = True

        elif arg == "--no-standalone":
            config["standalone"] = False

        elif arg == "--no-embed":
            config["embed_images"] = False

        elif arg == "--toc":
            config["include_toc"] = True

        elif arg == "--list-styles":
            list_available_styles()
            sys.exit(0)

        i += 1

    # Проверяем существование входного файла
    if not Path(input_file).exists():
        print(f"❌ Файл не найден: {input_file}")
        sys.exit(1)

    # Проверяем валидность стиля
    try:
        from pygments.styles import get_style_by_name

        get_style_by_name(code_style)
    except:
        print(
            f"⚠️ Неизвестный стиль '{code_style}', используется стиль по умолчанию 'monokai'"
        )
        print("   Используйте --list-styles для просмотра доступных стилей")
        code_style = "monokai"

    # Устанавливаем Playwright если нужно для PDF
    if output_format == OutputFormat.PDF and not use_online:
        setup_playwright()

    # Создаем конвертер и выполняем конвертацию
    converter = UniversalMarkdownConverter(
        input_file=input_file,
        output_format=output_format,
        output_file=output_file,
        code_style=code_style,
        theme=theme,
        config=config,
    )

    converter.convert(use_online_mermaid=use_online)


if __name__ == "__main__":
    main()
