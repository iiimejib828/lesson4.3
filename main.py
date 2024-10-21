import pickle
import os
import random


class Animal:
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age

    def get_name(self):
        return self._name

    def make_sound(self):
        raise NotImplementedError("Метод надо переопределить в подклассе")

    def eat(self):
        print(f"{self._name} ест.")

    def __repr__(self):
        return f"{self.__class__.__name__}(Имя: {self._name}, Возраст: {self._age})"


class Bird(Animal):
    def __init__(self, name: str, age: int, can_fly: bool = True):
        super().__init__(name, age)
        self._can_fly = can_fly

    def make_sound(self):
        print(f"{self._name} Чирик-Кар-Фьють!")

    def fly(self):
        if self._can_fly:
            print(f"{self._name} летает.")
        else:
            print(f"{self._name} не летает.")


class Mammal(Animal):
    def make_sound(self):
        print(f"{self._name} Гав-Мяу!")


class Reptile(Animal):
    def make_sound(self):
        print(f"{self._name} Шшшшшшшшшш!.")


class Staff:
    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return f"{self.__class__.__name__}(Имя: {self._name})"


class ZooKeeper(Staff):
    def feed_animal(self, animal: Animal):
        print(f"{self._name} кормит животное {animal._name}.")
        animal.eat()

    def __repr__(self):
        return f"Работник (Имя: {self._name})"


class Veterinarian(Staff):
    def heal_animal(self, animal: Animal):
        print(f"{self._name} лечит животное {animal.get_name()}.")
        animal.make_sound()
        print(f"{animal.get_name()} благодарит {self._name}.")

    def __repr__(self):
        return f"Ветеринар (Имя: {self._name})"


class Zoo:
    def __init__(self, name: str):
        self._name = name
        self._animals = []
        self._staff = []

    def add_animal(self, animal: Animal):
        self._animals.append(animal)
        print(f"В зоопарке появился(-ась) {animal}")

    def remove_animal(self, animal_name: str):
        for animal in self._animals:
            if animal.get_name() == animal_name:
                self._animals.remove(animal)
                print(f"Животное {animal_name} удалено из зоопарка.")
                return
        print(f"Животное {animal_name} не найдено.")

    def add_staff(self, staff_member: Staff):
        self._staff.append(staff_member)
        print(f"В зоопарке добавился(-ась) работник {staff_member}")

    def remove_staff(self, staff_name: str):
        for staff in self._staff:
            if staff._name == staff_name:
                self._staff.remove(staff)
                print(f"Работник {staff_name} удален из зоопарка.")
                return
        print(f"Работник {staff_name} не найден.")

    def show_animals(self):
        print("Животные в зоопарке:")
        for animal in self._animals:
            print(animal)

    def show_staff(self):
        print("Работники в зоопарке:")
        for staff in self._staff:
            print(staff)

    def random_feed(self):
        if not self._animals or not self._staff:
            print("Нет животных или работников для кормления.")
            return
        animal = random.choice(self._animals)
        zookeeper = random.choice([s for s in self._staff if isinstance(s, ZooKeeper)])
        if zookeeper:
            zookeeper.feed_animal(animal)
        else:
            print("Нет работников для кормления животных.")

    def random_heal(self):
        if not self._animals or not self._staff:
            print("Нет животных или ветеринаров для лечения.")
            return
        animal = random.choice(self._animals)
        vet = random.choice([s for s in self._staff if isinstance(s, Veterinarian)])
        if vet:
            vet.heal_animal(animal)
        else:
            print("Нет ветеринаров для лечения животных.")

    def save_zoo(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        print(f"Зоопарк сохранён в {filename}.")

    @staticmethod
    def load_zoo(filename: str):
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'rb') as f:
                zoo = pickle.load(f)
            print(f"Зоопарк загружен из {filename}.")
            return zoo
        else:
            print(f"Файл {filename} не найден или пуст.")
            return None


# Файл для сохранения данных зоопарка
zoo_file = "zoo_data.pkl"

# Загружаем зоопарк, если файл существует и не пуст
zoo = Zoo.load_zoo(zoo_file)
if not zoo:
    # Если зоопарк не загружен, создаем новый
    zoo = Zoo("My Awesome Zoo")

# Меню для управления зоопарком
while True:
    print("\n1. Добавить животное")
    print("2. Удалить животное")
    print("3. Добавить работника")
    print("4. Удалить работника")
    print("5. Показать всех животных")
    print("6. Показать всех работников")
    print("7. Случайное кормление животного")
    print("8. Случайное лечение животного")
    print("9. Выйти и сохранить изменения")

    choice = input("Выберите действие: ")

    if choice == '1':
        name = input("Введите имя животного: ")
        age = int(input("Введите возраст животного: "))
        animal_type = input("Введите тип животного (Bird, Mammal, Reptile): ")
        if animal_type == "Bird":
            can_fly = input("Может ли летать (yes/no): ").lower() == "yes"
            animal = Bird(name, age, can_fly)
        elif animal_type == "Mammal":
            animal = Mammal(name, age)
        elif animal_type == "Reptile":
            animal = Reptile(name, age)
        else:
            print("Неверный тип животного.")
            continue
        zoo.add_animal(animal)

    elif choice == '2':
        name = input("Введите имя животного, которое хотите удалить: ")
        zoo.remove_animal(name)

    elif choice == '3':
        name = input("Введите имя работника: ")
        staff_type = input("Введите тип работника (ZooKeeper, Veterinarian): ")
        if staff_type == "ZooKeeper":
            staff = ZooKeeper(name)
        elif staff_type == "Veterinarian":
            staff = Veterinarian(name)
        else:
            print("Неверный тип работника.")
            continue
        zoo.add_staff(staff)

    elif choice == '4':
        name = input("Введите имя работника, которого хотите удалить: ")
        zoo.remove_staff(name)

    elif choice == '5':
        zoo.show_animals()

    elif choice == '6':
        zoo.show_staff()

    elif choice == '7':
        zoo.random_feed()

    elif choice == '8':
        zoo.random_heal()

    elif choice == '9':
        zoo.save_zoo(zoo_file)
        break

    else:
        print("Неверный выбор, попробуйте еще раз.")
