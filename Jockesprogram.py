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

# Klass för djurägaren som äger djur och bollar
class PetOwner:
    def __init__(self, name):
        self.__name = name  # Djurägarens namn
        # Lista över djur som djurägaren äger
        self.__djur = [
            Dog(3, "Pelle"),  # Hund med ålder 3 och namn Pelle
            Cat(2, "Misse"),  # Katt med ålder 2 och namn Misse
            Puppy(0, 6, "Lilla Gubben")  # Valp med ålder 0 år och 6 månader och namn Lilla Gubben
        ]
        # Lista över bollar som djurägaren äger
        self.balls = [
            Ball("röd", 100),  # Röd boll med kvalitet 100
            Ball("blå", 100),  # Blå boll med kvalitet 100
            Ball("grön", 100)  # Grön boll med kvalitet 100
        ]

    def print_animals(self):
        # Skriv ut detaljer om alla djur som djurägaren äger
        print("Skriv ut alla djur")
        for index, animal in enumerate(self.__djur):
            print(f"{index}: {animal}")

    def print_balls(self):
        # Skriv ut detaljer om alla bollar som djurägaren äger
        print("Skriv ut alla bollar")
        for index, ball in enumerate(self.balls):
            print(f"{index}: {ball}")

    def print_food_options(self):
        # Skriv ut tillgängliga matalternativ
        print("Tillgängliga matalternativ:")
        print("1. Köttbullar")
        print("2. Fisk")
        print("3. Hundmat")
        print("4. Kattemat")

    def play(self, animal_index, ball_index):
        # Leka med ett specifikt djur med en specifik boll
        print("Vi leker")
        if 0 <= animal_index < len(self.__djur) and 0 <= ball_index < len(self.balls):
            self.__djur[animal_index].interact(self.balls[ball_index])
        else:
            print("Ogiltigt index")  # Felmeddelande om index är utanför giltigt intervall

    def feed(self, animal_index, food):
        # Mata ett specifikt djur med angiven mat
        print("Djuret äter")
        if 0 <= animal_index < len(self.__djur):
            self.__djur[animal_index].eat(food)
        else:
            print("Ogiltigt index")  # Felmeddelande om index är utanför giltigt intervall

    def run(self):
        # Huvudmeny för att interagera med programmet
        while True:
            print("\nMeny:")
            print("1. Skriv ut alla djur")
            print("2. Leka med djur")
            print("3. Mata djur")
            print("0. Avsluta")
            choice = int(input("Välj ett alternativ: "))
            if choice == 1:
                self.print_animals()
            elif choice == 2:
                self.print_animals()
                animal_index = int(input("Välj ett djur (index): "))
                self.print_balls()
                ball_index = int(input("Välj en boll (index): "))
                self.play(animal_index, ball_index)
            elif choice == 3:
                self.print_animals()
                animal_index = int(input("Välj ett djur (index): "))
                self.print_food_options()
                food_choice = int(input("Ange mat (nummer): "))
                food = ""
                if food_choice == 1:
                    food = "köttbullar"
                elif food_choice == 2:
                    food = "fisk"
                elif food_choice == 3:
                    food = "hundmat"
                elif food_choice == 4:
                    food = "kattemat"
                else:
                    print("Ogiltigt val av mat.")
                    continue
                self.feed(animal_index, food)
            elif choice == 0:
                break
            else:
                print("Ogiltigt val, försök igen.")

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
            print(f"{self._name} är mätt och nöjd.")
            self._hungry = False  # Djuret är inte längre hungrigt
        else:
            print(f"{self._name} är fortfarande hungrig och tittar på dig med stora ögon.")
            self._hungry = True  # Djuret är fortfarande hungrigt

    @abstractmethod
    def interact(self, ball):
        # Abstrakt metod för att interagera med en boll
        pass

    def __str__(self):
        # Returnera en strängrepresentation av djuret
        hungrig_status = "Ja" if self._hungry else "Nej"
        return f"{self._name}, ålder: {self._age}, hungrig: {hungrig_status}"

# Klass för hundar som ärver från Animal
class Dog(Animal):
    def __init__(self, age, name):
        super().__init__(age, name, "köttbullar")  # Sätt hundens favoritmat till köttbullar
        print("En hund har skapats")

    def eat(self, food):
        # Implementera ätbeteende för hund
        super().eat(food)

    def interact(self, ball):
        # Implementera interaktion med boll för hund
        if not self._hungry:
            ball.lower_quality(10)  # Minska bollens kvalitet
            print(f"{self._name} leker glatt med {ball.color} bollen och kvaliteten sjunker till {ball.quality}")
        else:
            print(f"{self._name} är för hungrig för att leka.")

# Klass för valpar som ärver från hund
class Puppy(Dog):
    def __init__(self, age, months, name):
        super().__init__(age, name)
        self._months = months  # Antal månader gammal valpen är

    def __str__(self):
        # Returnera en strängrepresentation av valpen
        return super().__str__() + f", månader: {self._months}"

# Klass för katter som ärver från Animal
class Cat(Animal):
    def __init__(self, age, name):
        super().__init__(age, name, "fisk")  # Sätt kattens favoritmat till fisk
        print("En katt har skapats")

    def eat(self, food):
        # Implementera ätbeteende för katt
        if food == self._favourite_food:
            print(f"{self._name} njuter av sin fisk och är mätt.")
            self._hungry = False  # Katten är inte längre hungrig
        else:
            print(f"{self._name} rynkar på nosen åt maten och är fortfarande hungrig.")
            # Katten jagar en mus om den inte får sin favoritmat
            if random.random() > 0.5:
                print(f"{self._name} fångar en mus och blir mätt.")
                self._hungry = False  # Katten är inte längre hungrig efter att ha ätit en mus
            else:
                print(f"{self._name} misslyckas med att fånga en mus och är fortfarande hungrig.")

    def interact(self, ball):
        # Implementera interaktion med boll för katt
        if not self._hungry:
            print(f"{self._name} leker graciöst med {ball.color} bollen.")
        else:
            print(f"{self._name} är för hungrig för att leka.")

# Huvudprogram
Jocke = PetOwner("Jocke")  # Skapa en instans av PetOwner
Jocke.run()  # Kör huvudmenyn för att interagera med programmet
