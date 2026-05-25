"""
Название проекта: Генератор паролей + БД сохранённых
Автор: Копосов Егор | Группа: [Твоя группа] | Вариант №: 3
Описание: Консольное приложение для безопасной генерации паролей.
"""

import sys
from .generator import generate_password, check_strength
from .db import (
    init_db, is_master_password_set, set_master_password,
    verify_master_password, save_entry, get_all_entries
)
from .export import export_to_keepass_csv


def main():
    print("🟢 Инициализация базы данных...")
    init_db()

    # Блок авторизации
    if not is_master_password_set():
        print("\nДобро пожаловать! Похоже, вы запускаете программу впервые.")
        master_pwd = input("Придумайте Мастер-пароль: ")
        set_master_password(master_pwd)
        print("✅ Мастер-пароль успешно установлен!")
    else:
        print("\n🔒 Вход в хранилище")
        attempts = 3
        while attempts > 0:
            master_pwd = input("Введите Мастер-пароль: ")
            if verify_master_password(master_pwd):
                print("✅ Доступ разрешен!")
                break
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"❌ Неверный пароль. Попыток: {attempts}")

        if attempts == 0:
            print("⛔ Доступ запрещен. Выход из программы.")
            return 1

    # Главное меню программы
    while True:
        print("\n" + "="*30)
        print("🛡 ГЛАВНОЕ МЕНЮ")
        print("="*30)
        print("1. Сгенерировать и сохранить пароль")
        print("2. Посмотреть сохраненные пароли")
        print("3. Экспорт в KeePass (CSV)")
        print("4. Выход")

        choice = input("\nВыберите действие (1-4): ")

        if choice == '1':
            service = input("Введите название сервиса (например, GitHub): ")
            username = input("Введите логин/email: ")
            length_str = input("Введите длину (нажмите Enter для 12): ")

            length = int(length_str) if length_str.isdigit() else 12

            new_pwd = generate_password(length=length)
            strength = check_strength(new_pwd)

            print(f"\n🔑 Сгенерирован пароль: {new_pwd}")
            print(f"🛡 Надежность: {strength}")

            save_entry(service, username, new_pwd)
            print("✅ Запись успешно сохранена в базу!")

        elif choice == '2':
            entries = get_all_entries()
            if not entries:
                print("\n📭 База паролей пока пуста.")
            else:
                print("\n" + "-"*30)
                print("📂 СОХРАНЕННЫЕ ПАРОЛИ")
                print("-"*30)
                for idx, (srv, usr, pwd) in enumerate(entries, 1):
                    print(f"{idx}. {srv} | Логин: {usr} | Пароль: {pwd}")

        elif choice == '3':
            print("\n⏳ Подготовка файла для KeePass...")
            success, message = export_to_keepass_csv()
            print(message)

        elif choice == '4':
            print("\n👋 Завершение работы. До свидания!")
            break

        else:
            print("\n❌ Неизвестная команда. Попробуйте снова.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
