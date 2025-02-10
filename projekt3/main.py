from functools import cache
import time
import numpy as np
import matplotlib.pyplot as plt



def my_decorator(func):
    def timed_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        timed_wrapper.execution_times.append(execution_time)
        average_time = sum(timed_wrapper.execution_times) / len(timed_wrapper.execution_times)
        print( f"\n Czas wykonania: {execution_time} sekund")
        print(f"Średni czas wykonania: {average_time} sekund")
        print(f"Minimalny czas wykonania: {min(timed_wrapper.execution_times)} sekund")
        print(f"Maksymalny czas wykonania: {max(timed_wrapper.execution_times)} sekund")

        return result
    timed_wrapper.execution_times = []
    return timed_wrapper



@my_decorator
def funkcja(n):
    lista = []
    a = 1
    b = 1
    for i in range(n):
        print(a, end=' ')
        b += a
        a = b - a
        lista.append(a)
    
    gold = lista[-1] / lista[-2]
    angles = np.linspace(0, 8 * np.pi, num=len(lista))    
    radius = gold ** (angles / np.pi)
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    
    plt.figure(figsize=(8, 8))
    plt.plot(x, y, color="blue", linewidth=2)
    plt.axis("equal")
    plt.axis("off")
    plt.savefig('fibo.png')


n=int(input("Podaj długość ciągu fibbonaciego: "))
funkcja(n)

funkcja(n)


funkcja(n)