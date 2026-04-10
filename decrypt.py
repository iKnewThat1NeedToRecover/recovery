import hashlib
import os
import sys
import time
import getpass

def clear(): os.system("cls")

def banner():
    print("╔" + "═"*54 + "╗")
    print("║" + "  🔑  ДЕШИФРАТОР ПАРОЛЯ".center(54) + "║")
    print("║" + "  файл → ключевое слово → пароль архива".center(54) + "║")
    print("╚" + "═"*54 + "╝")
    print()

def progress(msg, steps=18, delay=0.04):
    print(f"\n  {msg}")
    print("  [", end="", flush=True)
    for _ in range(steps):
        time.sleep(delay)
        print("█", end="", flush=True)
    print("] ✔\n")

def key_stream(keyword: str, length: int) -> str:
    """Растягивает ключ через SHA-256 до нужной длины."""
    stream = hashlib.sha256(keyword.encode()).hexdigest()
    while len(stream) < length:
        stream += hashlib.sha256(stream.encode()).hexdigest()
    return stream

def derive_password(hex_data: str, keyword: str) -> str:
    """
    hex_data — зашифрованный hex из файла (создан через cipher.py)
    keyword  — ключевое слово
    Результат — оригинальный пароль архива
    """
    encoded = bytes.fromhex(hex_data).decode("utf-8")
    ks = key_stream(keyword, len(encoded))
    return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(encoded, ks))

def box(label: str, value: str):
    width = max(len(value) + 6, 52)
    print("  ╔" + "═"*width + "╗")
    print("  ║" + f"  {label}".ljust(width) + "║")
    print("  ║" + " "*width + "║")
    print("  ║" + f"  {value}".ljust(width) + "║")
    print("  ║" + " "*width + "║")
    print("  ╚" + "═"*width + "╝")

def main():
    clear()
    banner()

    # ─── ШАГ 1: файл с hex ───────────────────────────────────
    print("  ШАГ 1 — Укажи путь к файлу с набором символов:")
    print()
    seed_path = input("  Путь к файлу: ").strip().strip('"')

    if not os.path.exists(seed_path):
        print(f"\n  [ОШИБКА] Файл не найден: {seed_path}")
        input("\n  Enter для выхода..."); sys.exit(1)

    try:
        hex_data = open(seed_path, "r", encoding="utf-8").read().strip()
    except Exception as e:
        print(f"\n  [ОШИБКА] Не удалось прочитать файл: {e}")
        input("\n  Enter для выхода..."); sys.exit(1)

    if not hex_data:
        print("\n  [ОШИБКА] Файл пустой.")
        input("\n  Enter для выхода..."); sys.exit(1)

    print(f"\n  ✔  Файл прочитан  ({len(hex_data)} символов)")

    # ─── ШАГ 2: ключевое слово ───────────────────────────────
    print()
    print("  ШАГ 2 — Введи ключевое слово:")
    print("  (ввод скрыт)")
    print()
    keyword = getpass.getpass("  Ключевое слово: ").strip()

    if not keyword:
        print("\n  [ОШИБКА] Ключевое слово не может быть пустым.")
        input("\n  Enter для выхода..."); sys.exit(1)

    # ─── ВЫЧИСЛЕНИЕ ──────────────────────────────────────────
    progress("Расшифровываю пароль...")

    try:
        password = derive_password(hex_data, keyword)
    except Exception:
        print("  [ОШИБКА] Не удалось расшифровать — неверный файл или ключ.")
        input("\n  Enter для выхода..."); sys.exit(1)

    # ─── РЕЗУЛЬТАТ ───────────────────────────────────────────
    box("ПАРОЛЬ ДЛЯ АРХИВА:", password)

    print()
    print("  Скопируй пароль и введи его при открытии архива.")
    print()
    print("  ⚠  Закрой окно после использования —")
    print("     пароль нигде не сохраняется.")
    print()

    input("  Enter для выхода...")

    password = "0" * len(password)
    keyword = ""
    sys.exit(0)

if __name__ == "__main__":
    main()
