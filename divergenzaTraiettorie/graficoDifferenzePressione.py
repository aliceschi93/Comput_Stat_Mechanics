# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ast
import decimal

pressionitemp1 = []
with open('C:\\Users\\alice\\Google Drive\\UNI\\Sapienza\\Homework3\\MDloop\\Run_0.001.txt', 'U') as f:
	data = f.read()
	righe = data.split('\n') #divide per riga in una lista di stringhe
	for riga in righe[1:-1]:
		valori = riga.split('\t')
		pressione = float(valori[5])
		pressionitemp1.append(pressione)

deltat = 0.081
pressioni2 = []
with open('C:\\Users\\alice\\Google Drive\\UNI\\Sapienza\\Homework3\\MDloop\\Run_' + str(deltat) + '.txt', 'U') as f:
	data = f.read()
	righe = data.split('\n') #divide per riga in una lista di stringhe
	for riga in righe[1:-1]:
		valori = riga.split('\t')
		pressione = float(valori[5])
		pressioni2.append(pressione)

pressioni1 = []
for indice, pressione in enumerate(pressioni2): #seleziona gli elementi allo stesso tempo di pressioni3
	indice *= int(deltat * 10 ** 3)
	pressioni1.append(pressionitemp1[indice])

differenza21 = []
for E1,E2 in zip(pressioni1, pressioni2):
	diff = E2 - E1
	differenza21.append(diff)

with open('differenzaPressione' + str(deltat) + '.txt', 'w') as the_file:
	the_file.write(str(differenza21))


ascissa = [0]*len(differenza21)
for indice in range(len(ascissa)):
	ascissa[indice] = deltat * indice

# Create a dataset:
df=pd.DataFrame({'iterazioni': np.array(ascissa), 'pressioni': np.array(differenza21)})

# plot
plt.plot('iterazioni', 'pressioni', data=df, linestyle='-', linewidth=0.2, marker='', markersize = 1.0, color ='black')
plt.xlabel('t*')
plt.xlim(0.0, 25.0)
plt.ylabel('P5-P1')
plt.show()
