#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def get_files_by_size_os_walk(directory, reverse=True):
    """
    Получает список файлов, отсортированных по размеру, используя os.walk()
    
    Args:
        directory (str): Путь к директории для сканирования
        reverse (bool): True для сортировки от большего к меньшему
    
    Returns:
        list: Список кортежей (размер, путь_к_файлу)
    """
    files_info = []
    
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    files_info.append((file_size, file_path))
                except (OSError, IOError) as e:
                    print(f"Ошибка при обработке файла {file_path}: {e}")
                    continue
    except PermissionError as e:
        print(f"Нет доступа к директории {directory}: {e}")
        return []
    
    # Сортируем по размеру
    files_info.sort(key=lambda x: x[0], reverse=reverse)
    return files_info

def get_files_by_size_pathlib(directory, reverse=True):
    """
    Получает список файлов, отсортированных по размеру, используя pathlib
    
    Args:
        directory (str): Путь к директории для сканирования
        reverse (bool): True для сортировки от большего к меньшему
    
    Returns:
        list: Список кортежей (размер, путь_к_файлу)
    """
    files_info = []
    path = Path(directory)
    
    if not path.exists():
        print(f"Директория {directory} не существует")
        return []
    
    if not path.is_dir():
        print(f"{directory} не является директорией")
        return []
    
    try:
        # Рекурсивно находим все файлы
        for file_path in path.rglob('*'):
            if file_path.is_file():
                try:
                    file_size = file_path.stat().st_size
                    files_info.append((file_size, str(file_path)))
                except (OSError, IOError) as e:
                    print(f"Ошибка при обработке файла {file_path}: {e}")
                    continue
    except PermissionError as e:
        print(f"Нет доступа к директории {directory}: {e}")
        return []
    
    # Сортируем по размеру
    files_info.sort(key=lambda x: x[0], reverse=reverse)
    return files_info

def format_size(size_bytes):
    """
    Форматирует размер файла в человекочитаемый вид
    
    Args:
        size_bytes (int): Размер в байтах
    
    Returns:
        str: Отформатированный размер
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def print_files_info(files_info, show_count=None):
    """
    Выводит информацию о файлах
    
    Args:
        files_info (list): Список кортежей (размер, путь)
        show_count (int): Количество файлов для показа (None = все)
    """
    if not files_info:
        print("Файлы не найдены")
        return
    
    print(f"Найдено файлов: {len(files_info)}")
    print("-" * 80)
    print(f"{'Размер':<15} {'Путь к файлу'}")
    print("-" * 80)
    
    files_to_show = files_info[:show_count] if show_count else files_info
    
    for size, file_path in files_to_show:
        formatted_size = format_size(size)
        print(f"{formatted_size:<15} {file_path}")
    
    if show_count and len(files_info) > show_count:
        print(f"\n... и еще {len(files_info) - show_count} файлов")

def main():
    """Основная функция"""
    if len(sys.argv) < 2:
        print("Использование: python script.py <директория> [количество_файлов] [--asc]")
        print("  директория: Путь к директории для сканирования")
        print("  количество_файлов: Максимальное количество файлов для показа (опционально)")
        print("  --asc: Сортировка от меньшего к большему (по умолчанию от большего к меньшему)")
        sys.exit(1)
    
    directory = sys.argv[1]
    show_count = None
    reverse = True  # По умолчанию от большего к меньшему
    
    # Парсим аргументы
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--asc":
            reverse = False
        elif arg.isdigit():
            show_count = int(arg)
    
    print(f"Сканирование директории: {directory}")
    print(f"Сортировка: {'по убыванию' if reverse else 'по возрастанию'}")
    print()
    
    # Используем pathlib (более современный подход)
    files_info = get_files_by_size_pathlib(directory, reverse)
    
    # Альтернативно можно использовать os.walk:
    # files_info = get_files_by_size_os_walk(directory, reverse)
    
    print_files_info(files_info, show_count)

if __name__ == "__main__":
    main()
