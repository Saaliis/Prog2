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
        if (self.quality < 0):  # Kvaliteten kan inte bli mindre än 0
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
        # Abstrakt metod för att interagera med en boll
        pass

    def __str__(self):
        hungrig_status = "Ja" if self._hungry else "Nej"
        return f"{self._name}, ålder: {self._age}, hungrig: {hungrig_status}"

# Klass för hundar som ärver från Animal
class Dog(Animal):
    def __init__(self, age, name):
        super().__init__(age, name, "köttbullar")  # Hundens favoritmat är köttbullar

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
        self._months = months  # Antal månader gammal valpen är

    def __str__(self):
        return super().__str__() + f", månader: {self._months}"

# Klass för katter som ärver från Animal
class Cat(Animal):
    def __init__(self, age, name):
        super().__init__(age, name, "fisk")  # Kattens favoritmat är fisk

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

    def get_animals(self):
        # Returnera listan över djur
        return self.__djur

    def get_balls(self):
        # Returnera listan över bollar
        return self.balls

    def print_animals(self):
        # Returnera en strängrepresentation av alla djur
        animals = "Skriv ut alla djur\n"
        for index, animal in enumerate(self.__djur):
            animals += f"{index}: {animal}\n"
        return animals

    def print_balls(self):
        # Returnera en strängrepresentation av alla bollar
        balls = "Skriv ut alla bollar\n"
        for index, ball in enumerate(self.balls):
            balls += f"{index}: {ball}\n"
        return balls

    def feed(self, animal_index, food):
        # Mata ett specifikt djur med angiven mat
        if 0 <= animal_index < len(self.__djur):
            return self.__djur[animal_index].eat(food)
        else:
            return "Ogiltigt index"

    def play(self, animal_index, ball_index):
        # Leka med ett specifikt djur med en specifik boll
        if 0 <= animal_index < len(self.__djur) and 0 <= ball_index < len(self.balls):
            return self.__djur[animal_index].interact(self.balls[ball_index])
        else:
            return "Ogiltigt index"

# GUI-applikation
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Djurpark")
        self.configure(bg='black')  # Sätt bakgrundsfärg till svart
        self.geometry("600x600")
        self.owner = PetOwner("Jocke")
        self.create_widgets()

    def create_widgets(self):
        # Skapa och konfigurera huvudetiketten
        self.label = tk.Label(self, text="Välkommen till Djurparken", fg='lime', bg='black', font=('Helvetica', 16))
        self.label.pack(pady=10)

        # Skapa och konfigurera ram för utmatningstext
        self.output_frame = tk.Frame(self, bg='black')
        self.output_frame.pack(pady=10)

        self.output_text = tk.Text(self.output_frame, height=10, width=60, fg='lime', bg='black', font=('Helvetica', 12))
        self.output_text.pack()

        # Skapa och konfigurera ram för knappar
        self.button_frame = tk.Frame(self, bg='black')
        self.button_frame.pack(pady=10)

        # Skapa och konfigurera knappar
        self.print_animals_button = tk.Button(self.button_frame, text="Skriv ut alla djur", command=self.print_animals, fg='black', bg='lime', font=('Helvetica', 12))
        self.print_animals_button.grid(row=0, column=0, padx=10, pady=5)

        self.print_balls_button = tk.Button(self.button_frame, text="Skriv ut alla bollar", command=self.print_balls, fg='black', bg='lime', font=('Helvetica', 12))
        self.print_balls_button.grid(row=0, column=1, padx=10, pady=5)

        self.feed_button = tk.Button(self.button_frame, text="Mata djur", command=self.show_feed_options, fg='black', bg='lime', font=('Helvetica', 12))
        self.feed_button.grid(row=1, column=0, padx=10, pady=5)

        self.play_button = tk.Button(self.button_frame, text="Leka med djur", command=self.show_play_options, fg='black', bg='lime', font=('Helvetica', 12))
        self.play_button.grid(row=1, column=1, padx=10, pady=5)

        self.quit_button = tk.Button(self.button_frame, text="Avsluta", command=self.quit, fg='black', bg='lime', font=('Helvetica', 12))
        self.quit_button.grid(row=2, column=0, columnspan=2, pady=5)

    def print_animals(self):
        # Visa alla djur i utmatningstexten
        animals = self.owner.print_animals()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, animals)

    def print_balls(self):
        # Visa alla bollar i utmatningstexten
        balls = self.owner.print_balls()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, balls)

    def show_feed_options(self):
        # Visa alternativ för att mata djur
        self.clear_frame(self.button_frame)

        animals = self.owner.get_animals()
        animal_options = [f"{index}: {animal}" for index, animal in enumerate(animals)]

        # Skapa etikett och dropdown-meny för att välja djur att mata
        self.label_select_animal = tk.Label(self.button_frame, text="Välj ett djur att mata:", fg='lime', bg='black', font=('Helvetica', 12))
        self.label_select_animal.grid(row=0, column=0, pady=5)
        
        self.animal_var = tk.StringVar(self.button_frame)
        self.animal_menu = tk.OptionMenu(self.button_frame, self.animal_var, *animal_options)
        self.animal_menu.config(fg='black', bg='lime', font=('Helvetica', 12))
        self.animal_menu.grid(row=0, column=1, pady=5)

        # Skapa etikett och dropdown-meny för att välja mat
        self.label_select_food = tk.Label(self.button_frame, text="Välj mat:", fg='lime', bg='black', font=('Helvetica', 12))
        self.label_select_food.grid(row=1, column=0, pady=5)

        self.food_var = tk.StringVar(self.button_frame)
        self.food_menu = tk.OptionMenu(self.button_frame, self.food_var, "köttbullar", "fisk", "hundmat", "kattemat")
        self.food_menu.config(fg='black', bg='lime', font=('Helvetica', 12))
        self.food_menu.grid(row=1, column=1, pady=5)

        # Skapa knapp för att mata djuret
        self.feed_button_confirm = tk.Button(self.button_frame, text="Mata", command=self.feed_animal, fg='black', bg='lime', font=('Helvetica', 12))
        self.feed_button_confirm.grid(row=2, column=0, columnspan=2, pady=5)

    def feed_animal(self):
        # Hämta valt djur och mat och visa resultatet i utmatningstexten
        animal_index = self.animal_var.get().split(":")[0]
        food = self.food_var.get()
        if animal_index and food:
            result = self.owner.feed(int(animal_index), food)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, result)

    def show_play_options(self):
        # Visa alternativ för att leka med djur
        self.clear_frame(self.button_frame)

        animals = self.owner.get_animals()
        animal_options = [f"{index}: {animal}" for index, animal in enumerate(animals)]

        # Skapa etikett och dropdown-meny för att välja djur att leka med
        self.label_select_animal = tk.Label(self.button_frame, text="Välj ett djur att leka med:", fg='lime', bg='black', font=('Helvetica', 12))
        self.label_select_animal.grid(row=0, column=0, pady=5)

        self.animal_var = tk.StringVar(self.button_frame)
        self.animal_menu = tk.OptionMenu(self.button_frame, self.animal_var, *animal_options)
        self.animal_menu.config(fg='black', bg='lime', font=('Helvetica', 12))
        self.animal_menu.grid(row=0, column=1, pady=5)

        balls = self.owner.get_balls()
        ball_options = [f"{index}: {ball}" for index, ball in enumerate(balls)]

        # Skapa etikett och dropdown-meny för att välja boll
        self.label_select_ball = tk.Label(self.button_frame, text="Välj en boll:", fg='lime', bg='black', font=('Helvetica', 12))
        self.label_select_ball.grid(row=1, column=0, pady=5)

        self.ball_var = tk.StringVar(self.button_frame)
        self.ball_menu = tk.OptionMenu(self.button_frame, self.ball_var, *ball_options)
        self.ball_menu.config(fg='black', bg='lime', font=('Helvetica', 12))
        self.ball_menu.grid(row=1, column=1, pady=5)

        # Skapa knapp för att leka med djuret
        self.play_button_confirm = tk.Button(self.button_frame, text="Leka", command=self.play_with_animal, fg='black', bg='lime', font=('Helvetica', 12))
        self.play_button_confirm.grid(row=2, column=0, columnspan=2, pady=5)

    def play_with_animal(self):
        # Hämta valt djur och boll och visa resultatet i utmatningstexten
        animal_index = self.animal_var.get().split(":")[0]
        ball_index = self.ball_var.get().split(":")[0]
        if animal_index and ball_index:
            result = self.owner.play(int(animal_index), int(ball_index))
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, result)

    def clear_frame(self, frame):
        # Rensa innehållet i ett frame
        for widget in frame.winfo_children():
            widget.destroy()
        self.create_widgets()

# Huvudprogram
if __name__ == "__main__":
    app = Application()
    app.mainloop()
