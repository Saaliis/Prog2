import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
import random

# Klass för att representera en boll med färg och kvalitet
class Ball:
    def __init__(self, color, quality):
        self.color = color  # Bollens färg
        self.quality = quality  # Bollens kvalitet, ett mått på hur mycket bollen kan användas innan den går sönder

    def lower_quality(self, amount):
        # Minska bollens kvalitet med ett angivet värde
        self.quality -= amount
        if self.quality < 0:  # Kvaliteten kan inte bli mindre än 0
            self.quality = 0

    def __str__(self):
        # Returnera en strängrepresentation av bollen
        return f"Bollens färg: {self.color}, kvalitet: {self.quality}"

# Abstrakt klass för djur
class Animal(ABC):
    def __init__(self, age, name, favourite_food):
        self._age = age  # Djurets ålder
        self._name = name  # Djurets namn
        self._hungry = True  # Indikerar om djuret är hungrigt
        self._favourite_food = favourite_food  # Djurets favoritmat

    @abstractmethod
    def eat(self, food):
        # Abstrakt metod för att äta mat och bli mätt om det är favoritmat
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
        self.configure(bg='black')
        self.geometry("600x400")
        self.owner = PetOwner("Jocke")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Välkommen till Djurparken", fg='lime', bg='black', font=('Helvetica', 16))
        self.label.pack(pady=10)

        self.print_animals_button = tk.Button(self, text="Skriv ut alla djur", command=self.print_animals, fg='black', bg='lime', font=('Helvetica', 12))
        self.print_animals_button.pack(pady=5)

        self.print_balls_button = tk.Button(self, text="Skriv ut alla bollar", command=self.print_balls, fg='black', bg='lime', font=('Helvetica', 12))
        self.print_balls_button.pack(pady=5)

        self.feed_button = tk.Button(self, text="Mata djur", command=self.feed_animal, fg='black', bg='lime', font=('Helvetica', 12))
        self.feed_button.pack(pady=5)

        self.play_button = tk.Button(self, text="Leka med djur", command=self.play_with_animal, fg='black', bg='lime', font=('Helvetica', 12))
        self.play_button.pack(pady=5)

        self.quit_button = tk.Button(self, text="Avsluta", command=self.quit, fg='black', bg='lime', font=('Helvetica', 12))
        self.quit_button.pack(pady=5)

    def print_animals(self):
        animals = self.owner.print_animals()
        messagebox.showinfo("Alla djur", animals)

    def print_balls(self):
        balls = self.owner.print_balls()
        messagebox.showinfo("Alla bollar", balls)

    def feed_animal(self):
        animals = self.owner.print_animals().split('\n')[1:-1]
        animal_index = self.select_item(animals, "Välj ett djur att mata:")
        if animal_index is None:
            return

        foods = ["köttbullar", "fisk", "hundmat", "kattemat"]
        food = self.select_item(foods, "Välj mat:")
        if food is None:
            return

        result = self.owner.feed(int(animal_index), foods[int(food)])
        messagebox.showinfo("Mata djur", result)

    def play_with_animal(self):
        animals = self.owner.print_animals().split('\n')[1:-1]
        animal_index = self.select_item(animals, "Välj ett djur att leka med:")
        if animal_index is None:
            return

        balls = self.owner.print_balls().split('\n')[1:-1]
        ball_index = self.select_item(balls, "Välj en boll:")
        if ball_index is None:
            return

        result = self.owner.play(int(animal_index), int(ball_index))
        messagebox.showinfo("Leka med djur", result)

    def select_item(self, items, title):
        top = tk.Toplevel(self)
        top.title(title)
        top.configure(bg='black')
        listbox = tk.Listbox(top, fg='lime', bg='black', font=('Helvetica', 12))
        for item in items:
            listbox.insert(tk.END, item)
        listbox.pack(pady=10)

        selected_item = tk.StringVar()
        def on_select():
            try:
                selected_item.set(listbox.curselection()[0])
                top.destroy()
            except IndexError:
                pass

        select_button = tk.Button(top, text="Välj", command=on_select, fg='black', bg='lime', font=('Helvetica', 12))
        select_button.pack(pady=5)

        self.wait_window(top)
        return selected_item.get() if selected_item.get() else None

# Huvudprogram
if __name__ == "__main__":
    app = Application()
    app.mainloop()
