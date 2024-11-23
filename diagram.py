import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Універсум дискурсу
temperature = np.arange(35, 43, 0.1)  # Температура: 35–42 °C
pulse = np.arange(40, 181, 1)         # Пульс: 40–180 bpm
risk = np.arange(0, 101, 1)           # Ризик: 0–100

# Функції належності для температури
temp_low = fuzz.trimf(temperature, [35, 35, 37])
temp_normal = fuzz.trimf(temperature, [36, 37, 38])
temp_high = fuzz.trimf(temperature, [37, 42, 42])

# Функції належності для пульсу
pulse_low = fuzz.trimf(pulse, [40, 40, 60])
pulse_normal = fuzz.trimf(pulse, [60, 80, 100])
pulse_high = fuzz.trimf(pulse, [90, 180, 180])

# Функції належності для ризику
risk_low = fuzz.trimf(risk, [0, 0, 33])
risk_medium = fuzz.trimf(risk, [33, 50, 66])
risk_high = fuzz.trimf(risk, [66, 100, 100])

# Візуалізація функцій належності
plt.figure(figsize=(10, 8))

# Графік температури
plt.subplot(3, 1, 1)
plt.plot(temperature, temp_low, 'b', label='Low')
plt.plot(temperature, temp_normal, 'g', label='Normal')
plt.plot(temperature, temp_high, 'r', label='High')
plt.title('Membership Functions for Temperature')
plt.xlabel('Temperature (°C)')
plt.ylabel('Degree of Membership')
plt.legend()

# Графік пульсу
plt.subplot(3, 1, 2)
plt.plot(pulse, pulse_low, 'b', label='Low')
plt.plot(pulse, pulse_normal, 'g', label='Normal')
plt.plot(pulse, pulse_high, 'r', label='High')
plt.title('Membership Functions for Pulse')
plt.xlabel('Pulse (bpm)')
plt.ylabel('Degree of Membership')
plt.legend()

# Графік ризику
plt.subplot(3, 1, 3)
plt.plot(risk, risk_low, 'b', label='Low')
plt.plot(risk, risk_medium, 'g', label='Medium')
plt.plot(risk, risk_high, 'r', label='High')
plt.title('Membership Functions for Risk')
plt.xlabel('Risk Level')
plt.ylabel('Degree of Membership')
plt.legend()

plt.tight_layout()
plt.show()
