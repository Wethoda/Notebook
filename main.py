from datetime import datetime

class Note:
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags
        self.date = datetime.now().strftime("%Y-%m-%d")  # Убрано время (%H:%M:%S) пока что убрал переделаю потом фильтрацию

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
        print("Записка добавлена.")

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            print(f"Запись с индексом {index} удалена.")
        else:
            print(f"Запись с индексом {index} не найдена.")

    def edit_note(self, index, new_text, new_tags):
        if 0 <= index < len(self.notes):
            self.notes[index].text = new_text
            self.notes[index].tags = new_tags
            print(f"Запись с индексом {index} изменена.")
        else:
            print(f"Запись с индексом {index} не найдена.")

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

notebook1 = Note("Первая заметка", ["Работа", "Важное"])
notebook2 = Diary()
notebook2.add_note("Первая заметка", ["Хобби", "Развлечение"])
notebook2.add_note("Вторая заметка", ["работа", "Важное"])
notebook2.add_note("Третья заметка", ["Фитнес", "Здоровье"])

print("Список всех заметок:")
for note in notebook2.list_notes():
    print(note)

notebook2.delete_note(2)

print("\nСписок заметок после удаления:")
for note in notebook2.list_notes():
    print(note)

notebook2.edit_note(0, "Новая заметка", ["личное"])

print("\nСписок заметок после редактирования:")
for note in notebook2.list_notes():
    print(note)

print("\nПоиск заметок по тегу 'работа':")
for note in notebook2.find_tags('работа'):
    print(note)

print("\nПоиск заметок по дате '2025-03-06':")
for note in notebook2.find_date('2025-03-06'):
    print(note)

print("\nФильтрация заметок по дате:")
for note in notebook2.filter_by_date():
    print(note.to_dict())

print("\nФильтрация заметок по тегам:")
for note in notebook2.filter_by_tags():
    print(note.to_dict())