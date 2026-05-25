import csv
import os
from .db import get_all_entries


def export_to_keepass_csv() -> tuple[bool, str]:
    """Экспортирует сохраненные пароли в CSV файл для KeePass."""
    base_dir = os.path.dirname(__file__)
    export_path = os.path.join(base_dir, '..', 'data', 'keepass_export.csv')
    entries = get_all_entries()

    if not entries:
        return False, "База данных пуста. Нечего экспортировать."

    try:
        with open(export_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['Group', 'Title', 'Username', 'Password', 'URL', 'Notes']
            )

            for service, username, password in entries:
                writer.writerow([
                    'Python Export', service, username, password, '',
                    'Сгенерировано нашим приложением'
                ])

        abs_path = os.path.abspath(export_path)
        return True, f"✅ Экспорт завершен!\n📁 Файл: {abs_path}"
    except Exception as e:
        return False, f"❌ Ошибка при экспорте: {e}"
ы