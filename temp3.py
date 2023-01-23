# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:58:46 2023

@author: Mohamed sall
"""
import numpy as np
import csv
import webbrowser
import matplotlib.pyplot as plt



#Ouverture et lecture du fichier à traiter 
fichier=open("Fichier_à_traiter.txt", "r")

#création des listes = nous allons remplir chacune de ses listes par les informations issues de l'analyseur de paquets tcpdump
ipsrc=[]
ipdes=[]
longueur=[]
flag=[]
seq=[]
heure=[]

#création des compteurs
#compteur du nombre de flag [P] = counter for flag [P] number
flagcounterP=0
#compteur du nombre de flag [S] = counter for flag [S] number
flagcounterS=0
#compteur du nombre de flag [.] = counter for flag [.] number
flagcounter=0
#compteur des trames échangés = counter for number of frames  exchanged on network
framecounter=0
#compteur request = counter for the number of requests
requestcounter=0
#compteur reply = counter for number of replies
replycounter=0
#compteur sequence = sequences counter
seqcounter=0
#compteur acknowledgement = acknowledgments counter
ackcounter=0
#compteur window = windows counter
wincounter=0

for ligne in fichier:
    #espace comme délimiteur
    split=ligne.split(" ")
    #Les blocs hexadécimaux seront supprimés et les lignes contenant les informations seront gardées
    if "IP" in ligne :
    #filling the flag list    
        framecounter+=1
        if "[P.]" in ligne :
            flag.append("[P.]")
            flagcounterP+=1
        if "[.]" in ligne :
            flag.append("[.]")
            flagcounter+=1
        if "[S]" in ligne :
            flag.append("[S]")
            flagcounterS+=1
        #filling the seq list     
        if "seq" in ligne :
            seqcounter+=1
            seq.append(split[8])
        #counting windows   
        if "win" in ligne :
            wincounter+=1
        #counting acks   
        if "ack" in ligne:
            ackcounter+=1
            
            
        #Remplissage pour les IP sources (ipsrc) 
        ipsrc.append(split[2])  
        #Remplissage pour les IP destinations(ipdes)
        ipdes.append(split[4])
        #Remplissage pour les heures(heure)
        heure.append(split[0])
        # Remplissage pour les longueurs
        if "length" in ligne:
            split = ligne.split(" ")
            if "HTTP" in ligne :
                longueur.append(split[-2])
            else: 
                longueur.append(split[-1]) 
        #Réperer les demandes et les réponses à travers le protocole ICMP       
        if "ICMP" in ligne:
            if "request" in ligne:
                requestcounter+=1
            if "reply" in ligne:
                replycounter+=1


             
globalflagcounter=flagcounter+flagcounterP+flagcounterS

P=flagcounterP/globalflagcounter
S=flagcounterS/globalflagcounter
A=flagcounter/globalflagcounter 

globalreqrepcounter=replycounter+requestcounter
req=requestcounter/globalreqrepcounter
rep=replycounter/globalreqrepcounter
         
#Transformation des compteurs en listes pour les visualiser sur un fichier CSV 
flagcounter=[flagcounter]
flagcounterP=[flagcounterP]
flagcounterS=[flagcounterS]
framecounter=[framecounter]
requestcounter=[requestcounter]
replycounter=[replycounter]
seqcounter=[seqcounter]
ackcounter=[ackcounter]
wincounter=[wincounter]



#Création de graphes avec le bibliothéque matplotlib
  #circular graphic for flags
name = ['Flag [.]', 'Flag [P]', 'Flag [S]']
data = [A,P,S]

explode=(0, 0, 0)
plt.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
plt.axis('equal')
plt.savefig("g1.png")
plt.show()
  #circular graphic for request and reply 
name2 = ['Request' , 'Reply']
data2 = [req,rep]  
explode=(0,0)
plt.pie(data2,explode=explode,labels=name2, autopct='%1.1f%%',startangle=90, shadow=True)
plt.savefig("g2.png")
plt.show()


#contenu de la page web = web page content 
htmlcontenu='''
<html>
   <head>
      <meta charset="utf-8">
      <title> Traitement de données SAE15 </title>
      <style>
      body{
          background-color:green;
          }
      </style>
   </head>
   
   <body>
       <center><h2> Mohamed SALL-Projet SAE 15</h2></center>
       <center><p>Cette page WEB a le but de vous montrer les informations et données importantes tirées du fichier qu'on a traité(dumpfile)</p></center>
       <center><h3> Nombre total des trames échangés</h3> %s</center>
       <br>
       <center><h3> Drapeaux (Flags)<h3></center>
       <center>Nombre de flags [P] (PUSH) = %s
       <br>Nombre de flags [S] (SYN) = %s  
       <br>Nombre de flag [.] (ACK) = %s
       <br>
       <br>
       <img src="g1.png">
       <h3> Nombre de demande et réponse </h3>
       Request = %s 
       <br>
       Reply = %s
       <br>
       <br>
       <img src="g2.png">
       <h3>Statistiques entre seq et win et ack </h3>
       Nombre de seq = %s
           <br>
       Nombre de win = %s
           <br>
       Nombre de ack = %s
       
      
   </body>

</html>
'''%(framecounter,flagcounterP,flagcounterS,flagcounter,requestcounter,replycounter,seqcounter,wincounter,ackcounter)

#ouverture d'un fichier csv = open a csv file for data extracted from txt file untreated 
with open('test.csv', 'w', newline='') as fichiercsv:
    writer = csv.writer(fichiercsv)
    writer.writerow(['Heure','IP source','IP destination','Flag','Seq','Length'])
    writer.writerows(zip(heure,ipsrc,ipdes,flag,seq,longueur))
    fichiercsv.close()
    
#ouverture d'un fichier csv    = open a csv file for different stats
with open('Statistiques.csv', 'w', newline='') as fichier2:
    writer = csv.writer(fichier2)
    writer.writerow(['Flag[P] (PUSH)','Flag[S] (SYN)','Flag[.] (ACK)','Nombre total de trames',"nb of request","nb of reply","nb of sequence","nb of acknowledgment","nb de window"])
    writer.writerows(zip(flagcounterP,flagcounterS,flagcounter,framecounter,requestcounter,replycounter,seqcounter,ackcounter,wincounter))
    fichier2.close()
    
#partie page  web = open a web page with important information and statistics
with open("SAE15.html","w") as html:
    html.write(htmlcontenu)
    print(" Votre page web est créée avec succès")

       
fichier.close()