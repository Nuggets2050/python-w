from PIL import Image, ImageDraw
import random
import math
import os
from numba import njit
import numpy as np
from rich.progress import Progress
import time

# Prompt the user for the size of the array
rozmiar = int(input("rozmiar tablicy : "))

# Generate an array of the specified size
array = np.zeros((rozmiar, rozmiar), dtype=np.int32)

# Fill the array with random -1 and 1 values
for i in range(rozmiar):
    for j in range(rozmiar):
        if random.random() < 0.5:
            array[i][j] = 1
        else: 
            array[i][j]=-1



j = float(input("Podaj wartość j w przedziale od 0,4 do 0,6: "))
B = float(input("Podaj wartość pola magnetycznego B: "))
T = float(input("Podaj wartość temperatury T w °C: "))
liczba_iteracji = int(input("Podaj liczbę iteracji: "))

beta = 10**23 / (1.38 * (273 - T))

@njit
def hamiltonian(array, i, j, rozmiar, j_val, B):
    return -j_val * array[i, j] * (array[i - 1, j] + array[(i + 1) % rozmiar, j] + array[i, j - 1] + array[i, (j + 1) % rozmiar]) - B * array[i, j]

@njit
def monte_carlo(array, beta, rozmiar, j_val, B):
    for _ in range(rozmiar**2):
        i = random.randint(0, rozmiar - 1)
        j = random.randint(0, rozmiar - 1)
        delta_E = 2 * hamiltonian(array, i, j, rozmiar, j_val, B)
        if delta_E < 0 or random.random() < math.exp(-beta * delta_E):
            array[i, j] *= -1
    return array

output_dir = "images"
output_dir1 = "gif"
images = []
magnetyzacja = 0
start_time = time.time()
with Progress() as progress:
    task = progress.add_task("Trwa symulacja....", total=liczba_iteracji)  # Tworzenie paska postępu

    for k in range(liczba_iteracji):
        array = monte_carlo(array, beta, rozmiar, j, B)  # Perform one iteration at a time
        image = Image.new("RGB", (rozmiar, rozmiar), "white")
        draw = ImageDraw.Draw(image)
        for i in range(rozmiar):
         for j in range(rozmiar):
                magnetyzacja += array[i, j]
                if array[i, j] == 1:
                   draw.point((i, j), fill="black")
                elif array[i, j] == -1:
                   draw.point((i, j), fill="white")
        image_path = os.path.join(output_dir, f"output_{k}.png")
        gif_path = os.path.join(output_dir1, "output.gif")
        image.save(image_path, "PNG")
        images.append(image)
        progress.update(task, advance=1)
end_time = time.time()
magnetyzacja /= rozmiar**2
print("magnetyzacja: ", magnetyzacja)
print("czas: ", end_time - start_time)
images[0].save(gif_path, save_all=True, append_images=images[1:], duration=100, loop=0)
