# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ast
import decimal

temperaturetemp1 = []
with open('C:\\Users\\alice\\Google Drive\\UNI\\Sapienza\\Homework3\\MDloop\\Run_0.001.txt', 'U') as f:
	data = f.read()
	righe = data.split('\n') #divide per riga in una lista di stringhe
	for riga in righe[1:-1]:
		valori = riga.split('\t')
		temperatura = float(valori[4])
		temperaturetemp1.append(temperatura)

deltat = 0.081
temperature2 = []
with open('C:\\Users\\alice\\Google Drive\\UNI\\Sapienza\\Homework3\\MDloop\\Run_' + str(deltat) + '.txt', 'U') as f:
	data = f.read()
	righe = data.split('\n') #divide per riga in una lista di stringhe
	for riga in righe[1:-1]:
		valori = riga.split('\t')
		temperatura = float(valori[4])
		temperature2.append(temperatura)

temperature1 = []
for indice, temperatura in enumerate(temperature2): #seleziona gli elementi allo stesso tempo di temperature3
	indice *= int(deltat * 10 ** 3)
	temperature1.append(temperaturetemp1[indice])

differenza21 = []
for E1,E2 in zip(temperature1, temperature2):
	diff = E2 - E1
	differenza21.append(diff)

with open('differenzatemperatura' + str(deltat) + '.txt', 'w') as the_file:
	the_file.write(str(differenza21))


ascissa = [0]*len(differenza21)
for indice in range(len(ascissa)):
	ascissa[indice] = deltat * indice

# Create a dataset:
df=pd.DataFrame({'iterazioni': np.array(ascissa), 'temperature': np.array(differenza21)})

# plot
plt.plot('iterazioni', 'temperature', data=df, linestyle='-', linewidth = 0.5, marker='', markersize = 0.5, color ='black')
plt.xlabel('t*')
plt.xlim(0.0, 25.0)
plt.ylabel('T5-T1')
plt.show()
