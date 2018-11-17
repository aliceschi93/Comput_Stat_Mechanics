# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ast

deltat = 0.081
energie = []
with open('C:\\Users\\alice\\Google Drive\\UNI\\Sapienza\\Homework3\\MDloop\\Run_' + str(deltat) + '.txt', 'U') as f:
	data = f.read()
	righe = data.split('\n') #divide per riga in una lista di stringhe
	for riga in righe[1:-1]:
		valori = riga.split('\t')
		energia = float(valori[3])
		energie.append(energia)


ascissa = [0] * len(energie)
for indice in range(len(ascissa)):
	ascissa[indice] = deltat * indice


# Create a dataset:
df=pd.DataFrame({'iterazioni': np.array(ascissa), 'energie': np.array(energie)})

# plot
plt.plot('iterazioni', 'energie', data=df, linestyle='-', linewidth=0.2, marker='', color ='black')
plt.xlabel('t*')
plt.xlim(0.0, 25.0)
plt.ylabel('eTot')
plt.show()
