# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 17:31:34 2023

@author: Mohamed sall
"""

import re
import matplotlib.pyplot as plt

# Ouvrir le fichier en mode lecture
with open('fichier_à_traiter.txt', 'r') as f:
    trames = f.read()

# Utiliser une expression régulière pour extraire les adresses IP
adresses_ip = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', trames)

# Utiliser un dictionnaire pour compter le nombre d'occurrences de chaque adresse
occurrences_ip = {}

for adresse in adresses_ip:
    if adresse in occurrences_ip:
        occurrences_ip[adresse] += 1
    else:
        occurrences_ip[adresse] = 1
       
# Afficher les résultats
print("Adresses IP destination :")
for adresse, occurrences in occurrences_ip.items():
    print(adresse, ":", occurrences)
           

# Trier les adresses IP par ordre décroissant d'occurrences
adresses_triees = [x for _,x in sorted(zip(occurrences_ip.values(),occurrences_ip.keys()), reverse=True)]
occurrences_triees = sorted(occurrences_ip.values(), reverse=True)

#Les 12 adresses IP les plus fréquentes
adresses_affichees = adresses_triees[:12]
occurrences_affichees = occurrences_triees[:12]

# Création de l'histogramme l'histogramme
plt.bar(adresses_affichees, occurrences_affichees)
plt.xlabel('Adresse IP')
plt.ylabel('Nombre d\'occurrences')
plt.title('Occurrences d\'adresses IP')
plt.xticks(rotation=45)

