# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ast


energie = []
with open('energiaK.txt', 'U') as f: #apre file
	data=f.read() #copia in una stringa tutto il documento
	#data=data.split('\n') #divide per riga in una lista di stringhe
	#for numero in data[:-1]:
		#print numero
		#energie.append(float(numero))
	energie = ast.literal_eval(data)

ascissa = [0]*len(energie)
for indice in range(len(ascissa)):
	ascissa[indice] = 0.002 * indice


# Create a dataset:
#df=pd.DataFrame({'k': range(1,101), 'sigma': np.random.randn(100)*15+range(1,101) })
df=pd.DataFrame({'iterazioni': np.array(ascissa), 'energie': np.array(energie)})

# plot
plt.plot('iterazioni', 'energie', data=df, linestyle='-', linewidth=0.5, marker='', color ='black')
plt.xlabel('tempo')
plt.ylabel('energia per particella')
plt.show()
