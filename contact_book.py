from collections import UserDict
from typing import List, Optional


class Field:
    """Базовий клас для полів запису."""
    
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону. Має валідацію формату (10 цифр)."""
    
    def __init__(self, value: str) -> None:
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен складатися з 10 цифр.")
        super().__init__(value)


class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів."""
    
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: List[Phone] = []

    def add_phone(self, phone_number: str) -> None:
        """Додавання телефону."""
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number: str) -> None:
        """Видалення телефону."""
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Номер телефону не знайдено.")

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        """Редагування телефону."""
        for i, p in enumerate(self.phones):
            if p.value == old_phone_number:
                self.phones[i] = Phone(new_phone_number)
                return
        raise ValueError("Номер телефону для редагування не знайдено.")

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        """Пошук телефону."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Клас для зберігання та управління записами."""
    
    def add_record(self, record: Record) -> None:
        """Додавання запису."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Пошук запису за ім'ям."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видалення запису за ім'ям."""
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Контакт не знайдено.")


def main() -> None:
    """Головна функція програми."""
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print("All records in the address book:")
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    if john:
        print("\nEditing John's phone...")
        john.edit_phone("1234567890", "1112223333")

        print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

        # Пошук конкретного телефону у записі John
        print("\nSearching for a specific phone in John's record:")
        found_phone = john.find_phone("5555555555")
        print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    print("\nDeleting Jane's record...")
    book.delete("Jane")
    
    print("\nAll records after deletion:")
    for name, record in book.data.items():
        print(record)


if __name__ == "__main__":
    main()
