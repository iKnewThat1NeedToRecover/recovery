proton.me




{

import hashlib

# 1. Взять символы из файла
seed = open("pass.seed", encoding="utf-8").read().strip()

# 2. Провести через ключевое слово
keyword = input("Ключевое слово: ")

# 3. Получить пароль
password = (f"{seed}::{keyword}".encode())

# 4. Вывести
print(password)

}
