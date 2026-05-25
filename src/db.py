import sqlite3
import hashlib
import os

# Путь к файлу базы данных будет вести в папку data/
DB_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'data', 'passwords.db'
)


def get_connection():
    """Создает подключение к БД и гарантирует наличие папки data."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """Создает таблицы, если они не существуют."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Таблица для мастер-пароля (храним только хэш)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS master (
                id INTEGER PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        ''')
        # Таблица для сохраненных паролей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()


def hash_password(password: str) -> str:
    """Возвращает SHA-256 хэш пароля."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def set_master_password(password: str):
    """Сохраняет хэш мастер-пароля (заменяя старый, если был)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM master")
        cursor.execute(
            "INSERT INTO master (password_hash) VALUES (?)",
            (hash_password(password),)
        )
        conn.commit()


def verify_master_password(password: str) -> bool:
    """Проверяет, совпадает ли введенный пароль с хэшем в БД."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM master LIMIT 1")
        result = cursor.fetchone()
        if not result:
            return False
        return result[0] == hash_password(password)


def is_master_password_set() -> bool:
    """Проверяет, установлен ли мастер-пароль."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM master")
        return cursor.fetchone()[0] > 0


def save_entry(service: str, username: str, password: str):
    """Сохраняет новую запись в БД."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO entries (service, username, password) VALUES (?, ?, ?)",
            (service, username, password)
        )
        conn.commit()


def get_all_entries() -> list:
    """Получает все записи из БД."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT service, username, password FROM entries")
        return cursor.fetchall()
