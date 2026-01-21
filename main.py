
# Importation des modules nécessaires
import unicodedata  # Pour normaliser et supprimer les accents
from tablelancerdedes import format_5_derniers_lancers  # Pour afficher l'historique des lancers
import random  # Pour générer les résultats des dés
import re  # Pour analyser les commandes avec expressions régulières
from datetime import datetime  # Pour enregistrer la date et l'heure des lancers


class DiceRoller:
    """
    Classe principale pour gérer les lancers de dés et l'historique.
    """
    def __init__(self):
        # Initialise une liste vide pour stocker l'historique des lancers
        self.historique = []

    def roll(self, command: str, joueur: str):
        """
        Traite une commande de lancer de dés et ajoute le résultat à l'historique.
        Args:
            command (str): La commande du joueur (ex: /2dés6)
            joueur (str): Le pseudo du joueur
        Returns:
            result (str): Résultat formaté pour affichage
            histo_entry (str): Entrée complète pour l'historique
        """
        # Supprime tous les accents pour faciliter l'analyse
        command = ''.join(
            c for c in unicodedata.normalize('NFD', command)
            if unicodedata.category(c) != 'Mn'
        )
        # Analyse la commande avec une expression régulière
        match = re.match(r"/(\d+)des(\d+)", command)
        if not match:
            # Si la commande n'est pas reconnue, retourne None
            return None, None
        nb, faces = int(match.group(1)), int(match.group(2))  # Nombre de dés et nombre de faces
        if nb < 1 or faces < 2:
            # Vérifie que les valeurs sont valides
            return None, None
        # Génère les résultats des dés
        rolls = [random.randint(1, faces) for _ in range(nb)]
        # Récupère la date et l'heure du lancer
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Prépare le texte du résultat pour affichage
        result = f"Lancer {nb}d{faces} : {rolls} (total: {sum(rolls)})"
        # Prépare l'entrée pour l'historique
        histo_entry = f"{now} | {joueur} a lancé {nb}d{faces} : {rolls} (total: {sum(rolls)})"
        # Ajoute à l'historique
        self.historique.append(histo_entry)
        return result, histo_entry

    def get_history(self):
        """
        Retourne la liste complète de l'historique des lancers.
        """
        return self.historique



def main():
    """
    Fonction principale pour lancer le programme en mode console.
    Permet à l'utilisateur de lancer des dés et de consulter l'historique.
    """
    print("Bienvenue dans le lanceur de dés JDR !")  # Message d'accueil
    roller = DiceRoller()  # Instancie le gestionnaire de dés
    joueur = input("Entrez votre pseudo : ")  # Demande le pseudo du joueur
    while True:
        # Boucle principale du programme
        cmd = input("Entrez une commande de lancer de dés (ex: /1dés100, /2dés6), 'h' pour historique, ou 'q' pour quitter : ")
        if cmd.lower() == 'q':
            # Quitte le programme
            break
        if cmd.lower() == 'h':
            # Affiche l'historique des 5 derniers lancers pour chaque joueur
            print("\n--- 5 derniers lancers par utilisateur ---")
            print(format_5_derniers_lancers(roller.get_history()))
            print("------------------------------------------\n")
            continue
        # Tente d'effectuer un lancer de dés avec la commande donnée
        result, _ = roller.roll(cmd, joueur)
        if result is not None:
            # Affiche le résultat si la commande est valide
            print(result)
        else:
            # Message d'erreur si la commande est invalide
            print("Commande invalide. Essayez : /1dés100 ou /2dés6 ...")


# Point d'entrée du script : lance la fonction main si le fichier est exécuté directement
if __name__ == "__main__":
    main()
