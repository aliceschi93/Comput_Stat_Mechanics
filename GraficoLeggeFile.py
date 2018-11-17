# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ast


E3 = []
with open('provaE3.txt', 'U') as f: #apre file
	data = f.read()
	E3 = ast.literal_eval(data)

E1 = []
with open('provaE1.txt', 'U') as f: #apre file
	data = f.read()
	E1 = ast.literal_eval(data)

ascissa = [0]*len(E1)
for indice in range(len(ascissa)):
	ascissa[indice] = 0.009 * indice

differenza = []
for indice, energia in enumerate(E3):
	energia -= E1[indice]
	differenza.append(energia)
	print differenza


# Create a dataset:
df=pd.DataFrame({'iterazioni': np.array(ascissa), 'energie': np.array(differenza)})

# plot
plt.plot('iterazioni', 'energie', data=df, linestyle='-', linewidth=0.5, marker='', color ='black')
plt.xlabel('tempo')
plt.ylabel('energia per particella')
plt.show()
