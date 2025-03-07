from datetime import datetime
import json

class Note:
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags
        self.date = datetime.now().strftime("%Y-%m-%d")  # Убрано время (%H:%M:%S)

    def to_dict(self):
        return {
            "text": self.text,
            "tags": self.tags,
            "date": self.date
        }

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

    def filter_by_date(self):
        return sorted(self.notes, key=lambda note: note.date)

    def find_tags(self, tag):
        return [note.to_dict() for note in self.notes if tag.lower() in [t.lower() for t in note.tags]]

    def filter_by_tags(self):
        return sorted(self.notes, key=lambda note: ", ".join(note.tags))

    def list_notes(self):
        return [note.to_dict() for note in self.notes]

    def save_to_json(self, filename="notes.json"):
        data = [note.to_dict() for note in self.notes]
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print("Заметки сохранены.")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

    def load_from_json(self, filename="notes.json"):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.notes = [Note(note['text'], note['tags']) for note in data]
            print("Заметки загружены.")
        except FileNotFoundError:
            print("Файл отсутствует!")
        except json.JSONDecodeError:
            print("Ошибка при чтении JSON.")

def main():
    diary = Diary()
    while True:
        print("\nМеню:")
        print("1. Добавить заметку")
        print("2. Удалить заметку")
        print("3. Редактировать заметку")
        print("4. Фильтровать заметки по дате (формат YYYY-MM-DD)")
        print("5. Фильтровать заметки по тегу")
        print("6. Сохранить заметки")
        print("7. Загрузить заметки")
        print("8. Просмотреть все заметки")
        print("9. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            text = input("Введите текст заметки: ")
            tags = input("Введите теги через запятую: ").split(",")
            diary.add_note(text, tags)

        elif choice == "2":
            try:
                index = int(input("Введите индекс заметки для удаления: "))
                diary.delete_note(index)
            except ValueError:
                print("Ошибка: Введите корректный индекс.")

        elif choice == "3":
            try:
                index = int(input("Введите индекс заметки для редактирования: "))
                new_text = input("Введите новый текст: ")
                new_tags = input("Введите новые теги через запятую: ").split(",")
                diary.edit_note(index, new_text, new_tags)
            except ValueError:
                print("Ошибка: Введите корректный индекс.")

        elif choice == "4":
            date = input("Введите дату для фильтрации (YYYY-MM-DD): ")
            filtered_notes = diary.find_date(date)
            if filtered_notes:
                for note in filtered_notes:
                    print(f"Дата: {note['date']}, Текст: {note['text']}, Теги: {', '.join(note['tags'])}")
            else:
                print("Заметки не найдены.")

        elif choice == "5":
            tag = input("Введите тег для фильтрации: ")
            filtered_notes = diary.find_tags(tag)
            if filtered_notes:
                for note in filtered_notes:
                    print(f"Дата: {note['date']}, Текст: {note['text']}, Теги: {', '.join(note['tags'])}")
            else:
                print("Заметки не найдены.")

        elif choice == "6":
            filename = input("Введите имя файла для сохранения: ")
            diary.save_to_json(filename)

        elif choice == "7":
            filename = input("Введите имя файла для загрузки: ")
            diary.load_from_json(filename)

        elif choice == "8":
            notes = diary.list_notes()
            if notes:
                print("Список всех заметок:")
                for note in notes:
                    print(f"Дата: {note['date']}, Текст: {note['text']}, Теги: {', '.join(note['tags'])}")
            else:
                print("Заметок нет.")

        elif choice == "9":
            print("Выход из программы.")
            break

        else:
            print("Ошибка: Некорректный выбор.")

if __name__ == "__main__":
    main()