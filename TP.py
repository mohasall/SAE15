import csv

# Ouvrir le fichier ics
with open('ADE_RT1_Septembre2022_Decembre2022.ics', 'r') as f:
    # Lire le contenu du fichier
    data = f.readlines()

# Initialiser une liste pour stocker les données CSV
csv_data = []

# Parcourir chaque ligne du fichier ics
for line in data:
    # Si la ligne contient "BEGIN:VEVENT", c'est le début d'un événement
    if "BEGIN:VEVENT" in line:
        # Initialiser un dictionnaire pour stocker les données de l'événement
        event_data = {}
    # Si la ligne contient "END:VEVENT", c'est la fin d'un événement
    elif "END:VEVENT" in line:
        # Ajouter les données de l'événement à la liste des données CSV
        csv_data.append(event_data)
    else:
        # Séparer la ligne en clé et valeur
        key, value = line.strip().split(':')
        # Ajouter la clé et la valeur au dictionnaire des données de l'événement

        event_data[key] = value

# Ecrire les données CSV dans un fichier
with open('ADE_RT1_Septembre2022_Decembre2022.csv', 'w') as f:
    # Créer un objet csv.DictWriter pour écrire les données
    writer = csv.DictWriter(f, fieldnames=event_data.keys())
    # Écrire les en-têtes de colonne
    writer.writeheader()
    # Écrire les données
    writer.writerows(csv_data)
