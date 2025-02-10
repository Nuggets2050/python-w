import argparse
import sys
import rich
from PIL import Image, ImageDraw
import random
import math
import os
from rich.progress import Progress
import time

class IsingModel:
    def __init__(self, rozmiar, j, B, T, liczba_iteracji):
        self.rozmiar = rozmiar
        self.j = j
        self.B = B
        self.T = T
        self.liczba_iteracji = liczba_iteracji
        self.beta = 10**23 / (1.38 * (273 - T))
        self.array = self.generate_array()

    def generate_array(self):
        array = [[1 if random.random() < 0.5 else -1 for _ in range(self.rozmiar)] for _ in range(self.rozmiar)]
        return array

    def hamiltonian(self, i, j):
        return -self.j * self.array[i][j] * (self.array[i - 1][j] + self.array[(i + 1) % self.rozmiar][j] + self.array[i][j - 1] + self.array[i][(j + 1) % self.rozmiar]) - self.B * self.array[i][j]

    def monte_carlo(self):
        for _ in range(self.rozmiar**2):
            i = random.randint(0, self.rozmiar - 1)
            j = random.randint(0, self.rozmiar - 1)
            delta_E = 2 * self.hamiltonian(i, j)

            if delta_E < 0 or random.random() < math.exp(-self.beta * delta_E):
                self.array[i][j] *= -1

    def save_images(self, output_dir, output_dir1):
       start_time = time.time()
       with Progress() as progress:
        task = progress.add_task("Trwa symulacja....", total=liczba_iteracji)  # Tworzenie paska postępu
        os.makedirs(output_dir, exist_ok=True)
        images = []
        for k in range(self.liczba_iteracji):
            self.monte_carlo()
            image = Image.new("RGB", (self.rozmiar, self.rozmiar), "white")
            draw = ImageDraw.Draw(image)
            for i in range(self.rozmiar):
                for j in range(self.rozmiar):
                    if self.array[i][j] == 1:
                        draw.point((i, j), fill="black")
                    elif self.array[i][j] == -1:
                        draw.point((i, j), fill="white")

            image_path = os.path.join(output_dir, f"output_{k}.png")
            gif_path = os.path.join(output_dir1, "output.gif")
            image.save(image_path, "PNG")
            images.append(image)
            progress.update(task, advance=1)  # Aktualizacja paska postępu
        end_time = time.time()
        print("czas: ", end_time - start_time)
        images[0].save(gif_path, save_all=True, append_images=images[1:], duration=100, loop=0)

if __name__ == "__main__":
        rozmiar = int(input("rozmiar tablicy : "))
        j = float(input("Podaj wartość j w przedziale od 0,4 do 0,6: "))
        B = float(input("Podaj wartość pola magnetycznego B: "))
        T = float(input("Podaj wartość temperatury T w °C: "))
        liczba_iteracji = int(input("Podaj liczbę iteracji: "))

        model = IsingModel(rozmiar, j, B, T, liczba_iteracji)
        output_dir = "images"
        output_dir1 = "gif"
        
        model.save_images(output_dir, output_dir1)
