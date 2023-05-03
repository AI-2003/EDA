# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:04:42 2022

@author: RGAMBOAH
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

cadsep = "="  * 60

tray = os.path.abspath(os.path.dirname(__file__)) + '/names/yob{0}.txt'

#
# lectura de datos
#
pieces = []
years = range(1880,2021)
for year in years:
    frame = pd.read_csv(tray.format(year),names=['name','sex','births'])
    frame['year'] = year
    pieces.append(frame)
names = pd.concat(pieces,ignore_index=True)
print(cadsep)
#
# diferencias entre .loc[] y .iloc[]:
#
# df.loc[inicio:fin]  ... se refiere al índice del registro, incluye inicio y fin, el rango del índice debe ser iterable    
# df.iloc[inicio:fin] ... se refiere a la posición de los registros
#
print("names.loc[0:10]:\n",names.loc[0:10])
print("names.iloc[0:10]:\n",names.iloc[0:10])
print(cadsep)
#
# nombres más populares en 1880
#
n1880        = names[names.year==1880]

n1880F           = n1880[n1880.sex=='F']
maxF1880         = n1880F.births.max()
nameMostPop1880F = n1880F[n1880F.births==maxF1880].name
print('Nombre(s) de mujer mas populares en 1880 con ',maxF1880,' casos:')
for t in nameMostPop1880F:
    print(t)

n1880M           = n1880[n1880.sex=='M']
maxM1880         = n1880M.births.max()
nameMostPop1880M = n1880M[n1880M.births==maxM1880].name
print('Nombre(s) de hombre mas populares en 1880 con ',maxM1880,' casos:')
for t in nameMostPop1880M:
    print(t)
print(cadsep)
#
# nombres mas populares en toda la historia
#
# Generamos una serie por medio de un grupby por género y nombre, sumando los nacimientos
#
gNh = names.groupby(by=['sex','name']).births.sum()
#
print("gNh:\n",gNh)
print("type(gNh):",type(gNh))
#
# obtengo las series para mujeres y para hombres trabajando sobre el índice de la serie 
# en dos niveles
#
print("gNh.index:\n",gNh.index)
print(cadsep)
#
# Filtramos sobre el lugar[0] del índice y extraemos una serie por género
#
gNhF = gNh.loc[[x[0]=='F' for x in gNh.index]]
gNhM = gNh.loc[[x[0]=='M' for x in gNh.index]]
#
# obtenemos el valor máximo para el número de nacimientos de la serie para cada género
#
maxgNhF = gNhF.max()
maxgNhM = gNhM.max()
#
# y obtenemos en una lista los nombres del máximo para la serie de cada género
#
nomPopHistF = [t[1] for t in gNhF[gNhF==maxgNhF].index]
nomPopHistM = [t[1] for t in gNhM[gNhM==maxgNhM].index]

print("nombre(s) de mujer más popular(es) en la historia, con {:,}".format(maxgNhF), " casos:")
for t in nomPopHistF: 
    print(t)

print("nombre(s) de hombre más popular(es) en la historia, con {:,}".format(maxgNhM)," casos:")
for t in nomPopHistM: 
    print(t)    

print(cadsep)

#
# Gráfica de la evolución del primer nombre más popular de cada género
#
nameMostPopF  = nomPopHistF[0]
nameMostPopM  = nomPopHistM[0]
# obtenemos el dataFrame del nombre de cada género con un truco o en dos pasos para evitar los warnings
# y porque la lambda tarda horrores
#
# xF    = names[names.apply(lambda r: r['name']==nameMostPopF and r['sex']=='F',axis=1)]
#
# Este va en un dos pasos pero es muy rápido
#
xf=names[names.name==nameMostPopF]['sex']=='F' # se obtiene una serie pero trae algunos falsos
xxf=xf[xf]  # truco sucio para quedarme con los registros de los True
dfnomSexF = names.loc[xxf.index]

xm=names[names.name==nameMostPopM]['sex']=='M' # se obtiene una serie pero trae algunos falsos
xxm=xm[xm]  # truco sucio para quedarme con los registros de los True
dfnomSexM = names.loc[xxm.index]

"""
# Este es muy canónico, en dos pasos 
dfnomF    = names[names.name==nameMostPopF]
dfnomSexF = dfnomF[dfnomF.sex=='F']

dfnomM    = names[names.name==nameMostPopM]
dfnomSexM = dfnomM[dfnomM.sex=='M']
"""
plt.plot(dfnomSexF.year,dfnomSexF.births)
plt.plot(dfnomSexM.year,dfnomSexM.births)
plt.legend(['Mujeres:'+nameMostPopF,'Hombres:'+nameMostPopM])  
plt.title("Evolución del nombre más popular por género") 
plt.show()

# =============================================================================
#    Fin del ejercicio
# =============================================================================
