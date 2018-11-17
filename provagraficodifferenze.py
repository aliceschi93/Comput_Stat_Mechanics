# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ast
import decimal

energietemp1 = []
with open('Run_0.001.txt', 'U') as f:
	data = f.read()
	righe = data.split('\n') #divide per riga in una lista di stringhe
	for riga in righe[1:-1]:
		#print riga
		valori = riga.split('\t')
		energia = float(valori[3])
		#print energia
		energietemp1.append(energia)

energie3 = []
with open('Run_0.009.txt', 'U') as f:
	data = f.read()
	righe = data.split('\n') #divide per riga in una lista di stringhe
	for riga in righe[1:-1]:
		#print riga
		valori = riga.split('\t')
		energia = float(valori[3])
		#print energia
		energie3.append(energia)
#print energie2

energie1 = []
for indice, energia in enumerate(energietemp1): #seleziona gli elementi allo stesso tempo di energie3
	if (len(energie1) <= len(energie3)):
		indice *= 9
		energie1.append(energia)

with open('provaE1.txt', 'w') as the_file:
	the_file.write(str(energie1))

with open('provaE3.txt', 'w') as the_file:
	the_file.write(str(energie3))

differenza31 = []
for E1,E3 in zip(energie1, energie3):
	diff = E3 - E1
	differenza31.append(diff)
	#print differenza31
	#print (E1, E3)

with open('provaDifferenze.txt', 'w') as the_file:
	the_file.write(str(differenza31))


ascissa = [0]*len(differenza31)
for indice in range(len(ascissa)):
	ascissa[indice] = 0.009 * indice

# Create a dataset:
df=pd.DataFrame({'iterazioni': np.array(ascissa), 'energie': np.array(differenza31)})

# plot
plt.plot('iterazioni', 'energie', data=df, linestyle='', linewidth=0.5, marker=',', color ='black')
plt.xlabel('tempo')
plt.ylabel('differenza energia')
plt.show()
