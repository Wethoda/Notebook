from datetime import datetime
import json
import csv

# Класс для заметки
class Note:
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags
        self.date = datetime.now().strftime("%Y-%m-%d")  # Убрано время (%H:%M:%S)

    def to_dict(self):
        return {
            "text": self.text,
            "tags": ", ".join(self.tags),
            "date": self.date
        }

# Класс для дневника
class Diary:
    def __init__(self):
        self.notes = []

    def add_note(self, text, tags):
        note = Note(text, tags)
        self.notes.append(note)
        print("Заметка добавлена.")

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            print(f"Заметка с индексом {index} удалена.")
        else:
            print(f"Ошибка: Заметка с индексом {index} не найдена.")

    def edit_note(self, index, new_text, new_tags):
        if 0 <= index < len(self.notes):
            self.notes[index].text = new_text
            self.notes[index].tags = new_tags
            print(f"Заметка с индексом {index} изменена.")
        else:
            print(f"Ошибка: Заметка с индексом {index} не найдена.")

    def find_date(self, date):
        return [note.to_dict() for note in self.notes if note.date == date]

    def find_text(self, text):
        return [note.to_dict() for note in self.notes if text.lower() in note.text.lower()]

    def find_tags(self, tag):
        return [note.to_dict() for note in self.notes if tag.lower() in [t.lower() for t in note.tags]]

    def list_notes(self):
        return [note.to_dict() for note in self.notes]

    def save_to_json(self, filename="notes.json"):
        data = [note.to_dict() for note in self.notes]
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            print("Заметки сохранены в JSON.")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

    def load_from_json(self, filename="notes.json"):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.notes = [Note(note['text'], note['tags'].split(", ")) for note in data]
            print("Заметки загружены из JSON.")
        except FileNotFoundError:
            print("Файл отсутствует!")
        except json.JSONDecodeError:
            print("Ошибка при чтении JSON.")

# Класс для пользователя
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.diary = Diary()

    def save_user_data(self):
        filename = f"{self.username}_notes.json"
        self.diary.save_to_json(filename)

    def load_user_data(self):
        filename = f"{self.username}_notes.json"
        self.diary.load_from_json(filename)

# Функция для работы с пользователями
def register():
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    users = load_users()
    if username in users:
        print("Ошибка: Пользователь уже существует.")
        return None
    users[username] = password
    save_users(users)
    print("Пользователь зарегистрирован.")
    return User(username, password)

def login():
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    users = load_users()
    if username in users and users[username] == password:
        print("Вход выполнен успешно.")
        return User(username, password)
    else:
        print("Ошибка: Неверное имя пользователя или пароль.")
        return None

def load_users():
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

# Основная программа
def main():
    current_user = None
    while True:
        if not current_user:
            print("\nДобро пожаловать!")
            print("1. Войти")
            print("2. Зарегистрироваться")
            print("3. Выйти")
            choice = input("Выберите действие: ")

            if choice == "1":
                current_user = login()
            elif choice == "2":
                current_user = register()
            elif choice == "3":
                print("Выход из программы.")
                break
            else:
                print("Ошибка: Некорректный выбор.")
        else:
            print(f"\nМеню пользователя {current_user.username}:")
            print("1. Добавить заметку")
            print("2. Удалить заметку")
            print("3. Редактировать заметку")
            print("4. Поиск по тексту")
            print("5. Сохранить заметки")
            print("6. Загрузить заметки")
            print("7. Просмотреть все заметки")
            print("8. Выйти из аккаунта")
            choice = input("Выберите действие: ")

            if choice == "1":
                text = input("Введите текст заметки: ")
                tags = input("Введите теги через запятую: ").split(",")
                current_user.diary.add_note(text, tags)

            elif choice == "2":
                try:
                    index = int(input("Введите индекс заметки для удаления: "))
                    current_user.diary.delete_note(index)
                except ValueError:
                    print("Ошибка: Введите корректный индекс.")

            elif choice == "3":
                try:
                    index = int(input("Введите индекс заметки для редактирования: "))
                    new_text = input("Введите новый текст: ")
                    new_tags = input("Введите новые теги через запятую: ").split(",")
                    current_user.diary.edit_note(index, new_text, new_tags)
                except ValueError:
                    print("Ошибка: Введите корректный индекс.")

            elif choice == "4":
                text = input("Введите текст заметки, которую ищете: ")
                filtered_notes = current_user.diary.find_text(text)
                if filtered_notes:
                    for note in filtered_notes:
                        print(f"Дата: {note['date']}, Текст: {note['text']}, Теги: {note['tags']}")
                else:
                    print("Заметки не найдены.")

            elif choice == "5":
                current_user.save_user_data()

            elif choice == "6":
                current_user.load_user_data()

            elif choice == "7":
                notes = current_user.diary.list_notes()
                if notes:
                    print("Список всех заметок:")
                    for note in notes:
                        print(f"Дата: {note['date']}, Текст: {note['text']}, Теги: {note['tags']}")
                else:
                    print("Заметок нет.")

            elif choice == "8":
                print("Выход из аккаунта.")
                current_user = None

            else:
                print("Ошибка: Некорректный выбор.")

if __name__ == "__main__":
    main()