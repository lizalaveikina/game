from __future__ import annotations

"""
Модуль класів гри блукачки
"""


class Room:
    """
    Клас кімнати
    """

    def __init__(self, name: str) -> None:
        """
        Конструктор класу кімнати

        >>> kitchen = Room("Kitchen")
        >>> kitchen.name
        'Kitchen'
        """
        self.name = name
        self.description = ""
        self.connected_rooms = dict()
        self.character = None
        self.item = None

    def set_description(self, description: str) -> None:
        """
        Встановлення опису кімнати

        >>> kitchen = Room("Kitchen")
        >>> kitchen.set_description("A dank and dirty room buzzing with flies.")
        >>> kitchen.description
        'A dank and dirty room buzzing with flies.'
        """
        self.description = description

    def link_room(self, other: Room, direction: str) -> None:
        """
        З'єднання кімнати з сусідньою

        >>> kitchen = Room("Kitchen")
        >>> kitchen.set_description("A dank and dirty room buzzing with flies.")
        >>> dining_hall = Room("Dining Hall")
        >>> dining_hall.set_description("A large room with ornate golden decorations on each wall.")
        >>> kitchen.link_room(dining_hall, "south")
        >>> kitchen.connected_rooms["south"].name
        'Dining Hall'
        """
        self.connected_rooms[direction] = other

    def get_details(self) -> str:
        """
        Детальний опис кімнати

        >>> kitchen = Room("Kitchen")
        >>> kitchen.set_description("A dank and dirty room buzzing with flies.")
        >>> kitchen.get_details()
        Kitchen
        --------------------
        A dank and dirty room buzzing with flies.
        'Kitchen\\n--------------------\\nA dank and dirty room buzzing with flies.'
        """
        connected_rooms_string = "\n".join(
            [
                f"The {v.name} is {k}"
                for k, v in sorted(
                    self.connected_rooms.items(), key=lambda i: (i[1].name, i[0])
                )
            ]
        )
        character = "" if self.character is None else f"{self.character.describe()}"
        item = "" if self.item is None else f"{self.item.describe()}"
        details_list = [
            self.name,
            "-" * 20,
            self.description,
            connected_rooms_string,
            character,
            item,
        ]
        details = "\n".join(i for i in details_list if i)
        print(details)
        return details

    def get_character(self) -> Enemy:
        """
        Одержання персонажа з кімнати

        >>> dining_hall = Room("Dining Hall")
        >>> dining_hall.set_description("A large room with ornate golden decorations on each wall.")
        >>> dave = Enemy("Dave", "A smelly zombie")
        >>> dave.set_conversation("What's up, dude! I'm hungry.")
        >>> dining_hall.set_character(dave)
        >>> character = dining_hall.get_character()
        >>> character.name
        'Dave'
        """
        return self.character

    def set_character(self, character: Enemy) -> None:
        """
        Встановлення персонажа у кімнаті

        >>> dining_hall = Room("Dining Hall")
        >>> dining_hall.set_description("A large room with ornate golden decorations on each wall.")
        >>> dave = Enemy("Dave", "A smelly zombie")
        >>> dave.set_conversation("What's up, dude! I'm hungry.")
        >>> dining_hall.set_character(dave)
        >>> dining_hall.character.name
        'Dave'
        """
        self.character = character

    def get_item(self) -> Item:
        """
        Одержавання інвентарю з кімнати
        >>> dining_hall = Room("Dining Hall")
        >>> dining_hall.set_description("A large room with ornate golden decorations on each wall.")
        >>> book = Item("book")
        >>> book.set_description("A really good book entitled 'Knitting for dummies'") #+
        >>> dining_hall.set_item(book)
        >>> item = dining_hall.get_item()
        >>> item.name
        'book'
        """
        return self.item

    def set_item(self, item: Item) -> None:
        """
        Додати інвентар до кімнати

        >>> dining_hall = Room("Dining Hall")
        >>> dining_hall.set_description("A large room with ornate golden decorations on each wall.")
        >>> book = Item("book")
        >>> book.set_description("A really good book entitled 'Knitting for dummies'") #+
        >>> dining_hall.set_item(book)
        >>> dining_hall.item.name
        'book'
        """
        self.item = item

    def move(self, direction: str) -> Room:
        """
        Одержання наступно кімнати за напрямком

        >>> kitchen = Room("Kitchen")
        >>> kitchen.set_description("A dank and dirty room buzzing with flies.")
        >>> dining_hall = Room("Dining Hall")
        >>> dining_hall.set_description("A large room with ornate golden decorations on each wall.")
        >>> kitchen.link_room(dining_hall, "south")
        >>> next_room = kitchen.move("south")
        >>> next_room.name
        'Dining Hall'
        """
        try:
            next_room = self.connected_rooms[direction]
            return next_room
        except KeyError:
            return self


class Enemy:
    """
    Клас ворога
    """

    defeated = 0
    count = 0

    def __init__(self, name: str, description: str) -> None:
        """
        Конструктор класу ворогів

        >>> dave = Enemy("Dave", "A smelly zombie")
        >>> dave.name
        'Dave'
        >>> dave.description
        'A smelly zombie'
        """
        self.name = name
        self.description = description
        self.conversation = None
        self.weakness = None
        Enemy.count += 1

    def set_conversation(self, conversation: str) -> None:
        """
        Встановлення фрази для ворога

        >>> dave = Enemy("Dave", "A smelly zombie")
        >>> dave.set_conversation("What's up, dude! I'm hungry.")
        >>> dave.conversation
        "What's up, dude! I'm hungry."
        """
        self.conversation = conversation

    def set_weakness(self, weakness: str) -> None:
        """
        Встановлення предмету для загибилі

        >>> dave = Enemy("Dave", "A smelly zombie")
        >>> dave.set_conversation("What's up, dude! I'm hungry.")
        >>> dave.set_weakness("cheese")
        >>> dave.weakness
        'cheese'
        """
        self.weakness = weakness

    def talk(self) -> str:
        """
        Повертає фразу в розмові

        >>> dave = Enemy("Dave", "A smelly zombie")
        >>> dave.set_conversation("What's up, dude! I'm hungry.")
        >>> dave.talk()
        [Dave says]: What's up, dude! I'm hungry.
        "[Dave says]: What's up, dude! I'm hungry."
        """
        answer = f"[{self.name} says]: {self.conversation}"
        print(answer)
        return answer

    def fight(self, item: str) -> bool:
        """
        Спроба вбити ворога за допомогою об'єкта

        >>> dave = Enemy("Dave", "A smelly zombie")
        >>> dave.set_conversation("What's up, dude! I'm hungry.")
        >>> dave.set_weakness("cheese")
        >>> dave.fight("book")
        Dave crushes you, puny adventurer!
        False
        >>> dave.fight("cheese")
        You fend Dave off with the cheese
        True
        """
        if item == self.weakness:
            Enemy.defeated += 1
            print(f"You fend {self.name} off with the {self.weakness}")
            return True
        print(f"{self.name} crushes you, puny adventurer!")
        return False

    def describe(self) -> str:
        """
        Генереє опис ворога

        >>> dave = Enemy("Dave", "A smelly zombie")
        >>> dave.set_conversation("What's up, dude! I'm hungry.")
        >>> dave.describe()
        'Dave is here!\\nA smelly zombie'
        """
        return f"{self.name} is here!\n{self.description}"

    def get_defeated(self) -> int:
        """
        Повертає кількість убитих ворогів

        >>> Enemy.defeated = 0
        >>> dave = Enemy("Dave", "A smelly zombie")
        >>> dave.set_conversation("What's up, dude! I'm hungry.")
        >>> dave.set_weakness("cheese")
        >>> dave.fight("cheese")
        You fend Dave off with the cheese
        True
        >>> dave.get_defeated()
        1
        """
        return self.__class__.defeated


class Item:
    """
    Клас обєкта, яким можна вбити ворога
    """

    def __init__(self, name) -> None:
        """
        Конструктор класу об'єкта

        >>> cheese = Item("cheese")
        >>> cheese.name
        'cheese'
        """
        self.name = name
        self.description = ""

    def set_description(self, description: str) -> None:
        """
        Встановлює опис об'єкта

        >>> cheese = Item("cheese")
        >>> cheese.set_description("A large and smelly block of cheese")
        >>> cheese.description
        'A large and smelly block of cheese'
        """
        self.description = description

    def describe(self) -> str:
        """
        Повретає опис обєкта
        >>> cheese = Item("cheese")
        >>> cheese.set_description("A large and smelly block of cheese")
        >>> cheese.describe()
        'The [cheese] is here - A large and smelly block of cheese'
        """
        return f"The [{self.name}] is here - {self.description}"

    def __eq__(self, other: Item) -> bool:
        """
        Порявняння двох об'єктів

        >>> cheese = Item("cheese")
        >>> cheese.set_description("A large and smelly block of cheese")
        >>> book = Item("book")
        >>> book.set_description("A really good book entitled 'Knitting for dummies'")
        >>> cheese == book
        False
        """
        return self.__dict__ == other.__dict__

    def get_name(self) -> str:
        """
        Повертає ім'я об'єкта

        >>> book = Item("book")
        >>> book.get_name()
        'book'
        """
        return self.name


if __name__ == "__main__":
    import doctest

    doctest.testmod()
