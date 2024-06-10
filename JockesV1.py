import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
import random

# Klass för att representera en boll med färg och kvalitet
class Ball:
    def __init__(self, color, quality):
        self.color = color
        self.quality = quality

    def lower_quality(self, amount):
        self.quality -= amount
        if self.quality < 0:
            self.quality = 0

    def __str__(self):
        return f"Bollens färg: {self.color}, kvalitet: {self.quality}"

# Abstrakt klass för djur
class Animal(ABC):
    def __init__(self, age, name, favourite_food):
        self._age = age
        self._name = name
        self._hungry = True
        self._favourite_food = favourite_food

    @abstractmethod
    def eat(self, food):
        if food == self._favourite_food:
            self._hungry = False
            return f"{self._name} är mätt och nöjd."
        else:
            self._hungry = True
            return f"{self._name} är fortfarande hungrig och tittar på dig med stora ögon."

    @abstractmethod
    def interact(self, ball):
        pass

    def __str__(self):
        hungrig_status = "Ja" if self._hungry else "Nej"
        return f"{self._name}, ålder: {self._age}, hungrig: {hungrig_status}"

# Klass för hundar som ärver från Animal
class Dog(Animal):
    def __init__(self, age, name):
        super().__init__(age, name, "köttbullar")

    def eat(self, food):
        return super().eat(food)

    def interact(self, ball):
        if not self._hungry:
            ball.lower_quality(10)
            return f"{self._name} leker glatt med {ball.color} bollen och kvaliteten sjunker till {ball.quality}"
        else:
            return f"{self._name} är för hungrig för att leka."

# Klass för valpar som ärver från hund
class Puppy(Dog):
    def __init__(self, age, months, name):
        super().__init__(age, name)
        self._months = months

    def __str__(self):
        return super().__str__() + f", månader: {self._months}"

# Klass för katter som ärver från Animal
class Cat(Animal):
    def __init__(self, age, name):
        super().__init__(age, name, "fisk")

    def eat(self, food):
        if food == self._favourite_food:
            self._hungry = False
            return f"{self._name} njuter av sin fisk och är mätt."
        else:
            if random.random() > 0.5:
                self._hungry = False
                return f"{self._name} fångar en mus och blir mätt."
            else:
                self._hungry = True
                return f"{self._name} misslyckas med att fånga en mus och är fortfarande hungrig."

    def interact(self, ball):
        if not self._hungry:
            return f"{self._name} leker graciöst med {ball.color} bollen."
        else:
            return f"{self._name} är för hungrig för att leka."

# Klass för djurägaren som äger djur och bollar
class PetOwner:
    def __init__(self, name):
        self.__name = name
        self.__djur = [
            Dog(3, "Pelle"),
            Cat(2, "Misse"),
            Puppy(0, 6, "Lilla Gubben")
        ]
        self.balls = [
            Ball("röd", 100),
            Ball("blå", 100),
            Ball("grön", 100)
        ]

    def print_animals(self):
        animals = "Skriv ut alla djur\n"
        for index, animal in enumerate(self.__djur):
            animals += f"{index}: {animal}\n"
        return animals

    def print_balls(self):
        balls = "Skriv ut alla bollar\n"
        for index, ball in enumerate(self.balls):
            balls += f"{index}: {ball}\n"
        return balls

    def feed(self, animal_index, food):
        if 0 <= animal_index < len(self.__djur):
            return self.__djur[animal_index].eat(food)
        else:
            return "Ogiltigt index"

    def play(self, animal_index, ball_index):
        if 0 <= animal_index < len(self.__djur) and 0 <= ball_index < len(self.balls):
            return self.__djur[animal_index].interact(self.balls[ball_index])
        else:
            return "Ogiltigt index"

# GUI-applikation
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Djurpark")
        self.geometry("600x400")
        self.owner = PetOwner("Jocke")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Välkommen till Djurparken")
        self.label.pack()

        self.print_animals_button = tk.Button(self, text="Skriv ut alla djur", command=self.print_animals)
        self.print_animals_button.pack()

        self.print_balls_button = tk.Button(self, text="Skriv ut alla bollar", command=self.print_balls)
        self.print_balls_button.pack()

        self.feed_button = tk.Button(self, text="Mata djur", command=self.feed_animal)
        self.feed_button.pack()

        self.play_button = tk.Button(self, text="Leka med djur", command=self.play_with_animal)
        self.play_button.pack()

    def print_animals(self):
        animals = self.owner.print_animals()
        messagebox.showinfo("Alla djur", animals)

    def print_balls(self):
        balls = self.owner.print_balls()
        messagebox.showinfo("Alla bollar", balls)

    def feed_animal(self):
        self.print_animals()
        animal_index = int(input("Välj ett djur (index): "))
        food = input("Ange mat: ")
        result = self.owner.feed(animal_index, food)
        messagebox.showinfo("Mata djur", result)

    def play_with_animal(self):
        self.print_animals()
        animal_index = int(input("Välj ett djur (index): "))
        self.print_balls()
        ball_index = int(input("Välj en boll (index): "))
        result = self.owner.play(animal_index, ball_index)
        messagebox.showinfo("Leka med djur", result)

# Huvudprogram
if __name__ == "__main__":
    app = Application()
    app.mainloop()
