import random
import math
import numpy as np
import ast

def calcolaL(numeroMolecole):
	L = (2 * numeroMolecole)**(1.0/3.0) #L = L/sigma
	return L

def raggioCritico(L):
	rc = L / 2.0
	return rc

def distanza(molecola1, molecola2, L):
	distanzaXYZ=[]
	for indice in range(0,3):
		di= molecola2[indice] - molecola1[indice]
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

def calcolaK(velocitaPrim, numeroMolecole): #energia cinetica
	k = 0.0
	for v in velocitaPrim:
		k += v[0]**2 + v[1]**2 + v[2]**2
	k *= 0.5
	return k

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

def calcolaU(posizioni, numeroMolecole, L, rc):
    u = 0.0
    for indice, molecola in enumerate(posizioni):
        for molecola2 in posizioni[indice+1:]:
            if molecola == molecola2:
                continue
            r = distanza(molecola, molecola2, L)
            if r > rc:
                continue
            u += (1 / r) * math.exp(-r)
    return u

def calcolaP(posizioni, numeroMolecole, L, rc, temperatura):
    pId =  numeroMolecole * temperatura / (L ** 3)
    pEx = 0.0
    for indice, molecola in enumerate(posizioni):
        for molecola2 in posizioni[indice+1:]:
            if molecola == molecola2:
                continue
            r = distanza(molecola, molecola2, L)
            if r > rc:
                continue
            pEx += (1/(3 * L ** 3)) * (1 / r + 1) * math.exp(-r)
    p = pId + pEx
    return p

def calcolaT(energia): #prende in ingresso energia per molecola
    temperatura =  2.0 / 3.0 * energia
    return temperatura

def energiaTotale(energia, potenziale):
    eTot = energia + potenziale
    return eTot

#def controllo(coordinata, L):
#  if coordinata < 0:
#    return coordinata + L
#  if coordinata > L :
#    return coordinata - L
#  return coordinata

def MDloop(rc, posizioni, velocitaStart, deltat, forze, tArrivo, L, numeroMolecole):
	t = 0.0
	listaK = []
	listaU = []
	listaeTot = []
	listaTemp = []
	listaP = []
	listaF = []
	listaTempo = []
	k = calcolaK(velocitaStart, numeroMolecole) / numeroMolecole
	u = calcolaU(posizioni, numeroMolecole, L, rc) / numeroMolecole
	eTot = energiaTotale(k, u)
	temp = calcolaT(k)
	p = calcolaP(posizioni, numeroMolecole, L, rc, temp)
	listaU.append(u)
	listaK.append(k)
	listaeTot.append(eTot)
	listaTemp.append(temp)
	listaP.append(p)
	listaTempo.append(0)
	while(t + deltat < tArrivo):
		t += deltat
		listaTempo.append(t)
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
		velocitaStart = velocitaNuove[:]
		forze = forzeNuove[:]

		k = calcolaK(velocitaStart, numeroMolecole) / numeroMolecole
		u = calcolaU(posizioni, numeroMolecole, L, rc) / numeroMolecole
		eTot = energiaTotale(k, u)
		temp = calcolaT(k)
		p = calcolaP(posizioni, numeroMolecole, L, rc, temp)
		listaU.append(u)
		listaK.append(k)
		listaeTot.append(eTot)
		listaTemp.append(temp)
		listaP.append(p)

	with open('MDloop\\RunVelPos_' + str(deltat) + '.txt', 'w') as the_file:
		for posizione, velocita, forza in zip(posizioni, velocitaStart, forze):
			the_file.write(str(posizione) + '\t' + str(velocita) + '\t' + str(forza))
	        the_file.write('\n')
	with open('MDloop\\Run_' + str(deltat) + '.txt', 'w') as the_file:
		the_file.write('tempo\t\t' + 'K\t\t\t' + 'U\t\t\t' + '\teTot\t\t\t' + '\ttemp\t\t' + 'P\n')
		#print len(zip(listaTempo, listaK, listaU, listaeTot, listaTemp, listaP))
		for tempo, K, U, eTot, Temp, P in zip(listaTempo, listaK, listaU, listaeTot, listaTemp, listaP):
			the_file.write(str(tempo) + '\t' + str(K) + '\t' + str(U) + '\t' + str(eTot) + '\t' + str(Temp) + '\t' + str(P) )
			the_file.write('\n')
	#CKT = []
	numeroIterazioni = tArrivo/deltat
	mediaU = media(listaU, numeroIterazioni)
	kU, tauU, tauUdeltat, sigmaU, CKU = autocorrAnalisi(listaU, mediaU, deltat)
	mediaP = media(listaP, numeroIterazioni)
	kP, tauP, tauPdeltat, sigmaP, CKP = autocorrAnalisi(listaP, mediaP, deltat)
	mediaeTot = media(listaeTot, numeroIterazioni)
	kE, tauE, tauEdeltat, sigmaE, CKE = autocorrAnalisi(listaeTot, mediaeTot, deltat)
	mediaTemp = media(listaTemp, numeroIterazioni)
	kT, tauT, tauTdeltat, sigmaT, CKT = autocorrAnalisi(listaTemp, mediaTemp, deltat)
	with open('autoCorrelazione\\autoCorrAnal_Run_' + str(deltat) + '.txt', 'w') as the_file:
		the_file.write('\t\tmedia' + '\t\t\t' + 'tau(n)' + '\t\t\t' + 'tau(t)' + '\t\t\t'  + 'sigma' + '\n')
		the_file.write('U:\t' + str(mediaU) + '\t' + str(tauU) +'\t' + str(tauUdeltat) + '\t' + str(sigmaU))
		the_file.write('\n')
		the_file.write('P:\t' + str(mediaP) + '\t' + str(tauP) + '\t' + str(tauPdeltat) + '\t'  + str(sigmaP))
		the_file.write('\n')
		the_file.write('E:\t' + str(mediaeTot) + '\t' + str(tauE) + '\t' + str(tauEdeltat) + '\t' + str(sigmaE))
		the_file.write('\n')
		the_file.write('T:\t' + str(mediaTemp) + '\t' + str(tauT) + '\t' + str(tauTdeltat) + '\t' + str(sigmaT))


def media(variabili, numeroCampioni):
	media = 0.0
	for variabile in variabili:
		media += variabile
	media /= numeroCampioni
	return media

def autocorrelazione(variabile, k, media):
	autocorr = 0.0
	for indice in range(0, len(variabile) - k):
		autocorr += (variabile[indice+k] - media) * (variabile[indice] - media)
	C = (1.0 / (len(variabile) - k)) * autocorr
	return C

def autocorrAnalisi(variabile, media, deltat):
	kauto = 0
	Trovato = False
	listaCK = []
	while ((not Trovato) or (kauto < 50)):
		ktemp = autocorrelazione(variabile, kauto, media)
		listaCK.append(ktemp)
		if ktemp <0 and not Trovato:
			k1 = kauto - 1
			Trovato = True
		kauto += 1
	#C0 = CK[0]
	tau = 0.0
	for k in range(1, k1):
		tau += listaCK[k] / listaCK[0]
	tau += 0.5
	sigma = math.sqrt((listaCK[0] / len(variabile)) * 2 * tau)
	return (kauto, tau, tau*deltat, sigma, listaCK)


def main():
    posizioni = []
    vstart = []
    with open('startingConfig\\posizioni.txt', 'U') as f: #apre file
    	data=f.read()
    	posizioni = ast.literal_eval(data)
    with open('startingConfig\\listaVelScal.txt', 'U') as f: #apre file
    	data=f.read()
    	vstart = ast.literal_eval(data)
    numeroMolecole = 60
    L = calcolaL(numeroMolecole)
    rc = raggioCritico(L)
    forze = calcolaF(posizioni, rc, L)
    MDloop(rc, posizioni, vstart, 0.001, forze, 25.0, L, numeroMolecole)




main()
