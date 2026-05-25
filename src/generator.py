import secrets
import string


def generate_password(
    length: int = 12,
    use_upper: bool = True,
    use_digits: bool = True,
    use_special: bool = True
) -> str:
    """Генерирует случайный пароль заданной длины с учетом флагов."""
    alphabet = string.ascii_lowercase
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_special:
        alphabet += string.punctuation

    if not alphabet:
        raise ValueError("Должен быть выбран хотя бы один набор символов.")

    return ''.join(secrets.choice(alphabet) for _ in range(length))


def check_strength(password: str) -> str:
    """Оценивает силу пароля по шкале от 'Слабый' до 'Надежный'."""
    score = 0
    if len(password) >= 12:
        score += 1
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 1:
        return "Слабый"
    elif score <= 3:
        return "Средний"
    return "Надежный"
