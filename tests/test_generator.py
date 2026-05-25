import pytest
from src.generator import generate_password, check_strength

def test_password_default_length():
    """Проверяет длину пароля по умолчанию."""
    pwd = generate_password()
    assert len(pwd) == 12

def test_password_custom_length():
    """Проверяет заданную длину пароля."""
    pwd = generate_password(length=16)
    assert len(pwd) == 16
    pwd_short = generate_password(length=6)
    assert len(pwd_short) == 6

def test_strength_weak():
    """Проверяет оценку слабого пароля (только буквы одного регистра)."""
    assert check_strength("abcdef") == "Слабый"

def test_strength_medium():
    """
    Проверяет оценку среднего пароля.
    (Разные регистры + цифры = 2 балла -> Средний).
    """
    assert check_strength("aB123456") == "Средний"

def test_strength_strong():
    """
    Проверяет оценку надежного пароля.
    (Длина >= 12, разные регистры, цифры, спецсимволы = 4 балла -> Надежный).
    """
    assert check_strength("aB3!56789012") == "Надежный"