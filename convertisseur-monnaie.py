# Ce script Python est un programme simple permettant à l'utilisateur de convertir une somme donnée d'une devise à une autre,
# tout en sauvegardant l'historique des conversions.
from forex_python.converter import CurrencyRates
import json
from datetime import datetime
# convertir_devise : Cette fonction utilise la bibliothèque forex-python pour obtenir le taux de change entre deux devises
# et effectue la conversion.
# Si une erreur se produit pendant la conversion, elle imprime un message d'erreur et renvoie None.
# Créez une instance de la classe CurrencyRates
c = CurrencyRates()

# Obtenez le taux de change entre l'USD et l'EUR
rate = c.get_rate('USD', 'EUR')
print(f"Taux de change USD vers EUR : {rate}")

def convertir_devise(montant, devise_source, devise_cible):
    try:
        taux = CurrencyRates().get_rate(devise_source, devise_cible)
        montant_converti = montant * taux
        return montant_converti
    except Exception as e:
        print(f"Erreur de conversion : {e}")
        return None

# charger_historique : Cette fonction tente de charger l'historique des conversions à partir d'un fichier JSON.
# Si le fichier n'est pas trouvé (première exécution ou fichier supprimé), elle retourne une liste vide.

def charger_historique():
    try:
        # with open('historique_conversions.json', 'r') as file: : Cette ligne ouvre le fichier 'historique_conversions.json' en mode lecture ('r').
        # La déclaration with assure que le fichier est correctement fermé après l'utilisation, même en cas d'erreur.
        with open('historique_conversions.json', 'r') as file:
            # json.load(file) : Cette ligne charge le contenu du fichier JSON (file) dans une structure de données Python.
            # Cela suppose que le contenu du fichier est au format JSON valide.
            # Si le fichier est vide ou ne contient pas de JSON valide, cela pourrait provoquer une exception de type json.JSONDecodeError.
            return json.load(file)
            # except FileNotFoundError: : Si le fichier 'historique_conversions.json' n'est pas trouvé
            # (c'est-à-dire s'il n'existe pas ou s'il y a une faute de frappe dans le nom du fichier),
            # le programme capture cette exception de type FileNotFoundError.
    except FileNotFoundError:
        return []

# --------------------------------------------------------------------------------------------------------------------------------

# sauvegarder_historique : Cette fonction charge l'historique actuel, ajoute la nouvelle conversion avec la date actuelle,
# puis sauvegarde l'ensemble dans le fichier JSON. Le fichier est ouvert en mode écriture ('w'), ce qui écrase le contenu existant.

def sauvegarder_historique(conversion):
    # historique = charger_historique() : Cette ligne utilise la fonction charger_historique,
    # pour obtenir l'historique actuel des conversions à partir du fichier JSON.
    # La fonction charger_historique renvoie une liste contenant les conversions précédentes.
    historique = charger_historique()
    # conversion['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') :
    # Cette ligne ajoute une clé 'date' à la structure de données conversion et lui assigne la date et l'heure actuelles sous un format
    # spécifique ('%Y-%m-%d %H:%M:%S').
    conversion['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # historique.append(conversion) : Cette ligne ajoute la conversion actuelle (avec la nouvelle clé 'date') à la liste historique.
    # La conversion est ainsi ajoutée à la fin de la liste.
    historique.append(conversion)
# with open('historique_conversions.json', 'w') as file: : Cette ligne ouvre le fichier 'historique_conversions.json' en mode écriture ('w').
# La déclaration with assure que le fichier sera correctement fermé après utilisation, même en cas d'erreur.
    with open('historique_conversions.json', 'w') as file:
        # json.dump(historique, file, indent=2) : Cette ligne utilise la fonction json.dump pour écrire,
        # le contenu de la liste historique dans le fichier JSON spécifié (file).
        # L'argument indent=2 indique d'ajouter une indentation de 2 espaces pour rendre le fichier JSON plus lisible.
        json.dump(historique, file, indent=2)

# --------------------------------------------------------------------------------------------------------------------------------
# afficher_historique : Cette fonction affiche l'historique des conversions à partir des données chargées.
# Si l'historique est vide, elle imprime un message indiquant l'absence de conversions.
def afficher_historique():
    historique = charger_historique()

    if historique:
        print("Historique des conversions :")
        for conversion in historique:
            print(f"{conversion['date']} - {conversion['montant']} {conversion['devise_source']} en {conversion['devise_cible']} : {conversion['montant_converti']} {conversion['devise_cible']}")
    else:
        print("Aucun historique de conversions.")
# __main__ : Cette section est exécutée si le script est exécuté directement (et non importé en tant que module).
# Elle prend l'entrée utilisateur pour le montant, la devise source et la devise cible, puis appelle convertir_devise.
# Si la conversion réussit, elle affiche le résultat, sauvegarde l'historique et affiche l'historique actuel.
if __name__ == "__main__":
    montant = float(input("Entrez le montant à convertir : "))
    devise_source = input("Entrez la devise source (par ex. USD) : ").upper() 
    devise_cible = input("Entrez la devise cible (par ex. EUR) : ").upper()

    montant_converti = convertir_devise(montant, devise_source, devise_cible)

    if montant_converti is not None:
        print(f"{montant} {devise_source} équivaut à {montant_converti} {devise_cible}")

        # Sauvegarder l'historique avec la variable (conversion)
        conversion = {
            'montant': montant,
            'devise_source': devise_source,
            'devise_cible': devise_cible,
            'montant_converti': montant_converti
        }
        sauvegarder_historique(conversion)

        # Affichage de l'historique
        afficher_historique()
