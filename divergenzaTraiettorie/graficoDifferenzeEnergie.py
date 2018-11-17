# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ast
import decimal

energietemp1 = []
with open('C:\\Users\\alice\\Google Drive\\UNI\\Sapienza\\Homework3\\MDloop\\Run_0.001.txt', 'U') as f:
	data = f.read()
	righe = data.split('\n') #divide per riga in una lista di stringhe
	for riga in righe[1:-1]:
		valori = riga.split('\t')
		energia = float(valori[3])
		energietemp1.append(energia)

deltat = 0.081
energie2 = []
with open('C:\\Users\\alice\\Google Drive\\UNI\\Sapienza\\Homework3\\MDloop\\Run_' + str(deltat) + '.txt', 'U') as f:
	data = f.read()
	righe = data.split('\n') #divide per riga in una lista di stringhe
	for riga in righe[1:-1]:
		valori = riga.split('\t')
		energia = float(valori[3])
		energie2.append(energia)

energie1 = []
for indice, energia in enumerate(energie2): #seleziona gli elementi allo stesso tempo di energie3
	indice *= int(deltat * 10 ** 3)
	energie1.append(energietemp1[indice])

differenza21 = []
for E1,E2 in zip(energie1, energie2):
	diff = E2 - E1
	differenza21.append(diff)

with open('differenzaEnergia' + str(deltat) + '.txt', 'w') as the_file:
	the_file.write(str(differenza21))


ascissa = [0] * len(differenza21)
for indice in range(len(ascissa)):
	ascissa[indice] = deltat * indice

# Create a dataset:
df=pd.DataFrame({'iterazioni': np.array(ascissa), 'energie': np.array(differenza21)})

# plot
plt.plot('iterazioni', 'energie', data=df, linestyle='-', linewidth=0.2, marker='', markersize=0.5, color ='black')
plt.xlabel('t*')
plt.xlim(0.0, 25.0)
plt.ylabel('E5-E1')
plt.show()
