import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def covid19(y, t, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


beta = float(input("Podaj wartość współczynnika określającego tempo z jakim osoby się zarażają: "))
gamma = float(input("Podaj wartość współczynnika określającego tempo w jakim osoby są uzdrawiane: "))
R0=beta/gamma
N=int(input("Podaj populacje: "))
I0=int(input("Podaj ilość początkowych zarażonych: "))
S0=N-I0-R0
print("Podaj ilość podejrzanych o zarażenie: ", S0)
t = np.linspace(0,20,100)
y0 = S0, I0, R0
S, I, R = odeint(covid19, y0, t, args=(beta, gamma)).T


plt.plot(t, S, alpha =0.7, linewidth=2,color='orange',  label='Podatni')
plt.plot(t, I, alpha=0.7, linewidth=2,color='red', label='zarażeni')
plt.plot(t, R, alpha=0.7, linewidth=2,color='green', label='uzdrowieni')
plt.xlabel('Czas[Dni]')
plt.ylabel('Liczba osób')
plt.title('Model SIR')
plt.legend()
plt.show()