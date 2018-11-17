import random
import math
import numpy as np

def calcolaL(numeroMolecole):
	L = (2 * numeroMolecole)**(1.0/3.0) #L = L/sigma
	return L

def raggioCritico(L):
	rc = L / 2.0
	return rc

def posizIniz(numeroMolecole, L): #posizioni distribuite casualmente nel cubo
	posizioni = set()
	while len(posizioni) < numeroMolecole:
		x = random.random() * L
		y = random.random() * L
		z = random.random() * L
		posizioni.add((x,y,z))
	return list(posizioni)

def velocIniz(numeroMolecole, L): #velocita distribuite casualmente
	velocita = []
	for indice in range(0, numeroMolecole):
		vx = random.random() - 0.5
		vy = random.random() - 0.5
		vz = random.random() - 0.5
		velocita.append((vx, vy, vz))
	return velocita

def velocitaCM(velocita, numeroMolecole):
	momentox = 0.0
	momentoy = 0.0
	momentoz = 0.0
	for v in velocita:
		momentox += v[0]
		momentoy += v[1]
		momentoz += v[2]
	momentox /= numeroMolecole
	momentoy /= numeroMolecole
	momentoz /= numeroMolecole
	return (momentox, momentoy, momentoz)

def velocitaPrim(velocita, momento): #velocita primate
	velocitaPrim = []
	for v in velocita:
		vxPrim = v[0] - momento[0]
		vyPrim = v[1] - momento[1]
		vzPrim = v[2] - momento[2]
		velocitaPrim.append((vxPrim, vyPrim, vzPrim))
	return velocitaPrim


def calcolaK(velocitaPrim, numeroMolecole): #energia cinetica
	k = 0.0
	for v in velocitaPrim:
		k += v[0]**2 + v[1]**2 + v[2]**2
	k *= 0.5
	return k

def calcolaAlpha(numeroMolecole, k):
	alpha = math.sqrt(0.8 * numeroMolecole / k)
	return alpha

def velocitaStart(velocitaPrim, alpha, numeroMolecole): #velocita iniziali
	vStart = []
	for v in velocitaPrim:
		velocitaStartx = v[0] * alpha
		velocitaStarty = v[1] * alpha
		velocitaStartz = v[2] * alpha
		vStart.append((velocitaStartx, velocitaStarty, velocitaStartz))
	return vStart

def distanza(molecola1, molecola2, L):
	distanzaXYZ=[]
	for indice in range(0,3):
		di= molecola2[indice]-molecola1[indice]
		di-= L*round(di/L)
		distanzaXYZ.append(di)
	sommaQuadrati = 0.0
	for coordinata in distanzaXYZ:
		sommaQuadrati+= coordinata**2
	distanza12 = math.sqrt(sommaQuadrati)
	return distanza12

def calcolaRx(molecola1, molecola2, L, coordinata):
	di = molecola1[coordinata] - molecola2[coordinata]
	di -= L * round(di/L)
	return di

def calcolaF(posizioni, rc, L):
	forza = []
	for molecola in posizioni:
		fx = 0.0
		fy = 0.0
		fz = 0.0
		for molecola2 in posizioni:
			if molecola == molecola2:
				continue
			r = distanza(molecola, molecola2, L)
			if r > rc:
				continue
			rx = calcolaRx(molecola, molecola2, L, 0)
			ry = calcolaRx(molecola, molecola2, L, 1)
			rz = calcolaRx(molecola, molecola2, L, 2)
			fx += (rx / (r ** 3)) * (1 + r) * math.exp(-r)
			fy += (ry / (r ** 3)) * (1 + r) * math.exp(-r)
			fz += (rz / (r ** 3)) * (1 + r) * math.exp(-r)
		forza.append((fx, fy, fz))
	return forza

def MDloop(rc, posizioni, velocitaStart, deltat, forze, tArrivo, L, numeroMolecole):
	t = 0.0
	listaEnergia = []
	while(t < tArrivo):
		t += deltat
		posizNuove = []
		for posizione, velocita, forza in zip(posizioni, velocitaStart, forze):
			nuovaPosizX = posizione[0] + velocita[0] * deltat + 0.5 * forza[0] * (deltat ** 2)
			nuovaPosizY = posizione[1] + velocita[1] * deltat + 0.5 * forza[1] * (deltat ** 2)
			nuovaPosizZ = posizione[2] + velocita[2] * deltat + 0.5 * forza[2] * (deltat ** 2)
			posizNuove.append((nuovaPosizX, nuovaPosizY, nuovaPosizZ))
		posizioni = posizNuove
		forzeNuove = calcolaF(posizioni, rc, L)
		velocitaNuove = []
		for velocita, forza, forzaNuova in zip(velocitaStart, forze, forzeNuove):
			velocitaNuovaX = velocita[0] + 0.5 * forza[0] * deltat + 0.5 * forzaNuova[0] * deltat
			velocitaNuovaY = velocita[1] + 0.5 * forza[1] * deltat + 0.5 * forzaNuova[1] * deltat
			velocitaNuovaZ = velocita[2] + 0.5 * forza[2] * deltat + 0.5 * forzaNuova[2] * deltat
			velocitaNuove.append((velocitaNuovaX, velocitaNuovaY, velocitaNuovaZ))
		velocitaStart = velocitaNuove
		forze = forzeNuove
		energiaK = calcolaK(velocitaStart, numeroMolecole)

		listaEnergia.append(energiaK)

	listaVelScal = []
	for velocita in velocitaStart:
		vScalaX = math.sqrt(numeroMolecole/ listaEnergia[-1]) * velocita[0]
		vScalaY = math.sqrt(numeroMolecole/ listaEnergia[-1]) * velocita[1]
		vScalaZ = math.sqrt(numeroMolecole/ listaEnergia[-1]) * velocita[2]
		listaVelScal.append((vScalaX, vScalaY, vScalaZ))

	energieNuove = []
	for energia in listaEnergia:
		energieNuove.append(energia / 60.0)

	with open('startingConfig\\posizioni.txt', 'w') as the_file:
		the_file.write(str(posizioni))
	with open('startingConfig\\listaVelScal.txt', 'w') as the_file:
		the_file.write(str(listaVelScal))
	with open('startingConfig\\energiaK.txt', 'w') as the_file:
		the_file.write(str(energieNuove))





def main():
	numeroMolecole = 60
	L = calcolaL(numeroMolecole)
	rc = raggioCritico(L)
	posizioni = posizIniz(numeroMolecole, L)
	viniz = velocIniz(numeroMolecole, L)
	vCM = velocitaCM(viniz, numeroMolecole)
	vprim = velocitaPrim(viniz, vCM)
	k = calcolaK(vprim, numeroMolecole)
	alpha = calcolaAlpha(numeroMolecole, k)
	vstart = velocitaStart(vprim, alpha, numeroMolecole)
	forze = calcolaF(posizioni, rc, L)
	MDloop(rc, posizioni, vstart, 0.002, forze, 1.0, L, numeroMolecole)



main()
